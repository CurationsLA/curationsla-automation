
/**
 * CurationsLA Newsletter Content - Friday September 26th, 2025
 * Generated with Good Vibes and Morning Brew style blend
 */

const CurationsLANewsletter = {
    date: '2025-09-26',
    day: 'Friday',
    generated: '2025-09-25T20:30:26.813Z',
    
    // Newsletter Header
    header: {
        greeting: "HEY LOS ANGELES! 🌴",
        tagline: "IT'S FRIDAY - YOUR WEEKLY DOSE OF GOOD VIBES",
        intro: "Welcome to your daily dose of LA's good vibes! We've scoured the city to bring you the best openings, events, and community celebrations happening right now."
    },

    // Content Categories with Hyperlinked Articles
    content: {
  "eats": {
    "category": "EATS",
    "emoji": "🍴",
    "intro": "The food scene is absolutely buzzing right now...",
    "articles": [
      {
        "title": "New Ramen Shop Opens in Silver Lake",
        "blurb": "Good morning, LA legends! 💫 Michelin-trained chef brings authentic tonkotsu to the eastside. This is absolutely obsessed for our fellow angels! 🌟",
        "link": "https://la.eater.com/sample-ramen-silver-lake",
        "source": "LA Eater",
        "neighborhood": "Silver Lake",
        "category": "eats",
        "publishDate": "2025-09-24",
        "hyperlinkHtml": "<a href=\"https://la.eater.com/sample-ramen-silver-lake\" target=\"_blank\" rel=\"noopener noreferrer\">New Ramen Shop Opens in Silver Lake</a>",
        "hyperlinkMarkdown": "[New Ramen Shop Opens in Silver Lake](https://la.eater.com/sample-ramen-silver-lake)"
      },
      {
        "title": "Venice Beach Farmers Market Expands",
        "blurb": "Good morning, LA legends! 💫 More local vendors join the weekly celebration of fresh produce. This is absolutely obsessed for our our people! 🌟",
        "link": "https://laist.com/sample-venice-farmers-market",
        "source": "LAist",
        "neighborhood": "Venice",
        "category": "eats",
        "publishDate": "2025-09-25",
        "hyperlinkHtml": "<a href=\"https://laist.com/sample-venice-farmers-market\" target=\"_blank\" rel=\"noopener noreferrer\">Venice Beach Farmers Market Expands</a>",
        "hyperlinkMarkdown": "[Venice Beach Farmers Market Expands](https://laist.com/sample-venice-farmers-market)"
      }
    ],
    "count": 2
  },
  "events": {
    "category": "EVENTS",
    "emoji": "🎉",
    "intro": "Your social calendar is about to get very full...",
    "articles": [
      {
        "title": "Free Concert Series at Grand Park",
        "blurb": "Rise and grind, Angels! ☀️ Local artists perform every Friday evening through October. This is absolutely obsessed for our neighbors! 🌟",
        "link": "https://www.timeout.com/sample-grand-park-concerts",
        "source": "Time Out LA",
        "neighborhood": "Downtown",
        "category": "events",
        "publishDate": "2025-09-23",
        "hyperlinkHtml": "<a href=\"https://www.timeout.com/sample-grand-park-concerts\" target=\"_blank\" rel=\"noopener noreferrer\">Free Concert Series at Grand Park</a>",
        "hyperlinkMarkdown": "[Free Concert Series at Grand Park](https://www.timeout.com/sample-grand-park-concerts)"
      }
    ],
    "count": 1
  },
  "community": {
    "category": "COMMUNITY",
    "emoji": "🤝",
    "intro": "LA's heart is showing up in the best ways...",
    "articles": [
      {
        "title": "Highland Park Community Garden Ribbon Cutting",
        "blurb": "Good morning, LA legends! 💫 Neighbors transform vacant lot into green oasis for all to enjoy. This is absolutely obsessed for our LA family! 🌟",
        "link": "https://www.theeastsiderla.com/sample-community-garden",
        "source": "The Eastsider LA",
        "neighborhood": "Highland Park",
        "category": "community",
        "publishDate": "2025-09-25",
        "hyperlinkHtml": "<a href=\"https://www.theeastsiderla.com/sample-community-garden\" target=\"_blank\" rel=\"noopener noreferrer\">Highland Park Community Garden Ribbon Cutting</a>",
        "hyperlinkMarkdown": "[Highland Park Community Garden Ribbon Cutting](https://www.theeastsiderla.com/sample-community-garden)"
      }
    ],
    "count": 1
  }
},

    // Utility Functions
    utils: {
        getArticleLink: function(category, index) {
            const article = CurationsLANewsletter.content[category].articles[index];
            return article ? article.link : '#';
        },
        
        getArticleHTML: function(category, index) {
            const article = CurationsLANewsletter.content[category].articles[index];
            return article ? article.hyperlinkHtml : '';
        },
        
        getArticleMarkdown: function(category, index) {
            const article = CurationsLANewsletter.content[category].articles[index];
            return article ? article.hyperlinkMarkdown : '';
        },
        
        getAllLinks: function() {
            const allLinks = [];
            Object.values(CurationsLANewsletter.content).forEach(category => {
                category.articles.forEach(article => {
                    allLinks.push({
                        title: article.title,
                        url: article.link,
                        category: article.category,
                        source: article.source
                    });
                });
            });
            return allLinks;
        }
    },

    // Newsletter Footer
    footer: {
        signature: "Made with 💜 in Los Angeles",
        tagline: "Bringing Good Vibes when our city needs it most",
        contact: {
            email: "la@curations.cc",
            website: "https://la.curations.cc",
            phone: "747-200-5740"
        }
    }
};

// Export for Node.js environments
if (typeof module !== 'undefined' && module.exports) {
    module.exports = CurationsLANewsletter;
}

// Make available globally for browsers
if (typeof window !== 'undefined') {
    window.CurationsLANewsletter = CurationsLANewsletter;
}
