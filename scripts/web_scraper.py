#!/usr/bin/env python3
"""
CurationsLA Web Scraper
Web scraping utility to replace failed RSS feeds with direct content extraction
"""

import requests
from bs4 import BeautifulSoup
import time
import random
from datetime import datetime
from typing import Dict, List, Any
import json
import re
from urllib.parse import urljoin, urlparse

class WebScraper:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'CurationsLA/1.0 (Newsletter Aggregator; +https://la.curations.cc)',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        })
        
        # LA-specific content scrapers
        self.scrapers = {
            'laist': self.scrape_laist,
            'laweekly': self.scrape_laweekly,
            'timeout_la': self.scrape_timeout_la,
            'welikela': self.scrape_welikela,
            'thrillist_la': self.scrape_thrillist_la,
            'la_magazine': self.scrape_la_magazine,
            'secret_la': self.scrape_secret_la,
            'discoverla': self.scrape_discoverla,
            'lacanvas': self.scrape_lacanvas,
            'la_downtown_news': self.scrape_la_downtown_news,
        }
    
    def scrape_content(self, source: str, category: str = 'general', limit: int = 10) -> List[Dict]:
        """Main scraping method"""
        if source not in self.scrapers:
            print(f"⚠️  No scraper available for {source}")
            return []
        
        try:
            print(f"🕷️  Scraping {source}...")
            articles = self.scrapers[source](category, limit)
            print(f"✅ Scraped {len(articles)} articles from {source}")
            time.sleep(random.uniform(1, 3))  # Be respectful
            return articles
        except Exception as e:
            print(f"❌ Error scraping {source}: {str(e)}")
            return []
    
    def scrape_laist(self, category: str, limit: int) -> List[Dict]:
        """Scrape LAist content"""
        base_url = "https://laist.com"
        category_urls = {
            'food': '/news/food',
            'events': '/arts-and-entertainment', 
            'local': '/news',
            'general': '/news'
        }
        
        url = f"{base_url}{category_urls.get(category, '/news')}"
        response = self.session.get(url, timeout=30)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        articles = []
        
        # Find article containers
        article_elements = soup.find_all(['article', 'div'], class_=re.compile(r'post|article|story'), limit=limit)
        
        for element in article_elements[:limit]:
            try:
                title_elem = element.find(['h1', 'h2', 'h3'], class_=re.compile(r'title|headline'))
                link_elem = element.find('a', href=True)
                excerpt_elem = element.find(['p', 'div'], class_=re.compile(r'excerpt|summary|description'))
                
                if title_elem and link_elem:
                    article = {
                        'title': title_elem.get_text(strip=True),
                        'link': urljoin(base_url, link_elem['href']),
                        'description': excerpt_elem.get_text(strip=True) if excerpt_elem else '',
                        'published': datetime.now().isoformat(),
                        'source': 'LAist',
                        'category': category
                    }
                    articles.append(article)
            except Exception as e:
                continue
        
        return articles
    
    def scrape_laweekly(self, category: str, limit: int) -> List[Dict]:
        """Scrape LA Weekly content"""
        base_url = "https://www.laweekly.com"
        category_urls = {
            'food': '/restaurants',
            'events': '/music',
            'arts': '/arts',
            'general': '/news'
        }
        
        url = f"{base_url}{category_urls.get(category, '/news')}"
        response = self.session.get(url, timeout=30)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        articles = []
        
        article_elements = soup.find_all(['article', 'div'], class_=re.compile(r'post|story|article'), limit=limit)
        
        for element in article_elements[:limit]:
            try:
                title_elem = element.find(['h1', 'h2', 'h3'])
                link_elem = element.find('a', href=True)
                excerpt_elem = element.find(['p', 'div'], class_=re.compile(r'excerpt|summary'))
                
                if title_elem and link_elem:
                    article = {
                        'title': title_elem.get_text(strip=True),
                        'link': urljoin(base_url, link_elem['href']),
                        'description': excerpt_elem.get_text(strip=True) if excerpt_elem else '',
                        'published': datetime.now().isoformat(),
                        'source': 'LA Weekly',
                        'category': category
                    }
                    articles.append(article)
            except Exception as e:
                continue
        
        return articles
    
    def scrape_timeout_la(self, category: str, limit: int) -> List[Dict]:
        """Scrape Time Out LA content"""
        base_url = "https://www.timeout.com/los-angeles"
        category_urls = {
            'food': '/restaurants',
            'events': '/things-to-do',
            'nightlife': '/nightlife',
            'general': '/things-to-do'
        }
        
        url = f"{base_url}{category_urls.get(category, '/things-to-do')}"
        response = self.session.get(url, timeout=30)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        articles = []
        
        article_elements = soup.find_all(['div', 'article'], class_=re.compile(r'card|item|feature'), limit=limit)
        
        for element in article_elements[:limit]:
            try:
                title_elem = element.find(['h1', 'h2', 'h3', 'h4'])
                link_elem = element.find('a', href=True)
                excerpt_elem = element.find('p')
                
                if title_elem and link_elem:
                    article = {
                        'title': title_elem.get_text(strip=True),
                        'link': urljoin(base_url, link_elem['href']),
                        'description': excerpt_elem.get_text(strip=True) if excerpt_elem else '',
                        'published': datetime.now().isoformat(),
                        'source': 'Time Out LA',
                        'category': category
                    }
                    articles.append(article)
            except Exception as e:
                continue
        
        return articles
    
    def scrape_welikela(self, category: str, limit: int) -> List[Dict]:
        """Scrape We Like LA content"""
        base_url = "https://welikela.com"
        category_urls = {
            'food': '/category/food-drink',
            'events': '/category/events-entertainment', 
            'community': '/category/community',
            'general': '/'
        }
        
        url = f"{base_url}{category_urls.get(category, '/')}"
        response = self.session.get(url, timeout=30)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        articles = []
        
        article_elements = soup.find_all(['article', 'div'], class_=re.compile(r'post|entry'), limit=limit)
        
        for element in article_elements[:limit]:
            try:
                title_elem = element.find(['h1', 'h2', 'h3'])
                link_elem = element.find('a', href=True)
                excerpt_elem = element.find(['div', 'p'], class_=re.compile(r'excerpt|content'))
                
                if title_elem and link_elem:
                    article = {
                        'title': title_elem.get_text(strip=True),
                        'link': urljoin(base_url, link_elem['href']),
                        'description': excerpt_elem.get_text(strip=True) if excerpt_elem else '',
                        'published': datetime.now().isoformat(),
                        'source': 'We Like LA',
                        'category': category
                    }
                    articles.append(article)
            except Exception as e:
                continue
        
        return articles
    
    def scrape_thrillist_la(self, category: str, limit: int) -> List[Dict]:
        """Scrape Thrillist LA content"""
        base_url = "https://www.thrillist.com/los-angeles"
        response = self.session.get(base_url, timeout=30)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        articles = []
        
        article_elements = soup.find_all(['div', 'article'], class_=re.compile(r'card|story|post'), limit=limit)
        
        for element in article_elements[:limit]:
            try:
                title_elem = element.find(['h1', 'h2', 'h3'])
                link_elem = element.find('a', href=True)
                excerpt_elem = element.find('p')
                
                if title_elem and link_elem:
                    article = {
                        'title': title_elem.get_text(strip=True),
                        'link': urljoin('https://www.thrillist.com', link_elem['href']),
                        'description': excerpt_elem.get_text(strip=True) if excerpt_elem else '',
                        'published': datetime.now().isoformat(),
                        'source': 'Thrillist LA',
                        'category': category
                    }
                    articles.append(article)
            except Exception as e:
                continue
        
        return articles
    
    def scrape_la_magazine(self, category: str, limit: int) -> List[Dict]:
        """Scrape LA Magazine content"""
        base_url = "https://lamag.com"
        category_urls = {
            'food': '/category/food-drink',
            'events': '/category/arts-entertainment',
            'general': '/'
        }
        
        url = f"{base_url}{category_urls.get(category, '/')}"
        response = self.session.get(url, timeout=30)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        articles = []
        
        article_elements = soup.find_all(['article', 'div'], class_=re.compile(r'post|story'), limit=limit)
        
        for element in article_elements[:limit]:
            try:
                title_elem = element.find(['h1', 'h2', 'h3'])
                link_elem = element.find('a', href=True)
                excerpt_elem = element.find(['p', 'div'], class_=re.compile(r'excerpt|summary'))
                
                if title_elem and link_elem:
                    article = {
                        'title': title_elem.get_text(strip=True),
                        'link': urljoin(base_url, link_elem['href']),
                        'description': excerpt_elem.get_text(strip=True) if excerpt_elem else '',
                        'published': datetime.now().isoformat(),
                        'source': 'LA Magazine',
                        'category': category
                    }
                    articles.append(article)
            except Exception as e:
                continue
        
        return articles
    
    def scrape_secret_la(self, category: str, limit: int) -> List[Dict]:
        """Scrape Secret Los Angeles content"""
        base_url = "https://secretlosangeles.com"
        response = self.session.get(base_url, timeout=30)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        articles = []
        
        article_elements = soup.find_all(['div', 'article'], class_=re.compile(r'post|article|card'), limit=limit)
        
        for element in article_elements[:limit]:
            try:
                title_elem = element.find(['h1', 'h2', 'h3'])
                link_elem = element.find('a', href=True)
                excerpt_elem = element.find('p')
                
                if title_elem and link_elem:
                    article = {
                        'title': title_elem.get_text(strip=True),
                        'link': urljoin(base_url, link_elem['href']),
                        'description': excerpt_elem.get_text(strip=True) if excerpt_elem else '',
                        'published': datetime.now().isoformat(),
                        'source': 'Secret Los Angeles',
                        'category': category
                    }
                    articles.append(article)
            except Exception as e:
                continue
        
        return articles
    
    def scrape_discoverla(self, category: str, limit: int) -> List[Dict]:
        """Scrape Discover LA content"""
        base_url = "https://www.discoverlosangeles.com"
        response = self.session.get(base_url, timeout=30)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        articles = []
        
        article_elements = soup.find_all(['div', 'article'], class_=re.compile(r'card|feature|listing'), limit=limit)
        
        for element in article_elements[:limit]:
            try:
                title_elem = element.find(['h1', 'h2', 'h3', 'h4'])
                link_elem = element.find('a', href=True)
                excerpt_elem = element.find('p')
                
                if title_elem and link_elem:
                    article = {
                        'title': title_elem.get_text(strip=True),
                        'link': urljoin(base_url, link_elem['href']),
                        'description': excerpt_elem.get_text(strip=True) if excerpt_elem else '',
                        'published': datetime.now().isoformat(),
                        'source': 'Discover LA',
                        'category': category
                    }
                    articles.append(article)
            except Exception as e:
                continue
        
        return articles
    
    def scrape_lacanvas(self, category: str, limit: int) -> List[Dict]:
        """Scrape LA Canvas content (if accessible)"""
        # This might have SSL issues, so we'll try with verify=False as fallback
        try:
            base_url = "https://lacanvas.com"
            response = self.session.get(base_url, timeout=30, verify=False)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            articles = []
            
            article_elements = soup.find_all(['div', 'article'], class_=re.compile(r'post|event|story'), limit=limit)
            
            for element in article_elements[:limit]:
                try:
                    title_elem = element.find(['h1', 'h2', 'h3'])
                    link_elem = element.find('a', href=True)
                    excerpt_elem = element.find('p')
                    
                    if title_elem and link_elem:
                        article = {
                            'title': title_elem.get_text(strip=True),
                            'link': urljoin(base_url, link_elem['href']),
                            'description': excerpt_elem.get_text(strip=True) if excerpt_elem else '',
                            'published': datetime.now().isoformat(),
                            'source': 'LA Canvas',
                            'category': category
                        }
                        articles.append(article)
                except Exception as e:
                    continue
            
            return articles
        except Exception as e:
            print(f"⚠️  LA Canvas not accessible: {str(e)}")
            return []
    
    def scrape_la_downtown_news(self, category: str, limit: int) -> List[Dict]:
        """Scrape LA Downtown News content"""
        base_url = "https://www.ladowntownnews.com"
        response = self.session.get(base_url, timeout=30)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        articles = []
        
        article_elements = soup.find_all(['div', 'article'], class_=re.compile(r'story|post|article'), limit=limit)
        
        for element in article_elements[:limit]:
            try:
                title_elem = element.find(['h1', 'h2', 'h3'])
                link_elem = element.find('a', href=True)
                excerpt_elem = element.find('p')
                
                if title_elem and link_elem:
                    article = {
                        'title': title_elem.get_text(strip=True),
                        'link': urljoin(base_url, link_elem['href']),
                        'description': excerpt_elem.get_text(strip=True) if excerpt_elem else '',
                        'published': datetime.now().isoformat(),
                        'source': 'LA Downtown News',
                        'category': category
                    }
                    articles.append(article)
            except Exception as e:
                continue
        
        return articles

def main():
    """Test the web scraper"""
    scraper = WebScraper()
    
    # Test a few sources
    test_sources = ['laist', 'secret_la', 'timeout_la']
    
    for source in test_sources:
        print(f"\n🕷️  Testing {source}...")
        articles = scraper.scrape_content(source, 'general', 5)
        
        for article in articles:
            print(f"   📰 {article['title'][:60]}...")
            print(f"   🔗 {article['link']}")

if __name__ == "__main__":
    main()