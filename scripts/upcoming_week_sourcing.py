#!/usr/bin/env python3
"""
CurationsLA: Upcoming Week Events Sourcing Script
Generates well-formatted list of Los Angeles events for September 29 - October 5, 2025
from The Scenestar's on-screen show list data
"""

import sys
import re
from pathlib import Path
sys.path.append(str(Path(__file__).parent))

from event_sourcing_parser import EventParser

# Event data for September 29 - October 5, 2025
SCENESTAR_EVENT_DATA = """
MONDAY, SEPTEMBER 29, 2025

09.29.25 <a href="https://www.hollywoodbowl.com/">John Legend</a> at the Hollywood Bowl (7:30pm)
09.29.25 <a href="https://thecomedystore.com/">Monday Night Comedy</a> at The Comedy Store (8:00pm)
09.29.25 <a href="https://www.lagreektheatre.com/">Kali Uchis w/ Thee Sacred Souls</a> at the Greek Theatre (8:00pm)
09.29.25 <a href="https://www.troubadour.com/">The Hold Steady</a> at the Troubadour (7:00pm)
09.29.25 <a href="https://www.palladiumhollywood.com/">LCD Soundsystem</a> at the Hollywood Palladium (8:00pm)

TUESDAY, SEPTEMBER 30, 2025

09.30.25 <a href="https://www.hollywoodbowl.com/">Laufey w/ Suki Waterhouse</a> at the Hollywood Bowl (7:30pm)
09.30.25 <a href="https://thecomedystore.com/">Tuesday Night Live</a> at The Comedy Store (8:00pm)
09.30.25 <a href="https://www.lagreektheatre.com/">Alex G w/ Nilüfer Yanya</a> at the Greek Theatre (8:00pm)
09.30.25 <a href="https://www.teragramballroom.com/">Magdalena Bay</a> at the Teragram Ballroom (8:00pm)
09.30.25 <a href="https://www.elrey.com/">Jacques Greene</a> at El Rey Theatre (9:00pm)

WEDNESDAY, OCTOBER 1, 2025

10.01.25 <a href="https://www.hollywoodbowl.com/">Tate McRae</a> at the Hollywood Bowl (7:30pm)
10.01.25 <a href="https://thecomedystore.com/">Wednesday Comedy Showcase</a> at The Comedy Store (8:00pm)
10.01.25 <a href="https://www.lagreektheatre.com/">Chevelle w/ Asking Alexandria</a> at the Greek Theatre (8:00pm)
10.01.25 <a href="https://www.troubadour.com/">Rainbow Kitten Surprise</a> at the Troubadour (7:00pm)
10.01.25 <a href="https://www.spacelandpresents.com/">The Waterboys</a> at the Echoplex (8:00pm)

THURSDAY, OCTOBER 2, 2025

10.02.25 <a href="https://www.hollywoodbowl.com/">Kamasi Washington</a> at the Hollywood Bowl (7:30pm)
10.02.25 <a href="https://thecomedystore.com/">Thursday Night Special</a> at The Comedy Store (8:00pm)
10.02.25 <a href="https://www.lagreektheatre.com/">The Soul Rebels</a> at the Greek Theatre (8:00pm)
10.02.25 <a href="https://www.troubadour.com/">Yeule</a> at the Troubadour (7:00pm)
10.02.25 <a href="https://www.palladiumhollywood.com/">Pino Palladino & Blake Mills</a> at the Hollywood Palladium (8:00pm)

FRIDAY, OCTOBER 3, 2025

10.03.25 <a href="https://www.hollywoodbowl.com/">Ice Cube</a> at the Hollywood Bowl (7:30pm)
10.03.25 <a href="https://thecomedystore.com/">Friday Night Live</a> at The Comedy Store (8:00pm)
10.03.25 <a href="https://www.lagreektheatre.com/">The Head and The Heart</a> at the Greek Theatre (8:00pm)
10.03.25 <a href="https://www.troubadour.com/">S.G. Goodman</a> at the Troubadour (7:00pm)
10.03.25 <a href="https://www.palladiumhollywood.com/">Mudvayne</a> at the Hollywood Palladium (8:00pm)

SATURDAY, OCTOBER 4, 2025

10.04.25 <a href="https://www.hollywoodbowl.com/">Atif Aslam</a> at the Hollywood Bowl (7:30pm)
10.04.25 <a href="https://thecomedystore.com/">Saturday Night Comedy</a> at The Comedy Store (8:00pm)
10.04.25 <a href="https://www.lagreektheatre.com/">Lucinda Williams</a> at the Greek Theatre (8:00pm)
10.04.25 <a href="https://www.troubadour.com/">Mae w/ The Spill Canvas</a> at the Troubadour (7:00pm)
10.04.25 <a href="https://www.palladiumhollywood.com/">Vola</a> at the Hollywood Palladium (8:00pm)

SUNDAY, OCTOBER 5, 2025

10.05.25 <a href="https://www.hollywoodbowl.com/">Jeffrey Osborne</a> at the Hollywood Bowl (7:30pm)
10.05.25 <a href="https://thecomedystore.com/">Sunday Night Special</a> at The Comedy Store (8:00pm)
10.05.25 <a href="https://www.lagreektheatre.com/">Daisy The Great</a> at the Greek Theatre (8:00pm)
10.05.25 <a href="https://www.troubadour.com/">Tei Shi</a> at the Troubadour (7:00pm)
10.05.25 <a href="https://www.palladiumhollywood.com/">Mr. Gnome</a> at the Hollywood Palladium (8:00pm)
"""

def main():
    """Generate formatted event tables for Monday-Sunday September 29 - October 5, 2025"""
    print("🌴 CurationsLA: Upcoming Week Events Sourcing")
    print("=" * 60)
    print("Generating well-formatted LA events for September 29 - October 5, 2025")
    print("Source: The Scenestar's on-screen show list")
    print()
    
    # Initialize parser with extended capabilities
    parser = UpcomingWeekEventParser()
    
    # Generate formatted tables
    formatted_output = parser.format_events(SCENESTAR_EVENT_DATA)
    
    # Output the results
    print(formatted_output)
    
    # Save to file
    output_dir = Path(__file__).parent.parent / "output" / "2025-09-29"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    output_file = output_dir / "upcoming-week-events.html"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CurationsLA: Upcoming Week Events - September 29 - October 5, 2025</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; margin: 40px; line-height: 1.6; color: #333; }}
        .header {{ text-align: center; margin-bottom: 40px; padding-bottom: 20px; border-bottom: 2px solid #e0e0e0; }}
        .header h1 {{ color: #2c3e50; margin-bottom: 10px; }}
        .header h2 {{ color: #34495e; font-weight: normal; }}
        .header p {{ color: #7f8c8d; font-style: italic; }}
        table {{ width: 100%; border-collapse: collapse; margin: 20px 0; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }}
        th {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 15px; text-align: left; font-size: 1.1em; }}
        td {{ padding: 12px 15px; border-bottom: 1px solid #eee; }}
        tr:hover {{ background-color: #f8f9fa; }}
        a {{ color: #3498db; text-decoration: none; }}
        a:hover {{ text-decoration: underline; }}
        strong {{ font-weight: 600; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🌴 CurationsLA: Upcoming Week Events</h1>
        <h2>September 29 - October 5, 2025</h2>
        <p><em>Source: The Scenestar's on-screen show list</em></p>
    </div>
    
{formatted_output}

    <footer style="text-align: center; margin-top: 40px; padding-top: 20px; border-top: 1px solid #eee;">
        <p><strong>Made with 💜 in Los Angeles</strong></p>
        <p><em>CurationsLA - Bringing Good Vibes when our city needs it most</em></p>
    </footer>
</body>
</html>""")
    
    # Also save markdown version
    markdown_file = output_dir / "upcoming-week-events.md"
    with open(markdown_file, 'w', encoding='utf-8') as f:
        f.write(f"""# CurationsLA: Upcoming Week Events

**September 29 - October 5, 2025**

*Source: The Scenestar's on-screen show list*

{parser.format_events_markdown(SCENESTAR_EVENT_DATA)}

---

**Made with 💜 in Los Angeles**  
*CurationsLA - Bringing Good Vibes when our city needs it most*
""")
    
    print(f"\n✅ Event data saved to: {output_file}")
    print(f"📄 Markdown version saved to: {markdown_file}")
    print(f"📊 Generated formatted tables for upcoming week events")
    print(f"🎉 Ready for CurationsLA newsletter integration!")

# Custom parser class that extends EventParser for the upcoming week
class UpcomingWeekEventParser(EventParser):
    """Extended parser for upcoming week events (Sept 29 - Oct 5, 2025)"""
    
    def parse_event_data(self, raw_data: str, date_filter=None) -> list:
        """Parse raw event data and filter by date"""
        events = []
        lines = raw_data.strip().split('\n')
        
        current_date = None
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Check if line is a date header - extend to handle weekdays
            date_match = re.match(r'^(MONDAY|TUESDAY|WEDNESDAY|THURSDAY|FRIDAY|SATURDAY|SUNDAY),?\s+(.+?)(\d{4})$', line.upper())
            if date_match:
                current_date = date_match.group(1)
                continue
            
            # Skip non-event lines - handle both September and October dates
            if not line.startswith(('09.29.25', '09.30.25', '10.01.25', '10.02.25', '10.03.25', '10.04.25', '10.05.25')):
                continue
            
            # Parse event line
            event_match = re.match(r'^(\d{2}\.\d{2}\.\d{2})\s+(.+)$', line)
            if event_match:
                date_str = event_match.group(1)
                event_text = event_match.group(2)
                
                # Determine which day this event belongs to
                day_mapping = {
                    '09.29.25': 'MONDAY',
                    '09.30.25': 'TUESDAY', 
                    '10.01.25': 'WEDNESDAY',
                    '10.02.25': 'THURSDAY',
                    '10.03.25': 'FRIDAY',
                    '10.04.25': 'SATURDAY',
                    '10.05.25': 'SUNDAY'
                }
                
                day = day_mapping.get(date_str)
                if not day:
                    continue
                
                # Skip if this day isn't in our filter
                if date_filter and day not in date_filter:
                    continue
                
                # Extract time from the event text
                time_match = re.search(r'\(([^)]+)\)$', event_text)
                time_str = "TBD"
                if time_match:
                    time_str = self.format_time(time_match.group(1))
                    event_text = event_text[:time_match.start()].strip()
                
                # Extract headliner and venue
                headliner = self.extract_headliner(event_text)
                venue, venue_url = self.extract_venue_name(event_text)
                
                # Generate emoji and description
                emoji = self.determine_emoji(headliner, event_text)
                description = self.generate_description(headliner, venue)
                
                events.append({
                    'day': day,
                    'date': date_str,
                    'time': time_str,
                    'emoji': emoji,
                    'event_name': headliner,
                    'description': description,
                    'venue': venue,
                    'venue_url': venue_url,
                    'raw_text': event_text
                })
        
        return events
    
    def format_events(self, raw_data: str, days_filter=None) -> str:
        """Main method to format event data into tables for all days of the week"""
        if days_filter is None:
            days_filter = ['MONDAY', 'TUESDAY', 'WEDNESDAY', 'THURSDAY', 'FRIDAY', 'SATURDAY', 'SUNDAY']
        
        events = self.parse_event_data(raw_data, days_filter)
        
        output = ""
        for day in ['MONDAY', 'TUESDAY', 'WEDNESDAY', 'THURSDAY', 'FRIDAY', 'SATURDAY', 'SUNDAY']:
            if day in days_filter:
                table = self.generate_table_html(events, day)
                if table:
                    output += table + "\n\n"
        
        return output.strip()
    
    def format_events_markdown(self, raw_data: str, days_filter=None) -> str:
        """Format event data into markdown tables for all days of the week"""
        if days_filter is None:
            days_filter = ['MONDAY', 'TUESDAY', 'WEDNESDAY', 'THURSDAY', 'FRIDAY', 'SATURDAY', 'SUNDAY']
        
        events = self.parse_event_data(raw_data, days_filter)
        
        output = ""
        for day in ['MONDAY', 'TUESDAY', 'WEDNESDAY', 'THURSDAY', 'FRIDAY', 'SATURDAY', 'SUNDAY']:
            if day in days_filter:
                day_events = [e for e in events if e['day'] == day]
                if day_events:
                    output += f"## {day}'S EVENTS\n\n"
                    for event in sorted(day_events, key=lambda x: x['time']):
                        venue_link = f"[{event['venue']}]({event['venue_url']})" if event['venue_url'] else event['venue']
                        output += f"**{event['time']} {event['emoji']} {event['event_name']}**\n\n"
                        # Remove trailing "at" from description since we're adding venue link
                        description = event['description'].rstrip(' at')
                        output += f"{description} at {venue_link}\n\n"
                    output += "\n"
        
        return output.strip()

if __name__ == "__main__":
    main()