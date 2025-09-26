#!/usr/bin/env python3
"""
CurationsLA Event Sourcing Integration
Main integration script for the CurationsLA automation system
Handles Friday-Sunday event sourcing from The Scenestar's show list
"""

import sys
import argparse
from pathlib import Path
from datetime import datetime

# Add the scripts directory to the path
sys.path.append(str(Path(__file__).parent))

from friday_sunday_sourcing import SCENESTAR_EVENT_DATA, EventParser

class CurationsLAEventSourcing:
    """Main class for CurationsLA event sourcing integration"""
    
    def __init__(self):
        self.parser = EventParser()
        self.output_dir = Path(__file__).parent.parent / "output" / "2025-09-26"
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def generate_event_tables(self, days=None, output_format='html'):
        """Generate event tables for specified days"""
        if days is None:
            days = ['FRIDAY', 'SATURDAY', 'SUNDAY']
        
        print(f"🌴 CurationsLA Event Sourcing: {', '.join(days)}")
        print("=" * 60)
        print("Generating well-formatted LA events for September 26-28, 2025")
        print("Source: The Scenestar's on-screen show list")
        print()
        
        # Parse events
        events = self.parser.parse_event_data(SCENESTAR_EVENT_DATA, days)
        
        if not events:
            print("⚠️  No events found for specified days")
            return None
        
        # Generate output based on format
        if output_format == 'html':
            return self._generate_html_output(events, days)
        elif output_format == 'markdown':
            return self._generate_markdown_output(events, days)
        elif output_format == 'json':
            return self._generate_json_output(events, days)
        else:
            raise ValueError(f"Unsupported output format: {output_format}")
    
    def _generate_html_output(self, events, days):
        """Generate HTML formatted output"""
        html_content = ""
        
        for day in days:
            table = self.parser.generate_table_html(events, day)
            if table:
                html_content += table + "\n\n"
        
        # Save full HTML file
        html_file = self.output_dir / "friday-sunday-events.html"
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(self._get_html_template(html_content))
        
        print(f"✅ HTML output saved to: {html_file}")
        return html_content.strip()
    
    def _generate_markdown_output(self, events, days):
        """Generate Markdown formatted output"""
        markdown_content = "# CurationsLA: Friday - Sunday Events\n\n"
        markdown_content += "**September 26-28, 2025**\n\n"
        markdown_content += "*Source: The Scenestar's on-screen show list*\n\n"
        
        for day in days:
            day_events = [e for e in events if e['day'] == day]
            if not day_events:
                continue
            
            day_events.sort(key=lambda x: x['time'])
            
            markdown_content += f"## {day}'S EVENTS\n\n"
            
            for event in day_events:
                markdown_content += f"**{event['time']} {event['emoji']} {event['event_name']}**\n\n"
                markdown_content += f"{event['description']} [{event['venue']}]({event['venue_url']})\n\n"
        
        # Save markdown file
        md_file = self.output_dir / "friday-sunday-events.md"
        with open(md_file, 'w', encoding='utf-8') as f:
            f.write(markdown_content)
        
        print(f"✅ Markdown output saved to: {md_file}")
        return markdown_content
    
    def _generate_json_output(self, events, days):
        """Generate JSON formatted output"""
        import json
        
        json_data = {
            'title': 'CurationsLA: Friday - Sunday Events',
            'date_range': 'September 26-28, 2025',
            'source': "The Scenestar's on-screen show list",
            'generated': datetime.now().isoformat(),
            'events_by_day': {}
        }
        
        for day in days:
            day_events = [e for e in events if e['day'] == day]
            if day_events:
                day_events.sort(key=lambda x: x['time'])
                json_data['events_by_day'][day.lower()] = day_events
        
        # Save JSON file
        json_file = self.output_dir / "friday-sunday-events.json"
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(json_data, f, indent=2, ensure_ascii=False)
        
        print(f"✅ JSON output saved to: {json_file}")
        return json_data
    
    def _get_html_template(self, content):
        """Get HTML template with embedded content"""
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CurationsLA: Friday - Sunday Events | September 26-28, 2025</title>
    <style>
        body {{ font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }}
        table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
        th {{ background-color: #f4f4f4; padding: 15px; text-align: left; }}
        td {{ padding: 15px; border-bottom: 1px solid #eee; }}
        strong {{ font-weight: bold; }}
        a {{ color: #0066cc; text-decoration: none; }}
        a:hover {{ text-decoration: underline; }}
        .header {{ text-align: center; margin-bottom: 30px; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🌴 CurationsLA: Friday - Sunday Events</h1>
        <h2>September 26-28, 2025</h2>
        <p><em>Source: The Scenestar's on-screen show list</em></p>
    </div>
    
{content}

    <footer style="text-align: center; margin-top: 40px; padding-top: 20px; border-top: 1px solid #eee;">
        <p><strong>Made with 💜 in Los Angeles</strong></p>
        <p><em>CurationsLA - Bringing Good Vibes when our city needs it most</em></p>
    </footer>
</body>
</html>"""
    
    def get_event_count_by_day(self):
        """Get count of events by day for reporting"""
        events = self.parser.parse_event_data(SCENESTAR_EVENT_DATA, ['FRIDAY', 'SATURDAY', 'SUNDAY'])
        
        counts = {}
        for day in ['FRIDAY', 'SATURDAY', 'SUNDAY']:
            day_events = [e for e in events if e['day'] == day]
            counts[day] = len(day_events)
        
        return counts
    
    def validate_requirements(self):
        """Validate that all formatting requirements are met"""
        print("🔍 Validating formatting requirements...")
        
        # Run basic validation
        events = self.parser.parse_event_data(SCENESTAR_EVENT_DATA, ['FRIDAY', 'SATURDAY', 'SUNDAY'])
        
        if not events:
            print("❌ No events parsed")
            return False
        
        # Check required elements
        for event in events[:5]:  # Check first 5 events
            # Time format
            if not event['time'].endswith(('AM', 'PM')):
                print(f"❌ Time format issue: {event['time']}")
                return False
            
            # Emoji present
            if not event['emoji']:
                print(f"❌ Missing emoji for: {event['event_name']}")
                return False
            
            # Event name is uppercase
            if not event['event_name'].isupper():
                print(f"❌ Event name not uppercase: {event['event_name']}")
                return False
            
            # Venue name is uppercase
            if not event['venue'].isupper():
                print(f"❌ Venue name not uppercase: {event['venue']}")
                return False
        
        print("✅ All formatting requirements validated!")
        return True

def main():
    """Main CLI interface"""
    parser = argparse.ArgumentParser(description='CurationsLA Event Sourcing')
    parser.add_argument('--days', nargs='+', choices=['FRIDAY', 'SATURDAY', 'SUNDAY'],
                        default=['FRIDAY', 'SATURDAY', 'SUNDAY'],
                        help='Days to include in output')
    parser.add_argument('--format', choices=['html', 'markdown', 'json'],
                        default='html', help='Output format')
    parser.add_argument('--validate', action='store_true',
                        help='Validate formatting requirements')
    parser.add_argument('--stats', action='store_true',
                        help='Show event statistics')
    
    args = parser.parse_args()
    
    # Initialize sourcing system
    sourcing = CurationsLAEventSourcing()
    
    # Handle different commands
    if args.validate:
        success = sourcing.validate_requirements()
        sys.exit(0 if success else 1)
    
    if args.stats:
        counts = sourcing.get_event_count_by_day()
        print("📊 Event Statistics:")
        for day, count in counts.items():
            print(f"   {day}: {count} events")
        total = sum(counts.values())
        print(f"   TOTAL: {total} events")
        return
    
    # Generate event tables
    output = sourcing.generate_event_tables(args.days, args.format)
    
    if output:
        print("\n🎉 Event sourcing completed successfully!")
        print(f"📊 Generated events for: {', '.join(args.days)}")
        print(f"🎯 Output format: {args.format}")
        
        # Show sample output if HTML
        if args.format == 'html' and len(output) > 200:
            print(f"\n📝 Sample output (first 200 chars):")
            print(output[:200] + "...")
    else:
        print("❌ No output generated")
        sys.exit(1)

if __name__ == "__main__":
    main()