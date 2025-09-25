/**
 * CurationsLA Newsletter Content - Friday September 26th, 2025
 * Generated with Good Vibes and Morning Brew style blend
 */

const CurationsLANewsletter = {
    date: '2025-09-26',
    day: 'Friday',
    generated: '2025-09-25T22:36:53.621911',
    
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
    "emoji": "\ud83c\udf74",
    "intro": "The food scene is absolutely buzzing right now...",
    "articles": [],
    "count": 0
  },
  "events": {
    "category": "EVENTS",
    "emoji": "\ud83c\udf89",
    "intro": "Your social calendar is about to get very full...",
    "articles": [],
    "count": 0
  },
  "community": {
    "category": "COMMUNITY",
    "emoji": "\ud83e\udd1d",
    "intro": "LA's heart is showing up in the best ways...",
    "articles": [],
    "count": 0
  },
  "development": {
    "category": "DEVELOPMENT",
    "emoji": "\ud83c\udfd7\ufe0f",
    "intro": "The city is transforming before our eyes...",
    "articles": [],
    "count": 0
  },
  "business": {
    "category": "BUSINESS",
    "emoji": "\ud83d\udcbc",
    "intro": "Local entrepreneurs are crushing it...",
    "articles": [],
    "count": 0
  },
  "entertainment": {
    "category": "ENTERTAINMENT",
    "emoji": "\ud83c\udfad",
    "intro": "The creative energy is off the charts...",
    "articles": [],
    "count": 0
  },
  "sports": {
    "category": "SPORTS",
    "emoji": "\ud83c\udfc6",
    "intro": "Our teams and athletes are bringing the heat...",
    "articles": [],
    "count": 0
  },
  "goodies": {
    "category": "GOODIES",
    "emoji": "\u2728",
    "intro": "Hidden gems and special finds await...",
    "articles": [],
    "count": 0
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
