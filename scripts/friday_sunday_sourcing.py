#!/usr/bin/env python3
"""
CurationsLA: Friday - Sunday Events Sourcing Script
Generates well-formatted list of Los Angeles events for September 26-28, 2025
from The Scenestar's on-screen show list data
"""

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent))

from event_sourcing_parser import EventParser

# Full event data from The Scenestar for September 26-28, 2025
SCENESTAR_EVENT_DATA = """
FRIDAY, SEPTEMBER 26, 2025

09.26.25 <a href="https://ticketmaster.evyy.net/c/252995/264167/4272?u=https://www.ticketmaster.com/lcd-soundsystem-pulp-hollywood-california-09-26-2025/event/0B00627A91462744">Pulp w/ LCD Soundsystem & DJ Harvey </a>at the Hollywood Bowl (5:30pm)
09.26.25 <a href="https://www.axs.com/events/979111/laufey-tickets?skin=crypto">Laufey w/ Suki Waterhouse </a>at Crypto.com Arena (7:30pm)
09.26.25 <a href="https://ticketmaster.evyy.net/c/252995/264167/4272?u=https://www.ticketmaster.com/tate-mcrae-miss-possessive-tour-inglewood-california-09-26-2025/event/0900616C0D62312D">Tate McRae w/ Zara Larsson </a>at the Kia Forum (7:00pm)
09.26.25 <a href="https://www.axs.com/events/972527/alex-g-tickets?skin=goldenvoice">Alex G w/ Nilüfer Yanya </a>at the Greek Theatre (8:00pm)
09.26.25 <a href="https://ticketmaster.evyy.net/c/252995/264167/4272?u=https://www.ticketweb.com/event/magdalena-bay-imaginal-mystery-tour-hollywood-forever-tickets/13701614">Magdalena Bay w/ Oxis </a>at Fairbanks Lawn at Hollywood Forever Cemetery (8:00pm)
09.26.25 <a href="https://ticketmaster.evyy.net/c/252995/264167/4272?u=https://concerts.livenation.com/chevelle-with-special-guests-asking-alexandria-hollywood-california-09-26-2025/event/09006273DCCA3B4D">Chevelle w/ Asking Alexandria & Dead Poet Society </a>at the Hollywood Palladium (7:00pm)
09.26.25 <a href="https://www.theford.com/events/performances/4087/2025-09-26/pino-palladino-blake-mills">Pino Palladino & Blake Mills (featuring Sam Gendel & Chris Dave) w/ Jeremiah Chiu </a>at the Ford (8:00pm)
09.26.25 <a href="https://ticketmaster.evyy.net/c/252995/264167/4272?u=https://www.ticketmaster.com/event/0900632F7A640CA3">Rainbow Kitten Surprise </a>at Echoplex (8:00pm)
09.26.25 <a href="https://www.axs.com/events/913839/bandalos-chinos-tickets?skin=goldenvoice">Bandalos Chinos w/ Darumas & Mia Zeta </a>at the Fonda Theatre (9:00pm)
09.26.25 <a href="https://ticketmaster.evyy.net/c/252995/264167/4272?u=https://www.ticketmaster.com/the-waterboys-los-angeles-california-09-26-2025/event/0900626ECEAB38DE?camefrom=CFC_THEBELLWETHER_scenestar&brand=thebellwether">The Waterboys w/ Anna Tivel </a>at the Bellwether (8:00pm)
09.26.25 <a href="https://ticketmaster.evyy.net/c/252995/264167/4272?u=https://www.ticketmaster.com/beherit-finland-sold-out-los-angeles-california-09-26-2025/event/09006238E8D64B98">Beherit </a>at the Regent Theater (8:00pm)
09.26.25 <a href="https://ticketmaster.evyy.net/c/252995/264167/4272?u=https://www.ticketmaster.com/the-hold-steady-los-angeles-california-09-26-2025/event/090062C2E2132D26">The Hold Steady w/ Near Beer </a>at the Teragram Ballroom (7:00pm)
09.26.25 <a href="https://ticketmaster.evyy.net/c/252995/264167/4272?u=https://www.ticketmaster.com/yeule-los-angeles-california-09-26-2025/event/090062CCD8CC3F12">Yeule w/ Fish Narc </a>at the Belasco (8:00pm)
09.26.25 <a href="https://www.axs.com/events/1022098/jacques-greene-nosaj-thing-tickets?skin=elrey">Jacques Greene w/ Nosaj Thing </a>at El Rey Theatre (8:00pm)
09.26.25 <a href="https://wl.seetickets.us/event/sg-goodman/646889?afflky=TheTroubadour">S.G. Goodman w/ Becca Mancari </a>at the Troubadour (7:00pm)
09.26.25 <a href="https://www.axs.com/events/909184/mae-and-the-spill-canvas-tickets?skin=roxy">Mae w/ The Spill Canvas & Fred Mascherino </a>at The Roxy (8:00pm)
09.26.25 <a href="https://ticketmaster.evyy.net/c/252995/264167/4272?u=https://www.ticketmaster.com/joon-presents-one-night-in-la-los-angeles-california-09-26-2025/event/09006315D7B694B4">Joon w/ FanFan </a>at the Moroccan Lounge (9:30pm)
09.26.25 <a href="https://dice.fm/event/nvb879-daisy-the-great-live-in-los-angeles-26th-sep-el-cid-los-angeles-tickets">Daisy The Great w/ The Ophelias & Theo Moss </a>at El Cid (6:00pm)
09.26.25 <a href="https://www.lodgeroomhlp.com/shows/tei-shi-2/">Tei Shi w/ Harmony </a>at the Lodge Room (8:00pm)
09.26.25 <a href="https://dice.fm/partner/dice/event/l82ppl-mr-gnome-26th-sep-gold-diggers-los-angeles-tickets?dice_id=5981752">Mr. Gnome </a>at Gold-Diggers (7:00pm)
09.26.25 <a href="https://ticketmaster.evyy.net/c/252995/264167/4272?u=https://www.ticketmaster.com/stolen-gin-with-my-friend-catie-los-angeles-california-09-26-2025/event/090062C6EF254A85">Stolen Gin w/ My Friend Catie </a>at The Echo (7:00pm)
09.26.25 <a href="https://ticketmaster.evyy.net/c/252995/264167/4272?u=https://www.ticketmaster.com/yuri-inglewood-california-09-26-2025/event/0A00627BC3735090">Yuri </a>at YouTube Theater (8:00pm)
09.26.25 <a href="https://www.axs.com/events/1014754/jeffrey-osborne-tickets?skin=novo">Jeffrey Osborne (of Bar Kays) w/ Larry Dodson </a>at The Novo (8:00pm)
09.26.25 <a href="https://www.amoeba.com/live-shows/upcoming/detail-3039/">Neko Case ('Neon Grey Midnight Green' Listening Party) </a>at Amoeba Music - Hollywood (FREE - 5:00pm)
09.26.25 <a href="https://ticketmaster.evyy.net/c/252995/264167/4272?u=https://www.universe.com/events/the-drop-margo-price-tickets-BMZJGT">The Drop: Margo Price w/ Shooter Jennings (Moderator) </a>at the Ray Charles Rooftop Terrace at the Grammy Museum at L.A. Live (7:30pm)
09.26.25 <a href="https://www.laphil.com/events/performances/4043/2025-09-26/dudamel-leads-an-alpine-symphony">Dudamel Leads Leads An 'Alpine Symphony' w/ Gustavo Dudamel & the Los Angeles Philharmonic </a>at Walt Disney Concert Hall (8:00pm)
09.26.25 <a href="https://www.lacma.org/event/jazz-lacma-alexis-lombre">Jazz at LACMA w/ Alexis Lombre </a>at LACMA - Smidt Welcome Plaza (FREE - 6:00pm)
09.26.25 <a href="https://ticketmaster.evyy.net/c/252995/264167/4272?u=https://www.ticketweb.com/event/the-soul-rebels-special-blue-note-los-angeles-tickets/13834354">The Soul Rebels & Special Guest </a>at Blue Note Los Angeles (7:00pm)
09.26.25 <a href="https://ticketmaster.evyy.net/c/252995/264167/4272?u=https://www.ticketweb.com/event/the-soul-rebels-special-blue-note-los-angeles-tickets/13834374">Kamasi Washington </a>at Blue Note Los Angeles (9:30pm)

SATURDAY, SEPTEMBER 27, 2025

09.27.25 <a href="https://www.axs.com/events/990259/laufey-tickets?skin=crypto">Laufey w/ Suki Waterhouse </a>at Crypto.com Arena (7:30pm)
09.27.25 <a href="https://www.hollywoodbowl.com/events/performances/3649/2025-09-27/big-thief">Big Thief w/ Noname </a>at the Hollywood Bowl (8:00pm)
09.27.25 <a href="https://ticketmaster.evyy.net/c/252995/264167/4272?u=https://www.ticketmaster.com/tate-mcrae-miss-possessive-tour-inglewood-california-09-27-2025/event/09006172BA20276A">Tate McRae w/ Zara Larsson </a>at the Kia Forum (7:00pm)
09.27.25 <a href="https://www.axs.com/events/978492/alex-g-2nd-show-added-tickets?skin=goldenvoice">Alex G w/ Nilüfer Yanya & Kevin Abstract </a>at the Greek Theatre (8:00pm)
09.27.25 <a href="https://apollo.id/venue/zvb2Agt3qs/tickets/56lm5GJgd8">S2O Los Angeles w/ Afrojack, Steve Aoki, R3HAB, Elephante, Yetep, Cyberpunk, NTR, & Obers </a>at BMO Stadium (3:00pm)
09.27.25 <a href="https://ticketmaster.evyy.net/c/252995/264167/4272?u=https://www.ticketweb.com/event/magdalena-bay-imaginal-mystery-tour-hollywood-forever-tickets/13702164">Magdalena Bay w/ Oxis </a>at Fairbanks Lawn at Hollywood Forever Cemetery (8:00pm)
09.27.25 <a href="https://www.axs.com/events/961932/jessie-murph-tickets?skin=goldenvoice">Jessie Murph w/ Nino Paid </a>at Shrine Expo Hall (8:00pm)
09.27.25 <a href="https://ticketmaster.evyy.net/c/252995/264167/4272?u=https://www.ticketmaster.com/event/0900629DA7DC2B0F">James (performing 'Laid' in full) </a>at the Bellwether (8:00pm)
09.27.25 <a href="https://www.axs.com/events/962043/kiesza-tickets?skin=elrey">Kiesza w/ Bonnie McKee & Melanie Pfirrman </a>at El Rey Theatre (8:00pm)
09.27.25 <a href="https://ticketmaster.evyy.net/c/252995/264167/4272?u=https://concerts.livenation.com/se-so-neon-now-north-american-los-angeles-california-09-27-2025/event/090062AFC13459B7">Se So Neon </a>at the Wiltern (8:00pm)
09.27.25 <a href="https://ticketmaster.evyy.net/c/252995/264167/4272?u=https://concerts.livenation.com/hunx-his-punx-los-angeles-california-09-27-2025/event/090062A5020735D6">Hunx & His Punx w/ Niis & Slippers </a>at the Belasco (8:00pm)
09.27.25 <a href="https://www.axs.com/events/965799/the-hellp-tickets?skin=goldenvoice">The Hellp </a>at The Novo (9:00pm)
09.27.25 <a href="https://www.theford.com/events/performances/4088/2025-09-27/renee-elise-goldsberry">Renée Elise Goldsberry </a>at the Ford (8:00pm)
09.27.25 <a href="https://ticketmaster.evyy.net/c/252995/264167/4272?u=https://www.ticketmaster.com/the-hold-steady-los-angeles-california-09-27-2025/event/090062C2E36C2D40">The Hold Steady </a>at the Teragram Ballroom (7:00pm)
09.27.25 <a href="https://wl.seetickets.us/event/the-lone-bellow/648992?afflky=TheTroubadour">The Lone Bellow w/ Valley James </a>at the Troubadour (7:00pm)
09.27.25 <a href="https://ticketmaster.evyy.net/c/252995/264167/4272?u=https://www.ticketmaster.com/sorry-ghost-lavalove-los-angeles-california-09-27-2025/event/090062F5E8F15DA8">Sorry Ghost w/ LavaLove </a>at the Moroccan Lounge (6:30pm)
09.27.25 <a href="https://ticketmaster.evyy.net/c/252995/264167/4272?u=https://www.ticketmaster.com/eladio-carrion-don-kbrn-world-tour-inglewood-california-09-27-2025/event/0A00628EC2BA4696">Eladio Carrión </a>at YouTube Theater (8:00pm)

SUNDAY, SEPTEMBER 28, 2025

09.28.25 <a href="https://www.hollywoodbowl.com/events/performances/3650/2025-09-28/john-legend">John Legend </a>at the Hollywood Bowl (7:30pm)
09.28.25 <a href="https://ticketmaster.evyy.net/c/252995/264167/4272?u=https://www.ticketmaster.com/kali-uchis-the-sincerely-tour-inglewood-california-09-28-2025/event/090062C6304E6449">Kali Uchis w/ Thee Sacred Souls </a>at the Intuit Dome (8:00pm)
09.28.25 <a href="https://ticketmaster.evyy.net/c/252995/264167/4272?u=https://www.ticketmaster.com/the-head-and-the-heart-aperture-los-angeles-california-09-28-2025/event/09006255B9714731">The Head And The Heart w/ John Vincent III & Tyler Ballgame </a>at the Greek Theatre (7:00pm)
09.28.25 <a href="https://ticketmaster.evyy.net/c/252995/264167/4272?u=https://www.ticketmaster.com/ice-cube-truth-to-power-four-los-angeles-california-09-28-2025/event/2C00628AD33D08B9">Ice Cube </a>at Crypto.com Arena (8:00pm)
09.28.25 <a href="https://ticketmaster.evyy.net/c/252995/264167/4272?u=https://www.ticketmaster.com/spiritualized-pure-phase-performed-live-in-los-angeles-california-09-28-2025/event/09006290E92541D8">Spiritualized (performing 'Pure Phase' in it's entirety) </a>at the Orpheum Theatre (8:00pm)
09.28.25 <a href="https://ticketmaster.evyy.net/c/252995/264167/4272?u=https://concerts.livenation.com/mudvayne-ld-50-25th-anniversary-tour-hollywood-california-09-28-2025/event/09006297CC3C460A">Mudvayne w/ Static-X & Vended </a>at the Hollywood Palladium (7:00pm)
09.28.25 <a href="https://ticketmaster.evyy.net/c/252995/264167/4272?u=https://www.ticketmaster.com/the-hold-steady-los-angeles-california-09-28-2025/event/090062C2E6A02DCE">The Hold Steady </a>at the Moroccan Lounge (6:00pm)
09.28.25 <a href="https://ticketmaster.evyy.net/c/252995/264167/4272?u=https://www.ticketmaster.com/marvelous-3-los-angeles-california-09-28-2025/event/090062A6CD319F2B">The Marvelous 3 </a>at the Teragram Ballroom (7:00pm)
09.28.25 <a href="https://wl.eventim.us/event/lucinda-williams/656240?afflky=TheTroubadour">Lucinda Williams </a>at the Troubadour (7:00pm)
09.28.25 <a href="https://www.axs.com/events/942192/vola-tickets?skin=roxy">Vola w/ Daedric & Cosmic Ocean </a>at The Roxy (7:30pm)
09.28.25 <a href="https://ticketmaster.evyy.net/c/252995/264167/4272?u=https://www.ticketmaster.com/david-duchovny-los-angeles-california-09-28-2025/event/090062BDD37E5EB6">David Duchovny </a>at the Regent Theater (8:00pm)
09.28.25 <a href="https://ticketmaster.evyy.net/c/252995/264167/4272?u=https://www.ticketmaster.com/atif-aslam-hollywood-california-09-28-2025/event/090062E8DD1E31DA">Atif Aslam </a>at the Dolby Theatre (7:00pm)
"""

def main():
    """Generate formatted event tables for Friday-Sunday September 26-28, 2025"""
    print("🌴 CurationsLA: Friday - Sunday Events Sourcing")
    print("=" * 60)
    print("Generating well-formatted LA events for September 26-28, 2025")
    print("Source: The Scenestar's on-screen show list")
    print()
    
    # Initialize parser
    parser = EventParser()
    
    # Generate formatted tables
    formatted_output = parser.format_events(SCENESTAR_EVENT_DATA)
    
    # Output the results
    print(formatted_output)
    
    # Save to file
    output_dir = Path(__file__).parent.parent / "output" / "2025-09-26"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    output_file = output_dir / "friday-sunday-events.html"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(f"""<!DOCTYPE html>
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
    
{formatted_output}

    <footer style="text-align: center; margin-top: 40px; padding-top: 20px; border-top: 1px solid #eee;">
        <p><strong>Made with 💜 in Los Angeles</strong></p>
        <p><em>CurationsLA - Bringing Good Vibes when our city needs it most</em></p>
    </footer>
</body>
</html>""")
    
    print(f"\n✅ Event data saved to: {output_file}")
    print(f"📊 Generated formatted tables for Friday-Sunday events")
    print(f"🎉 Ready for CurationsLA newsletter integration!")

if __name__ == "__main__":
    main()