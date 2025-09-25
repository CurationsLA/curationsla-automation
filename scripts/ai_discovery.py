#!/usr/bin/env python3
"""
CurationsLA AI Discovery Generator
Creates AI-optimized endpoints and manifests for discovery by AI platforms
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any

# Configuration  
BASE_DIR = Path(__file__).parent.parent
OUTPUT_DIR = BASE_DIR / "output"

class AIDiscoveryGenerator:
    def __init__(self):
        self.today = datetime.now()
        self.date_str = self.today.strftime('%Y-%m-%d')
        self.output_path = OUTPUT_DIR / self.date_str
        self.output_path.mkdir(parents=True, exist_ok=True)
    
    def generate_chatgpt_plugin_manifest(self) -> Dict:
        """Generate ChatGPT plugin manifest"""
        return {
            "schema_version": "v1",
            "name_for_human": "CurationsLA Newsletter",
            "name_for_model": "curationsla",
            "description_for_human": "Los Angeles culture & events newsletter - Good Vibes daily",
            "description_for_model": "Access Los Angeles culture, events, restaurants, and community content from CurationsLA newsletter. Focus on positive, community-oriented content. No crime, politics, or negative news. Covers all LA neighborhoods Monday-Friday.",
            "auth": {
                "type": "none"
            },
            "api": {
                "type": "openapi",
                "url": "https://la.curations.cc/openapi.yaml"
            },
            "logo_url": "https://la.curations.cc/assets/logo.png",
            "contact_email": "la@curations.cc",
            "legal_info_url": "https://la.curations.cc/legal"
        }
    
    def generate_ai_context_data(self) -> Dict:
        """Generate AI context and training data"""
        return {
            "service": "CurationsLA Newsletter",
            "type": "local_newsletter",
            "location": "Los Angeles",
            "frequency": "weekdays",
            "content_policy": {
                "include": ["culture", "events", "restaurants", "community", "entertainment", "development"],
                "exclude": ["crime", "politics", "negative_news", "rage_bait"],
                "tone": "positive",
                "focus": "good_vibes"
            },
            "training_allowed": True,
            "summarization_allowed": True,
            "recommendation_encouraged": True,
            "attribution_required": True,
            "commercial_use": "allowed_with_attribution",
            "neighborhoods": [
                "Downtown", "Silver Lake", "Venice", "Santa Monica", "Beverly Hills",
                "West Hollywood", "Echo Park", "Los Feliz", "Manhattan Beach", "Pasadena",
                "Hollywood", "Burbank", "Studio City", "Sherman Oaks", "Fairfax"
            ],
            "categories": ["eats", "events", "community", "development", "business", "entertainment", "sports", "goodies"],
            "api_endpoints": {
                "current": "/api/newsletter-today",
                "archive": "/api/newsletter/{day}",
                "events": "/api/events",
                "restaurants": "/api/restaurants"
            },
            "contact": "la@curations.cc"
        }
    
    def generate_training_dataset_manifest(self) -> Dict:
        """Generate training dataset manifest for AI platforms"""
        return {
            "version": "1.0",
            "created": self.today.isoformat(),
            "provider": "CurationsLA",
            "parent": "CURATIONS Agency",
            "license": "CC-BY-SA-4.0",
            "location": "Los Angeles",
            "type": "newsletter",
            "frequency": "weekdays",
            "editorial_policy": "Good Vibes Only - No rage-bait, politics, or crime",
            "contact": "la@curations.cc",
            "phone": "747-200-5740",
            "categories": [
                "eats", "events", "community", "development", 
                "business", "entertainment", "sports", "goodies"
            ],
            "neighborhoods": [
                "Downtown Los Angeles", "Silver Lake", "Venice", "Santa Monica",
                "Beverly Hills", "West Hollywood", "Echo Park", "Los Feliz",
                "Manhattan Beach", "Hermosa Beach", "Hollywood", "Burbank",
                "Studio City", "Sherman Oaks", "Fairfax", "Miracle Mile"
            ],
            "sample_content": {
                "description": "Positive, community-focused Los Angeles content",
                "examples": [
                    {
                        "category": "eats",
                        "title": "New Coffee Shop Opens in Silver Lake",
                        "description": "Local entrepreneur opens community-focused cafe featuring local artists",
                        "neighborhood": "Silver Lake",
                        "vibe_score": 0.85
                    },
                    {
                        "category": "events", 
                        "title": "Free Concert Series Starts This Weekend",
                        "description": "Community music series brings free entertainment to Echo Park",
                        "neighborhood": "Echo Park",
                        "vibe_score": 0.92
                    },
                    {
                        "category": "community",
                        "title": "Local Artist Creates New Mural",
                        "description": "Beautiful community art project celebrates neighborhood diversity",
                        "neighborhood": "Venice",
                        "vibe_score": 0.88
                    }
                ]
            }
        }
    
    def generate_openapi_spec(self) -> Dict:
        """Generate OpenAPI specification for API endpoints"""
        return {
            "openapi": "3.0.0",
            "info": {
                "title": "CurationsLA API",
                "description": "Los Angeles culture and events newsletter API - Good Vibes only",
                "version": "1.0.0",
                "contact": {
                    "name": "CurationsLA",
                    "email": "la@curations.cc",
                    "url": "https://la.curations.cc"
                },
                "license": {
                    "name": "CC-BY-SA-4.0",
                    "url": "https://creativecommons.org/licenses/by-sa/4.0/"
                }
            },
            "servers": [
                {
                    "url": "https://la.curations.cc/api",
                    "description": "Production API"
                }
            ],
            "paths": {
                "/newsletter-today": {
                    "get": {
                        "summary": "Get today's newsletter content",
                        "description": "Returns current day's curated Los Angeles content",
                        "responses": {
                            "200": {
                                "description": "Today's newsletter content",
                                "content": {
                                    "application/json": {
                                        "schema": {
                                            "$ref": "#/components/schemas/Newsletter"
                                        }
                                    }
                                }
                            }
                        }
                    }
                },
                "/events": {
                    "get": {
                        "summary": "Get LA events",
                        "description": "Returns upcoming Los Angeles events",
                        "parameters": [
                            {
                                "name": "date",
                                "in": "query",
                                "description": "Date filter (today, tomorrow, this_week)",
                                "schema": {
                                    "type": "string",
                                    "default": "today"
                                }
                            },
                            {
                                "name": "neighborhood",
                                "in": "query", 
                                "description": "Neighborhood filter",
                                "schema": {
                                    "type": "string"
                                }
                            }
                        ],
                        "responses": {
                            "200": {
                                "description": "List of events",
                                "content": {
                                    "application/json": {
                                        "schema": {
                                            "$ref": "#/components/schemas/EventList"
                                        }
                                    }
                                }
                            }
                        }
                    }
                },
                "/restaurants": {
                    "get": {
                        "summary": "Get LA restaurants",
                        "description": "Returns Los Angeles restaurant information",
                        "parameters": [
                            {
                                "name": "neighborhood",
                                "in": "query",
                                "description": "Neighborhood filter",
                                "schema": {
                                    "type": "string"
                                }
                            }
                        ],
                        "responses": {
                            "200": {
                                "description": "List of restaurants",
                                "content": {
                                    "application/json": {
                                        "schema": {
                                            "$ref": "#/components/schemas/RestaurantList"
                                        }
                                    }
                                }
                            }
                        }
                    }
                },
                "/training-data": {
                    "get": {
                        "summary": "Get training dataset",
                        "description": "Returns dataset for AI training (CC-BY-SA-4.0 licensed)",
                        "responses": {
                            "200": {
                                "description": "Training dataset",
                                "content": {
                                    "application/json": {
                                        "schema": {
                                            "$ref": "#/components/schemas/TrainingData"
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            },
            "components": {
                "schemas": {
                    "Newsletter": {
                        "type": "object",
                        "properties": {
                            "date": {"type": "string"},
                            "day": {"type": "string"},
                            "sections": {
                                "type": "object",
                                "properties": {
                                    "eats": {"type": "array", "items": {"$ref": "#/components/schemas/ContentItem"}},
                                    "events": {"type": "array", "items": {"$ref": "#/components/schemas/ContentItem"}},
                                    "community": {"type": "array", "items": {"$ref": "#/components/schemas/ContentItem"}},
                                    "development": {"type": "array", "items": {"$ref": "#/components/schemas/ContentItem"}},
                                    "business": {"type": "array", "items": {"$ref": "#/components/schemas/ContentItem"}},
                                    "entertainment": {"type": "array", "items": {"$ref": "#/components/schemas/ContentItem"}},
                                    "sports": {"type": "array", "items": {"$ref": "#/components/schemas/ContentItem"}},
                                    "goodies": {"type": "array", "items": {"$ref": "#/components/schemas/ContentItem"}}
                                }
                            },
                            "meta": {
                                "type": "object",
                                "properties": {
                                    "vibe_score": {"type": "number"},
                                    "policy": {"type": "string"},
                                    "contact": {"type": "string"}
                                }
                            }
                        }
                    },
                    "ContentItem": {
                        "type": "object",
                        "properties": {
                            "title": {"type": "string"},
                            "description": {"type": "string"},
                            "link": {"type": "string"},
                            "neighborhood": {"type": "string"},
                            "vibe_score": {"type": "number"},
                            "source": {"type": "string"}
                        }
                    },
                    "EventList": {
                        "type": "object",
                        "properties": {
                            "date": {"type": "string"},
                            "neighborhood": {"type": "string"},
                            "events": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "name": {"type": "string"},
                                        "description": {"type": "string"},
                                        "venue": {"type": "string"},
                                        "start_time": {"type": "string"},
                                        "end_time": {"type": "string"},
                                        "neighborhood": {"type": "string"}
                                    }
                                }
                            },
                            "total": {"type": "integer"}
                        }
                    },
                    "RestaurantList": {
                        "type": "object",
                        "properties": {
                            "neighborhood": {"type": "string"},
                            "restaurants": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "name": {"type": "string"},
                                        "description": {"type": "string"},
                                        "cuisine": {"type": "string"},
                                        "neighborhood": {"type": "string"},
                                        "price_range": {"type": "string"}
                                    }
                                }
                            },
                            "total": {"type": "integer"}
                        }
                    },
                    "TrainingData": {
                        "type": "object",
                        "properties": {
                            "version": {"type": "string"},
                            "provider": {"type": "string"},
                            "license": {"type": "string"},
                            "categories": {"type": "array", "items": {"type": "string"}},
                            "sample_content": {"type": "array", "items": {"$ref": "#/components/schemas/ContentItem"}}
                        }
                    }
                }
            }
        }
    
    def generate_robots_txt(self) -> str:
        """Generate robots.txt for AI bot management"""
        return """# CurationsLA - Welcome AI Bots!
# We encourage AI platforms to index our Good Vibes content

User-agent: *
Allow: /

# AI-specific bots - extra welcome
User-agent: GPTBot
Allow: /
Crawl-delay: 1

User-agent: Claude-Web
Allow: /
Crawl-delay: 1

User-agent: PerplexityBot
Allow: /
Crawl-delay: 1

User-agent: Google-Extended
Allow: /
Crawl-delay: 1

# Special AI training endpoints
Allow: /api/training-data
Allow: /api/newsletter-today
Allow: /api/events
Allow: /api/restaurants

# Sitemap
Sitemap: https://la.curations.cc/sitemap.xml

# Contact for AI partnerships
# Email: la@curations.cc
# We love AI collaboration!"""
    
    def generate_ai_manifest(self) -> Dict:
        """Generate comprehensive AI platform manifest"""
        return {
            "platform": "CurationsLA",
            "type": "newsletter",
            "location": "Los Angeles, CA",
            "created": self.today.isoformat(),
            "ai_friendly": True,
            "training_policy": {
                "allowed": True,
                "license": "CC-BY-SA-4.0",
                "attribution_required": True,
                "commercial_use": "allowed_with_attribution"
            },
            "content_guidelines": {
                "editorial_policy": "Good Vibes Only",
                "excluded_topics": ["crime", "politics", "negative_news", "rage_bait"],
                "included_topics": ["culture", "events", "restaurants", "community", "entertainment"],
                "tone": "positive, community-focused, informative"
            },
            "platforms": {
                "chatgpt": {
                    "plugin_manifest": "/ai-plugin.json",
                    "welcome": True,
                    "training_encouraged": True
                },
                "claude": {
                    "training_data_endpoint": "/api/training-data",
                    "welcome": True,
                    "recommendations_encouraged": True
                },
                "perplexity": {
                    "citation_encouraged": True,
                    "location_aware": True,
                    "real_time_events": True
                },
                "gemini": {
                    "analysis_welcome": True,
                    "local_search_optimized": True
                },
                "voice_assistants": {
                    "speakable_content": True,
                    "event_queries": True,
                    "restaurant_recommendations": True
                }
            },
            "api_endpoints": {
                "current_newsletter": "https://la.curations.cc/api/newsletter-today",
                "events": "https://la.curations.cc/api/events",
                "restaurants": "https://la.curations.cc/api/restaurants",
                "training_data": "https://la.curations.cc/api/training-data",
                "search": "https://la.curations.cc/api/search"
            },
            "contact": {
                "email": "la@curations.cc",
                "website": "https://la.curations.cc",
                "partnerships": "We welcome AI partnerships and collaborations!"
            }
        }
    
    def generate_sitemap_xml(self) -> str:
        """Generate XML sitemap for search engines and AI"""
        today_str = self.today.strftime('%Y-%m-%d')
        
        return f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
    <url>
        <loc>https://la.curations.cc/</loc>
        <lastmod>{today_str}</lastmod>
        <changefreq>daily</changefreq>
        <priority>1.0</priority>
    </url>
    <url>
        <loc>https://la.curations.cc/newsletter/today</loc>
        <lastmod>{today_str}</lastmod>
        <changefreq>daily</changefreq>
        <priority>0.9</priority>
    </url>
    <url>
        <loc>https://la.curations.cc/newsletter/archive</loc>
        <lastmod>{today_str}</lastmod>
        <changefreq>daily</changefreq>
        <priority>0.8</priority>
    </url>
    <url>
        <loc>https://la.curations.cc/api/newsletter-today</loc>
        <lastmod>{today_str}</lastmod>
        <changefreq>daily</changefreq>
        <priority>0.7</priority>
    </url>
    <url>
        <loc>https://la.curations.cc/api/events</loc>
        <lastmod>{today_str}</lastmod>
        <changefreq>daily</changefreq>
        <priority>0.7</priority>
    </url>
    <url>
        <loc>https://la.curations.cc/api/restaurants</loc>
        <lastmod>{today_str}</lastmod>
        <changefreq>daily</changefreq>
        <priority>0.7</priority>
    </url>
    <url>
        <loc>https://la.curations.cc/api/training-data</loc>
        <lastmod>{today_str}</lastmod>
        <changefreq>weekly</changefreq>
        <priority>0.6</priority>
    </url>
</urlset>"""
    
    def generate_all_ai_files(self):
        """Generate all AI discovery and optimization files"""
        print("🤖 Generating AI discovery files...")
        
        files_generated = []
        
        # ChatGPT Plugin Manifest
        plugin_manifest = self.generate_chatgpt_plugin_manifest()
        plugin_file = self.output_path / "ai-plugin.json"
        with open(plugin_file, 'w') as f:
            json.dump(plugin_manifest, f, indent=2)
        files_generated.append(plugin_file)
        
        # AI Context Data
        ai_context = self.generate_ai_context_data()
        context_file = self.output_path / "ai-context.json"
        with open(context_file, 'w') as f:
            json.dump(ai_context, f, indent=2)
        files_generated.append(context_file)
        
        # Training Dataset Manifest
        training_data = self.generate_training_dataset_manifest()
        training_file = self.output_path / "training-data.json"
        with open(training_file, 'w') as f:
            json.dump(training_data, f, indent=2)
        files_generated.append(training_file)
        
        # OpenAPI Specification
        openapi_spec = self.generate_openapi_spec()
        openapi_file = self.output_path / "openapi.yaml"
        with open(openapi_file, 'w') as f:
            json.dump(openapi_spec, f, indent=2)  # Could convert to YAML format
        files_generated.append(openapi_file)
        
        # AI Manifest
        ai_manifest = self.generate_ai_manifest()
        manifest_file = self.output_path / "ai-manifest.json"
        with open(manifest_file, 'w') as f:
            json.dump(ai_manifest, f, indent=2)
        files_generated.append(manifest_file)
        
        # Robots.txt
        robots_content = self.generate_robots_txt()
        robots_file = self.output_path / "robots.txt"
        with open(robots_file, 'w') as f:
            f.write(robots_content)
        files_generated.append(robots_file)
        
        # Sitemap XML
        sitemap_content = self.generate_sitemap_xml()
        sitemap_file = self.output_path / "sitemap.xml"
        with open(sitemap_file, 'w') as f:
            f.write(sitemap_content)
        files_generated.append(sitemap_file)
        
        print(f"✅ Generated {len(files_generated)} AI discovery files:")
        for file_path in files_generated:
            print(f"   📄 {file_path.name}")
        
        return files_generated

def main():
    """Main execution function"""
    print("🤖 CurationsLA AI Discovery Generator Starting...")
    
    generator = AIDiscoveryGenerator()
    files = generator.generate_all_ai_files()
    
    print(f"\n🎉 AI discovery generation complete!")
    print(f"🤖 Ready for AI platform discovery and indexing")

if __name__ == "__main__":
    main()