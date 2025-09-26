#!/usr/bin/env python3
"""
CurationsLA Event Sourcing Parser
Formats Los Angeles events from The Scenestar's show list into well-formatted tables
for the specified date range (Friday - Sunday, September 26-28, 2025)
"""

import re
import datetime
from typing import List, Dict, Tuple, Optional
from bs4 import BeautifulSoup
from pathlib import Path

class EventParser:
    """Parser for Los Angeles events data with CurationsLA formatting"""
    
    def __init__(self):
        self.emoji_mapping = {
            'music': '🎸',  # Default music emoji
            'vocal': '🎵',  # For vocal/singing events
            'piano': '🎹',  # For piano/keyboard events
            'jazz': '🎷',  # For jazz events
            'comedy': '🎤',  # ONLY for comedy/humor/improv - NOT for music vocals
            'theater': '🎭',  # For theater/drama
            'film': '🎬',   # For movies/film events
            'dance': '💃',  # For dance events
            'electronic': '🎧',  # For electronic/DJ events
        }
        
        # Venue URL mapping for common LA venues
        self.venue_urls = {
            'HOLLYWOOD BOWL': 'https://www.hollywoodbowl.com/',
            'GREEK THEATRE': 'https://www.lagreektheatre.com/',
            'MOROCCAN LOUNGE': 'https://www.moroccanlounge.com/',
            'THE COMEDY STORE': 'https://thecomedystore.com/',
            'INTUIT DOME': 'https://www.intuitdome.com/',
            'CRYPTO.COM ARENA': 'https://www.cryptoarena.com/',
            'KIA FORUM': 'https://www.kiaforum.com/',
            'HOLLYWOOD PALLADIUM': 'https://www.palladiumhollywood.com/',
            'THE FORD': 'https://www.theford.com/',
            'WALT DISNEY CONCERT HALL': 'https://www.laphil.com/',
            'ECHOPLEX': 'https://www.spacelandpresents.com/echoplex/',
            'FONDA THEATRE': 'https://www.fondatheatre.com/',
            'BELLWETHER': 'https://www.bellwetherla.com/',
            'REGENT THEATER': 'https://www.regenttheater.com/',
            'TERAGRAM BALLROOM': 'https://www.spacelandpresents.com/teragram-ballroom/',
            'BELASCO': 'https://belascotheater.com/',
            'EL REY THEATRE': 'https://www.elreylosangeles.com/',
            'TROUBADOUR': 'https://www.troubadour.com/',
            'THE ROXY': 'https://theroxy.com/',
            'EL CID': 'https://elcidla.com/',
            'LODGE ROOM': 'https://www.lodgeroomhlp.com/',
            'GOLD-DIGGERS': 'https://www.golddiggersbar.com/',
            'THE ECHO': 'https://www.spacelandpresents.com/the-echo/',
            'YOUTUBE THEATER': 'https://www.youtube.com/intl/ALL_us/creators/theater/',
            'THE NOVO': 'https://www.thenovodtla.com/',
            'AMOEBA MUSIC - HOLLYWOOD': 'https://www.amoeba.com/',
            'BLUE NOTE LOS ANGELES': 'https://bluenotejazz.com/losangeles/',
            'CATALINA BAR & GRILL': 'https://catalinajazzclub.com/',
            'EXCHANGE L.A.': 'https://exchangela.com/',
            'ACADEMY L.A.': 'https://academyla.com/',
            'AVALON HOLLYWOOD': 'https://avalonhollywood.com/',
            'LOST PROPERTY - LP VINYL BAR': 'https://www.lostpropertybar.com/',
            'THE GRAND STAR JAZZ CLUB': 'https://grandstarjazzclub.com/',
            'BOARDNER\'S BY LA BELLE': 'https://boardnersbylabell.com/',
            'THE WARWICK': 'https://thewarwick.com/',
            'WILTERN': 'https://www.wiltern.com/',
            'MCCABE\'S GUITAR SHOP': 'https://www.mccabes.com/',
            'THE SMELL': 'https://www.thesmell.org/',
            'WHISKY A GO GO': 'https://whiskyagogo.com/',
            'HARVELLE\'S SANTA MONICA': 'https://santamonica.harvelles.com/',
            'THE GLASS HOUSE': 'https://www.theglasshousemusic.com/',
            'DOHENY STATE BEACH': 'https://www.parks.ca.gov/',
            'CHAIN REACTION': 'https://chainreaction.com/',
            'TIME NIGHTCLUB': 'https://timenightclub.com/',
            'SOKA PERFORMING ARTS CENTER': 'https://www.soka.edu/',
            'STAGE RED': 'https://stageredfontana.com/',
            'PAPPY & HARRIET\'S PIONEERTOWN PALACE': 'https://pappyandharriets.com/',
            'PECHANGA RESORT CASINO': 'https://www.pechanga.com/',
            'ANTELOPE VALLEY FAIR AND EVENT CENTER': 'https://avfair.com/',
            'VENTURA MUSIC HALL': 'https://venturamusichall.com/',
            'SANTA BARBARA BOWL': 'https://www.sbbowl.com/',
            'BMO STADIUM': 'https://www.bmostadium.com/',
            'SHRINE EXPO HALL': 'https://shrineauditorium.com/',
            'ORPHEUM THEATRE': 'https://laorpheum.com/',
            'DOLBY THEATRE': 'https://dolbytheatre.com/',
            'RAY CHARLES ROOFTOP TERRACE AT THE GRAMMY MUSEUM': 'https://grammymuseum.org/',
            'LACMA - SMIDT WELCOME PLAZA': 'https://www.lacma.org/',
            'FAIRBANKS LAWN AT HOLLYWOOD FOREVER CEMETERY': 'https://hollywoodforever.com/',
        }
    
    def determine_emoji(self, event_name: str, description: str = "") -> str:
        """Determine appropriate emoji based on event content"""
        event_lower = event_name.lower()
        desc_lower = description.lower()
        combined = f"{event_lower} {desc_lower}"
        
        # Comedy/humor/improv gets the standalone microphone emoji 🎤
        comedy_keywords = ['comedy', 'comedian', 'comic', 'humor', 'improv', 'stand-up', 'jokes', 'funny', 'freestyle comedy']
        if any(keyword in combined for keyword in comedy_keywords):
            return '🎤'
        
        # Piano/keyboard events get 🎹
        piano_keywords = ['piano', 'pianist', 'keyboard', 'john legend']
        if any(word in combined for word in piano_keywords):
            return '🎹'
        
        # Jazz events get 🎷
        jazz_keywords = ['jazz', 'saxophone', 'trumpet', 'bebop', 'laufey', 'kamasi washington', 'soul rebels']
        if any(word in combined for word in jazz_keywords):
            return '🎷'
        
        # Electronic/DJ events get 🎧
        electronic_keywords = ['dj', 'electronic', 'techno', 'house', 'edm', 'rave', 'lcd soundsystem', 
                              'afrojack', 'steve aoki', 'r3hab', 'jacques greene']
        if any(word in combined for word in electronic_keywords):
            return '🎧'
        
        # Film/movie events get 🎬
        film_keywords = ['film', 'movie', 'cinema', 'screening', 'david duchovny']
        if any(word in combined for word in film_keywords):
            return '🎬'
        
        # Theater/drama events get 🎭
        theater_keywords = ['theater', 'theatre', 'play', 'drama', 'musical', 'renée elise goldsberry']
        if any(word in combined for word in theater_keywords):
            return '🎭'
        
        # Dance events get 💃
        dance_keywords = ['dance', 'dancing', 'ballet', 'choreograph']
        if any(word in combined for word in dance_keywords):
            return '💃'
        
        # Vocal/singing specific (not comedy) get 🎵
        vocal_keywords = ['singer', 'vocal', 'choir', 'opera', 'tate mcrae', 'kali uchis', 'jessie murph']
        if any(word in combined for word in vocal_keywords) and not any(keyword in combined for keyword in comedy_keywords):
            return '🎵'
        
        # Specific artist emoji assignments for authenticity
        if 'big thief' in combined or 'alex g' in combined:
            return '🎸'  # Indie rock
        elif 'ice cube' in combined:
            return '🎤'  # Hip-hop gets microphone but not comedy microphone
        elif 'spiritualized' in combined or 'mudvayne' in combined:
            return '🎸'  # Rock/metal
        elif 'orchestra' in combined or 'symphony' in combined or 'philharmonic' in combined:
            return '🎼'  # Classical music
        
        # Default to guitar/music for everything else
        return '🎸'
    
    def extract_venue_name(self, text: str) -> Tuple[str, str]:
        """Extract venue name and return both venue name and potential URL"""
        # Common patterns for venue extraction
        venue_patterns = [
            r'at the (.+?)(?:\s*\(|$)',
            r'at (.+?)(?:\s*\(|$)',
        ]
        
        for pattern in venue_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                venue = match.group(1).strip()
                
                # Remove any HTML tags first
                soup = BeautifulSoup(venue, 'html.parser')
                venue = soup.get_text()
                
                # Clean up the venue name
                venue = venue.upper()
                # Remove common endings and cleanup
                venue = re.sub(r'\s+\([^)]*\)$', '', venue)
                venue = venue.replace(' - ', ' ').strip()
                
                # Get URL if we have it
                url = self.venue_urls.get(venue)
                if not url:
                    # Try with "THE" prefix for common venues
                    venue_with_the = f"THE {venue}"
                    url = self.venue_urls.get(venue_with_the)
                    if url:
                        venue = venue_with_the
                    else:
                        url = f"#{venue.lower().replace(' ', '-').replace('.', '').replace('&', 'and')}"
                return venue, url
        
        return "VENUE TBD", "#venue-tbd"
    
    def format_time(self, time_str: str) -> str:
        """Format time to 12hr with uppercase AM/PM"""
        # Extract time from string like "(5:30pm)" or "5:30pm"
        time_match = re.search(r'(\d{1,2}):?(\d{2})?\s*(am|pm)', time_str, re.IGNORECASE)
        if time_match:
            hour = int(time_match.group(1))
            minute = time_match.group(2) or "00"
            ampm = time_match.group(3).upper()
            
            return f"{hour}:{minute}{ampm}"
        
        return "TBD"
    
    def extract_headliner(self, event_text: str) -> str:
        """Extract the main headliner/event name"""
        # Remove the link tags and get the text content
        soup = BeautifulSoup(event_text, 'html.parser')
        link = soup.find('a')
        if link:
            text = link.get_text().strip()
            # Split on common separators and take the first part as headliner
            parts = re.split(r'\s+w/|\s+with|\s+featuring|\s+ft\.|\s+&', text)
            return parts[0].strip().upper()
        
        return "EVENT TBD"
    
    def generate_description(self, event_name: str, venue: str) -> str:
        """Generate a concise, empathetic description for the event"""
        event_lower = event_name.lower()
        venue_lower = venue.lower()
        
        # Specific artist descriptions for better personalization
        artist_descriptions = {
            'john legend': 'Award-winning soul singer brings heartfelt vocals at',
            'kali uchis': 'R&B star delivers hypnotic artistry and fearless stage presence at',
            'the head and the heart': 'Folk-pop harmonies and roots warmth create a communal evening at',
            'the hold steady': 'Alt-rock anthems and punchy live energy kick off at',
            'ice cube': 'Hip-hop legend brings West Coast energy and classic hits at',
            'big thief': 'Indie folk masters create intimate soundscapes at',
            'laufey': 'Jazz-pop sensation brings sophisticated vocals and modern elegance at',
            'tate mcrae': 'Pop sensation delivers chart-topping hits and dynamic performance at',
            'alex g': 'Indie rock innovator brings experimental sounds and devoted fanbase at',
            'pulp': 'Britpop legends return with anthemic energy and nostalgic power at',
            'lcd soundsystem': 'Dance-punk icons deliver pulsing beats and dance floor euphoria at',
            'mudvayne': 'Metal titans bring crushing riffs and explosive energy at',
            'spiritualized': 'Psychedelic rock pioneers create transcendent sonic journeys at',
            'david duchovny': 'The X-Files star explores his musical side with indie rock charm at'
        }
        
        # Check for specific artists first
        for artist, desc in artist_descriptions.items():
            if artist in event_lower:
                return desc
        
        # Category-based descriptions
        if any(word in event_lower for word in ['comedy', 'comic', 'comedian', 'freestyle comedy']):
            return "LA's sharpest comics bring late-night laughs with crowd work and bold, original sets at"
        elif any(word in event_lower for word in ['dj', 'electronic', 'house', 'techno', 'edm']):
            return "brings pulsing beats and dance floor euphoria at"
        elif any(word in event_lower for word in ['jazz', 'blues']):
            return "brings sophisticated soundscapes and musical virtuosity at"
        elif any(word in event_lower for word in ['orchestra', 'symphony', 'philharmonic']):
            return "brings classical mastery and orchestral grandeur at"
        elif 'listening party' in event_lower:
            return "intimate album experience brings fans together at"
        else:
            # Default music descriptions with variety
            descriptions = [
                "delivers hypnotic artistry and fearless stage presence at",
                "brings heartfelt vocals and emotional depth at",
                "creates a communal evening with infectious energy at",
                "kicks off with punchy live energy and anthems at",
                "brings indie charm and devoted fanbase at",
                "delivers chart-topping hits and dynamic performance at"
            ]
            # Use hash of event name to consistently assign same description
            return descriptions[hash(event_name) % len(descriptions)]
    
    def parse_event_data(self, raw_data: str, date_filter: str) -> List[Dict]:
        """Parse raw event data and filter by date"""
        events = []
        lines = raw_data.strip().split('\n')
        
        current_date = None
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Check if line is a date header
            date_match = re.match(r'^(FRIDAY|SATURDAY|SUNDAY),?\s+(.+?)(\d{4})$', line.upper())
            if date_match:
                current_date = date_match.group(1)
                continue
            
            # Skip non-event lines
            if not line.startswith(('09.26.25', '09.27.25', '09.28.25')):
                continue
            
            # Parse event line
            event_match = re.match(r'^(\d{2}\.\d{2}\.\d{2})\s+(.+)$', line)
            if event_match:
                date_str = event_match.group(1)
                event_text = event_match.group(2)
                
                # Determine which day this event belongs to
                if date_str == '09.26.25':
                    day = 'FRIDAY'
                elif date_str == '09.27.25':
                    day = 'SATURDAY'
                elif date_str == '09.28.25':
                    day = 'SUNDAY'
                else:
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
    
    def generate_table_html(self, events: List[Dict], day: str) -> str:
        """Generate HTML table for a specific day"""
        day_events = [e for e in events if e['day'] == day]
        if not day_events:
            return ""
        
        # Sort events by time
        day_events.sort(key=lambda x: x['time'])
        
        table_html = f"""<table>
  <thead>
    <tr>
      <th><strong>{day}'S EVENTS</strong></th>
    </tr>
  </thead>
  <tbody>"""
        
        for event in day_events:
            row = f"""
    <tr>
      <td>
        {event['time']} {event['emoji']} <strong>{event['event_name']}</strong> {event['description']} <a href="{event['venue_url']}"><strong>{event['venue']}</strong></a>
      </td>
    </tr>"""
            table_html += row
        
        table_html += """
  </tbody>
</table>"""
        
        return table_html
    
    def format_events(self, raw_data: str, days_filter: List[str] = None) -> str:
        """Main method to format event data into tables"""
        if days_filter is None:
            days_filter = ['FRIDAY', 'SATURDAY', 'SUNDAY']
        
        events = self.parse_event_data(raw_data, days_filter)
        
        output = ""
        for day in ['FRIDAY', 'SATURDAY', 'SUNDAY']:
            if day in days_filter:
                table = self.generate_table_html(events, day)
                if table:
                    output += table + "\n\n"
        
        return output.strip()

def main():
    """Main execution function for testing"""
    # Sample event data for testing
    sample_data = """
FRIDAY, SEPTEMBER 26, 2025

09.26.25 <a href="https://ticketmaster.evyy.net/c/252995/264167/4272?u=https://www.ticketmaster.com/lcd-soundsystem-pulp-hollywood-california-09-26-2025/event/0B00627A91462744">Pulp w/ LCD Soundsystem & DJ Harvey </a>at the Hollywood Bowl (5:30pm)
09.26.25 <a href="https://www.axs.com/events/979111/laufey-tickets?skin=crypto">Laufey w/ Suki Waterhouse </a>at Crypto.com Arena (7:30pm)
09.26.25 <a href="https://ticketmaster.evyy.net/c/252995/264167/4272?u=https://www.ticketmaster.com/tate-mcrae-miss-possessive-tour-inglewood-california-09-26-2025/event/0900616C0D62312D">Tate McRae w/ Zara Larsson </a>at the Kia Forum (7:00pm)

SUNDAY, SEPTEMBER 28, 2025

09.28.25 <a href="https://www.hollywoodbowl.com/events/performances/3650/2025-09-28/john-legend">John Legend </a>at the Hollywood Bowl (7:30pm)
09.28.25 <a href="https://ticketmaster.evyy.net/c/252995/264167/4272?u=https://www.ticketmaster.com/kali-uchis-the-sincerely-tour-inglewood-california-09-28-2025/event/090062C6304E6449">Kali Uchis w/ Thee Sacred Souls </a>at the Intuit Dome (8:00pm)
09.28.25 <a href="https://ticketmaster.evyy.net/c/252995/264167/4272?u=https://www.ticketweb.com/event/freestyle-comedy-jam-comedy-store-tickets/13902474">Freestyle Comedy Jam</a> at The Comedy Store (8:00pm)
"""
    
    parser = EventParser()
    formatted_output = parser.format_events(sample_data)
    print(formatted_output)

if __name__ == "__main__":
    main()