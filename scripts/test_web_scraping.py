#!/usr/bin/env python3
"""
Test Web Scraping Functionality
Tests the web scraper against various LA news sources
"""

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent))

from web_scraper import WebScraper
from content_generator import ContentGenerator
import time

def test_web_scraper():
    """Test web scraper functionality"""
    print("🕷️  Testing CurationsLA Web Scraper...")
    print("=" * 60)
    
    scraper = WebScraper()
    
    # Test sources with different categories
    test_cases = [
        ('laist', 'local', 3),
        ('timeout_la', 'events', 3),
        ('secret_la', 'general', 3),
        ('welikela', 'community', 2),
        ('thrillist_la', 'general', 2)
    ]
    
    total_articles = 0
    successful_sources = 0
    
    for source, category, limit in test_cases:
        print(f"\n🔍 Testing {source} ({category})...")
        try:
            articles = scraper.scrape_content(source, category, limit)
            
            if articles:
                successful_sources += 1
                total_articles += len(articles)
                print(f"✅ Success: {len(articles)} articles found")
                
                # Show first article as example
                if articles:
                    first = articles[0]
                    print(f"   📰 Sample: {first['title'][:50]}...")
                    print(f"   🔗 Link: {first['link']}")
                    print(f"   📝 Description: {first['description'][:80]}...")
            else:
                print(f"⚠️  No articles found for {source}")
                
        except Exception as e:
            print(f"❌ Error testing {source}: {str(e)}")
        
        time.sleep(2)  # Be respectful
    
    print(f"\n📊 Web Scraping Test Results:")
    print(f"   ✅ Successful sources: {successful_sources}/{len(test_cases)}")
    print(f"   📰 Total articles scraped: {total_articles}")
    print(f"   📈 Success rate: {successful_sources/len(test_cases)*100:.1f}%")

def test_content_generator_with_scraping():
    """Test content generator with web scraping fallbacks"""
    print("\n🌴 Testing Content Generator with Web Scraping...")
    print("=" * 60)
    
    generator = ContentGenerator()
    
    # Test one category
    print("\n🍴 Testing EATS category with fallbacks...")
    
    try:
        # This will try RSS first, then fallback to web scraping
        category_content = generator.process_category('eats')
        
        if category_content:
            print(f"✅ Generated {len(category_content)} eats items")
            
            # Show sample
            if category_content:
                sample = category_content[0]
                print(f"   📰 Sample: {sample.get('title', 'No title')[:50]}...")
                print(f"   🔗 Source: {sample.get('source', 'Unknown')}")
        else:
            print("⚠️  No content generated for eats category")
            
    except Exception as e:
        print(f"❌ Error testing content generator: {str(e)}")

def main():
    """Run all tests"""
    print("🧪 CurationsLA Web Scraping Test Suite")
    print("Testing fallback mechanisms for failed RSS feeds")
    print()
    
    # Test 1: Direct web scraper
    test_web_scraper()
    
    # Test 2: Content generator integration
    test_content_generator_with_scraping()
    
    print("\n🎉 Testing complete!")

if __name__ == "__main__":
    main()