/**
 * CurationsLA Newsletter Content - Friday September 26th, 2025
 * Generated with Good Vibes and Morning Brew style blend
 */

const CurationsLANewsletter = {
    date: '2025-09-26',
    day: 'Friday',
    generated: '2025-09-25T23:25:49.610798',
    
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
    "articles": [
      {
        "title": "LA Food Scene Updates",
        "blurb": "Keep exploring the vibrant culinary landscape of Los Angeles with new restaurant openings and chef collaborations acr... This is total game-changer for our fellow angels! \ud83c\udf1f",
        "link": "https://curationsla.com/food",
        "source": "CurationsLA",
        "neighborhood": "Los Angeles",
        "category": "eats",
        "publishDate": "Fri, 26 Sep 2025 00:00:00 +0000",
        "hyperlinkHtml": "<a href=\"https://curationsla.com/food\" target=\"_blank\" rel=\"noopener noreferrer\">LA Food Scene Updates</a>",
        "hyperlinkMarkdown": "[LA Food Scene Updates](https://curationsla.com/food)"
      }
    ],
    "count": 1
  },
  "events": {
    "category": "EVENTS",
    "emoji": "\ud83c\udf89",
    "intro": "Your social calendar is about to get very full...",
    "articles": [
      {
        "title": "Weekend Events in LA",
        "blurb": "Discover exciting events happening across Los Angeles this weekend, from art galleries to live music venues. This is can't even for our our people! \ud83c\udf1f",
        "link": "https://curationsla.com/events",
        "source": "CurationsLA",
        "neighborhood": "Los Angeles",
        "category": "events",
        "publishDate": "Fri, 26 Sep 2025 00:00:00 +0000",
        "hyperlinkHtml": "<a href=\"https://curationsla.com/events\" target=\"_blank\" rel=\"noopener noreferrer\">Weekend Events in LA</a>",
        "hyperlinkMarkdown": "[Weekend Events in LA](https://curationsla.com/events)"
      }
    ],
    "count": 1
  },
  "community": {
    "category": "COMMUNITY",
    "emoji": "\ud83e\udd1d",
    "intro": "LA's heart is showing up in the best ways...",
    "articles": [
      {
        "title": "LA Community Highlights",
        "blurb": "Celebrating the amazing people and initiatives that make Los Angeles neighborhoods vibrant and connected. This is total game-changer for our fellow angels! \ud83c\udf1f",
        "link": "https://curationsla.com/community",
        "source": "CurationsLA",
        "neighborhood": "Los Angeles",
        "category": "community",
        "publishDate": "Fri, 26 Sep 2025 00:00:00 +0000",
        "hyperlinkHtml": "<a href=\"https://curationsla.com/community\" target=\"_blank\" rel=\"noopener noreferrer\">LA Community Highlights</a>",
        "hyperlinkMarkdown": "[LA Community Highlights](https://curationsla.com/community)"
      }
    ],
    "count": 1
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
    "articles": [
      {
        "title": "LA Business Innovation",
        "blurb": "Local businesses continue to drive innovation and growth across Los Angeles, creating opportunities for our community. This is can't even for our LA family! \ud83c\udf1f",
        "link": "https://curationsla.com/business",
        "source": "CurationsLA",
        "neighborhood": "Los Angeles",
        "category": "business",
        "publishDate": "Fri, 26 Sep 2025 00:00:00 +0000",
        "hyperlinkHtml": "<a href=\"https://curationsla.com/business\" target=\"_blank\" rel=\"noopener noreferrer\">LA Business Innovation</a>",
        "hyperlinkMarkdown": "[LA Business Innovation](https://curationsla.com/business)"
      }
    ],
    "count": 1
  },
  "entertainment": {
    "category": "ENTERTAINMENT",
    "emoji": "\ud83c\udfad",
    "intro": "The creative energy is off the charts...",
    "articles": [
      {
        "title": "Arts & Entertainment in LA",
        "blurb": "From Hollywood premieres to intimate theater performances, LA's entertainment scene continues to inspire and delight. This is total game-changer for our fellow angels! \ud83c\udf1f",
        "link": "https://curationsla.com/entertainment",
        "source": "CurationsLA",
        "neighborhood": "Los Angeles",
        "category": "entertainment",
        "publishDate": "Fri, 26 Sep 2025 00:00:00 +0000",
        "hyperlinkHtml": "<a href=\"https://curationsla.com/entertainment\" target=\"_blank\" rel=\"noopener noreferrer\">Arts & Entertainment in LA</a>",
        "hyperlinkMarkdown": "[Arts & Entertainment in LA](https://curationsla.com/entertainment)"
      }
    ],
    "count": 1
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
