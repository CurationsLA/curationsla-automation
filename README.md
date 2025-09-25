# 🌴 CurationsLA Automation System

**Los Angeles Good Vibes Newsletter - Automated Content Generation with Web Scraping**

![Newsletter Status](https://img.shields.io/badge/Newsletter-Enhanced_With_Web_Scraping-success)
![Agent Status](https://img.shields.io/badge/Agents-10_Specialized_Deployed-active)
![Good Vibes](https://img.shields.io/badge/Good_Vibes-Guaranteed-brightgreen)
![Web Scraping](https://img.shields.io/badge/Web_Scraping-Enabled-blue)

## 🚀 System Status

**✅ FULLY OPERATIONAL - ENHANCED**
- **📅 Target Date**: Friday, September 26th, 2025
- **🤖 Specialized Agents Deployed**: 10 local LA news sourcing agents
- **📍 Coverage**: 26+ Los Angeles neighborhoods with hyperlocal focus
- **📰 Content Categories**: 10 specialized categories with dedicated agents
- **🕷️ Web Scraping**: Smart fallback system for failed RSS feeds
- **💜 Good Vibes Policy**: No rage-bait, politics, or crime - just community

## 🤖 Specialized Deployed Agents

### Local News & Community Agents
1. **LocalNewsScout** (`agent_la_news_001`) - Local LA news, breaking stories, community updates
2. **CommunityHero** (`agent_community_005`) - Neighborhood stories, local heroes, community initiatives

### Business & Development Agents  
3. **BizRealEstateTracker** (`agent_biz_realestate_002`) - Business openings, commercial real estate
4. **CommercialDevTracker** (`agent_commercial_development_008`) - Development projects, infrastructure

### Entertainment & Events Agents
5. **EntertainmentSpotter** (`agent_entertainment_003`) - Entertainment events, concerts, LA Scenestar-style coverage
6. **EventActivitiesScout** (`agent_events_activities_007`) - Weekend activities, events, family-friendly coverage

### Lifestyle & Culture Agents  
7. **EatsExplorer** (`agent_eats_004`) - Restaurant openings, food trucks, culinary events
8. **ShoppingCommercialScout** (`agent_shopping_commercial_009`) - Shopping, retail openings, pop-ups
9. **ArtsCultureSpotter** (`agent_arts_culture_010`) - Arts, culture, galleries, creative scene

### Sports & Recreation Agents
10. **SportsChampion** (`agent_sports_recreation_006`) - Sports teams, recreational activities, fitness events

## 🛠️ Enhanced System Components

### Core Infrastructure
- **GitHub Actions**: Daily automation (Monday-Friday at 6:00 AM)
- **Hybrid Content Sources**: RSS feeds with web scraping fallbacks
- **Smart Fallback System**: Automatically switches to web scraping when RSS feeds fail
- **Good Vibes Filter**: Removes negative content automatically  
- **Morning Brew Style**: Blends CurationsLA voice with Morning Brew newsletter approach

### Content Sources (60+ sources)
- **RSS Feeds**: Primary source for reliable publishers
- **Web Scraping**: Fallback for failed RSS feeds using BeautifulSoup
- **Specialized Agents**: Each agent targets specific LA news categories
- **Content Freshness**: Ensures content is not outdated by 3+ days

### Technical Features
- **JavaScript Content API**: Hyperlinked articles with utility functions
- **Schema.org**: SEO optimization for search engines
- **AI Discovery**: Optimized for ChatGPT, Claude, Perplexity, and other AI platforms
- **Cloudflare Worker**: Advanced SEO and performance optimization

## 📋 Deployment Instructions

### Prerequisites
```bash
# Install Python dependencies
pip install feedparser requests beautifulsoup4 python-dateutil lxml

# Clone repository
git clone https://github.com/CurationsLA/curationsla-automation.git
cd curationsla-automation
```

### Initial Setup
```bash
# 1. Deploy specialized agents
python scripts/deploy_specialized_agents.py

# 2. Test web scraping functionality  
python scripts/test_web_scraping.py

# 3. Generate newsletter content
python scripts/content_generator.py

# 4. Build Schema markup
python scripts/schema_builder.py --day friday

# 5. Create AI discovery files
python scripts/ai_discovery.py
```

### Environment Configuration
```bash
# Set environment variables (optional)
export OPENAI_API_KEY="your-api-key-here"  # For AI enhancements
export GITHUB_TOKEN="your-github-token"    # For automated commits

# GitHub Actions secrets required:
# - EMAIL_USERNAME: SMTP username for notifications
# - EMAIL_PASSWORD: SMTP password for notifications  
# - NOTIFICATION_EMAIL: Email for status updates
```

### Web Scraping Configuration
The system includes intelligent web scraping fallbacks for major LA news sources:

```python
# Supported scrapers (scripts/web_scraper.py):
scrapers = {
    'laist': 'LAist local news and culture',
    'laweekly': 'LA Weekly arts and events',  
    'timeout_la': 'Time Out LA restaurant and event guides',
    'welikela': 'We Like LA community content',
    'thrillist_la': 'Thrillist LA lifestyle content',
    'la_magazine': 'LA Magazine dining and culture',
    'secret_la': 'Secret Los Angeles hidden gems',
    'discoverla': 'Discover LA tourism and events',
    'la_downtown_news': 'LA Downtown News business coverage'
}
```

### Agent Configuration  
Each specialized agent includes:
- **RSS Sources**: Primary content feeds
- **Web Scraping Fallbacks**: Backup content sources
- **Good Vibes Filtering**: Content quality thresholds
- **Neighborhood Focus**: Geographic targeting
- **Focus Keywords**: Content relevance filtering

## 🔧 Troubleshooting Guide

### Common Issues & Solutions

#### RSS Feed Failures
```bash  
# Check RSS feed connectivity
python scripts/test_feeds.py --category eats

# View failed feeds in logs
grep "Error fetching" logs/content_generation.log

# Web scraping will automatically activate as fallback
```

#### Web Scraping Issues
```bash
# Test individual scrapers
python -c "
from scripts.web_scraper import WebScraper
scraper = WebScraper()
articles = scraper.scrape_content('laist', 'local', 5)
print(f'Found {len(articles)} articles')
"

# Check for blocked requests (rate limiting)
# Adjust rate limits in web_scraper.py:
rate_limiting = {
    'requests_per_minute': 10,  # Reduce if blocked
    'delay_between_requests': 6  # Increase delay
}
```

#### Low Content Volume
```bash
# Check agent configuration
cat agents/specialized/agent_la_news_001_config.json

# Reset agent status  
python scripts/deploy_specialized_agents.py

# Expand source diversity
# Edit source configurations in sources/feeds/
```

#### Good Vibes Filter Too Strict
```python
# Adjust filter thresholds in agent configs
"good_vibes_threshold": 0.6  # Lower = more permissive

# Check specific content scoring
from scripts.filters.good_vibes_filter import GoodVibesFilter
filter = GoodVibesFilter(threshold=0.5)
score = filter.calculate_vibe_score("your content here")
```

### Performance Monitoring
```bash
# System status check
python scripts/system_status.py

# Generate performance report  
python scripts/performance_report.py --date 2025-09-26

# Monitor RSS feed health
python scripts/feed_monitor.py --test-all

# View agent coordination
cat agents/specialized/specialized_coordination_system.json
```

### Emergency Protocols
- **RSS Feed Outage**: Web scraping automatically activates
- **Web Scraping Blocked**: Alternative scrapers deployed
- **Content Shortage**: Search parameters expanded dynamically
- **Quality Issues**: Enhanced Good Vibes filtering activated
- **Timeline Delays**: Priority content fast-tracked

## 📊 Content Generation Workflow

### 8-Step Enhanced Process
1. **Initialize**: Deploy all 10 specialized agents
2. **RSS Collection**: Attempt RSS feed collection for all sources
3. **Web Scraping Fallback**: Activate scrapers for failed RSS feeds
4. **Content Filtering**: Apply Good Vibes filtering with agent-specific thresholds
5. **Categorization**: Sort content by neighborhoods and specialties
6. **Style Application**: Apply CurationsLA + Morning Brew voice blending
7. **Newsletter Generation**: Create email, web, and JS versions
8. **Distribution**: Archive content and send notifications

### Content Quality Metrics
- **Volume Target**: 200+ high-quality content items
- **Geographic Coverage**: 20+ LA neighborhoods represented  
- **Category Balance**: Content across all 10 specialties
- **Good Vibes Score**: Average 0.8+ across all content
- **Web Scraping Success**: 80%+ fallback success rate
- **Timeliness**: Newsletter delivered by 6:00 AM Pacific

## 🔍 RSS Feed vs Web Scraping Strategy

### RSS Feeds (Primary)
- **Advantages**: Structured data, reliable format, fast processing
- **Limitations**: Many LA sources have broken/blocked feeds
- **Usage**: Primary method for major publishers (LA Times, etc.)

### Web Scraping (Fallback)  
- **Advantages**: Access to any website, works around feed failures
- **Limitations**: Slower, more complex, site-dependent
- **Usage**: Automatic fallback when RSS feeds fail
- **Rate Limiting**: Respectful crawling with delays

### Hybrid Approach Benefits
- **Resilience**: System continues working despite individual source failures
- **Comprehensive Coverage**: Access to sources without RSS feeds
- **Quality Maintenance**: Good Vibes filtering applies to all content
- **Scalability**: Easy to add new sources with either method

## 📞 Contact & Support

- **Email**: la@curations.cc
- **Phone**: 747-200-5740
- **Website**: https://la.curations.cc
- **GitHub Issues**: For technical problems and feature requests
- **Agent Configs**: `/agents/specialized/` directory

## 🚀 Recent Enhancements (v2.0)

### ✅ Completed
- [x] **Web Scraping Infrastructure**: Smart fallback system for failed RSS feeds
- [x] **10 Specialized Agents**: Dedicated agents for LA news categories  
- [x] **Enhanced Error Handling**: Graceful failures with fallback mechanisms
- [x] **Improved Content Diversity**: 26+ neighborhoods, 60+ sources
- [x] **Agent Coordination System**: Centralized management and monitoring
- [x] **Comprehensive Documentation**: Updated deployment and troubleshooting guides

### 🔄 In Progress  
- [ ] Advanced content deduplication across sources
- [ ] Machine learning for better Good Vibes scoring
- [ ] Real-time source health monitoring dashboard

---

**Made with 💜 in Los Angeles**  
*Bringing Good Vibes when our city needs it most - now with enhanced web scraping!*