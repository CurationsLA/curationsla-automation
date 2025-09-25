#!/usr/bin/env python3
"""
CurationsLA Content Generator
Generates daily newsletter content from RSS feeds with Good Vibes filtering
"""

import os
import json
import feedparser
import requests
from datetime import datetime, timedelta
from pathlib import Path
import re
from typing import Dict, List, Any
import time
import random

# Configuration
BASE_DIR = Path(__file__).parent.parent
SOURCES_DIR = BASE_DIR / "sources" / "feeds"
OUTPUT_DIR = BASE_DIR / "output"
CONTENT_DIR = BASE_DIR / "content"

# LA Neighborhoods mapping
NEIGHBORHOODS = {
    'DTLA': ['Downtown', 'Arts District', 'Little Tokyo', 'Chinatown'],
    'WESTSIDE': ['Santa Monica', 'Venice', 'Brentwood', 'West LA'],
    'VALLEY': ['Studio City', 'Sherman Oaks', 'Burbank', 'North Hollywood'],
    'EASTSIDE': ['Silver Lake', 'Echo Park', 'Los Feliz', 'Highland Park'],
    'SOUTHBAY': ['Manhattan Beach', 'Hermosa Beach', 'Redondo Beach'],
    'HOLLYWOOD': ['Hollywood', 'West Hollywood', 'Hollywood Hills'],
    'MIDCITY': ['Beverly Hills', 'Fairfax', 'Miracle Mile']
}

# Good Vibes Filter
GOOD_VIBES_KEYWORDS = [
    'opening', 'new', 'celebrate', 'community', 'festival', 'art', 'music',
    'food', 'restaurant', 'launch', 'debut', 'premiere', 'exhibition',
    'performance', 'achievement', 'winner', 'success', 'expansion',
    'collaboration', 'partnership', 'innovation', 'discovery', 'milestone'
]

BLOCKED_KEYWORDS = [
    'crime', 'murder', 'shooting', 'arrest', 'police', 'lawsuit', 'controversy',
    'scandal', 'protest', 'angry', 'outrage', 'closure', 'bankruptcy',
    'layoffs', 'fired', 'political', 'politics', 'election'
]

class ContentGenerator:
    def __init__(self):
        self.today = datetime.now()
        self.day_name = self.today.strftime('%A').lower()
        self.date_str = self.today.strftime('%Y-%m-%d')
        self.content = {}
        
        # Create output directory
        self.output_path = OUTPUT_DIR / self.date_str
        self.output_path.mkdir(parents=True, exist_ok=True)
        
    def load_feed_config(self, category: str) -> Dict:
        """Load RSS feed configuration for a category"""
        config_file = SOURCES_DIR / f"{category}.json"
        if not config_file.exists():
            print(f"⚠️  Config file not found: {config_file}")
            return {}
            
        with open(config_file, 'r') as f:
            return json.load(f)
    
    def fetch_rss_feed(self, url: str, name: str) -> List[Dict]:
        """Fetch and parse RSS feed"""
        try:
            print(f"📡 Fetching {name}...")
            
            # Add user agent to avoid blocking
            headers = {
                'User-Agent': 'CurationsLA/1.0 (Newsletter Aggregator; +https://la.curations.cc)'
            }
            
            # Some feeds require direct requests
            response = requests.get(url, headers=headers, timeout=30)
            response.raise_for_status()
            
            feed = feedparser.parse(response.content)
            
            if feed.bozo:
                print(f"⚠️  Feed parsing warning for {name}: {feed.bozo_exception}")
            
            items = []
            for entry in feed.entries[:10]:  # Limit to 10 most recent
                item = {
                    'title': getattr(entry, 'title', ''),
                    'link': getattr(entry, 'link', ''),
                    'description': getattr(entry, 'description', ''),
                    'published': getattr(entry, 'published', ''),
                    'summary': getattr(entry, 'summary', ''),
                    'source': name,
                    'feed_url': url
                }
                items.append(item)
            
            print(f"✅ Retrieved {len(items)} items from {name}")
            time.sleep(1)  # Be respectful to servers
            return items
            
        except Exception as e:
            print(f"❌ Error fetching {name}: {str(e)}")
            return []
    
    def calculate_vibe_score(self, text: str) -> float:
        """Calculate Good Vibes score for content"""
        text_lower = text.lower()
        
        good_score = sum(1 for keyword in GOOD_VIBES_KEYWORDS if keyword in text_lower)
        bad_score = sum(2 for keyword in BLOCKED_KEYWORDS if keyword in text_lower)
        
        # Calculate score between 0 and 1
        total_score = good_score - bad_score
        normalized_score = max(0, min(1, (total_score + 5) / 10))
        
        return normalized_score
    
    def extract_neighborhood(self, text: str) -> str:
        """Extract LA neighborhood from text"""
        text_lower = text.lower()
        
        for area, neighborhoods in NEIGHBORHOODS.items():
            for neighborhood in neighborhoods:
                if neighborhood.lower() in text_lower:
                    return neighborhood
        
        return "Los Angeles"  # Default fallback
    
    def filter_good_vibes(self, items: List[Dict], threshold: float = 0.3) -> List[Dict]:
        """Filter items for Good Vibes content"""
        filtered_items = []
        
        for item in items:
            # Combine title and description for scoring
            content_text = f"{item['title']} {item['description']}"
            vibe_score = self.calculate_vibe_score(content_text)
            
            if vibe_score >= threshold:
                item['vibe_score'] = vibe_score
                item['neighborhood'] = self.extract_neighborhood(content_text)
                filtered_items.append(item)
        
        # Sort by vibe score (highest first)
        filtered_items.sort(key=lambda x: x['vibe_score'], reverse=True)
        return filtered_items
    
    def aggregate_category_content(self, category: str) -> List[Dict]:
        """Aggregate content for a specific category"""
        print(f"\n🌴 Processing {category.upper()} category...")
        
        config = self.load_feed_config(category)
        if not config:
            return []
        
        all_items = []
        
        for feed in config.get('feeds', []):
            if feed.get('active', True):  # Default to active if not specified
                items = self.fetch_rss_feed(feed['url'], feed['name'])
                all_items.extend(items)
        
        # Filter for Good Vibes
        good_items = self.filter_good_vibes(all_items)
        
        print(f"📊 {category}: {len(all_items)} total → {len(good_items)} good vibes")
        
        return good_items[:8]  # Limit to top 8 per category
    
    def format_newsletter_section(self, category: str, items: List[Dict]) -> str:
        """Format items into newsletter section"""
        if not items:
            return f"#### {category.upper()}\n\n*No {category} updates today. Check back tomorrow!*\n\n"
        
        # Category icons
        icons = {
            'eats': '🍟', 'events': '📆', 'community': '🌴',
            'development': '🏡', 'business': '💼', 'entertainment': '🎬',
            'sports': '🏈', 'goodies': '🤙'
        }
        
        icon = icons.get(category, '✨')
        section = f"#### {icon} **{category.upper()}**\n\n"
        
        for item in items:
            # Clean title and create shortened version
            title = item['title'].replace('[', '').replace(']', '').strip()
            if len(title) > 80:
                title = title[:77] + "..."
            
            # Extract brief description
            desc = item['description'][:150] + "..." if len(item['description']) > 150 else item['description']
            desc = re.sub(r'<[^>]+>', '', desc)  # Remove HTML tags
            
            neighborhood = item.get('neighborhood', 'Los Angeles')
            
            section += f"**{neighborhood}** {icon} {title}\n\n"
            section += f"• {desc}\n"
            section += f"  - [READ MORE]({item['link']})\n\n"
        
        return section
    
    def generate_hov_lanes(self) -> str:
        """Generate HOV Lanes quick headlines section"""
        hov_content = "#### 🛣 **HOV LANES**\n\n"
        
        # Sample headlines (in production, these would come from news APIs)
        national_headlines = [
            "Tech Giants Announce Green Energy Partnership",
            "New Archaeological Discovery Changes History",
            "Space Mission Returns with Promising Samples",
            "Medical Breakthrough Shows Promise for Treatment",
            "Climate Initiative Gains Global Support",
            "Arts Education Funding Reaches Record High"
        ]
        
        local_headlines = [
            "LA Metro Expands Weekend Service",
            "Hollywood Bowl Announces Summer Series",
            "Santa Monica Pier Gets New Attraction",
            "DTLA Food Hall Opens This Weekend",
            "Griffith Observatory Unveils New Exhibit"
        ]
        
        fun_headlines = [
            "Viral Cat Video Brings Joy to Millions",
            "Community Garden Produces Giant Vegetables",
            "Local Artist Creates Interactive Mural",
            "Food Truck Festival Announces Lineup",
            "Beach Cleanup Breaks Participation Record"
        ]
        
        hov_content += "| **NATIONAL** |\n|:---:|\n"
        for headline in random.sample(national_headlines, 6):
            words = headline.split()
            if len(words) >= 3:
                link_text = " ".join(words[-2:])
                display_text = " ".join(words[:-2]) + f" [{link_text}](#)"
            else:
                display_text = f"[{headline}](#)"
            hov_content += f"| {display_text} |\n"
        
        hov_content += "\n| **LOCAL** | **FUN** |\n|:---:|:---:|\n"
        for local, fun in zip(random.sample(local_headlines, 5), random.sample(fun_headlines, 5)):
            local_words = local.split()
            fun_words = fun.split()
            
            if len(local_words) >= 3:
                local_link = " ".join(local_words[-2:])
                local_display = " ".join(local_words[:-2]) + f" [{local_link}](#)"
            else:
                local_display = f"[{local}](#)"
                
            if len(fun_words) >= 3:
                fun_link = " ".join(fun_words[-2:])
                fun_display = " ".join(fun_words[:-2]) + f" [{fun_link}](#)"
            else:
                fun_display = f"[{fun}](#)"
            
            hov_content += f"| {local_display} | {fun_display} |\n"
        
        return hov_content + "\n---\n\n"
    
    def generate_newsletter(self):
        """Generate complete newsletter content"""
        print(f"\n🌴 Generating CurationsLA newsletter for {self.day_name.title()}, {self.date_str}")
        
        # Aggregate content from all categories
        categories = ['eats', 'events', 'community', 'development', 'business', 'entertainment', 'sports', 'goodies']
        
        for category in categories:
            self.content[category] = self.aggregate_category_content(category)
        
        # Generate newsletter header
        day_name = self.day_name.title()
        newsletter_content = f"""**HEY LOS ANGELES!**

[GIF PLACEHOLDER - Insert animated GIF here]

**IT'S {day_name.upper()}**

👋 **HEY CUTIE!**

• Welcome to your daily dose of LA's good vibes! We've scoured the city to bring you the best openings, events, and community celebrations happening right now.

• From new restaurant launches in Silver Lake to art exhibitions in DTLA, we've got your weekend (and beyond) covered with positive energy only.

• Ready to explore? Let's dive into what makes LA amazing today! 🌴

---

🍟 [**EATS**](#eats) | 📆 [**EVENTS**](#events) | 🌴 [**COMMUNITY**](#community)

🏡 [**DEVELOPMENT**](#development) | 💼 [**BUSINESS**](#business) | 🎬 [**ENTERTAINMENT**](#entertainment)

🏈 [**SPORTS**](#sports) | 🤙 [**GOODIES**](#goodies)

---

{self.generate_hov_lanes()}"""

        # Add sponsor section template
        newsletter_content += """#### 💰 **SPONSOR TEMPLATE**

**[Partner with CurationsLA]** - Reach LA's most engaged community

Ready to share your Good Vibes with 15,000+ LA culture enthusiasts? Our newsletter connects local businesses with residents who love discovering the best of our city.

**Why Advertise with Us**: Authentic engagement, positive-only content, and a community that takes action on recommendations.

*[SPONSOR THIS SPOT →](mailto:la@curations.cc)*

---

<!-- NEWSLETTER VERSION ENDS HERE - CTA TO CONTINUE -->

**🍟 Want more? Ready for deeper dives into Good Vibes?**

[**CONTINUE TO EATS & MORE →**](#eats)

*[This CTA only appears in newsletter version - web version shows all content]*

<!-- END NEWSLETTER CTA -->

---

"""
        
        # Add all category sections
        for category in categories:
            items = self.content[category]
            newsletter_content += self.format_newsletter_section(category, items)
            newsletter_content += "---\n\n"
        
        # Add footer
        newsletter_content += """[GIF SENDOFF PLACEHOLDER - Insert farewell animated GIF here]

**GOOD VIBES ALWAYS!**

**SEE YOU NEXT WEEK, LA!** 🤙

---

<p class="universal-footer-tagline">
  🤙 Good Vibes curated with 💜 in LA by 👋 and 🤖 at
  <a href="https://curations.cc" target="_blank" rel="noopener" class="uf-brand-pill">CURATIONS</a>
</p>

[**↑ Back to HOV LANES**](#hov-lanes)"""

        # Save newsletter content
        self.save_newsletter_versions(newsletter_content)
        self.generate_summary_stats()
        
        print(f"\n✅ Newsletter generation complete!")
        print(f"📧 Email version: {self.output_path}/newsletter-email.md")
        print(f"🌐 Web version: {self.output_path}/newsletter-web.md")
    
    def save_newsletter_versions(self, content: str):
        """Save both email and web versions of newsletter"""
        
        # Email version (truncated at CTA)
        email_content = content.split("<!-- END NEWSLETTER CTA -->")[0]
        email_content += "\n\n**🍟 [Continue reading on the web →](https://la.curations.cc)**"
        
        with open(self.output_path / "newsletter-email.md", 'w') as f:
            f.write(email_content)
        
        # Web version (full content, remove CTA section)
        web_content = content.replace(
            "<!-- NEWSLETTER VERSION ENDS HERE - CTA TO CONTINUE -->", ""
        ).replace(
            "**🍟 Want more? Ready for deeper dives into Good Vibes?**\n\n[**CONTINUE TO EATS & MORE →**](#eats)\n\n*[This CTA only appears in newsletter version - web version shows all content]*\n\n<!-- END NEWSLETTER CTA -->", ""
        )
        
        with open(self.output_path / "newsletter-web.md", 'w') as f:
            f.write(web_content)
    
    def generate_summary_stats(self):
        """Generate summary statistics"""
        stats = {
            "date": self.date_str,
            "day": self.day_name,
            "generation_time": datetime.now().isoformat(),
            "categories": {},
            "total_items": 0,
            "avg_vibe_score": 0
        }
        
        total_score = 0
        total_items = 0
        
        for category, items in self.content.items():
            category_score = sum(item.get('vibe_score', 0) for item in items)
            stats["categories"][category] = {
                "items_count": len(items),
                "avg_vibe_score": round(category_score / len(items), 2) if items else 0,
                "neighborhoods": list(set(item.get('neighborhood', 'LA') for item in items))
            }
            total_items += len(items)
            total_score += category_score
        
        stats["total_items"] = total_items
        stats["avg_vibe_score"] = round(total_score / total_items, 2) if total_items else 0
        
        with open(self.output_path / "stats.json", 'w') as f:
            json.dump(stats, f, indent=2)

def main():
    """Main execution function"""
    print("🌴 CurationsLA Content Generator Starting...")
    
    generator = ContentGenerator()
    generator.generate_newsletter()
    
    print("\n🎉 All done! Good Vibes generated successfully!")

if __name__ == "__main__":
    main()