#!/usr/bin/env python3
"""
Test Event Sourcing Parser
Validates that the event sourcing functionality meets all requirements
"""

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent))

from event_sourcing_parser import EventParser
import re

def test_basic_functionality():
    """Test basic parsing functionality"""
    print("🧪 Testing basic event parsing functionality...")
    
    sample_data = """
FRIDAY, SEPTEMBER 26, 2025

09.26.25 <a href="https://www.hollywoodbowl.com/events/performances/3650/2025-09-28/john-legend">John Legend </a>at the Hollywood Bowl (7:30pm)
09.26.25 <a href="https://thecomedystore.com/">Freestyle Comedy Jam</a> at The Comedy Store (8:00pm)
09.26.25 <a href="https://www.intuitdome.com/">Kali Uchis w/ Thee Sacred Souls </a>at the Intuit Dome (8:00pm)

SUNDAY, SEPTEMBER 28, 2025

09.28.25 <a href="https://www.lagreektheatre.com/">The Head And The Heart w/ John Vincent III</a> at the Greek Theatre (7:00pm)
"""
    
    parser = EventParser()
    events = parser.parse_event_data(sample_data, ['FRIDAY', 'SUNDAY'])
    
    assert len(events) == 4, f"Expected 4 events, got {len(events)}"
    
    # Check Friday events
    friday_events = [e for e in events if e['day'] == 'FRIDAY']
    assert len(friday_events) == 3, f"Expected 3 Friday events, got {len(friday_events)}"
    
    # Check Sunday events  
    sunday_events = [e for e in events if e['day'] == 'SUNDAY']
    assert len(sunday_events) == 1, f"Expected 1 Sunday event, got {len(sunday_events)}"
    
    print("✅ Basic parsing functionality works!")

def test_time_formatting():
    """Test that time formatting follows 12hr uppercase AM/PM format"""
    print("🧪 Testing time formatting...")
    
    parser = EventParser()
    
    # Test cases for time formatting
    test_cases = [
        ("(7:30pm)", "7:30PM"),
        ("(5:00pm)", "5:00PM"),
        ("(8:00pm)", "8:00PM"),
        ("(12:00pm)", "12:00PM"),
        ("(12:00am)", "12:00AM"),
    ]
    
    for input_time, expected in test_cases:
        result = parser.format_time(input_time)
        assert result == expected, f"Time formatting failed: {input_time} -> {result}, expected {expected}"
    
    print("✅ Time formatting is correct!")

def test_emoji_assignment():
    """Test that emojis are assigned correctly according to rules"""
    print("🧪 Testing emoji assignment rules...")
    
    parser = EventParser()
    
    # Test comedy gets 🎤 (standalone microphone)
    emoji = parser.determine_emoji("Freestyle Comedy Jam", "comedy show")
    assert emoji == '🎤', f"Comedy should get 🎤, got {emoji}"
    
    # Test piano gets 🎹
    emoji = parser.determine_emoji("John Legend", "piano performance")
    assert emoji == '🎹', f"Piano should get 🎹, got {emoji}"
    
    # Test jazz gets 🎷
    emoji = parser.determine_emoji("Jazz at LACMA", "jazz performance")
    assert emoji == '🎷', f"Jazz should get 🎷, got {emoji}"
    
    # Test electronic/DJ gets 🎧
    emoji = parser.determine_emoji("LCD Soundsystem", "electronic music")
    assert emoji == '🎧', f"Electronic should get 🎧, got {emoji}"
    
    # Test default music gets 🎸
    emoji = parser.determine_emoji("The Hold Steady", "rock band")
    assert emoji == '🎸', f"Rock should get 🎸, got {emoji}"
    
    print("✅ Emoji assignment rules are correct!")

def test_venue_hyperlinks():
    """Test that venues are properly hyperlinked and uppercased"""
    print("🧪 Testing venue hyperlinks...")
    
    parser = EventParser()
    
    # Test known venue
    venue, url = parser.extract_venue_name("John Legend at the Hollywood Bowl")
    assert venue == "HOLLYWOOD BOWL", f"Expected 'HOLLYWOOD BOWL', got '{venue}'"
    assert url == "https://www.hollywoodbowl.com/", f"Expected Hollywood Bowl URL, got '{url}'"
    
    # Test another known venue
    venue, url = parser.extract_venue_name("Comedy show at The Comedy Store")
    assert venue == "THE COMEDY STORE", f"Expected 'THE COMEDY STORE', got '{venue}'"
    assert url == "https://thecomedystore.com/", f"Expected Comedy Store URL, got '{url}'"
    
    print("✅ Venue hyperlinks are correct!")

def test_table_format():
    """Test that HTML table format matches requirements"""
    print("🧪 Testing HTML table format...")
    
    sample_data = """
SUNDAY, SEPTEMBER 28, 2025

09.28.25 <a href="https://www.hollywoodbowl.com/events/performances/3650/2025-09-28/john-legend">John Legend </a>at the Hollywood Bowl (7:30pm)
09.28.25 <a href="https://thecomedystore.com/">Freestyle Comedy Jam</a> at The Comedy Store (8:00pm)
"""
    
    parser = EventParser()
    events = parser.parse_event_data(sample_data, ['SUNDAY'])
    table_html = parser.generate_table_html(events, 'SUNDAY')
    
    # Check table structure
    assert '<table>' in table_html, "Table should have opening tag"
    assert '</table>' in table_html, "Table should have closing tag"
    assert '<thead>' in table_html, "Table should have thead"
    assert '<tbody>' in table_html, "Table should have tbody"
    assert '<strong>SUNDAY\'S EVENTS</strong>' in table_html, "Table should have proper header"
    
    # Check that events are properly formatted
    assert '7:30PM 🎹 <strong>JOHN LEGEND</strong>' in table_html, "John Legend should be formatted correctly"
    assert '8:00PM 🎤 <strong>FREESTYLE COMEDY JAM</strong>' in table_html, "Comedy should be formatted correctly"
    
    # Check hyperlinks
    assert '<a href="https://www.hollywoodbowl.com/"><strong>HOLLYWOOD BOWL</strong></a>' in table_html, "Venue links should be correct"
    
    print("✅ HTML table format is correct!")

def test_event_descriptions():
    """Test that event descriptions are appropriate and empathetic"""
    print("🧪 Testing event descriptions...")
    
    parser = EventParser()
    
    # Test specific artist descriptions
    desc = parser.generate_description("John Legend", "Hollywood Bowl")
    assert "Award-winning soul singer" in desc, f"John Legend should have specific description, got: {desc}"
    
    desc = parser.generate_description("Kali Uchis", "Intuit Dome")
    assert "R&B star delivers hypnotic artistry" in desc, f"Kali Uchis should have specific description, got: {desc}"
    
    desc = parser.generate_description("Freestyle Comedy Jam", "Comedy Store")
    assert "sharpest comics bring late-night laughs" in desc, f"Comedy should have specific description, got: {desc}"
    
    print("✅ Event descriptions are appropriate!")

def test_formatting_requirements():
    """Test that all formatting requirements from the issue are met"""
    print("🧪 Testing all formatting requirements...")
    
    sample_data = """
SUNDAY, SEPTEMBER 28, 2025

09.28.25 <a href="https://www.hollywoodbowl.com/events/performances/3650/2025-09-28/john-legend">John Legend </a>at the Hollywood Bowl (7:30pm)
09.28.25 <a href="https://thecomedystore.com/">Freestyle Comedy Jam</a> at The Comedy Store (8:00pm)
09.28.25 <a href="https://www.intuitdome.com/">Kali Uchis w/ Thee Sacred Souls </a>at the Intuit Dome (8:00pm)
09.28.25 <a href="https://www.lagreektheatre.com/">The Head And The Heart w/ John Vincent III</a> at the Greek Theatre (7:00pm)
"""
    
    parser = EventParser()
    events = parser.parse_event_data(sample_data, ['SUNDAY'])
    table_html = parser.generate_table_html(events, 'SUNDAY')
    
    # Check formatting rules:
    # [TIME]: 12hr, uppercase AM/PM
    assert "7:30PM" in table_html, "Time should be 12hr with uppercase AM/PM"
    assert "8:00PM" in table_html, "Time should be 12hr with uppercase AM/PM"
    
    # [EMOJI]: Single relevant emoji
    emoji_count = len(re.findall(r'[🎸🎵🎤🎹🎬🎭🎷🎧💃🎼]', table_html))
    event_count = len(events)
    assert emoji_count == event_count, f"Should have {event_count} emojis, found {emoji_count}"
    
    # [EVENT NAME]: ALL CAPS, bold
    assert '<strong>JOHN LEGEND</strong>' in table_html, "Event name should be ALL CAPS and bold"
    assert '<strong>FREESTYLE COMEDY JAM</strong>' in table_html, "Event name should be ALL CAPS and bold"
    assert '<strong>KALI UCHIS</strong>' in table_html, "Event name should be ALL CAPS and bold"
    
    # [VENUE NAME]: ALL CAPS, hyperlinked, bold
    assert '<a href="https://www.hollywoodbowl.com/"><strong>HOLLYWOOD BOWL</strong></a>' in table_html, "Venue should be ALL CAPS, hyperlinked, and bold"
    assert '<a href="https://thecomedystore.com/"><strong>THE COMEDY STORE</strong></a>' in table_html, "Venue should be ALL CAPS, hyperlinked, and bold"
    
    # Only one venue hyperlink per line
    lines = table_html.split('\n')
    for line in lines:
        if '<td>' in line:
            href_count = line.count('<a href=')
            assert href_count <= 1, f"Should have max 1 hyperlink per line, found {href_count} in: {line}"
    
    print("✅ All formatting requirements are met!")

def main():
    """Run all tests"""
    print("🧪 CurationsLA Event Sourcing Test Suite")
    print("Testing Friday-Sunday Events Parser Functionality")
    print("=" * 60)
    
    try:
        test_basic_functionality()
        test_time_formatting()
        test_emoji_assignment()
        test_venue_hyperlinks()
        test_table_format()
        test_event_descriptions()
        test_formatting_requirements()
        
        print("\n🎉 All tests passed! Event sourcing parser is working correctly.")
        print("✅ Ready for CurationsLA production use!")
        
    except AssertionError as e:
        print(f"\n❌ Test failed: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n💥 Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()