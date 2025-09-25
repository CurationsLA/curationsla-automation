#!/usr/bin/env python3
"""
CurationsLA Publication Showcase
Display previous publications and help agents reference past content
"""

import os
import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any
import re
from archive_manager import ArchiveManager

# Configuration
BASE_DIR = Path(__file__).parent.parent
CONTENT_DIR = BASE_DIR / "content"

class PublicationShowcase:
    def __init__(self):
        self.content_dir = CONTENT_DIR
        self.archive_manager = ArchiveManager()
    
    def showcase_previous_publication(self, current_date: datetime = None) -> Dict:
        """Showcase the most recent publication before current date"""
        if not current_date:
            current_date = datetime.now()
        
        print(f"🔍 Searching for publications before {current_date.strftime('%A, %B %d, %Y')}...")
        
        # Get previous publication
        previous = self.archive_manager.get_previous_publication(current_date)
        
        if not previous:
            print("⚠️  No previous publication found")
            return {}
        
        print(f"\n📅 Most Recent Previous Publication")
        print("=" * 50)
        
        prev_date = datetime.fromisoformat(previous['date'])
        print(f"📆 Date: {prev_date.strftime('%A, %B %d, %Y')}")
        print(f"📁 Path: {previous['path']}")
        print(f"📄 Content Items: {previous.get('content_count', 'Unknown')}")
        print(f"🔗 Status: {'Available' if previous.get('exists') else 'Archived'}")
        
        # Try to load and display content samples
        if previous.get('exists'):
            pub_path = BASE_DIR / previous['path']
            content_samples = self._extract_content_samples(pub_path)
            
            if content_samples:
                print(f"\n📋 Content Samples:")
                print("-" * 30)
                
                for i, sample in enumerate(content_samples[:5], 1):
                    print(f"{i}. {sample['type']}: {sample['preview']}")
                    if sample.get('source'):
                        print(f"   Source: {sample['source']}")
                    print()
        
        return previous
    
    def _extract_content_samples(self, pub_path: Path) -> List[Dict]:
        """Extract content samples from a publication"""
        samples = []
        
        # Look for newsletter files
        for newsletter_file in pub_path.glob("newsletter-*.md"):
            try:
                with open(newsletter_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Extract different types of content
                samples.extend(self._parse_newsletter_content(content, newsletter_file.name))
                
            except Exception as e:
                print(f"⚠️  Error reading {newsletter_file}: {str(e)}")
        
        # Look for JSON content
        for json_file in pub_path.glob("*.json"):
            if json_file.name in ['stats.json', 'newsletter-content.json']:
                try:
                    with open(json_file, 'r') as f:
                        data = json.load(f)
                    
                    if json_file.name == 'stats.json':
                        samples.append({
                            'type': 'Statistics',
                            'preview': f"Generated {data.get('total_items', 0)} items across {len(data.get('categories', {}))} categories",
                            'source': 'stats.json'
                        })
                    
                    elif json_file.name == 'newsletter-content.json':
                        # Extract content from JSON structure
                        if isinstance(data, dict):
                            for category, items in data.items():
                                if isinstance(items, list) and items:
                                    sample_item = items[0]
                                    if isinstance(sample_item, dict) and 'title' in sample_item:
                                        samples.append({
                                            'type': f'{category.title()} Content',
                                            'preview': sample_item['title'][:80] + "..." if len(sample_item['title']) > 80 else sample_item['title'],
                                            'source': f'newsletter-content.json ({category})'
                                        })
                
                except Exception as e:
                    print(f"⚠️  Error reading {json_file}: {str(e)}")
        
        return samples
    
    def _parse_newsletter_content(self, content: str, filename: str) -> List[Dict]:
        """Parse newsletter content for samples"""
        samples = []
        lines = content.split('\n')
        
        current_section = None
        
        for line in lines:
            line = line.strip()
            
            # Detect section headers
            if line.startswith('##') or line.startswith('####'):
                section_match = re.search(r'[#]+\s*(.+)', line)
                if section_match:
                    current_section = section_match.group(1).strip()
            
            # Look for content items
            elif line and not line.startswith(('#', '|', '---', '**', '![', '•', '-')):
                if len(line) > 30 and current_section:
                    samples.append({
                        'type': current_section,
                        'preview': line[:100] + "..." if len(line) > 100 else line,
                        'source': filename
                    })
        
        return samples
    
    def compare_with_new_content(self, new_content_path: Path, previous_pub: Dict = None) -> Dict:
        """Compare new content with previous publication to identify potential duplicates"""
        
        if not previous_pub:
            current_date = datetime(2025, 9, 26)  # Target date
            previous_pub = self.archive_manager.get_previous_publication(current_date)
        
        if not previous_pub or not previous_pub.get('exists'):
            return {
                'has_previous': False,
                'duplicates': [],
                'comparison_possible': False
            }
        
        print(f"\n🔄 Comparing with previous publication from {previous_pub['date']}")
        print("=" * 60)
        
        # Extract content from new publication
        new_items = self.archive_manager.extract_content_items(new_content_path)
        
        # Check for duplicates
        duplicate_analysis = self.archive_manager.check_for_duplicates(new_items)
        
        print(f"📊 Duplicate Analysis Results:")
        print(f"   ✅ Unique items: {duplicate_analysis['unique_count']}")
        print(f"   🔄 Potential duplicates: {duplicate_analysis['duplicate_count']}")
        
        if duplicate_analysis['duplicates']:
            print(f"\n⚠️  Potential Duplicates Found:")
            print("-" * 40)
            
            for i, dup in enumerate(duplicate_analysis['duplicates'][:5], 1):
                content_preview = dup['item']['content'][:80] + "..." if len(dup['item']['content']) > 80 else dup['item']['content']
                prev_date = dup['previous_publication']['publication_date']
                
                print(f"{i}. {content_preview}")
                print(f"   Previously published: {prev_date}")
                print()
        
        return {
            'has_previous': True,
            'previous_date': previous_pub['date'],
            'duplicates': duplicate_analysis['duplicates'],
            'unique_items': duplicate_analysis['unique_items'],
            'duplicate_count': duplicate_analysis['duplicate_count'],
            'unique_count': duplicate_analysis['unique_count'],
            'comparison_possible': True
        }
    
    def generate_agent_reference_guide(self) -> str:
        """Generate a reference guide for agents based on previous publications"""
        
        print("📚 Generating Agent Reference Guide...")
        
        # Get recent publications for analysis
        try:
            with open(self.archive_manager.index_file, 'r') as f:
                index_data = json.load(f)
        except:
            index_data = {'publications': []}
        
        # Analyze patterns from recent publications
        recent_pubs = sorted(index_data.get('publications', []), 
                           key=lambda x: x['date'], reverse=True)[:5]
        
        guide_content = f"""# 🤖 CurationsLA Agent Reference Guide

Generated: {datetime.now().strftime('%A, %B %d, %Y at %I:%M %p')}

## 📋 Recent Publication Analysis

Based on the last {len(recent_pubs)} publications, here are patterns and guidelines for content sourcing:

"""
        
        if recent_pubs:
            guide_content += "### 📊 Publication Statistics\n\n"
            
            total_items = sum(pub.get('content_count', 0) for pub in recent_pubs)
            avg_items = total_items / len(recent_pubs) if recent_pubs else 0
            
            guide_content += f"- **Average Content Items**: {avg_items:.1f} per publication\n"
            guide_content += f"- **Total Items Analyzed**: {total_items}\n"
            guide_content += f"- **Publications Reviewed**: {len(recent_pubs)}\n\n"
            
            guide_content += "### 📅 Recent Publications\n\n"
            
            for pub in recent_pubs:
                pub_date = datetime.fromisoformat(pub['date'])
                guide_content += f"- **{pub_date.strftime('%B %d, %Y')}**: {pub.get('content_count', 0)} items\n"
            
            guide_content += "\n"
        
        guide_content += """### 🎯 Content Sourcing Guidelines

Based on successful previous publications:

#### ✅ Content Characteristics to Target:
- **Fresh Content**: Published within 3 days of newsletter date
- **Community Focus**: Local LA stories, business openings, events
- **Positive Tone**: Good vibes content that celebrates community
- **Geographic Diversity**: Cover multiple LA neighborhoods
- **Category Balance**: Ensure representation across all specialties

#### ❌ Content to Avoid:
- **Outdated Information**: Anything older than 3 days
- **Duplicate Content**: Check against recent publications
- **Negative News**: Crime, politics, controversy, rage-bait
- **Generic Content**: Non-LA specific stories

#### 🔍 Quality Indicators:
- **Local Relevance**: Mentions specific LA neighborhoods, venues, or people
- **Actionable Information**: Readers can visit, attend, or engage
- **Community Impact**: Stories that bring people together
- **Fresh Perspective**: New angles on familiar topics

### 🏘️ Neighborhood Coverage Priority

Ensure balanced coverage across LA areas:
- **Downtown/DTLA**: Business, arts, development
- **Westside**: Dining, entertainment, beaches  
- **Eastside**: Culture, community, creative scene
- **Valley**: Family events, recreation, local business
- **South LA**: Community initiatives, local heroes

### 📝 Content Sourcing Checklist

Before including any content item:

1. ✅ **Freshness Check**: Published within last 3 days?
2. ✅ **Duplicate Check**: Not in recent publications?
3. ✅ **Good Vibes Score**: Meets positivity threshold?
4. ✅ **LA Relevance**: Specific to Los Angeles area?
5. ✅ **Community Value**: Beneficial to readers?

---

*This guide is automatically updated based on publication patterns and should be referenced when agents are uncertain about content selection.*
"""
        
        # Save reference guide
        guide_file = self.archive_manager.archive_hub_dir / "agent_reference_guide.md"
        with open(guide_file, 'w') as f:
            f.write(guide_content)
        
        print(f"✅ Agent reference guide generated: {guide_file}")
        
        return str(guide_file)


def main():
    """Main execution for publication showcase"""
    import argparse
    
    parser = argparse.ArgumentParser(description='CurationsLA Publication Showcase')
    parser.add_argument('--show-previous', action='store_true', help='Show previous publication')
    parser.add_argument('--compare', help='Compare new content with previous publication')
    parser.add_argument('--generate-guide', action='store_true', help='Generate agent reference guide')
    parser.add_argument('--date', help='Target date (YYYY-MM-DD) for comparisons')
    
    args = parser.parse_args()
    
    showcase = PublicationShowcase()
    
    # Parse target date if provided
    target_date = None
    if args.date:
        try:
            target_date = datetime.strptime(args.date, '%Y-%m-%d')
        except ValueError:
            print(f"❌ Invalid date format: {args.date}. Use YYYY-MM-DD")
            return
    
    if args.show_previous:
        print("📅 CurationsLA Publication Showcase")
        print("=" * 40)
        showcase.showcase_previous_publication(target_date)
    
    if args.compare:
        new_content_path = Path(args.compare)
        if new_content_path.exists():
            comparison = showcase.compare_with_new_content(new_content_path)
            
            if comparison['comparison_possible']:
                if comparison['duplicate_count'] > 0:
                    print(f"\n⚠️  Warning: {comparison['duplicate_count']} potential duplicates found!")
                    print("Consider revising content to ensure freshness.")
                else:
                    print(f"\n✅ No duplicates detected! All {comparison['unique_count']} items appear to be fresh.")
            else:
                print("\n✅ No previous publication to compare against. All content is considered fresh.")
        else:
            print(f"❌ Content path not found: {new_content_path}")
    
    if args.generate_guide:
        guide_path = showcase.generate_agent_reference_guide()
        print(f"\n📚 Agent reference guide available at: {guide_path}")


if __name__ == "__main__":
    main()