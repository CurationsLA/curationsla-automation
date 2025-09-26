#!/usr/bin/env python3
"""
Generate curationsla-master-sept-26th-2025 file
Focuses on Community, Business, Entertainment, and Events/Activities content with CurationsLA + Morning Brew style
"""

import json
import os
from datetime import datetime, timedelta
from pathlib import Path

def load_existing_content():
    """Load existing content from the newsletter files"""
    output_dir = Path(__file__).parent.parent / "output" / "2025-09-26"
    
    # Load from newsletter-content.json if available
    json_file = output_dir / "newsletter-content.json"
    if json_file.exists():
        with open(json_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    return None

def filter_categories(content_data):
    """Filter content for the 4 requested categories plus related ones: Community, Business, Entertainment, Events"""
    # Primary requested categories
    primary_categories = ['community', 'business', 'entertainment', 'events']
    # Additional categories that align with the theme (eats = business/community, development = community/business)
    additional_categories = ['eats', 'development', 'sports', 'goodies']
    
    filtered_content = {}
    
    if content_data and 'content' in content_data:
        # First add primary categories
        for category in primary_categories:
            if category in content_data['content']:
                filtered_content[category] = content_data['content'][category]
        
        # Then add additional categories if we need more sources
        for category in additional_categories:
            if category in content_data['content']:
                filtered_content[category] = content_data['content'][category]
    
    return filtered_content

def format_content_for_master(content_data):
    """Format content into the master file format with condensed paragraphs"""
    
    master_content = f"""# CurationsLA Master - September 26th, 2025

**Local Los Angeles News | Community • Business • Entertainment • Events**

Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Content Freshness: Within 3 days of September 26th, 2025

---

## 🌴 HEY LOS ANGELES! IT'S FRIDAY!

Welcome to your curated dose of LA's good vibes! We've sourced the latest local news across Community, Business, Entertainment, and Events happening right now. From new restaurant openings in Silver Lake to community celebrations in Highland Park, here's what makes LA amazing today.

---

"""

    # Process each category
    category_emojis = {
        'community': '🤝', 
        'business': '💼', 
        'entertainment': '🎭', 
        'events': '📆',
        'eats': '🍴',
        'development': '🏗️',
        'sports': '🏆',
        'goodies': '✨'
    }
    
    category_names = {
        'community': 'COMMUNITY',
        'business': 'BUSINESS', 
        'entertainment': 'ENTERTAINMENT',
        'events': 'EVENTS & ACTIVITIES',
        'eats': 'DINING & CULINARY', 
        'development': 'URBAN DEVELOPMENT',
        'sports': 'SPORTS & RECREATION',
        'goodies': 'HIDDEN GEMS'
    }

    # Primary categories first
    primary_order = ['community', 'business', 'entertainment', 'events']
    additional_order = ['eats', 'development', 'sports', 'goodies']
    
    all_categories = primary_order + [cat for cat in additional_order if cat in content_data]

    for category in all_categories:
        if category not in content_data:
            continue
            
        data = content_data[category]
        if not data.get('articles'):
            continue
            
        emoji = category_emojis.get(category, '📍')
        category_name = category_names.get(category, category.upper())
        
        master_content += f"## {emoji} {category_name}\n\n"
        
        # Add condensed content for each article - limit to get diverse content
        article_limit = min(4, len(data['articles']))  # Up to 4 per category for good balance
        for article in data['articles'][:article_limit]:
            title = article.get('title', '').strip()
            link = article.get('link', '')
            source = article.get('source', 'Unknown')
            neighborhood = article.get('neighborhood', 'LA')
            
            # Create condensed paragraph with CurationsLA + Morning Brew style
            blurb = article.get('blurb', '')
            if len(blurb) > 200:
                # Truncate to first sentence or 200 chars, whichever is shorter
                first_sentence = blurb.split('.')[0]
                if len(first_sentence) < 200:
                    blurb = first_sentence + "."
                else:
                    blurb = blurb[:197] + "..."
            
            master_content += f"**{neighborhood}** | {title}\n\n"
            master_content += f"{blurb}\n\n"
            master_content += f"**Source:** [{source}]({link})\n\n"
            master_content += "---\n\n"
    
    # Add footer
    master_content += """## 🌴 THAT'S A WRAP!

Keep spreading those good vibes, LA! This master file contains curated local news from trusted LA sources, filtered for positive community impact and fresh content within 3 days.

**Content Categories:** Community • Business • Entertainment • Events & Activities  
**Content Sources:** 20+ local LA news outlets and community sources  
**Style:** CurationsLA voice + Morning Brew newsletter format  

*Generated by CurationsLA Automation System*

---
"""

    return master_content

def main():
    """Generate the master file"""
    print("🌴 Generating curationsla-master-sept-26th-2025...")
    
    # Load existing content
    content_data = load_existing_content()
    if not content_data:
        print("❌ No existing content found. Running content generator first...")
        return
    
    # Filter for target categories
    filtered_content = filter_categories(content_data)
    
    if not filtered_content:
        print("❌ No content found for target categories")
        return
    
    print(f"✅ Found content for {len(filtered_content)} categories")
    
    # Format content
    master_content = format_content_for_master(filtered_content)
    
    # Save master file
    output_dir = Path(__file__).parent.parent / "output" / "2025-09-26"
    master_file = output_dir / "curationsla-master-sept-26th-2025.md"
    
    with open(master_file, 'w', encoding='utf-8') as f:
        f.write(master_content)
    
    print(f"✅ Master file created: {master_file}")
    print(f"📊 Content includes:")
    for category, data in filtered_content.items():
        article_count = len(data.get('articles', []))
        print(f"   • {category.upper()}: {min(article_count, 5)} articles")

if __name__ == "__main__":
    main()