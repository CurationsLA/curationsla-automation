#!/usr/bin/env python3
"""
CurationsLA Archive Manager
Manages publication archives, prevents duplicates, and maintains 7-day retention policy
"""

import os
import json
import hashlib
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Set, Any
import re

# Configuration
BASE_DIR = Path(__file__).parent.parent
CONTENT_DIR = BASE_DIR / "content"
ARCHIVE_HUB_DIR = BASE_DIR / "archive_hub"

class ArchiveManager:
    def __init__(self):
        self.content_dir = CONTENT_DIR
        self.archive_hub_dir = ARCHIVE_HUB_DIR
        self.archive_hub_dir.mkdir(exist_ok=True)
        
        # Create index file if it doesn't exist
        self.index_file = self.archive_hub_dir / "publications_index.json"
        if not self.index_file.exists():
            self._create_index()
    
    def _create_index(self):
        """Create initial publications index"""
        index_data = {
            "last_updated": datetime.now().isoformat(),
            "total_publications": 0,
            "publications": [],
            "retention_policy": {
                "days": 7,
                "archive_threshold": 30
            }
        }
        
        with open(self.index_file, 'w') as f:
            json.dump(index_data, f, indent=2)
    
    def get_content_hash(self, content: str) -> str:
        """Generate hash for content deduplication"""
        # Normalize content for comparison
        normalized = re.sub(r'\s+', ' ', content.lower().strip())
        # Remove common words that might vary
        normalized = re.sub(r'\b(the|a|an|and|or|but|in|on|at|to|for|of|with|by)\b', '', normalized)
        return hashlib.md5(normalized.encode()).hexdigest()
    
    def extract_content_items(self, publication_path: Path) -> List[Dict]:
        """Extract individual content items from a publication"""
        items = []
        
        # Look for newsletter files
        for newsletter_file in publication_path.glob("newsletter-*.md"):
            try:
                with open(newsletter_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Extract article sections (this is a simple approach)
                # Look for patterns like headlines, links, etc.
                lines = content.split('\n')
                current_item = ""
                
                for line in lines:
                    # Skip metadata and headers
                    if line.startswith(('#', '**', '![', '|', '---')):
                        if current_item.strip() and len(current_item.strip()) > 50:
                            items.append({
                                'content': current_item.strip(),
                                'hash': self.get_content_hash(current_item.strip()),
                                'source_file': newsletter_file.name
                            })
                        current_item = line
                    else:
                        current_item += "\n" + line
                
                # Add final item
                if current_item.strip() and len(current_item.strip()) > 50:
                    items.append({
                        'content': current_item.strip(),
                        'hash': self.get_content_hash(current_item.strip()),
                        'source_file': newsletter_file.name
                    })
            
            except Exception as e:
                print(f"⚠️  Error extracting from {newsletter_file}: {str(e)}")
        
        return items
    
    def check_for_duplicates(self, new_content_items: List[Dict], lookback_days: int = 7) -> Dict:
        """Check for duplicate content against recent publications"""
        duplicates = []
        unique_items = []
        
        # Get recent publication hashes
        recent_hashes = self.get_recent_content_hashes(lookback_days)
        
        for item in new_content_items:
            item_hash = item.get('hash', self.get_content_hash(item.get('content', '')))
            
            if item_hash in recent_hashes:
                duplicates.append({
                    'item': item,
                    'previous_publication': recent_hashes[item_hash]
                })
            else:
                unique_items.append(item)
        
        return {
            'duplicates': duplicates,
            'unique_items': unique_items,
            'duplicate_count': len(duplicates),
            'unique_count': len(unique_items)
        }
    
    def get_recent_content_hashes(self, days: int = 7) -> Dict[str, Dict]:
        """Get content hashes from recent publications"""
        cutoff_date = datetime.now() - timedelta(days=days)
        hashes = {}
        
        # Load index
        try:
            with open(self.index_file, 'r') as f:
                index_data = json.load(f)
        except:
            return hashes
        
        for pub in index_data.get('publications', []):
            pub_date = datetime.fromisoformat(pub['date'])
            if pub_date >= cutoff_date:
                for item_hash in pub.get('content_hashes', []):
                    hashes[item_hash] = {
                        'publication_date': pub['date'],
                        'publication_path': pub['path']
                    }
        
        return hashes
    
    def archive_publication(self, publication_date: datetime, content_path: Path) -> Dict:
        """Archive a publication and update index"""
        
        # Extract content items for duplicate checking
        content_items = self.extract_content_items(content_path)
        content_hashes = [item['hash'] for item in content_items]
        
        # Create publication record
        publication_record = {
            'date': publication_date.isoformat(),
            'path': str(content_path.relative_to(BASE_DIR)),
            'content_hashes': content_hashes,
            'content_count': len(content_items),
            'archived_at': datetime.now().isoformat()
        }
        
        # Update index
        try:
            with open(self.index_file, 'r') as f:
                index_data = json.load(f)
        except:
            index_data = {'publications': []}
        
        index_data['publications'].append(publication_record)
        index_data['total_publications'] = len(index_data['publications'])
        index_data['last_updated'] = datetime.now().isoformat()
        
        with open(self.index_file, 'w') as f:
            json.dump(index_data, f, indent=2)
        
        print(f"📁 Archived publication: {publication_date.strftime('%Y-%m-%d')} ({len(content_items)} items)")
        
        return publication_record
    
    def cleanup_old_archives(self, retention_days: int = 7) -> Dict:
        """Clean up archives older than retention period"""
        cutoff_date = datetime.now() - timedelta(days=retention_days)
        
        cleaned_paths = []
        kept_paths = []
        
        # Scan content directory for old archives
        for year_dir in self.content_dir.glob("*"):
            if not year_dir.is_dir():
                continue
                
            for month_dir in year_dir.glob("*"):
                if not month_dir.is_dir():
                    continue
                
                for week_dir in month_dir.glob("*"):
                    if not week_dir.is_dir():
                        continue
                    
                    for day_dir in week_dir.glob("*"):
                        if not day_dir.is_dir():
                            continue
                        
                        # Try to parse date from path
                        try:
                            # Look for date files or use directory structure
                            date_indicators = list(day_dir.glob("*2025-*"))
                            if date_indicators:
                                # Extract date from filename
                                date_match = re.search(r'(\d{4}-\d{2}-\d{2})', str(date_indicators[0]))
                                if date_match:
                                    pub_date = datetime.strptime(date_match.group(1), '%Y-%m-%d')
                                    
                                    if pub_date < cutoff_date:
                                        # Archive before deletion
                                        self._create_lightweight_archive(day_dir, pub_date)
                                        
                                        # Remove old directory
                                        import shutil
                                        shutil.rmtree(day_dir)
                                        cleaned_paths.append(str(day_dir))
                                        print(f"🗑️  Cleaned old archive: {day_dir}")
                                    else:
                                        kept_paths.append(str(day_dir))
                        except Exception as e:
                            print(f"⚠️  Error processing {day_dir}: {str(e)}")
        
        return {
            'cleaned_count': len(cleaned_paths),
            'kept_count': len(kept_paths),
            'cleaned_paths': cleaned_paths,
            'kept_paths': kept_paths
        }
    
    def _create_lightweight_archive(self, pub_dir: Path, pub_date: datetime):
        """Create a lightweight archive record before deletion"""
        archive_record = {
            'date': pub_date.isoformat(),
            'original_path': str(pub_dir.relative_to(BASE_DIR)),
            'archived_at': datetime.now().isoformat(),
            'status': 'archived_and_cleaned'
        }
        
        # Try to extract key metadata
        try:
            stats_file = pub_dir / "stats.json"
            if stats_file.exists():
                with open(stats_file, 'r') as f:
                    stats = json.load(f)
                    archive_record['stats'] = stats
        except:
            pass
        
        # Save lightweight archive
        archive_file = self.archive_hub_dir / f"archive_{pub_date.strftime('%Y_%m_%d')}.json"
        with open(archive_file, 'w') as f:
            json.dump(archive_record, f, indent=2)
    
    def get_previous_publication(self, current_date: datetime) -> Dict:
        """Get the most recent publication before current date"""
        try:
            with open(self.index_file, 'r') as f:
                index_data = json.load(f)
        except:
            return {}
        
        # Find most recent publication before current date
        previous_pub = None
        for pub in sorted(index_data.get('publications', []), 
                         key=lambda x: x['date'], reverse=True):
            pub_date = datetime.fromisoformat(pub['date'])
            if pub_date < current_date:
                previous_pub = pub
                break
        
        if previous_pub:
            # Load additional details
            pub_path = BASE_DIR / previous_pub['path']
            if pub_path.exists():
                return {
                    'date': previous_pub['date'],
                    'path': previous_pub['path'],
                    'content_count': previous_pub.get('content_count', 0),
                    'exists': True
                }
        
        return {}
    
    def generate_archive_hub_index(self) -> str:
        """Generate an HTML index of all publications"""
        try:
            with open(self.index_file, 'r') as f:
                index_data = json.load(f)
        except:
            index_data = {'publications': []}
        
        html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CurationsLA Publications Archive</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; margin: 40px; }}
        .header {{ text-align: center; margin-bottom: 40px; }}
        .publication {{ background: #f8f9fa; padding: 20px; margin: 20px 0; border-radius: 8px; }}
        .date {{ font-weight: bold; color: #0366d6; }}
        .stats {{ color: #666; font-size: 0.9em; }}
        .recent {{ border-left: 4px solid #28a745; }}
        .archived {{ border-left: 4px solid #ffc107; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🌴 CurationsLA Publications Archive</h1>
        <p>Total Publications: {index_data.get('total_publications', 0)}</p>
        <p>Last Updated: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}</p>
    </div>
"""
        
        publications = sorted(index_data.get('publications', []), 
                            key=lambda x: x['date'], reverse=True)
        
        cutoff_date = datetime.now() - timedelta(days=7)
        
        for pub in publications:
            pub_date = datetime.fromisoformat(pub['date'])
            is_recent = pub_date >= cutoff_date
            
            status_class = "recent" if is_recent else "archived"
            status_text = "Recent" if is_recent else "Archived"
            
            html_content += f"""
    <div class="publication {status_class}">
        <div class="date">{pub_date.strftime('%A, %B %d, %Y')}</div>
        <div class="stats">
            📄 {pub.get('content_count', 0)} content items | 
            📁 {pub.get('path', 'Unknown')} |
            🏷️ {status_text}
        </div>
    </div>
"""
        
        html_content += """
</body>
</html>"""
        
        # Save archive hub index
        index_html = self.archive_hub_dir / "index.html"
        with open(index_html, 'w') as f:
            f.write(html_content)
        
        return str(index_html)


def main():
    """Main execution for archive management"""
    import argparse
    
    parser = argparse.ArgumentParser(description='CurationsLA Archive Manager')
    parser.add_argument('--cleanup', action='store_true', help='Clean up old archives')
    parser.add_argument('--generate-hub', action='store_true', help='Generate archive hub')
    parser.add_argument('--check-duplicates', help='Check for duplicates in given path')
    parser.add_argument('--archive', help='Archive publication at given path')
    parser.add_argument('--previous', action='store_true', help='Show previous publication')
    
    args = parser.parse_args()
    
    manager = ArchiveManager()
    
    if args.cleanup:
        print("🧹 Cleaning up old archives...")
        result = manager.cleanup_old_archives()
        print(f"✅ Cleaned {result['cleaned_count']} old archives, kept {result['kept_count']} recent ones")
    
    if args.generate_hub:
        print("🏗️  Generating archive hub...")
        hub_path = manager.generate_archive_hub_index()
        print(f"✅ Archive hub generated: {hub_path}")
    
    if args.check_duplicates:
        print(f"🔍 Checking for duplicates in: {args.check_duplicates}")
        pub_path = Path(args.check_duplicates)
        if pub_path.exists():
            items = manager.extract_content_items(pub_path)
            duplicates = manager.check_for_duplicates(items)
            print(f"📊 Found {duplicates['duplicate_count']} duplicates, {duplicates['unique_count']} unique items")
            
            for dup in duplicates['duplicates'][:5]:  # Show first 5 duplicates
                print(f"   🔄 Duplicate: {dup['item']['content'][:60]}...")
        else:
            print(f"❌ Path not found: {pub_path}")
    
    if args.archive:
        print(f"📁 Archiving publication: {args.archive}")
        pub_path = Path(args.archive)
        if pub_path.exists():
            pub_date = datetime.now()  # You might want to extract actual date
            record = manager.archive_publication(pub_date, pub_path)
            print(f"✅ Archived with {record['content_count']} items")
        else:
            print(f"❌ Path not found: {pub_path}")
    
    if args.previous:
        print("📅 Finding previous publication...")
        current_date = datetime(2025, 9, 26)  # Friday target
        previous = manager.get_previous_publication(current_date)
        if previous:
            print(f"✅ Previous publication: {previous['date']} ({previous['content_count']} items)")
            print(f"📁 Path: {previous['path']}")
        else:
            print("⚠️  No previous publication found")


if __name__ == "__main__":
    main()