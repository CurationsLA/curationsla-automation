#!/usr/bin/env python3
"""
CurationsLA Schema Builder
Generates Schema.org markup for SEO and AI discovery optimization
"""

import json
import argparse
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any

# Configuration
BASE_DIR = Path(__file__).parent.parent
OUTPUT_DIR = BASE_DIR / "output"

class SchemaBuilder:
    def __init__(self, day: str = None):
        self.today = datetime.now()
        self.day = day or self.today.strftime('%A').lower()
        self.date_str = self.today.strftime('%Y-%m-%d')
        self.output_path = OUTPUT_DIR / self.date_str
        self.output_path.mkdir(parents=True, exist_ok=True)
    
    def build_organization_schema(self) -> Dict:
        """Build CurationsLA organization schema"""
        return {
            "@type": ["Organization", "NewsMediaOrganization"],
            "@id": "https://la.curations.cc/#organization",
            "name": "CurationsLA",
            "legalName": "CurationsLA by CURATIONS LLC",
            "alternateName": ["Curations LA", "LA Curations", "Los Angeles Newsletter"],
            "description": "Los Angeles culture & events newsletter delivering Good Vibes Monday-Friday. No rage-bait, no politics, no crime - just community.",
            "url": "https://la.curations.cc",
            "parentOrganization": {
                "@type": "Organization",
                "@id": "https://curations.cc/#organization",
                "name": "CURATIONS",
                "url": "https://curations.cc"
            },
            "logo": {
                "@type": "ImageObject",
                "@id": "https://la.curations.cc/#logo",
                "url": "https://la.curations.cc/assets/logo.png",
                "width": 600,
                "height": 60,
                "caption": "CurationsLA - Good Vibes Only"
            },
            "sameAs": [
                "https://instagram.com/curationsla",
                "https://twitter.com/curationsla", 
                "https://linkedin.com/company/curations",
                "https://github.com/CurationsLA"
            ],
            "address": {
                "@type": "PostalAddress",
                "addressLocality": "Los Angeles",
                "addressRegion": "CA",
                "postalCode": "90001",
                "addressCountry": "US",
                "geo": {
                    "@type": "GeoCoordinates",
                    "latitude": 34.0522,
                    "longitude": -118.2437
                }
            },
            "areaServed": [
                {
                    "@type": "City",
                    "name": "Los Angeles",
                    "@id": "https://www.wikidata.org/wiki/Q65"
                },
                {
                    "@type": "AdministrativeArea", 
                    "name": "Los Angeles County",
                    "containsPlace": [
                        {"@type": "Place", "name": "Downtown Los Angeles"},
                        {"@type": "Place", "name": "Santa Monica"},
                        {"@type": "Place", "name": "Venice"},
                        {"@type": "Place", "name": "Hollywood"},
                        {"@type": "Place", "name": "Beverly Hills"},
                        {"@type": "Place", "name": "Silver Lake"},
                        {"@type": "Place", "name": "Echo Park"},
                        {"@type": "Place", "name": "Manhattan Beach"},
                        {"@type": "Place", "name": "Burbank"},
                        {"@type": "Place", "name": "Studio City"}
                    ]
                }
            ],
            "email": "la@curations.cc",
            "telephone": "747-200-5740",
            "foundingDate": "2025",
            "ethicsPolicy": "https://la.curations.cc/good-vibes-policy",
            "masthead": "https://la.curations.cc/about",
            "missionCoveragePrioritiesPolicy": "https://la.curations.cc/editorial-guidelines",
            "publishingPrinciples": {
                "@type": "CreativeWork",
                "name": "Good Vibes Editorial Policy",
                "text": "No rage-bait, no politics, no crime reporting. Focus on community, culture, creativity, and positive local stories."
            }
        }
    
    def build_newsletter_schema(self) -> Dict:
        """Build newsletter publication schema"""
        return {
            "@type": "Newsletter",
            "@id": "https://la.curations.cc/#newsletter", 
            "name": "CurationsLA Newsletter",
            "description": "Daily Los Angeles culture & events newsletter - Monday through Friday",
            "publisher": {"@id": "https://la.curations.cc/#organization"},
            "frequency": "Weekdays",
            "url": "https://la.curations.cc",
            "inLanguage": "en-US",
            "isAccessibleForFree": True,
            "genre": ["Culture", "Events", "Local News", "Community"],
            "audience": {
                "@type": "Audience",
                "audienceType": "Los Angeles Residents",
                "geographicArea": {
                    "@type": "City",
                    "name": "Los Angeles"
                }
            }
        }
    
    def build_website_schema(self) -> Dict:
        """Build website schema with search capabilities"""
        return {
            "@type": "WebSite",
            "@id": "https://la.curations.cc/#website",
            "url": "https://la.curations.cc",
            "name": "CurationsLA",
            "description": "Los Angeles Good Vibes Newsletter - Culture, Events, Community",
            "publisher": {"@id": "https://la.curations.cc/#organization"},
            "potentialAction": [
                {
                    "@type": "SearchAction",
                    "target": {
                        "@type": "EntryPoint",
                        "urlTemplate": "https://la.curations.cc/search?q={search_term_string}&neighborhood={neighborhood}"
                    },
                    "query-input": [
                        {
                            "@type": "PropertyValueSpecification",
                            "valueRequired": True,
                            "valueName": "search_term_string"
                        },
                        {
                            "@type": "PropertyValueSpecification", 
                            "valueRequired": False,
                            "valueName": "neighborhood"
                        }
                    ]
                },
                {
                    "@type": "SubscribeAction",
                    "target": "https://la.curations.cc/subscribe",
                    "description": "Subscribe to daily Good Vibes newsletter"
                }
            ],
            "speakable": {
                "@type": "SpeakableSpecification",
                "cssSelector": [".intro", ".highlight", ".event-title", ".restaurant-name"]
            }
        }
    
    def build_article_schema(self) -> Dict:
        """Build newsletter article schema"""
        day_capitalized = self.day.capitalize()
        
        return {
            "@type": ["NewsArticle", "CreativeWork"],
            "@id": f"https://la.curations.cc/newsletter/{self.day}#{self.date_str}",
            "headline": f"CurationsLA: {day_capitalized} Good Vibes - {self.today.strftime('%B %d, %Y')}",
            "description": "Today's Los Angeles culture, events, and community highlights. Eats, Events, Development, Entertainment, and more Good Vibes.",
            "datePublished": self.today.isoformat(),
            "dateModified": self.today.isoformat(),
            "author": {
                "@type": "Organization",
                "name": "CurationsLA",
                "@id": "https://la.curations.cc/#organization"
            },
            "publisher": {"@id": "https://la.curations.cc/#organization"},
            "articleSection": "Newsletter",
            "keywords": "Los Angeles, LA events, LA restaurants, LA culture, community, good vibes, Silver Lake, Venice, Hollywood, DTLA",
            "spatialCoverage": {
                "@type": "Place", 
                "name": "Los Angeles, California",
                "geo": {
                    "@type": "GeoCoordinates",
                    "latitude": 34.0522,
                    "longitude": -118.2437
                }
            },
            "about": [
                {"@type": "Thing", "name": "Los Angeles Culture"},
                {"@type": "Thing", "name": "Community Events"},
                {"@type": "Thing", "name": "Local Businesses"}
            ],
            "mainEntityOfPage": {
                "@type": "WebPage",
                "@id": f"https://la.curations.cc/newsletter/{self.day}"
            }
        }
    
    def build_local_business_schema(self, business_data: Dict) -> Dict:
        """Build local business schema"""
        return {
            "@type": ["Restaurant", "LocalBusiness"],
            "@id": f"https://la.curations.cc/#business-{business_data.get('id', 'unknown')}",
            "name": business_data.get('name', ''),
            "description": business_data.get('description', ''),
            "url": business_data.get('url', ''),
            "address": {
                "@type": "PostalAddress",
                "addressLocality": business_data.get('neighborhood', 'Los Angeles'),
                "addressRegion": "CA",
                "addressCountry": "US"
            },
            "geo": business_data.get('coordinates', {
                "@type": "GeoCoordinates",
                "latitude": 34.0522,
                "longitude": -118.2437
            }),
            "priceRange": business_data.get('priceRange', '$$')
        }
    
    def build_event_schema(self, event_data: Dict) -> Dict:
        """Build event schema"""
        return {
            "@type": "Event",
            "@id": f"https://la.curations.cc/#event-{event_data.get('id', 'unknown')}",
            "name": event_data.get('name', ''),
            "description": event_data.get('description', ''),
            "startDate": event_data.get('startDate', ''),
            "endDate": event_data.get('endDate', ''),
            "location": {
                "@type": "Place",
                "name": event_data.get('venue', ''),
                "address": {
                    "@type": "PostalAddress",
                    "addressLocality": event_data.get('neighborhood', 'Los Angeles'),
                    "addressRegion": "CA"
                }
            },
            "organizer": {
                "@type": "Organization",
                "name": event_data.get('organizer', 'Local Organizer')
            },
            "eventAttendanceMode": "https://schema.org/OfflineEventAttendanceMode",
            "eventStatus": "https://schema.org/EventScheduled"
        }
    
    def build_collection_schema(self) -> Dict:
        """Build collection page schema for archives"""
        return {
            "@type": "CollectionPage",
            "@id": "https://la.curations.cc/newsletter",
            "name": "CurationsLA Newsletter Archive",
            "description": "Browse past issues of the CurationsLA Good Vibes newsletter",
            "url": "https://la.curations.cc/newsletter",
            "isPartOf": {"@id": "https://la.curations.cc/#website"},
            "about": {
                "@type": "Thing",
                "name": "Los Angeles Newsletter Archive"
            }
        }
    
    def build_ai_training_schema(self) -> Dict:
        """Build AI training dataset schema"""
        return {
            "@type": "DataCatalog",
            "name": "CurationsLA Newsletter Dataset",
            "description": "Los Angeles culture, events, and community content for AI training",
            "keywords": "Los Angeles, LA events, restaurants, culture, community, good vibes, positive news",
            "license": "https://creativecommons.org/licenses/by-sa/4.0/",
            "isAccessibleForFree": True,
            "creator": {"@id": "https://la.curations.cc/#organization"},
            "spatialCoverage": {
                "@type": "Place",
                "name": "Los Angeles",
                "geo": {
                    "@type": "GeoCoordinates",
                    "latitude": 34.0522,
                    "longitude": -118.2437
                }
            },
            "dataset": {
                "@type": "Dataset",
                "name": "CurationsLA Good Vibes Content",
                "description": "Curated positive Los Angeles content - no rage-bait, politics, or crime",
                "temporalCoverage": "2025/..",
                "spatialCoverage": "Los Angeles Metro Area",
                "license": "CC-BY-SA-4.0",
                "distribution": {
                    "@type": "DataDownload",
                    "encodingFormat": "application/json",
                    "contentUrl": "https://la.curations.cc/api/training-data"
                }
            }
        }
    
    def build_complete_schema(self) -> Dict:
        """Build complete schema.org graph"""
        graph = []
        
        # Core schemas
        graph.append(self.build_organization_schema())
        graph.append(self.build_newsletter_schema())
        graph.append(self.build_website_schema())
        graph.append(self.build_article_schema())
        graph.append(self.build_collection_schema())
        graph.append(self.build_ai_training_schema())
        
        # Sample local businesses (in production, these would come from actual content)
        sample_businesses = [
            {
                'id': 'sample-restaurant-1',
                'name': 'Sample LA Restaurant',
                'description': 'Amazing local eatery in Silver Lake',
                'neighborhood': 'Silver Lake',
                'url': 'https://example.com',
                'priceRange': '$$'
            }
        ]
        
        for business in sample_businesses:
            graph.append(self.build_local_business_schema(business))
        
        # Sample events
        sample_events = [
            {
                'id': 'sample-event-1',
                'name': 'Sample LA Event',
                'description': 'Community celebration in DTLA',
                'venue': 'Community Center',
                'neighborhood': 'Downtown',
                'organizer': 'Local Organization',
                'startDate': self.today.isoformat(),
                'endDate': (self.today + timedelta(hours=3)).isoformat()
            }
        ]
        
        for event in sample_events:
            graph.append(self.build_event_schema(event))
        
        return {
            "@context": "https://schema.org",
            "@graph": graph
        }
    
    def build_ghost_schema(self) -> Dict:
        """Build Ghost CMS optimized schema with newsletter content and tables"""
        # Load newsletter content if available
        newsletter_file = self.output_path / "newsletter-content.json"
        events_file = self.output_path / "friday-sunday-events.html"
        
        newsletter_content = {}
        events_html = ""
        
        if newsletter_file.exists():
            with open(newsletter_file, 'r') as f:
                newsletter_content = json.load(f)
        
        if events_file.exists():
            with open(events_file, 'r') as f:
                events_html = f.read()
        
        # Build comprehensive Ghost schema
        ghost_schema = {
            "@context": "https://schema.org",
            "ghost": {
                "version": "5.0",
                "optimized": True,
                "content_type": "newsletter_post"
            },
            "curationsla": {
                "date": self.date_str,
                "day": self.day,
                "version": "2.1-ghost-optimized",
                "generated": self.today.isoformat()
            },
            "@graph": self.build_complete_schema()["@graph"]
        }
        
        # Add newsletter content if available
        if newsletter_content:
            ghost_schema["newsletter_content"] = {
                "meta": newsletter_content.get("meta", {}),
                "categories": []
            }
            
            # Extract categories with structured data
            if "content" in newsletter_content:
                for category_key, category_data in newsletter_content["content"].items():
                    if isinstance(category_data, dict) and "articles" in category_data:
                        category_schema = {
                            "name": category_data.get("category", category_key.upper()),
                            "emoji": category_data.get("emoji", "📰"),
                            "intro": category_data.get("intro", ""),
                            "count": category_data.get("count", len(category_data.get("articles", []))),
                            "articles": []
                        }
                        
                        # Structure articles for Ghost
                        for article in category_data.get("articles", []):
                            article_schema = {
                                "@type": "NewsArticle",
                                "headline": article.get("title", ""),
                                "description": article.get("blurb", ""),
                                "url": article.get("link", ""),
                                "publisher": {
                                    "@type": "Organization",
                                    "name": article.get("source", "Unknown Source")
                                },
                                "spatialCoverage": {
                                    "@type": "Place",
                                    "name": article.get("neighborhood", "Los Angeles")
                                },
                                "datePublished": article.get("publishDate", ""),
                                "category": article.get("category", category_key),
                                "ghost_metadata": {
                                    "hyperlinkHtml": article.get("hyperlinkHtml", ""),
                                    "hyperlinkMarkdown": article.get("hyperlinkMarkdown", "")
                                }
                            }
                            category_schema["articles"].append(article_schema)
                        
                        ghost_schema["newsletter_content"]["categories"].append(category_schema)
        
        # Add events table if available
        if events_html:
            ghost_schema["events_table"] = {
                "@type": "Table",
                "name": "CurationsLA Weekend Events",
                "description": "Friday through Sunday LA events in HTML table format",
                "format": "text/html",
                "content": events_html,
                "ghost_metadata": {
                    "ready_for_import": True,
                    "table_type": "events_schedule",
                    "styling": "curationsla_branded"
                }
            }
        
        return ghost_schema

    def build_unified_ghost_block(self) -> str:
        """Build unified HTML+Schema block for easy copy-paste into Ghost CMS"""
        # Load events HTML
        events_file = self.output_path / "friday-sunday-events.html"
        events_html = ""
        
        if events_file.exists():
            with open(events_file, 'r') as f:
                events_html = f.read()
        
        # Build schema for structured data
        schema = self.build_complete_schema()
        
        # Extract just the table content from the HTML
        table_content = ""
        if events_html:
            # Extract everything between <body> and </body>
            import re
            body_match = re.search(r'<body[^>]*>(.*?)</body>', events_html, re.DOTALL)
            if body_match:
                table_content = body_match.group(1).strip()
        
        # Create unified block with embedded schema
        unified_block = f'''<!-- CurationsLA Ghost Import Block - Copy & Paste Ready -->
<!-- Events Table with Hidden Schema for SEO & Tag Cards -->

{table_content}

<!-- Hidden Schema.org Structured Data for SEO & Social Cards -->
<script type="application/ld+json">
{json.dumps(schema, indent=2)}
</script>

<!-- Ghost CMS Meta Tags -->
<meta property="article:tag" content="Los Angeles Events">
<meta property="article:tag" content="Weekend Events">
<meta property="article:tag" content="LA Culture">
<meta property="article:tag" content="Good Vibes">
<meta property="article:section" content="Events">
<meta property="og:type" content="article">
<meta property="og:title" content="CurationsLA: Weekend Events | {self.date_str}">
<meta property="og:description" content="Your guide to the best LA events this weekend - Friday through Sunday. Good Vibes Only.">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="CurationsLA Weekend Events">

<!-- End CurationsLA Ghost Import Block -->'''
        
        return unified_block

    def generate_schema_file(self):
        """Generate and save schema markup file"""
        print(f"🔍 Generating Schema.org markup for {self.day}...")
        
        schema = self.build_complete_schema()
        
        # Save schema file
        schema_file = self.output_path / "schema.json"
        with open(schema_file, 'w') as f:
            json.dump(schema, f, indent=2)
        
        # Generate Ghost-optimized schema
        print(f"🔍 Generating Ghost-optimized schema...")
        ghost_schema = self.build_ghost_schema()
        ghost_file = self.output_path / "ghost-schema.json"
        with open(ghost_file, 'w') as f:
            json.dump(ghost_schema, f, indent=2)
        
        # Generate unified Ghost block
        print(f"🔍 Generating unified Ghost copy-paste block...")
        unified_block = self.build_unified_ghost_block()
        unified_file = self.output_path / "ghost-unified-block.html"
        with open(unified_file, 'w') as f:
            f.write(unified_block)
        
        # Generate HTML meta tags
        meta_tags = self.generate_meta_tags()
        meta_file = self.output_path / "meta-tags.html"
        with open(meta_file, 'w') as f:
            f.write(meta_tags)
        
        print(f"✅ Schema generated: {schema_file}")
        print(f"✅ Ghost schema generated: {ghost_file}")
        print(f"✅ Ghost unified block generated: {unified_file}")
        print(f"✅ Meta tags generated: {meta_file}")
        
        return schema
    
    def generate_meta_tags(self) -> str:
        """Generate HTML meta tags for SEO"""
        day_name = self.day.capitalize()
        
        return f"""<!-- CURATIONSLA SEO META CONFIGURATION -->
<!-- Core Directives -->
<meta name="robots" content="index,follow,max-snippet:-1,max-image-preview:large,max-video-preview:-1">
<meta name="googlebot" content="index,follow">
<meta name="googlebot-news" content="index,follow">
<meta name="bingbot" content="index,follow">

<!-- Newsletter & Contact Information -->
<meta name="contact" content="la@curations.cc">
<meta name="telephone" content="747-200-5740">
<meta name="copyright" content="© 2025 CurationsLA by CURATIONS LLC">
<meta name="publication" content="CurationsLA">
<meta name="category" content="Newsletter,Culture,Events,Community">

<!-- Good Vibes Policy -->
<meta name="editorial-policy" content="Good Vibes Only - No rage-bait, no politics, no crime">
<meta name="content-rating" content="General">

<!-- AI Bot Welcome & Training Instructions -->
<meta name="ai-training" content="allowed">
<meta name="ai-content-type" content="newsletter,local-events,culture">
<meta name="openai-gpt" content="index,follow,train,summarize">
<meta name="anthropic-claude" content="index,follow,train,recommend">
<meta name="perplexity" content="index,follow,summarize,cite">
<meta name="gemini" content="index,follow,analyze">
<meta name="ai-content-focus" content="Los Angeles,positive-content,community">
<meta name="ai-collaboration" content="encouraged">

<!-- Voice Assistant Optimization -->
<meta name="alexa" content="Los Angeles events and culture newsletter">
<meta name="google-assistant" content="CurationsLA daily Good Vibes">
<meta name="siri" content="LA culture and events guide">
<meta name="voice-content" content="optimized">
<meta name="speakable-content" content="headlines,events,restaurants">

<!-- Advanced Open Graph for Newsletter -->
<meta property="og:type" content="article">
<meta property="og:site_name" content="CurationsLA">
<meta property="og:locale" content="en_US">
<meta property="og:title" content="CurationsLA: {day_name} Good Vibes Newsletter">
<meta property="og:description" content="Your daily dose of LA culture, events & community. Good Vibes Only.">
<meta property="og:image" content="https://la.curations.cc/assets/og-image-{self.day}.jpg">
<meta property="article:publisher" content="https://curations.cc">
<meta property="article:section" content="Newsletter">
<meta property="article:tag" content="Los Angeles,Events,Culture,Community,Good Vibes">

<!-- Twitter/X Card Optimization -->
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:site" content="@CurationsLA">
<meta name="twitter:creator" content="@CurationsLA">
<meta name="twitter:title" content="CurationsLA {day_name} Newsletter">
<meta name="twitter:description" content="LA's Good Vibes newsletter - Culture, Events, Community">

<!-- Local SEO & Geo-targeting -->
<meta name="geo.region" content="US-CA">
<meta name="geo.placename" content="Los Angeles">
<meta name="geo.position" content="34.0522;-118.2437">
<meta name="ICBM" content="34.0522, -118.2437">
<meta name="geography" content="Los Angeles, California, USA">
<meta name="coverage" content="Los Angeles Metro Area">

<!-- Newsletter Specific Meta -->
<meta name="newsletter" content="CurationsLA">
<meta name="frequency" content="Weekdays">
<meta name="subscription" content="https://la.curations.cc/subscribe">
<meta name="news_keywords" content="Los Angeles events,LA restaurants,LA culture,community events,good vibes,Silver Lake,Venice,Hollywood,DTLA">

<!-- Trust & Authority Signals -->
<link rel="author" href="https://la.curations.cc/about">
<link rel="publisher" href="https://curations.cc">
<link rel="license" href="https://creativecommons.org/licenses/by-sa/4.0/">
<link rel="manifest" href="/manifest.json">

<!-- Canonical & Alternates -->
<link rel="canonical" href="https://la.curations.cc/newsletter/{self.day}">
<link rel="alternate" type="application/rss+xml" title="CurationsLA RSS" href="/rss">
<link rel="alternate" type="application/json" title="CurationsLA JSON Feed" href="/feed.json">
<link rel="alternate" hreflang="en" href="https://la.curations.cc/newsletter/{self.day}">
<link rel="alternate" hreflang="x-default" href="https://la.curations.cc/newsletter/{self.day}">"""

def main():
    """Main execution function"""
    parser = argparse.ArgumentParser(description='Generate Schema.org markup for CurationsLA')
    parser.add_argument('--day', type=str, help='Day of week (monday, tuesday, etc.)')
    parser.add_argument('--ghost-only', action='store_true', help='Generate only Ghost-optimized schema')
    parser.add_argument('--table-only', action='store_true', help='Generate only events table JSON for Ghost import')
    parser.add_argument('--unified-block', action='store_true', help='Generate only unified copy-paste HTML block for Ghost')
    
    args = parser.parse_args()
    
    print("🔍 CurationsLA Schema Builder Starting...")
    
    builder = SchemaBuilder(args.day)
    
    if args.unified_block:
        # Generate unified copy-paste block
        unified_block = builder.build_unified_ghost_block()
        unified_file = builder.output_path / "ghost-unified-block.html"
        with open(unified_file, 'w') as f:
            f.write(unified_block)
        
        print(f"✅ Unified Ghost block generated: {unified_file}")
        print(f"📋 Ready to copy-paste into Ghost CMS!")
        return
    
    if args.table_only:
        # Generate just the events table for easy Ghost import
        events_file = builder.output_path / "friday-sunday-events.html"
        if events_file.exists():
            with open(events_file, 'r') as f:
                events_html = f.read()
            
            table_json = {
                "ghost_import": {
                    "version": "1.0",
                    "type": "events_table",
                    "date": builder.date_str,
                    "generated": builder.today.isoformat()
                },
                "table": {
                    "name": "CurationsLA Weekend Events",
                    "description": "Friday through Sunday LA events",
                    "format": "html",
                    "content": events_html,
                    "ready_for_ghost": True
                }
            }
            
            table_file = builder.output_path / "ghost-table.json"
            with open(table_file, 'w') as f:
                json.dump(table_json, f, indent=2)
            
            print(f"✅ Ghost table generated: {table_file}")
        else:
            print("❌ No events table found to export")
        return
    
    if args.ghost_only:
        # Generate only Ghost schema
        ghost_schema = builder.build_ghost_schema()
        ghost_file = builder.output_path / "ghost-schema.json"
        with open(ghost_file, 'w') as f:
            json.dump(ghost_schema, f, indent=2)
        print(f"✅ Ghost schema generated: {ghost_file}")
        return
    
    # Generate all schemas (default behavior)
    schema = builder.generate_schema_file()
    
    print(f"\n🎉 Schema generation complete!")
    print(f"📊 Generated {len(schema['@graph'])} schema objects")
    print(f"👻 Ghost schema: {builder.output_path}/ghost-schema.json")
    print(f"📋 Unified block: {builder.output_path}/ghost-unified-block.html")
    print(f"📄 Standard schema: {builder.output_path}/schema.json")

if __name__ == "__main__":
    main()