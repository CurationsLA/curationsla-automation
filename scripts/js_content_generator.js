#!/usr/bin/env node
/**
 * CurationsLA JavaScript Content Generator
 * Generates newsletter content with hyperlinked articles for Friday September 26th, 2025
 * Blends CurationsLA voice with Morning Brew style
 */

const fs = require('fs');
const path = require('path');

class CurationsLAContentGenerator {
    constructor() {
        this.targetDate = '2025-09-26';
        this.contentData = {};
        this.morningBrewStyle = {
            intro: [
                "What's crackin', LA? 🌴",
                "Rise and grind, Angels! ☀️",
                "Good morning, LA legends! 💫",
                "Hey gorgeous people of LA! ✨"
            ],
            transitions: [
                "But wait, there's more...",
                "Speaking of which...",
                "In other news that'll make you smile...",
                "Plot twist:",
                "Meanwhile, across town..."
            ],
            callouts: [
                "💡 Pro tip:",
                "🔥 Hot take:",
                "📈 Trending up:",
                "✨ Good vibes only:",
                "🎯 Don't miss:"
            ]
        };
        this.curationsLAVoice = {
            enthusiasm: ["absolutely obsessed", "can't even", "total game-changer", "pure magic"],
            community: ["neighbors", "LA family", "our people", "fellow angels"],
            positivity: ["good vibes", "positive energy", "spreading joy", "celebrating wins"]
        };
    }

    generateContentBlurb(article) {
        const morningBrewIntro = this.getRandomElement(this.morningBrewStyle.intro);
        const enthusiasm = this.getRandomElement(this.curationsLAVoice.enthusiasm);
        const community = this.getRandomElement(this.curationsLAVoice.community);
        
        return {
            title: article.title,
            blurb: `${morningBrewIntro} ${article.summary} This is ${enthusiasm} for our ${community}! 🌟`,
            link: article.url,
            source: article.source,
            neighborhood: article.neighborhood || 'LA',
            category: article.category,
            publishDate: article.publishDate,
            hyperlinkHtml: `<a href="${article.url}" target="_blank" rel="noopener noreferrer">${article.title}</a>`,
            hyperlinkMarkdown: `[${article.title}](${article.url})`
        };
    }

    generateCategoryContent(category, articles) {
        const categoryIntro = this.getCategoryIntro(category);
        const processedArticles = articles
            .filter(article => this.isContentFresh(article.publishDate))
            .map(article => this.generateContentBlurb(article));

        return {
            category: category.toUpperCase(),
            emoji: this.getCategoryEmoji(category),
            intro: categoryIntro,
            articles: processedArticles,
            count: processedArticles.length
        };
    }

    getCategoryIntro(category) {
        const intros = {
            eats: "The food scene is absolutely buzzing right now...",
            events: "Your social calendar is about to get very full...",
            community: "LA's heart is showing up in the best ways...",
            development: "The city is transforming before our eyes...",
            business: "Local entrepreneurs are crushing it...",
            entertainment: "The creative energy is off the charts...",
            sports: "Our teams and athletes are bringing the heat...",
            goodies: "Hidden gems and special finds await..."
        };
        return intros[category] || "Amazing things are happening...";
    }

    getCategoryEmoji(category) {
        const emojis = {
            eats: "🍴",
            events: "🎉",
            community: "🤝",
            development: "🏗️",
            business: "💼",
            entertainment: "🎭",
            sports: "🏆",
            goodies: "✨"
        };
        return emojis[category] || "📍";
    }

    isContentFresh(publishDate) {
        const targetDate = new Date('2025-09-25'); // Thursday Sept 25th as reference
        const contentDate = new Date(publishDate);
        const daysDiff = (targetDate - contentDate) / (1000 * 60 * 60 * 24);
        return daysDiff <= 3; // Not outdated by more than 3 days
    }

    getRandomElement(array) {
        return array[Math.floor(Math.random() * array.length)];
    }

    generateNewsletterJS(contentData) {
        const jsContent = `
/**
 * CurationsLA Newsletter Content - Friday September 26th, 2025
 * Generated with Good Vibes and Morning Brew style blend
 */

const CurationsLANewsletter = {
    date: '2025-09-26',
    day: 'Friday',
    generated: '${new Date().toISOString()}',
    
    // Newsletter Header
    header: {
        greeting: "HEY LOS ANGELES! 🌴",
        tagline: "IT'S FRIDAY - YOUR WEEKLY DOSE OF GOOD VIBES",
        intro: "Welcome to your daily dose of LA's good vibes! We've scoured the city to bring you the best openings, events, and community celebrations happening right now."
    },

    // Content Categories with Hyperlinked Articles
    content: ${JSON.stringify(contentData, null, 2)},

    // Utility Functions
    utils: {
        getArticleLink: function(category, index) {
            const article = this.content[category].articles[index];
            return article ? article.link : '#';
        },
        
        getArticleHTML: function(category, index) {
            const article = this.content[category].articles[index];
            return article ? article.hyperlinkHtml : '';
        },
        
        getArticleMarkdown: function(category, index) {
            const article = this.content[category].articles[index];
            return article ? article.hyperlinkMarkdown : '';
        },
        
        getAllLinks: function() {
            const allLinks = [];
            Object.values(this.content).forEach(category => {
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
`;
        return jsContent;
    }

    async generateSampleContent() {
        // Sample content for demonstration - in real implementation, this would come from RSS feeds
        const sampleArticles = {
            eats: [
                {
                    title: "New Ramen Shop Opens in Silver Lake",
                    summary: "Michelin-trained chef brings authentic tonkotsu to the eastside.",
                    url: "https://la.eater.com/sample-ramen-silver-lake",
                    source: "LA Eater",
                    neighborhood: "Silver Lake",
                    category: "eats",
                    publishDate: "2025-09-24"
                },
                {
                    title: "Venice Beach Farmers Market Expands",
                    summary: "More local vendors join the weekly celebration of fresh produce.",
                    url: "https://laist.com/sample-venice-farmers-market",
                    source: "LAist",
                    neighborhood: "Venice",
                    category: "eats",
                    publishDate: "2025-09-25"
                }
            ],
            events: [
                {
                    title: "Free Concert Series at Grand Park",
                    summary: "Local artists perform every Friday evening through October.",
                    url: "https://www.timeout.com/sample-grand-park-concerts",
                    source: "Time Out LA",
                    neighborhood: "Downtown",
                    category: "events",
                    publishDate: "2025-09-23"
                }
            ],
            community: [
                {
                    title: "Highland Park Community Garden Ribbon Cutting",
                    summary: "Neighbors transform vacant lot into green oasis for all to enjoy.",
                    url: "https://www.theeastsiderla.com/sample-community-garden",
                    source: "The Eastsider LA",
                    neighborhood: "Highland Park",
                    category: "community",
                    publishDate: "2025-09-25"
                }
            ]
        };

        const processedContent = {};
        Object.keys(sampleArticles).forEach(category => {
            processedContent[category] = this.generateCategoryContent(category, sampleArticles[category]);
        });

        return processedContent;
    }

    async generateAndSaveContent() {
        console.log('🌴 Generating CurationsLA Newsletter JS Content...');
        
        const contentData = await this.generateSampleContent();
        const jsContent = this.generateNewsletterJS(contentData);
        
        // Create output directory
        const outputDir = path.join(__dirname, '..', 'output', this.targetDate);
        if (!fs.existsSync(outputDir)) {
            fs.mkdirSync(outputDir, { recursive: true });
        }

        // Write JS content file
        const jsFilePath = path.join(outputDir, 'newsletter-content.js');
        fs.writeFileSync(jsFilePath, jsContent);

        // Also create a JSON version for easy parsing
        const jsonFilePath = path.join(outputDir, 'newsletter-content.json');
        fs.writeFileSync(jsonFilePath, JSON.stringify({
            meta: {
                date: this.targetDate,
                generated: new Date().toISOString(),
                style: 'CurationsLA + Morning Brew blend'
            },
            content: contentData
        }, null, 2));

        console.log('✅ JS Content Generated Successfully!');
        console.log(`📄 JavaScript file: ${jsFilePath}`);
        console.log(`📄 JSON file: ${jsonFilePath}`);
        
        return { jsFilePath, jsonFilePath, contentData };
    }
}

// Run if called directly
if (require.main === module) {
    const generator = new CurationsLAContentGenerator();
    generator.generateAndSaveContent()
        .then(() => console.log('🎉 Newsletter content generation complete!'))
        .catch(console.error);
}

module.exports = CurationsLAContentGenerator;