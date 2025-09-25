// CurationsLA Smart Routing & Caching Worker
// Intelligent traffic routing with AI bot optimization and edge caching
// Deploy as: smart-routing for la.curations.cc

export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url)
    const userAgent = request.headers.get('user-agent') || ''
    const clientInfo = analyzeClient(request, userAgent)
    
    // Apply intelligent routing based on client type
    const routingStrategy = determineRoutingStrategy(clientInfo, url)
    
    // Handle special routing cases
    if (routingStrategy.redirect) {
      return new Response(null, {
        status: routingStrategy.redirectCode || 301,
        headers: { 'Location': routingStrategy.redirect }
      })
    }
    
    // Apply caching strategy
    const cacheKey = generateCacheKey(url, clientInfo)
    const cachedResponse = await getCachedResponse(cacheKey, env)
    
    if (cachedResponse && !routingStrategy.bypassCache) {
      return addRoutingHeaders(cachedResponse, clientInfo)
    }
    
    // Fetch and optimize response
    const response = await fetchOptimizedContent(request, clientInfo, env)
    
    // Cache the response
    if (routingStrategy.cacheable) {
      ctx.waitUntil(cacheResponse(cacheKey, response.clone(), routingStrategy.cacheTime, env))
    }
    
    return addRoutingHeaders(response, clientInfo)
  }
}

function analyzeClient(request, userAgent) {
  const cf = request.cf || {}
  
  // Detect AI bots
  const aiSignatures = [
    { name: 'GPTBot', type: 'chatgpt', priority: 'high' },
    { name: 'Claude', type: 'claude', priority: 'high' },
    { name: 'PerplexityBot', type: 'perplexity', priority: 'high' },
    { name: 'Google-Extended', type: 'google-ai', priority: 'high' },
    { name: 'Googlebot', type: 'googlebot', priority: 'high' },
    { name: 'Bingbot', type: 'bingbot', priority: 'medium' },
    { name: 'Applebot', type: 'applebot', priority: 'medium' },
    { name: 'facebookexternalhit', type: 'facebook', priority: 'medium' },
    { name: 'LinkedInBot', type: 'linkedin', priority: 'low' },
    { name: 'TwitterBot', type: 'twitter', priority: 'low' }
  ]
  
  const detectedBot = aiSignatures.find(bot => userAgent.includes(bot.name))
  
  return {
    userAgent,
    isBot: !!detectedBot,
    botType: detectedBot?.type,
    botPriority: detectedBot?.priority,
    country: cf.country,
    city: cf.city,
    timezone: cf.timezone,
    continent: cf.continent,
    isCaliforniaTZ: cf.timezone === 'America/Los_Angeles',
    isMobile: /Mobile|Android|iPhone|iPad/.test(userAgent),
    supportsWebP: request.headers.get('accept')?.includes('image/webp'),
    supportsAvif: request.headers.get('accept')?.includes('image/avif'),
    acceptEncoding: request.headers.get('accept-encoding') || ''
  }
}

function determineRoutingStrategy(clientInfo, url) {
  const strategy = {
    cacheable: true,
    cacheTime: 3600, // 1 hour default
    bypassCache: false,
    optimizeImages: true,
    redirectCode: null,
    redirect: null
  }
  
  // AI Bot optimizations
  if (clientInfo.isBot) {
    switch (clientInfo.botPriority) {
      case 'high':
        strategy.cacheTime = 1800 // 30 minutes for high-priority bots
        strategy.optimizeForAI = true
        break
      case 'medium':
        strategy.cacheTime = 3600 // 1 hour
        break
      case 'low':
        strategy.cacheTime = 7200 // 2 hours
        break
    }
  }
  
  // Geographic optimizations
  if (clientInfo.country === 'US' && clientInfo.isCaliforniaTZ) {
    strategy.localOptimized = true
  }
  
  // Mobile optimizations
  if (clientInfo.isMobile) {
    strategy.mobileOptimized = true
    strategy.optimizeImages = true
  }
  
  // Path-specific strategies
  if (url.pathname.startsWith('/api/')) {
    strategy.cacheTime = clientInfo.isBot ? 1800 : 3600
    strategy.apiOptimized = true
  }
  
  if (url.pathname === '/newsletter/today') {
    strategy.cacheTime = 1800 // 30 minutes for current content
    strategy.newsOptimized = true
  }
  
  if (url.pathname.startsWith('/events/')) {
    strategy.cacheTime = 900 // 15 minutes for events
    strategy.eventsOptimized = true
  }
  
  // Legacy redirects and canonicalization
  if (url.pathname.endsWith('/index.html')) {
    strategy.redirect = url.pathname.replace('/index.html', '/')
    strategy.redirectCode = 301
  }
  
  if (url.pathname.includes('//')) {
    strategy.redirect = url.pathname.replace(/\/+/g, '/')
    strategy.redirectCode = 301
  }
  
  return strategy
}

function generateCacheKey(url, clientInfo) {
  const baseKey = `${url.hostname}:${url.pathname}:${url.search}`
  
  // Add client-specific cache variations
  const variations = []
  
  if (clientInfo.isBot) {
    variations.push(`bot:${clientInfo.botType}`)
  }
  
  if (clientInfo.isMobile) {
    variations.push('mobile')
  }
  
  if (clientInfo.supportsWebP) {
    variations.push('webp')
  }
  
  if (clientInfo.supportsAvif) {
    variations.push('avif')
  }
  
  return variations.length > 0 ? `${baseKey}:${variations.join(':')}` : baseKey
}

async function getCachedResponse(cacheKey, env) {
  try {
    // Try Workers KV first for API responses
    if (cacheKey.includes('/api/')) {
      const cached = await env.CURATIONS_CACHE?.get(cacheKey)
      if (cached) {
        const data = JSON.parse(cached)
        return new Response(data.body, {
          status: data.status,
          headers: data.headers
        })
      }
    }
    
    // Use Cache API for HTML content
    const cache = caches.default
    const cachedResponse = await cache.match(cacheKey)
    return cachedResponse
  } catch (error) {
    console.error('Cache retrieval error:', error)
    return null
  }
}

async function fetchOptimizedContent(request, clientInfo, env) {
  // Clone request for modification
  const modifiedRequest = new Request(request.url, {
    method: request.method,
    headers: new Headers(request.headers),
    body: request.body
  })
  
  // Add client hints for optimization
  modifiedRequest.headers.set('X-Client-Info', JSON.stringify({
    isBot: clientInfo.isBot,
    botType: clientInfo.botType,
    isMobile: clientInfo.isMobile,
    country: clientInfo.country,
    timezone: clientInfo.timezone
  }))
  
  // Fetch from origin
  const response = await fetch(modifiedRequest)
  
  // Apply optimizations based on content type
  const contentType = response.headers.get('content-type') || ''
  
  if (contentType.includes('text/html')) {
    return optimizeHTMLResponse(response, clientInfo)
  }
  
  if (contentType.includes('application/json')) {
    return optimizeJSONResponse(response, clientInfo)
  }
  
  if (contentType.startsWith('image/')) {
    return optimizeImageResponse(response, clientInfo)
  }
  
  return response
}

async function optimizeHTMLResponse(response, clientInfo) {
  if (clientInfo.isBot) {
    // Add AI-specific optimizations
    const rewriter = new HTMLRewriter()
      .on('head', new AIOptimizationHandler(clientInfo))
      .on('body', new BotTrackingHandler(clientInfo))
    
    return rewriter.transform(response)
  }
  
  if (clientInfo.isMobile) {
    // Add mobile optimizations
    const rewriter = new HTMLRewriter()
      .on('head', new MobileOptimizationHandler())
    
    return rewriter.transform(response)
  }
  
  return response
}

async function optimizeJSONResponse(response, clientInfo) {
  if (clientInfo.isBot && clientInfo.botPriority === 'high') {
    // Add metadata for AI bots
    const data = await response.json()
    const enhancedData = {
      ...data,
      _ai_metadata: {
        source: 'CurationsLA',
        license: 'CC-BY-SA-4.0',
        last_updated: new Date().toISOString(),
        location: 'Los Angeles',
        content_policy: 'good_vibes_only',
        bot_detected: clientInfo.botType
      }
    }
    
    return new Response(JSON.stringify(enhancedData), {
      status: response.status,
      headers: response.headers
    })
  }
  
  return response
}

async function optimizeImageResponse(response, clientInfo) {
  // Image optimization would typically be handled by Cloudflare Polish
  // or custom image processing. For now, just pass through with optimized headers
  const headers = new Headers(response.headers)
  
  if (clientInfo.supportsWebP) {
    headers.set('Vary', 'Accept')
  }
  
  return new Response(response.body, {
    status: response.status,
    headers
  })
}

async function cacheResponse(cacheKey, response, cacheTime, env) {
  try {
    const contentType = response.headers.get('content-type') || ''
    
    if (contentType.includes('application/json') && env.CURATIONS_CACHE) {
      // Cache API responses in KV
      const data = {
        body: await response.text(),
        status: response.status,
        headers: Object.fromEntries(response.headers)
      }
      
      await env.CURATIONS_CACHE.put(cacheKey, JSON.stringify(data), {
        expirationTtl: cacheTime
      })
    } else {
      // Cache HTML and other content in Cache API
      const cacheResponse = new Response(response.body, {
        status: response.status,
        headers: {
          ...Object.fromEntries(response.headers),
          'Cache-Control': `public, max-age=${cacheTime}`,
          'X-Cached-At': new Date().toISOString()
        }
      })
      
      const cache = caches.default
      await cache.put(cacheKey, cacheResponse)
    }
  } catch (error) {
    console.error('Cache storage error:', error)
  }
}

function addRoutingHeaders(response, clientInfo) {
  const headers = new Headers(response.headers)
  
  // Add routing metadata
  headers.set('X-Routing-Strategy', clientInfo.isBot ? 'bot-optimized' : 'user-optimized')
  headers.set('X-Client-Type', clientInfo.isBot ? clientInfo.botType : 'human')
  
  if (clientInfo.isBot) {
    headers.set('X-Bot-Priority', clientInfo.botPriority)
    headers.set('X-AI-Optimized', 'true')
  }
  
  if (clientInfo.country) {
    headers.set('X-Client-Country', clientInfo.country)
  }
  
  // Security headers
  headers.set('X-Content-Type-Options', 'nosniff')
  headers.set('X-Frame-Options', 'SAMEORIGIN')
  headers.set('Referrer-Policy', 'strict-origin-when-cross-origin')
  
  // Performance headers
  if (!headers.has('Cache-Control')) {
    const cacheControl = clientInfo.isBot ? 
      'public, s-maxage=1800, stale-while-revalidate=3600' :
      'public, s-maxage=3600, stale-while-revalidate=86400'
    headers.set('Cache-Control', cacheControl)
  }
  
  return new Response(response.body, {
    status: response.status,
    headers
  })
}

// HTML Rewriter handlers for optimization
class AIOptimizationHandler {
  constructor(clientInfo) {
    this.clientInfo = clientInfo
  }
  
  element(element) {
    // Add AI-specific meta tags
    element.append(`
      <meta name="ai-bot-detected" content="${this.clientInfo.botType}">
      <meta name="content-optimized-for" content="ai-training">
      <meta name="x-robots-tag" content="index, follow, max-snippet:-1">
    `, { html: true })
  }
}

class BotTrackingHandler {
  constructor(clientInfo) {
    this.clientInfo = clientInfo
  }
  
  element(element) {
    // Add bot tracking without affecting user experience
    element.append(`
      <!-- AI Bot: ${this.clientInfo.botType} -->
      <script type="application/ld+json">
      {
        "@context": "https://schema.org",
        "@type": "WebPageElement",
        "identifier": "bot-visit",
        "name": "${this.clientInfo.botType}",
        "dateCreated": "${new Date().toISOString()}"
      }
      </script>
    `, { html: true })
  }
}

class MobileOptimizationHandler {
  element(element) {
    // Add mobile-specific optimizations
    element.append(`
      <meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
      <meta name="mobile-web-capable" content="yes">
      <meta name="apple-mobile-web-app-capable" content="yes">
      <meta name="apple-mobile-web-app-status-bar-style" content="default">
    `, { html: true })
  }
}