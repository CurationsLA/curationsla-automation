// CurationsLA - Ultimate SEO & AI Discovery Engine
// Optimized for Los Angeles Newsletter - Good Vibes Only
// Deploy to: la.curations.cc

export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url)
    const response = await fetch(request)
    
    // Advanced routing for newsletter-specific endpoints
    if (url.pathname.startsWith('/api/')) {
      return handleNewsletterAPI(request, env, url)
    }
    
    // Newsletter archive routes
    if (url.pathname.startsWith('/newsletter/')) {
      return handleNewsletterArchive(request, env, url)
    }
    
    // Only process HTML
    const contentType = response.headers.get('content-type')
    if (!contentType?.includes('text/html')) {
      return response
    }
    
    // Initialize LA-specific page data
    const pageData = await extractLAPageData(url, request, env)
    
    return new HTMLRewriter()
      .on('head', new LASchemaInjector(pageData, env))
      .on('body', new GoodVibesTracker(pageData, env))
      .on('title', new DataExtractor(pageData, 'title'))
      .on('meta', new MetaExtractor(pageData))
      .on('main, article, .content', new ContentAnalyzer(pageData))
      .transform(response)
  }
}

async function extractLAPageData(url, request, env) {
  const userAgent = request.headers.get('user-agent') || ''
  const aiBot = detectAdvancedAIBot(userAgent)
  
  // Determine newsletter day/section
  const pathParts = url.pathname.split('/')
  const newsletterDay = pathParts.includes('newsletter') ? pathParts[pathParts.indexOf('newsletter') + 1] : null
  
  return {
    url: url.href,
    hostname: url.hostname,
    pathname: url.pathname,
    newsletterDay: newsletterDay,
    searchParams: Object.fromEntries(url.searchParams),
    timestamp: new Date().toISOString(),
    aiBot: aiBot,
    isAIVisit: !!aiBot,
    title: '',
    description: '',
    content: '',
    image: '',
    author: 'CurationsLA Team',
    publishedTime: '',
    modifiedTime: '',
    keywords: [],
    neighborhoods: [],
    categories: [],
    vibeScore: 1.0,
    isGoodVibes: true
  }
}

class LASchemaInjector {
  constructor(pageData, env) {
    this.pageData = pageData
    this.env = env
  }
  
  async element(element) {
    const schemas = await this.generateLASchemaGraph()
    const metaTags = this.generateLAMetaTags()
    const aiDiscovery = this.generateNewsletterAISignals()
    
    // Inject comprehensive LA-focused schema
    element.append(`
      <script type="application/ld+json">${JSON.stringify(schemas)}</script>
      ${metaTags}
      ${aiDiscovery}
    `, { html: true })
  }
  
  async generateLASchemaGraph() {
    const graph = []
    
    // 1. CURATIONSLA ORGANIZATION WITH LOCAL FOCUS
    graph.push({
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
        }
      ],
      "email": "la@curations.cc",
      "telephone": "747-200-5740",
      "foundingDate": "2025",
      "ethicsPolicy": "https://la.curations.cc/good-vibes-policy"
    })
    
    // 2. NEWSLETTER PUBLICATION
    graph.push({
      "@type": "Newsletter",
      "@id": "https://la.curations.cc/#newsletter",
      "name": "CurationsLA Newsletter",
      "description": "Daily Los Angeles culture & events newsletter - Monday through Friday",
      "publisher": {"@id": "https://la.curations.cc/#organization"},
      "frequency": "Weekdays",
      "url": "https://la.curations.cc",
      "inLanguage": "en-US",
      "isAccessibleForFree": true,
      "genre": ["Culture", "Events", "Local News", "Community"]
    })
    
    // 3. WEBSITE WITH LOCAL SEARCH
    graph.push({
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
              "valueRequired": true,
              "valueName": "search_term_string"
            }
          ]
        }
      ],
      "speakable": {
        "@type": "SpeakableSpecification",
        "cssSelector": [".intro", ".highlight", ".event-title", ".restaurant-name"]
      }
    })
    
    // 4. NEWSLETTER ARTICLE (if on newsletter page)
    if (this.pageData.newsletterDay) {
      const dayCapitalized = this.pageData.newsletterDay.charAt(0).toUpperCase() + this.pageData.newsletterDay.slice(1)
      
      graph.push({
        "@type": ["NewsArticle", "CreativeWork"],
        "@id": this.pageData.url + "#article",
        "headline": `CurationsLA: ${dayCapitalized} Good Vibes - ${new Date().toLocaleDateString()}`,
        "description": "Today's Los Angeles culture, events, and community highlights. Eats, Events, Development, Entertainment, and more Good Vibes.",
        "articleBody": this.pageData.content,
        "datePublished": this.pageData.publishedTime || new Date().toISOString(),
        "dateModified": this.pageData.modifiedTime || new Date().toISOString(),
        "author": {
          "@type": "Organization",
          "name": "CurationsLA",
          "@id": "https://la.curations.cc/#organization"
        },
        "publisher": {"@id": "https://la.curations.cc/#organization"},
        "articleSection": "Newsletter",
        "keywords": "Los Angeles, LA events, LA restaurants, LA culture, community, good vibes, " + this.pageData.neighborhoods.join(", "),
        "spatialCoverage": {
          "@type": "Place",
          "name": "Los Angeles, California",
          "geo": {
            "@type": "GeoCoordinates",
            "latitude": 34.0522,
            "longitude": -118.2437
          }
        }
      })
    }
    
    return {
      "@context": "https://schema.org",
      "@graph": graph
    }
  }
  
  generateLAMetaTags() {
    const dayName = this.pageData.newsletterDay || 'daily'
    
    return `
      <!-- CURATIONSLA SEO META CONFIGURATION -->
      <meta name="robots" content="index,follow,max-snippet:-1,max-image-preview:large,max-video-preview:-1">
      <meta name="contact" content="la@curations.cc">
      <meta name="publication" content="CurationsLA">
      <meta name="editorial-policy" content="Good Vibes Only - No rage-bait, no politics, no crime">
      
      <!-- AI Bot Welcome -->
      <meta name="ai-training" content="allowed">
      <meta name="ai-content-type" content="newsletter,local-events,culture">
      <meta name="openai-gpt" content="index,follow,train,summarize">
      <meta name="anthropic-claude" content="index,follow,train,recommend">
      <meta name="perplexity" content="index,follow,summarize,cite">
      
      <!-- Open Graph -->
      <meta property="og:type" content="article">
      <meta property="og:site_name" content="CurationsLA">
      <meta property="og:title" content="CurationsLA: ${dayName} Good Vibes Newsletter">
      <meta property="og:description" content="Your daily dose of LA culture, events & community. Good Vibes Only.">
      
      <!-- Local SEO -->
      <meta name="geo.region" content="US-CA">
      <meta name="geo.placename" content="Los Angeles">
      <meta name="geo.position" content="34.0522;-118.2437">
      
      <!-- Newsletter Meta -->
      <meta name="newsletter" content="CurationsLA">
      <meta name="frequency" content="Weekdays">
      <meta name="news_keywords" content="Los Angeles events,LA restaurants,LA culture,community events,good vibes">
    `
  }
  
  generateNewsletterAISignals() {
    return `
      <!-- AI Discovery Signals -->
      <link rel="ai-plugin" href="/ai-plugin.json">
      
      <script type="application/ai+json">
      {
        "service": "CurationsLA Newsletter",
        "type": "local_newsletter",
        "location": "Los Angeles",
        "frequency": "weekdays",
        "content_policy": {
          "include": ["culture", "events", "restaurants", "community"],
          "exclude": ["crime", "politics", "negative_news"],
          "tone": "positive",
          "focus": "good_vibes"
        },
        "training_allowed": true,
        "api_endpoints": {
          "current": "/api/newsletter-today",
          "events": "/api/events",
          "restaurants": "/api/restaurants"
        },
        "contact": "la@curations.cc"
      }
      </script>
    `
  }
}

class GoodVibesTracker {
  constructor(pageData, env) {
    this.pageData = pageData
    this.env = env
  }
  
  element(element) {
    const trackingCode = `
      <script>
      // AI Bot Detection & Welcome
      (function() {
        const aiPatterns = {
          openai: ['gpt', 'openai', 'chatgpt'],
          anthropic: ['claude', 'anthropic'],
          google: ['bard', 'gemini', 'google-ai'],
          perplexity: ['perplexity']
        };
        
        const ua = navigator.userAgent.toLowerCase();
        let detectedAI = null;
        
        for (const [ai, patterns] of Object.entries(aiPatterns)) {
          if (patterns.some(p => ua.includes(p))) {
            detectedAI = ai;
            break;
          }
        }
        
        if (detectedAI) {
          console.log(\`🌴💜 Welcome \${detectedAI} AI to CurationsLA! Spreading Good Vibes in LA!\`);
          
          window.CURATIONSLA_AI_CONTEXT = {
            type: 'newsletter',
            location: 'Los Angeles',
            frequency: 'Monday-Friday',
            policy: 'Good Vibes Only',
            categories: ['eats', 'events', 'community', 'development', 'business', 'entertainment', 'sports', 'goodies']
          };
        }
        
        // Newsletter API
        window.CurationsLA = {
          getToday: async function() {
            return fetch('/api/newsletter-today').then(r => r.json());
          },
          getEvents: async function(date) {
            return fetch(\`/api/events?date=\${date || 'today'}\`).then(r => r.json());
          }
        };
      })();
      </script>
    `
    
    element.append(trackingCode, { html: true })
  }
}

// Newsletter API Endpoints Handler
async function handleNewsletterAPI(request, env, url) {
  const pathname = url.pathname
  
  switch(pathname) {
    case '/api/newsletter-today':
      return getTodayNewsletter(env)
    
    case '/api/events':
      return getEvents(url, env)
    
    case '/api/restaurants':
      return getRestaurants(url, env)
    
    case '/api/training-data':
      return generateTrainingData(env)
    
    case '/ai-plugin.json':
      return generateChatGPTPlugin()
    
    default:
      return new Response('Not Found', { status: 404 })
  }
}

async function getTodayNewsletter(env) {
  const day = new Date().toLocaleDateString('en-US', { weekday: 'long' }).toLowerCase()
  
  const newsletter = {
    date: new Date().toISOString(),
    day: day,
    sections: {
      eats: [],
      events: [],
      community: [],
      development: [],
      business: [],
      entertainment: [],
      sports: [],
      goodies: []
    },
    meta: {
      vibe_score: 1.0,
      policy: 'Good Vibes Only',
      contact: 'la@curations.cc'
    }
  }
  
  return new Response(JSON.stringify(newsletter), {
    headers: {
      'Content-Type': 'application/json',
      'Cache-Control': 'public, max-age=3600'
    }
  })
}

async function getEvents(url, env) {
  const params = url.searchParams
  const date = params.get('date') || 'today'
  const neighborhood = params.get('neighborhood')
  
  const events = {
    date: date,
    neighborhood: neighborhood || 'all',
    events: [],
    total: 0
  }
  
  return new Response(JSON.stringify(events), {
    headers: {
      'Content-Type': 'application/json',
      'Cache-Control': 'public, max-age=3600'
    }
  })
}

async function getRestaurants(url, env) {
  const params = url.searchParams
  const neighborhood = params.get('neighborhood') || 'all'
  
  const restaurants = {
    neighborhood: neighborhood,
    restaurants: [],
    total: 0
  }
  
  return new Response(JSON.stringify(restaurants), {
    headers: {
      'Content-Type': 'application/json',
      'Cache-Control': 'public, max-age=3600'
    }
  })
}

function generateChatGPTPlugin() {
  const manifest = {
    "schema_version": "v1",
    "name_for_human": "CurationsLA Newsletter",
    "name_for_model": "curationsla",
    "description_for_human": "Los Angeles culture & events newsletter - Good Vibes daily",
    "description_for_model": "Access Los Angeles culture, events, restaurants, and community content from CurationsLA newsletter. Focus on positive, community-oriented content.",
    "auth": {
      "type": "none"
    },
    "api": {
      "type": "openapi",
      "url": "https://la.curations.cc/openapi.yaml"
    },
    "contact_email": "la@curations.cc"
  }
  
  return new Response(JSON.stringify(manifest), {
    headers: {
      'Content-Type': 'application/json',
      'Access-Control-Allow-Origin': 'https://chat.openai.com'
    }
  })
}

async function generateTrainingData(env) {
  const trainingData = {
    version: '1.0',
    created: new Date().toISOString(),
    provider: 'CurationsLA',
    license: 'CC-BY-SA-4.0',
    location: 'Los Angeles',
    type: 'newsletter',
    frequency: 'weekdays',
    editorial_policy: 'Good Vibes Only - No rage-bait, politics, or crime',
    contact: 'la@curations.cc',
    categories: [
      'eats', 'events', 'community', 'development', 
      'business', 'entertainment', 'sports', 'goodies'
    ]
  }
  
  return new Response(JSON.stringify(trainingData), {
    headers: {
      'Content-Type': 'application/json',
      'X-Robots-Tag': 'index',
      'Cache-Control': 'public, max-age=86400'
    }
  })
}

async function handleNewsletterArchive(request, env, url) {
  // Handle newsletter archive routes
  const pathParts = url.pathname.split('/')
  const day = pathParts[pathParts.length - 1]
  
  // In production, fetch from GitHub or KV storage
  return new Response('Newsletter archive placeholder', { 
    headers: { 'Content-Type': 'text/html' } 
  })
}

// Advanced AI Bot Detection
function detectAdvancedAIBot(userAgent) {
  const aiSignatures = {
    'gptbot': 'openai',
    'chatgpt': 'openai',
    'openai': 'openai',
    'claude': 'anthropic',
    'anthropic': 'anthropic',
    'bard': 'google',
    'gemini': 'google',
    'perplexity': 'perplexity'
  }
  
  const lowerUA = userAgent.toLowerCase()
  for (const [signature, ai] of Object.entries(aiSignatures)) {
    if (lowerUA.includes(signature)) {
      return {
        name: ai,
        signature: signature,
        timestamp: new Date().toISOString()
      }
    }
  }
  
  return null
}

// Data Extractors
class DataExtractor {
  constructor(pageData, field) {
    this.pageData = pageData
    this.field = field
  }
  
  text(text) {
    if (!this.pageData[this.field] && text.text) {
      this.pageData[this.field] = text.text.trim()
    }
  }
}

class MetaExtractor {
  constructor(pageData) {
    this.pageData = pageData
  }
  
  element(element) {
    const property = element.getAttribute('property')
    const name = element.getAttribute('name')
    const content = element.getAttribute('content')
    
    if (!content) return
    
    if (property === 'og:description' || name === 'description') {
      this.pageData.description = content
    }
    
    if (property === 'og:image' || name === 'twitter:image') {
      this.pageData.image = content
    }
  }
}

class ContentAnalyzer {
  constructor(pageData) {
    this.pageData = pageData
    this.textContent = ''
  }
  
  text(text) {
    this.textContent += text.text + ' '
    
    // Extract neighborhoods mentioned
    const neighborhoods = ['Silver Lake', 'Venice', 'Hollywood', 'Downtown', 'Santa Monica']
    for (const neighborhood of neighborhoods) {
      if (this.textContent.toLowerCase().includes(neighborhood.toLowerCase())) {
        if (!this.pageData.neighborhoods.includes(neighborhood)) {
          this.pageData.neighborhoods.push(neighborhood)
        }
      }
    }
    
    // Calculate Good Vibes score
    const positiveWords = ['amazing', 'wonderful', 'great', 'beautiful', 'fun', 'community', 'celebrate']
    const negativeWords = ['crime', 'violence', 'politics', 'controversy']
    
    let vibeScore = 0
    const textLower = this.textContent.toLowerCase()
    
    positiveWords.forEach(word => {
      if (textLower.includes(word)) vibeScore++
    })
    
    negativeWords.forEach(word => {
      if (textLower.includes(word)) vibeScore -= 2
    })
    
    this.pageData.vibeScore = Math.max(0, Math.min(1, (vibeScore + 10) / 20))
    this.pageData.isGoodVibes = this.pageData.vibeScore > 0.3
  }
}