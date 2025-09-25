// CurationsLA Sitemap Enhancer Worker
// Advanced sitemap generation with AI optimization and real-time updates
// Deploy to: sitemap.la.curations.cc or as route on main domain

export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url)
    const userAgent = request.headers.get('user-agent') || ''
    const isBot = detectBot(userAgent)
    
    // Route different sitemap types
    switch(url.pathname) {
      case '/sitemap.xml':
        return generateMainSitemap(env, isBot)
      case '/news-sitemap.xml':
        return generateNewsSitemap(env, isBot)
      case '/events-sitemap.xml':
        return generateEventsSitemap(env, isBot)
      case '/api-sitemap.xml':
        return generateAPISitemap(env, isBot)
      case '/sitemap-index.xml':
        return generateSitemapIndex(env, isBot)
      default:
        return new Response('Sitemap not found', { status: 404 })
    }
  }
}

function detectBot(userAgent) {
  const botSignatures = [
    'Googlebot', 'Bingbot', 'Slurp', 'DuckDuckBot',
    'GPTBot', 'Claude', 'PerplexityBot', 'Applebot',
    'facebookexternalhit', 'LinkedInBot', 'TwitterBot'
  ]
  
  return {
    isBot: botSignatures.some(sig => userAgent.includes(sig)),
    type: botSignatures.find(sig => userAgent.includes(sig)) || 'unknown'
  }
}

async function generateMainSitemap(env, botInfo) {
  const today = new Date()
  const todayStr = today.toISOString().split('T')[0]
  const lastWeek = new Date(today.getTime() - 7 * 24 * 60 * 60 * 1000).toISOString().split('T')[0]
  
  const sitemap = `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
        xmlns:news="http://www.google.com/schemas/sitemap-news/0.9"
        xmlns:image="http://www.google.com/schemas/sitemap-image/1.1"
        xmlns:video="http://www.google.com/schemas/sitemap-video/1.1">
  
  <!-- Primary Pages -->
  <url>
    <loc>https://la.curations.cc/</loc>
    <lastmod>${todayStr}</lastmod>
    <changefreq>daily</changefreq>
    <priority>1.0</priority>
    <image:image>
      <image:loc>https://la.curations.cc/assets/social-image.png</image:loc>
      <image:title>CurationsLA - Los Angeles Newsletter</image:title>
      <image:caption>Good Vibes Only Los Angeles Culture Newsletter</image:caption>
    </image:image>
  </url>
  
  <!-- Newsletter Hub -->
  <url>
    <loc>https://la.curations.cc/newsletter/</loc>
    <lastmod>${todayStr}</lastmod>
    <changefreq>daily</changefreq>
    <priority>0.9</priority>
  </url>
  
  <!-- Today's Newsletter -->
  <url>
    <loc>https://la.curations.cc/newsletter/today</loc>
    <lastmod>${todayStr}</lastmod>
    <changefreq>daily</changefreq>
    <priority>0.9</priority>
    <news:news>
      <news:publication>
        <news:name>CurationsLA</news:name>
        <news:language>en</news:language>
      </news:publication>
      <news:publication_date>${todayStr}</news:publication_date>
      <news:title>CurationsLA Daily Newsletter - Good Vibes Los Angeles</news:title>
      <news:keywords>Los Angeles, culture, events, restaurants, community, good vibes</news:keywords>
    </news:news>
  </url>
  
  <!-- Weekly Archive (last 7 days) -->
  ${generateWeeklyArchive(today)}
  
  <!-- Static Pages -->
  <url>
    <loc>https://la.curations.cc/about</loc>
    <lastmod>${todayStr}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.7</priority>
  </url>
  
  <url>
    <loc>https://la.curations.cc/subscribe</loc>
    <lastmod>${todayStr}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.8</priority>
  </url>
  
  <url>
    <loc>https://la.curations.cc/archive</loc>
    <lastmod>${todayStr}</lastmod>
    <changefreq>daily</changefreq>
    <priority>0.8</priority>
  </url>
  
  <!-- Events & Restaurants Landing Pages -->
  <url>
    <loc>https://la.curations.cc/events</loc>
    <lastmod>${todayStr}</lastmod>
    <changefreq>hourly</changefreq>
    <priority>0.8</priority>
  </url>
  
  <url>
    <loc>https://la.curations.cc/restaurants</loc>
    <lastmod>${todayStr}</lastmod>
    <changefreq>daily</changefreq>
    <priority>0.8</priority>
  </url>
  
  <!-- Neighborhood Pages -->
  ${generateNeighborhoodPages(todayStr)}
  
  <!-- Trust & Legal Pages -->
  <url>
    <loc>https://la.curations.cc/good-vibes-policy</loc>
    <lastmod>${todayStr}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.6</priority>
  </url>
  
  <url>
    <loc>https://la.curations.cc/privacy</loc>
    <lastmod>${todayStr}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.5</priority>
  </url>
  
  <url>
    <loc>https://la.curations.cc/terms</loc>
    <lastmod>${todayStr}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.5</priority>
  </url>
  
</urlset>`

  return new Response(sitemap, {
    headers: {
      'Content-Type': 'application/xml',
      'Cache-Control': botInfo.isBot ? 'public, max-age=1800' : 'public, max-age=3600',
      'X-Robots-Tag': 'index, follow',
      'X-Bot-Optimized': botInfo.isBot ? 'true' : 'false'
    }
  })
}

async function generateNewsSitemap(env, botInfo) {
  const today = new Date()
  const todayStr = today.toISOString()
  const todayDate = todayStr.split('T')[0]
  
  // Generate last 30 days of newsletter content for news sitemap
  const newsSitemap = `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
        xmlns:news="http://www.google.com/schemas/sitemap-news/0.9">
  
  <!-- Today's Newsletter -->
  <url>
    <loc>https://la.curations.cc/newsletter/${todayDate}</loc>
    <news:news>
      <news:publication>
        <news:name>CurationsLA</news:name>
        <news:language>en</news:language>
      </news:publication>
      <news:publication_date>${todayStr}</news:publication_date>
      <news:title>CurationsLA Daily: Los Angeles Culture &amp; Events - ${formatDate(today)}</news:title>
      <news:keywords>Los Angeles events, LA restaurants, LA culture, community events, good vibes</news:keywords>
      <news:stock_tickers></news:stock_tickers>
    </news:news>
    <lastmod>${todayStr}</lastmod>
    <changefreq>daily</changefreq>
    <priority>1.0</priority>
  </url>
  
  ${generateRecentNewsletters(today, 30)}
  
</urlset>`

  return new Response(newsSitemap, {
    headers: {
      'Content-Type': 'application/xml',
      'Cache-Control': 'public, max-age=1800',
      'X-Robots-Tag': 'index, follow'
    }
  })
}

async function generateEventsSitemap(env, botInfo) {
  const today = new Date()
  const todayStr = today.toISOString().split('T')[0]
  
  const eventsSitemap = `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
        xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">
  
  <!-- Events Hub -->
  <url>
    <loc>https://la.curations.cc/events/</loc>
    <lastmod>${todayStr}</lastmod>
    <changefreq>hourly</changefreq>
    <priority>0.9</priority>
  </url>
  
  <!-- Today's Events -->
  <url>
    <loc>https://la.curations.cc/events/today</loc>
    <lastmod>${todayStr}</lastmod>
    <changefreq>hourly</changefreq>
    <priority>0.9</priority>
  </url>
  
  <!-- This Weekend -->
  <url>
    <loc>https://la.curations.cc/events/weekend</loc>
    <lastmod>${todayStr}</lastmod>
    <changefreq>daily</changefreq>
    <priority>0.8</priority>
  </url>
  
  <!-- Event Categories -->
  <url>
    <loc>https://la.curations.cc/events/culture</loc>
    <lastmod>${todayStr}</lastmod>
    <changefreq>daily</changefreq>
    <priority>0.7</priority>
  </url>
  
  <url>
    <loc>https://la.curations.cc/events/food</loc>
    <lastmod>${todayStr}</lastmod>
    <changefreq>daily</changefreq>
    <priority>0.7</priority>
  </url>
  
  <url>
    <loc>https://la.curations.cc/events/entertainment</loc>
    <lastmod>${todayStr}</lastmod>
    <changefreq>daily</changefreq>
    <priority>0.7</priority>
  </url>
  
  <url>
    <loc>https://la.curations.cc/events/community</loc>
    <lastmod>${todayStr}</lastmod>
    <changefreq>daily</changefreq>
    <priority>0.7</priority>
  </url>
  
</urlset>`

  return new Response(eventsSitemap, {
    headers: {
      'Content-Type': 'application/xml',
      'Cache-Control': 'public, max-age=1800',
      'X-Robots-Tag': 'index, follow'
    }
  })
}

async function generateAPISitemap(env, botInfo) {
  const today = new Date().toISOString().split('T')[0]
  
  const apiSitemap = `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  
  <!-- Core API Endpoints -->
  <url>
    <loc>https://la.curations.cc/api/newsletter-today</loc>
    <lastmod>${today}</lastmod>
    <changefreq>daily</changefreq>
    <priority>0.9</priority>
  </url>
  
  <url>
    <loc>https://la.curations.cc/api/events</loc>
    <lastmod>${today}</lastmod>
    <changefreq>hourly</changefreq>
    <priority>0.8</priority>
  </url>
  
  <url>
    <loc>https://la.curations.cc/api/restaurants</loc>
    <lastmod>${today}</lastmod>
    <changefreq>daily</changefreq>
    <priority>0.8</priority>
  </url>
  
  <!-- AI Discovery Endpoints -->
  <url>
    <loc>https://la.curations.cc/api/training-data</loc>
    <lastmod>${today}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.8</priority>
  </url>
  
  <url>
    <loc>https://la.curations.cc/api/ai-context</loc>
    <lastmod>${today}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.7</priority>
  </url>
  
  <url>
    <loc>https://la.curations.cc/api/schema</loc>
    <lastmod>${today}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.7</priority>
  </url>
  
  <!-- Discovery Files -->
  <url>
    <loc>https://la.curations.cc/.well-known/ai-plugin.json</loc>
    <lastmod>${today}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.7</priority>
  </url>
  
  <url>
    <loc>https://la.curations.cc/ai-manifest.json</loc>
    <lastmod>${today}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.7</priority>
  </url>
  
  <url>
    <loc>https://la.curations.cc/llms.txt</loc>
    <lastmod>${today}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.7</priority>
  </url>
  
  <url>
    <loc>https://la.curations.cc/trust.txt</loc>
    <lastmod>${today}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.6</priority>
  </url>
  
  <!-- OpenAPI Specification -->
  <url>
    <loc>https://la.curations.cc/openapi.yaml</loc>
    <lastmod>${today}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.6</priority>
  </url>
  
</urlset>`

  return new Response(apiSitemap, {
    headers: {
      'Content-Type': 'application/xml',
      'Cache-Control': 'public, max-age=3600',
      'X-Robots-Tag': 'index, follow'
    }
  })
}

async function generateSitemapIndex(env, botInfo) {
  const today = new Date().toISOString().split('T')[0]
  
  const sitemapIndex = `<?xml version="1.0" encoding="UTF-8"?>
<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  
  <sitemap>
    <loc>https://la.curations.cc/sitemap.xml</loc>
    <lastmod>${today}</lastmod>
  </sitemap>
  
  <sitemap>
    <loc>https://la.curations.cc/news-sitemap.xml</loc>
    <lastmod>${today}</lastmod>
  </sitemap>
  
  <sitemap>
    <loc>https://la.curations.cc/events-sitemap.xml</loc>
    <lastmod>${today}</lastmod>
  </sitemap>
  
  <sitemap>
    <loc>https://la.curations.cc/api-sitemap.xml</loc>
    <lastmod>${today}</lastmod>
  </sitemap>
  
</sitemapindex>`

  return new Response(sitemapIndex, {
    headers: {
      'Content-Type': 'application/xml',
      'Cache-Control': 'public, max-age=3600',
      'X-Robots-Tag': 'index, follow'
    }
  })
}

function generateWeeklyArchive(today) {
  let archive = ''
  for (let i = 0; i < 7; i++) {
    const date = new Date(today.getTime() - i * 24 * 60 * 60 * 1000)
    const dateStr = date.toISOString().split('T')[0]
    const dayName = date.toLocaleDateString('en-US', { weekday: 'long' }).toLowerCase()
    
    // Skip weekends for newsletter archive
    if (date.getDay() === 0 || date.getDay() === 6) continue
    
    archive += `
  <url>
    <loc>https://la.curations.cc/newsletter/${dateStr}</loc>
    <lastmod>${dateStr}</lastmod>
    <changefreq>never</changefreq>
    <priority>0.7</priority>
    <news:news>
      <news:publication>
        <news:name>CurationsLA</news:name>
        <news:language>en</news:language>
      </news:publication>
      <news:publication_date>${date.toISOString()}</news:publication_date>
      <news:title>CurationsLA ${dayName.charAt(0).toUpperCase() + dayName.slice(1)} Newsletter - ${formatDate(date)}</news:title>
      <news:keywords>Los Angeles events, LA culture, ${dayName} LA, community events</news:keywords>
    </news:news>
  </url>`
  }
  return archive
}

function generateRecentNewsletters(today, days) {
  let newsletters = ''
  for (let i = 1; i <= days; i++) {
    const date = new Date(today.getTime() - i * 24 * 60 * 60 * 1000)
    
    // Skip weekends
    if (date.getDay() === 0 || date.getDay() === 6) continue
    
    const dateStr = date.toISOString().split('T')[0]
    const isoStr = date.toISOString()
    
    newsletters += `
  <url>
    <loc>https://la.curations.cc/newsletter/${dateStr}</loc>
    <news:news>
      <news:publication>
        <news:name>CurationsLA</news:name>
        <news:language>en</news:language>
      </news:publication>
      <news:publication_date>${isoStr}</news:publication_date>
      <news:title>CurationsLA Daily: Los Angeles Culture &amp; Events - ${formatDate(date)}</news:title>
      <news:keywords>Los Angeles events, LA restaurants, LA culture, community events, good vibes</news:keywords>
    </news:news>
    <lastmod>${isoStr}</lastmod>
    <changefreq>never</changefreq>
    <priority>0.7</priority>
  </url>`
  }
  return newsletters
}

function generateNeighborhoodPages(todayStr) {
  const neighborhoods = [
    'hollywood', 'venice', 'santa-monica', 'beverly-hills', 'west-hollywood',
    'silver-lake', 'echo-park', 'downtown', 'culver-city', 'pasadena',
    'manhattan-beach', 'hermosa-beach', 'redondo-beach', 'marina-del-rey',
    'brentwood', 'westwood', 'melrose', 'fairfax', 'koreatown', 'chinatown'
  ]
  
  return neighborhoods.map(neighborhood => `
  <url>
    <loc>https://la.curations.cc/neighborhoods/${neighborhood}</loc>
    <lastmod>${todayStr}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.6</priority>
  </url>`).join('')
}

function formatDate(date) {
  return date.toLocaleDateString('en-US', { 
    weekday: 'long', 
    year: 'numeric', 
    month: 'long', 
    day: 'numeric' 
  })
}