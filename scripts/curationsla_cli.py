#!/usr/bin/env python3
"""
CurationsLA Command Line Interface
Unified interface for all CurationsLA automation features
"""

import argparse
import sys
from datetime import datetime
from pathlib import Path

# Add current directory to path for imports
sys.path.append(str(Path(__file__).parent))

def main():
    """Main CLI interface"""
    parser = argparse.ArgumentParser(
        description='CurationsLA Automation CLI',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate newsletter with duplicate prevention
  python curationsla_cli.py generate --enhanced
  
  # Show previous publication
  python curationsla_cli.py showcase --previous
  
  # Check for duplicates in current content
  python curationsla_cli.py showcase --compare output/2025-09-26
  
  # Clean up old archives (7+ days)
  python curationsla_cli.py archive --cleanup
  
  # Generate archive hub index
  python curationsla_cli.py archive --generate-hub
  
  # Generate agent reference guide
  python curationsla_cli.py showcase --generate-guide
"""
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Generate command
    gen_parser = subparsers.add_parser('generate', help='Generate newsletter content')
    gen_parser.add_argument('--enhanced', action='store_true', 
                           help='Use enhanced generation with duplicate prevention')
    gen_parser.add_argument('--date', help='Target date (YYYY-MM-DD)')
    
    # Showcase command
    show_parser = subparsers.add_parser('showcase', help='Showcase and compare publications')
    show_parser.add_argument('--previous', action='store_true', 
                            help='Show previous publication')
    show_parser.add_argument('--compare', 
                            help='Compare new content with previous (path to content)')
    show_parser.add_argument('--generate-guide', action='store_true',
                            help='Generate agent reference guide')
    show_parser.add_argument('--date', help='Target date (YYYY-MM-DD)')
    
    # Archive command
    arch_parser = subparsers.add_parser('archive', help='Manage publication archives')
    arch_parser.add_argument('--cleanup', action='store_true',
                            help='Clean up archives older than 7 days')
    arch_parser.add_argument('--generate-hub', action='store_true',
                            help='Generate archive hub index')
    arch_parser.add_argument('--check-duplicates',
                            help='Check for duplicates in given path')
    arch_parser.add_argument('--archive-path',
                            help='Archive publication at given path')
    
    # Test command
    test_parser = subparsers.add_parser('test', help='Test system components')
    test_parser.add_argument('--web-scraping', action='store_true',
                            help='Test web scraping functionality')
    test_parser.add_argument('--validate', action='store_true',
                            help='Validate all enhancements')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    # Execute commands
    if args.command == 'generate':
        from content_generator import ContentGenerator, ARCHIVE_MANAGEMENT_AVAILABLE
        
        print("🌴 CurationsLA Newsletter Generation")
        print("=" * 40)
        
        generator = ContentGenerator()
        
        if args.enhanced and ARCHIVE_MANAGEMENT_AVAILABLE:
            print("✨ Using enhanced generation with duplicate prevention")
            generator.generate_enhanced_newsletter()
        elif args.enhanced:
            print("⚠️  Enhanced features not available, using standard generation")
            generator.generate_newsletter()
        else:
            print("📝 Using standard newsletter generation")
            generator.generate_newsletter()
    
    elif args.command == 'showcase':
        try:
            from publication_showcase import PublicationShowcase
            
            showcase = PublicationShowcase()
            
            # Parse target date if provided
            target_date = None
            if args.date:
                try:
                    target_date = datetime.strptime(args.date, '%Y-%m-%d')
                except ValueError:
                    print(f"❌ Invalid date format: {args.date}. Use YYYY-MM-DD")
                    return
            
            if args.previous:
                print("📅 CurationsLA Publication Showcase")
                print("=" * 40)
                showcase.showcase_previous_publication(target_date)
            
            elif args.compare:
                content_path = Path(args.compare)
                if content_path.exists():
                    print(f"🔄 Comparing content with previous publications")
                    print("=" * 50)
                    
                    comparison = showcase.compare_with_new_content(content_path)
                    
                    if comparison['comparison_possible']:
                        if comparison['duplicate_count'] > 0:
                            print(f"\n⚠️  Warning: {comparison['duplicate_count']} potential duplicates found!")
                            print("Consider revising content to ensure freshness.")
                        else:
                            print(f"\n✅ No duplicates detected! All {comparison['unique_count']} items appear to be fresh.")
                    else:
                        print("\n✅ No previous publication to compare against. All content is considered fresh.")
                else:
                    print(f"❌ Content path not found: {content_path}")
            
            elif args.generate_guide:
                print("📚 Generating Agent Reference Guide")
                print("=" * 40)
                guide_path = showcase.generate_agent_reference_guide()
                print(f"\n✅ Agent reference guide generated: {guide_path}")
            
            else:
                print("Please specify --previous, --compare, or --generate-guide")
        
        except ImportError:
            print("❌ Archive management features not available")
            print("Install required dependencies or check import paths")
    
    elif args.command == 'archive':
        try:
            from archive_manager import ArchiveManager
            
            manager = ArchiveManager()
            
            if args.cleanup:
                print("🧹 Cleaning up old archives (7+ days)")
                print("=" * 40)
                result = manager.cleanup_old_archives()
                print(f"✅ Cleaned {result['cleaned_count']} old archives, kept {result['kept_count']} recent ones")
            
            elif args.generate_hub:
                print("🏗️  Generating archive hub")
                print("=" * 30)
                hub_path = manager.generate_archive_hub_index()
                print(f"✅ Archive hub generated: {hub_path}")
            
            elif args.check_duplicates:
                print(f"🔍 Checking for duplicates in: {args.check_duplicates}")
                print("=" * 50)
                
                pub_path = Path(args.check_duplicates)
                if pub_path.exists():
                    items = manager.extract_content_items(pub_path)
                    duplicates = manager.check_for_duplicates(items)
                    print(f"📊 Found {duplicates['duplicate_count']} duplicates, {duplicates['unique_count']} unique items")
                    
                    if duplicates['duplicates']:
                        print("\n🔄 Sample duplicates:")
                        for i, dup in enumerate(duplicates['duplicates'][:3], 1):
                            content_preview = dup['item']['content'][:60] + "..."
                            print(f"   {i}. {content_preview}")
                else:
                    print(f"❌ Path not found: {pub_path}")
            
            elif args.archive_path:
                print(f"📁 Archiving publication: {args.archive_path}")
                print("=" * 40)
                
                pub_path = Path(args.archive_path)
                if pub_path.exists():
                    pub_date = datetime.now()  # You might want to extract actual date
                    record = manager.archive_publication(pub_date, pub_path)
                    print(f"✅ Archived with {record['content_count']} items")
                else:
                    print(f"❌ Path not found: {pub_path}")
            
            else:
                print("Please specify --cleanup, --generate-hub, --check-duplicates, or --archive-path")
        
        except ImportError:
            print("❌ Archive management features not available")
            print("Install required dependencies or check import paths")
    
    elif args.command == 'test':
        if args.web_scraping:
            try:
                from test_web_scraping import main as test_scraping
                print("🕷️  Testing Web Scraping")
                print("=" * 30)
                test_scraping()
            except ImportError:
                print("❌ Web scraping test not available")
        
        elif args.validate:
            try:
                from validate_enhancements import main as validate
                print("🧪 Validating All Enhancements")
                print("=" * 35)
                validate()
            except ImportError:
                print("❌ Validation script not available")
        
        else:
            print("Please specify --web-scraping or --validate")


if __name__ == "__main__":
    main()