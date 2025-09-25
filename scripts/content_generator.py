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

# Try to import web scraper, but make it optional
try:
    from web_scraper import WebScraper
    WEB_SCRAPING_AVAILABLE = True
except ImportError:
    print("⚠️  Web scraping not available - install beautifulsoup4")
    WEB_SCRAPING_AVAILABLE = False

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

# Morning Brew Style Elements
MORNING_BREW_STYLE = {
    'intros': [
        "What's crackin', LA? 🌴",
        "Rise and grind, Angels! ☀️", 
        "Good morning, LA legends! 💫",
        "Hey gorgeous people of LA! ✨"
    ],
    'transitions': [
        "But wait, there's more...",
        "Speaking of which...",
        "In other news that'll make you smile...",
        "Plot twist:",
        "Meanwhile, across town..."
    ],
    'callouts': [
        "💡 Pro tip:",
        "🔥 Hot take:",
        "📈 Trending up:",
        "✨ Good vibes only:",
        "🎯 Don't miss:"
    ]
}

# CurationsLA Voice Elements  
CURATIONS_VOICE = {
    'enthusiasm': ["absolutely obsessed", "can't even", "total game-changer", "pure magic"],
    'community': ["neighbors", "LA family", "our people", "fellow angels"],
    'positivity': ["good vibes", "positive energy", "spreading joy", "celebrating wins"]
}

class ContentGenerator:
    def __init__(self):
        self.target_date = datetime(2025, 9, 26)  # Friday September 26th, 2025
        self.today = self.target_date  # Use target date instead of current date
        self.day_name = self.target_date.strftime('%A').lower()
        self.date_str = self.target_date.strftime('%Y-%m-%d')
        self.cutoff_date = datetime(2025, 9, 25) - timedelta(days=3)  # Not outdated by 3 days from Sept 25
        self.content = {}
        self.js_content_data = {}
        
        # Initialize web scraper for failed RSS feeds (if available)
        if WEB_SCRAPING_AVAILABLE:
            self.web_scraper = WebScraper()
        else:
            self.web_scraper = None
        
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
    
    def fetch_with_scraping_fallback(self, feed_info: Dict, category: str) -> List[Dict]:
        """Fetch content with web scraping fallback for failed RSS feeds"""
        # First try RSS
        rss_items = self.fetch_rss_feed(feed_info['url'], feed_info['name'])
        
        if rss_items:
            return rss_items
        
        # If RSS failed and web scraping is available, try web scraping fallback
        if not self.web_scraper:
            return []
            
        print(f"🕷️  RSS failed for {feed_info['name']}, attempting web scraping...")
        
        # Map common sources to scrapers
        scraper_mapping = {
            'laist': 'laist',
            'la weekly': 'laweekly', 
            'timeout': 'timeout_la',
            'time out': 'timeout_la',
            'we like la': 'welikela',
            'thrillist': 'thrillist_la',
            'la magazine': 'la_magazine',
            'secret': 'secret_la',
            'discover': 'discoverla',
            'downtown news': 'la_downtown_news'
        }
        
        # Try to find a matching scraper
        source_name = feed_info['name'].lower()
        scraper_name = None
        
        for key, scraper in scraper_mapping.items():
            if key in source_name:
                scraper_name = scraper
                break
        
        if scraper_name:
            try:
                scraped_items = self.web_scraper.scrape_content(scraper_name, category, 10)
                if scraped_items:
                    print(f"✅ Web scraping successful for {feed_info['name']}: {len(scraped_items)} items")
                    return scraped_items
            except Exception as e:
                print(f"❌ Web scraping also failed for {feed_info['name']}: {str(e)}")
        
        return []
    
    def is_content_fresh(self, item_date_str: str) -> bool:
        """Check if content is not outdated by more than 3 days from Sept 25, 2025"""
        try:
            # Parse the date from the RSS item
            item_date = datetime.strptime(item_date_str, '%a, %d %b %Y %H:%M:%S %z')
            item_date = item_date.replace(tzinfo=None)  # Remove timezone for comparison
            return item_date >= self.cutoff_date
        except:
            # If we can't parse the date, assume it's fresh
            return True
    
    def get_random_style_element(self, category: str) -> str:
        """Get random Morning Brew or CurationsLA style element"""
        if category == 'intro':
            return random.choice(MORNING_BREW_STYLE['intros'])
        elif category == 'transition':
            return random.choice(MORNING_BREW_STYLE['transitions'])
        elif category == 'callout':
            return random.choice(MORNING_BREW_STYLE['callouts'])
        elif category == 'enthusiasm':
            return random.choice(CURATIONS_VOICE['enthusiasm'])
        elif category == 'community':
            return random.choice(CURATIONS_VOICE['community'])
        elif category == 'positivity':
            return random.choice(CURATIONS_VOICE['positivity'])
        return ""
    
    def generate_morning_brew_style_blurb(self, item: Dict) -> str:
        """Generate content blurb mixing Morning Brew and CurationsLA styles"""
        enthusiasm = self.get_random_style_element('enthusiasm')
        community = self.get_random_style_element('community')
        
        # Clean and shorten description
        desc = re.sub(r'<[^>]+>', '', item['description'])
        if len(desc) > 120:
            desc = desc[:117] + "..."
        
        # Create Morning Brew style blurb
        blurb = f"{desc} This is {enthusiasm} for our {community}! 🌟"
        return blurb
    
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
                items = self.fetch_with_scraping_fallback(feed, category)
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
        self.generate_js_content()  # Generate JS content file
        self.generate_summary_stats()
        
        print(f"\n✅ Newsletter generation complete!")
        print(f"📧 Email version: {self.output_path}/newsletter-email.md")
        print(f"🌐 Web version: {self.output_path}/newsletter-web.md")
        print(f"📄 JS content: {self.output_path}/newsletter-content.js")
    
    def generate_js_content(self):
        """Generate JavaScript content file with hyperlinked articles"""
        print("📄 Generating JavaScript content file...")
        
        # Process content for JS format
        js_content_data = {}
        for category, items in self.content.items():
            js_articles = []
            for item in items:
                if self.is_content_fresh(item.get('published', '')):
                    js_article = {
                        'title': item['title'],
                        'blurb': self.generate_morning_brew_style_blurb(item),
                        'link': item['link'],
                        'source': item.get('source', 'Unknown'),
                        'neighborhood': item.get('neighborhood', 'Los Angeles'),
                        'category': category,
                        'publishDate': item.get('published', '2025-09-25'),
                        'hyperlinkHtml': f'<a href="{item["link"]}" target="_blank" rel="noopener noreferrer">{item["title"]}</a>',
                        'hyperlinkMarkdown': f'[{item["title"]}]({item["link"]})'
                    }
                    js_articles.append(js_article)
            
            js_content_data[category] = {
                'category': category.upper(),
                'emoji': self.get_category_emoji(category),
                'intro': self.get_category_intro(category),
                'articles': js_articles,
                'count': len(js_articles)
            }
        
        # Generate JS file content
        js_content = f'''/**
 * CurationsLA Newsletter Content - Friday September 26th, 2025
 * Generated with Good Vibes and Morning Brew style blend
 */

const CurationsLANewsletter = {{
    date: '{self.date_str}',
    day: '{self.day_name.title()}',
    generated: '{datetime.now().isoformat()}',
    
    // Newsletter Header
    header: {{
        greeting: "HEY LOS ANGELES! 🌴",
        tagline: "IT'S {self.day_name.upper()} - YOUR WEEKLY DOSE OF GOOD VIBES",
        intro: "Welcome to your daily dose of LA's good vibes! We've scoured the city to bring you the best openings, events, and community celebrations happening right now."
    }},

    // Content Categories with Hyperlinked Articles
    content: {json.dumps(js_content_data, indent=2)},

    // Utility Functions
    utils: {{
        getArticleLink: function(category, index) {{
            const article = CurationsLANewsletter.content[category].articles[index];
            return article ? article.link : '#';
        }},
        
        getArticleHTML: function(category, index) {{
            const article = CurationsLANewsletter.content[category].articles[index];
            return article ? article.hyperlinkHtml : '';
        }},
        
        getArticleMarkdown: function(category, index) {{
            const article = CurationsLANewsletter.content[category].articles[index];
            return article ? article.hyperlinkMarkdown : '';
        }},
        
        getAllLinks: function() {{
            const allLinks = [];
            Object.values(CurationsLANewsletter.content).forEach(category => {{
                category.articles.forEach(article => {{
                    allLinks.push({{
                        title: article.title,
                        url: article.link,
                        category: article.category,
                        source: article.source
                    }});
                }});
            }});
            return allLinks;
        }}
    }},

    // Newsletter Footer
    footer: {{
        signature: "Made with 💜 in Los Angeles",
        tagline: "Bringing Good Vibes when our city needs it most",
        contact: {{
            email: "la@curations.cc",
            website: "https://la.curations.cc",
            phone: "747-200-5740"
        }}
    }}
}};

// Export for Node.js environments
if (typeof module !== 'undefined' && module.exports) {{
    module.exports = CurationsLANewsletter;
}}

// Make available globally for browsers
if (typeof window !== 'undefined') {{
    window.CurationsLANewsletter = CurationsLANewsletter;
}}
'''
        
        # Save JS content file
        js_file_path = self.output_path / 'newsletter-content.js'
        with open(js_file_path, 'w') as f:
            f.write(js_content)
        
        # Also save JSON version
        json_file_path = self.output_path / 'newsletter-content.json'
        with open(json_file_path, 'w') as f:
            json.dump({
                'meta': {
                    'date': self.date_str,
                    'generated': datetime.now().isoformat(),
                    'style': 'CurationsLA + Morning Brew blend'
                },
                'content': js_content_data
            }, f, indent=2)
        
        print(f"✅ JavaScript content saved: {js_file_path}")
        
    def get_category_emoji(self, category: str) -> str:
        """Get emoji for category"""
        emojis = {
            'eats': '🍴',
            'events': '🎉', 
            'community': '🤝',
            'development': '🏗️',
            'business': '💼',
            'entertainment': '🎭',
            'sports': '🏆',
            'goodies': '✨'
        }
        return emojis.get(category, '📍')
    
    def get_category_intro(self, category: str) -> str:
        """Get Morning Brew style intro for category"""
        intros = {
            'eats': "The food scene is absolutely buzzing right now...",
            'events': "Your social calendar is about to get very full...",
            'community': "LA's heart is showing up in the best ways...",
            'development': "The city is transforming before our eyes...",
            'business': "Local entrepreneurs are crushing it...",
            'entertainment': "The creative energy is off the charts...",
            'sports': "Our teams and athletes are bringing the heat...",
            'goodies': "Hidden gems and special finds await..."
        }
        return intros.get(category, "Amazing things are happening...")
    
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