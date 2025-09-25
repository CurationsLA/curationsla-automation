#!/usr/bin/env python3
"""
CurationsLA Good Vibes Filter
Filters content to maintain positive, community-focused newsletter tone
"""

import re
from typing import List, Dict, Tuple

# Positive keywords that boost Good Vibes score
GOOD_VIBES_KEYWORDS = [
    # Openings & Launches
    'opening', 'launch', 'debut', 'premiere', 'unveiling', 'grand opening',
    'soft opening', 'ribbon cutting', 'new', 'introducing', 'announcing',
    
    # Community & Celebration
    'community', 'celebrate', 'celebration', 'festival', 'party', 'gathering',
    'reunion', 'anniversary', 'milestone', 'achievement', 'success', 'winner',
    'award', 'recognition', 'honor', 'tribute',
    
    # Culture & Arts
    'art', 'artist', 'exhibition', 'gallery', 'museum', 'performance',
    'concert', 'music', 'theater', 'dance', 'creative', 'culture',
    'mural', 'installation', 'sculpture', 'painting',
    
    # Food & Dining
    'restaurant', 'cafe', 'coffee', 'food', 'chef', 'menu', 'dining',
    'brewery', 'bar', 'cocktail', 'wine', 'brunch', 'dinner', 'lunch',
    'farmers market', 'food truck', 'bakery', 'dessert',
    
    # Business & Innovation
    'expansion', 'growth', 'innovation', 'collaboration', 'partnership',
    'investment', 'funding', 'startup', 'entrepreneur', 'business',
    'hiring', 'jobs', 'opportunity', 'development',
    
    # Positive Activities
    'free', 'family-friendly', 'outdoor', 'fun', 'exciting', 'amazing',
    'beautiful', 'stunning', 'gorgeous', 'incredible', 'wonderful',
    'fantastic', 'awesome', 'brilliant', 'inspiring', 'uplifting',
    
    # Community Improvement
    'renovation', 'restoration', 'improvement', 'upgrade', 'modernization',
    'beautification', 'revitalization', 'transformation', 'enhancement',
    'sustainability', 'green', 'eco-friendly', 'renewable'
]

# Negative keywords that reduce Good Vibes score or block content
BLOCKED_KEYWORDS = [
    # Crime & Violence
    'murder', 'shooting', 'stabbing', 'robbery', 'theft', 'burglary',
    'assault', 'attack', 'violence', 'crime', 'criminal', 'arrest',
    'police', 'investigation', 'suspect', 'victim', 'death', 'killed',
    'injured', 'hospital', 'emergency',
    
    # Politics & Controversy
    'political', 'politics', 'election', 'candidate', 'voting', 'ballot',
    'republican', 'democrat', 'conservative', 'liberal', 'government',
    'city council', 'mayor', 'congressman', 'senator', 'governor',
    'protest', 'rally', 'demonstration', 'activist', 'activism',
    
    # Legal & Financial Problems
    'lawsuit', 'legal', 'court', 'judge', 'trial', 'settlement',
    'bankruptcy', 'foreclosure', 'eviction', 'closure', 'closing',
    'layoffs', 'fired', 'terminated', 'downsizing', 'cuts', 'losses',
    'debt', 'financial trouble', 'scandal', 'fraud', 'corruption',
    
    # Controversy & Conflict
    'controversy', 'controversial', 'outrage', 'angry', 'anger',
    'upset', 'furious', 'complaint', 'complain', 'criticism', 'critic',
    'oppose', 'opposition', 'against', 'conflict', 'dispute', 'fight',
    'argument', 'disagreement', 'tension', 'divided',
    
    # Negative Business
    'decline', 'decrease', 'drop', 'fall', 'plummet', 'crash',
    'fail', 'failure', 'struggling', 'problem', 'issue', 'concern',
    'worry', 'fear', 'threat', 'danger', 'risk', 'warning'
]

# Neighborhood name patterns for LA
LA_NEIGHBORHOODS = {
    'downtown': ['downtown', 'dtla', 'downtown la', 'downtown los angeles', 'arts district', 'little tokyo', 'chinatown'],
    'westside': ['westside', 'santa monica', 'venice', 'brentwood', 'west la', 'west los angeles', 'mar vista', 'palms'],
    'valley': ['valley', 'san fernando valley', 'studio city', 'sherman oaks', 'burbank', 'north hollywood', 'van nuys', 'encino'],
    'eastside': ['eastside', 'silver lake', 'echo park', 'los feliz', 'highland park', 'eagle rock', 'mount washington'],
    'south_bay': ['south bay', 'manhattan beach', 'hermosa beach', 'redondo beach', 'el segundo', 'torrance'],
    'hollywood': ['hollywood', 'west hollywood', 'weho', 'hollywood hills', 'sunset strip', 'melrose'],
    'mid_city': ['mid city', 'beverly hills', 'fairfax', 'miracle mile', 'mid-wilshire', 'koreatown', 'pico-robertson'],
    'pasadena': ['pasadena', 'south pasadena', 'altadena', 'san marino', 'alhambra'],
    'beaches': ['manhattan beach', 'hermosa beach', 'redondo beach', 'el segundo', 'playa del rey']
}

class GoodVibesFilter:
    def __init__(self, threshold: float = 0.3):
        """
        Initialize Good Vibes Filter
        
        Args:
            threshold: Minimum vibe score (0-1) for content to pass filter
        """
        self.threshold = threshold
        self.good_keywords = set(keyword.lower() for keyword in GOOD_VIBES_KEYWORDS)
        self.blocked_keywords = set(keyword.lower() for keyword in BLOCKED_KEYWORDS)
    
    def calculate_vibe_score(self, text: str) -> float:
        """
        Calculate Good Vibes score for text content
        
        Args:
            text: Content to analyze
            
        Returns:
            float: Vibe score between 0 (bad vibes) and 1 (good vibes)
        """
        if not text:
            return 0.0
        
        text_lower = text.lower()
        
        # Count positive keywords
        good_score = 0
        for keyword in self.good_keywords:
            if keyword in text_lower:
                good_score += 1
        
        # Count negative keywords (weighted more heavily)
        bad_score = 0
        for keyword in self.blocked_keywords:
            if keyword in text_lower:
                bad_score += 2  # Negative keywords have more impact
        
        # Calculate final score
        net_score = good_score - bad_score
        
        # Normalize to 0-1 scale
        # Add baseline of 5 to prevent completely neutral content from scoring 0
        normalized_score = max(0, min(1, (net_score + 5) / 10))
        
        return normalized_score
    
    def extract_neighborhood(self, text: str) -> str:
        """
        Extract Los Angeles neighborhood from text
        
        Args:
            text: Content to analyze
            
        Returns:
            str: Neighborhood name or "Los Angeles" as fallback
        """
        text_lower = text.lower()
        
        # Check for neighborhood mentions
        for area, neighborhoods in LA_NEIGHBORHOODS.items():
            for neighborhood in neighborhoods:
                if neighborhood in text_lower:
                    # Return properly capitalized neighborhood name
                    return neighborhood.title()
        
        # Default fallback
        return "Los Angeles"
    
    def is_good_vibes(self, text: str) -> bool:
        """
        Check if content meets Good Vibes standards
        
        Args:
            text: Content to check
            
        Returns:
            bool: True if content passes Good Vibes filter
        """
        vibe_score = self.calculate_vibe_score(text)
        return vibe_score >= self.threshold
    
    def filter_content_list(self, items: List[Dict]) -> List[Dict]:
        """
        Filter list of content items for Good Vibes
        
        Args:
            items: List of content dictionaries with 'title' and 'description' keys
            
        Returns:
            List[Dict]: Filtered items with added vibe_score and neighborhood
        """
        filtered_items = []
        
        for item in items:
            # Combine title and description for analysis
            full_text = f"{item.get('title', '')} {item.get('description', '')}"
            
            # Calculate vibe score
            vibe_score = self.calculate_vibe_score(full_text)
            
            # Only include items that meet threshold
            if vibe_score >= self.threshold:
                # Add metadata
                item['vibe_score'] = round(vibe_score, 3)
                item['neighborhood'] = self.extract_neighborhood(full_text)
                item['is_good_vibes'] = True
                
                filtered_items.append(item)
        
        # Sort by vibe score (highest first)
        filtered_items.sort(key=lambda x: x['vibe_score'], reverse=True)
        
        return filtered_items
    
    def analyze_content(self, text: str) -> Dict:
        """
        Comprehensive analysis of content
        
        Args:
            text: Content to analyze
            
        Returns:
            Dict: Analysis results including score, neighborhood, keywords found
        """
        text_lower = text.lower()
        
        # Find positive keywords
        good_keywords_found = [kw for kw in self.good_keywords if kw in text_lower]
        
        # Find negative keywords
        bad_keywords_found = [kw for kw in self.blocked_keywords if kw in text_lower]
        
        # Calculate score
        vibe_score = self.calculate_vibe_score(text)
        
        # Extract neighborhood
        neighborhood = self.extract_neighborhood(text)
        
        return {
            'vibe_score': round(vibe_score, 3),
            'passes_filter': vibe_score >= self.threshold,
            'neighborhood': neighborhood,
            'good_keywords_found': good_keywords_found,
            'bad_keywords_found': bad_keywords_found,
            'good_keyword_count': len(good_keywords_found),
            'bad_keyword_count': len(bad_keywords_found),
            'text_length': len(text),
            'analysis_timestamp': None  # Could add timestamp if needed
        }
    
    def get_filter_stats(self) -> Dict:
        """
        Get statistics about the filter configuration
        
        Returns:
            Dict: Filter statistics
        """
        return {
            'threshold': self.threshold,
            'good_keywords_count': len(self.good_keywords),
            'blocked_keywords_count': len(self.blocked_keywords),
            'neighborhoods_tracked': len(LA_NEIGHBORHOODS),
            'total_neighborhood_variations': sum(len(neighs) for neighs in LA_NEIGHBORHOODS.values())
        }

# Convenience functions for direct use
def filter_good_vibes(items: List[Dict], threshold: float = 0.3) -> List[Dict]:
    """
    Convenience function to filter items for Good Vibes
    
    Args:
        items: List of content items to filter
        threshold: Minimum vibe score threshold
        
    Returns:
        List[Dict]: Filtered items
    """
    filter_instance = GoodVibesFilter(threshold)
    return filter_instance.filter_content_list(items)

def calculate_vibe_score(text: str) -> float:
    """
    Convenience function to calculate vibe score
    
    Args:
        text: Content to score
        
    Returns:
        float: Vibe score (0-1)
    """
    filter_instance = GoodVibesFilter()
    return filter_instance.calculate_vibe_score(text)

def is_good_vibes(text: str, threshold: float = 0.3) -> bool:
    """
    Convenience function to check if content is Good Vibes
    
    Args:
        text: Content to check
        threshold: Minimum score threshold
        
    Returns:
        bool: True if content passes filter
    """
    filter_instance = GoodVibesFilter(threshold)
    return filter_instance.is_good_vibes(text)

if __name__ == "__main__":
    # Test the filter
    test_content = [
        {
            'title': 'New Restaurant Opens in Silver Lake',
            'description': 'A beautiful new cafe featuring local artists and community events opens this weekend.'
        },
        {
            'title': 'Crime Wave Hits Downtown',
            'description': 'Police investigate series of robberies and violent incidents in the area.'
        },
        {
            'title': 'Art Festival Celebrates Community',
            'description': 'Local artists come together for a wonderful celebration of creativity and culture.'
        }
    ]
    
    print("🌴 Testing Good Vibes Filter...")
    
    filter_instance = GoodVibesFilter()
    filtered_items = filter_instance.filter_content_list(test_content)
    
    print(f"\nOriginal items: {len(test_content)}")
    print(f"Good Vibes items: {len(filtered_items)}")
    
    for item in filtered_items:
        print(f"\n✅ {item['title']}")
        print(f"   Vibe Score: {item['vibe_score']}")
        print(f"   Neighborhood: {item['neighborhood']}")