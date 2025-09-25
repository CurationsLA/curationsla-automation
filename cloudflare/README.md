# CurationsLA Advanced Cloudflare Workers

## 🚀 Advanced SEO & AI Discovery Infrastructure

This directory contains a comprehensive suite of Cloudflare Workers designed to optimize la.curations.cc for advanced SEO, AI discovery, and performance. The workers provide state-of-the-art optimization for search engines, AI platforms, and user experience.

## 🏗️ Architecture Overview

### Core Workers

1. **Advanced SEO Worker** (`advanced-seo-worker.js`)
   - Primary worker handling all HTML optimization
   - AI bot detection and specialized responses
   - Comprehensive meta tag injection
   - Schema.org markup enhancement
   - Performance optimization

2. **Sitemap Enhancer Worker** (`sitemap-enhancer-worker.js`)
   - Dynamic sitemap generation
   - News sitemap with AI optimization
   - Events and API endpoint sitemaps
   - Bot-specific caching strategies

3. **Smart Routing Worker** (`smart-routing-worker.js`)
   - Intelligent traffic routing
   - AI bot prioritization
   - Geographic optimization
   - Advanced caching strategies

4. **Trust Signals Worker** (`trust-signals-worker.js`)
   - robots.txt with AI bot welcome
   - llms.txt for LLM discovery
   - trust.txt for authority signals
   - .well-known endpoint handling

5. **AI Discovery Worker** (`ai-discovery-worker.js`)
   - ai-manifest.json generation
   - OpenAPI specification
   - AI context and training data
   - Platform-specific optimizations

## 🎯 Key Features

### AI Platform Optimization
- **ChatGPT/GPT-4**: Plugin manifest, training encouragement, citation optimization
- **Claude**: Analysis welcome, local search optimization, community focus
- **Perplexity**: Citation encouragement, real-time events, location awareness
- **Google AI**: Knowledge graph ready, structured data rich
- **Voice Assistants**: Speakable content, natural language optimization

### SEO Excellence
- **Core Web Vitals**: Optimized for performance scores
- **Schema.org**: Comprehensive structured data
- **News SEO**: Google News optimized sitemaps
- **Local SEO**: Geographic targeting and optimization
- **Technical SEO**: Advanced header optimization

### Trust & Authority
- **Editorial Standards**: Transparent good vibes policy
- **Verification**: Weekly venue and event verification
- **Transparency**: Clear content policies and contact information
- **Security**: Comprehensive security headers and policies

## 📁 File Structure

```
cloudflare/
├── advanced-seo-worker.js      # Primary SEO optimization
├── sitemap-enhancer-worker.js  # Dynamic sitemap generation
├── smart-routing-worker.js     # Intelligent routing & caching
├── trust-signals-worker.js     # Trust & discovery signals
├── ai-discovery-worker.js      # AI platform integration
├── wrangler.toml              # Worker configuration
├── deploy-workers.sh          # Deployment script
└── README.md                  # This file
```

## 🚀 Quick Deployment

### Prerequisites
1. Install Wrangler CLI: `npm install -g wrangler`
2. Authenticate: `wrangler login`
3. Configure zone access in Cloudflare dashboard

### Deploy All Workers
```bash
chmod +x deploy-workers.sh
./deploy-workers.sh
```

### Deploy Individual Worker
```bash
wrangler deploy advanced-seo-worker.js --name curationsla-seo-prod --env production
```

## 🛠️ Configuration

### Environment Variables
Set in `wrangler.toml` or Cloudflare dashboard:
- `SITE_URL`: https://la.curations.cc
- `CONTACT_EMAIL`: la@curations.cc
- `ORGANIZATION_NAME`: CurationsLA
- `CONTENT_POLICY`: good_vibes_only
- `LICENSE`: CC-BY-SA-4.0

### KV Namespaces
- `CURATIONS_CACHE`: Response caching and optimization
- `CURATIONS_DATA`: Configuration and content storage

## 🎯 Key Endpoints Created

### Discovery Files
- `/robots.txt` - AI-friendly crawler directives
- `/llms.txt` - LLM training and discovery manifest
- `/trust.txt` - Authority and transparency signals
- `/ai-manifest.json` - Comprehensive AI platform support
- `/.well-known/ai-plugin.json` - ChatGPT plugin manifest

### Sitemaps
- `/sitemap.xml` - Main sitemap with AI optimization
- `/news-sitemap.xml` - Google News compliant sitemap
- `/events-sitemap.xml` - Events-focused sitemap
- `/api-sitemap.xml` - API endpoints for discovery
- `/sitemap-index.xml` - Master sitemap index

### API Endpoints
- `/api/newsletter-today` - Current newsletter content
- `/api/events` - LA events with verification
- `/api/restaurants` - Restaurant recommendations
- `/api/training-data` - AI training optimized data
- `/api/ai-context` - AI context and optimization data

## 🤖 AI Bot Detection & Optimization

### Detected Platforms
- **High Priority**: GPTBot, Claude, PerplexityBot, Google-Extended
- **Medium Priority**: Bingbot, Applebot, FacebookBot
- **Low Priority**: LinkedInBot, TwitterBot

### Bot-Specific Optimizations
- Specialized response headers
- Optimized caching strategies
- Enhanced metadata injection
- Citation-friendly formatting

## 📊 Performance Features

### Caching Strategy
- **AI Bots**: 30-minute cache for current content
- **Users**: 1-hour cache with stale-while-revalidate
- **Static Content**: 24-hour cache with CDN optimization

### Geographic Optimization
- **California Users**: Local timezone optimization
- **Mobile Users**: Performance-optimized responses
- **International**: CDN edge optimization

## 🔒 Security & Privacy

### Security Headers
- Content Security Policy (CSP)
- X-Content-Type-Options: nosniff
- X-Frame-Options: SAMEORIGIN
- Referrer-Policy: strict-origin-when-cross-origin

### Privacy Compliance
- CCPA compliant data handling
- Transparent data collection
- User consent management

## 📈 Monitoring & Analytics

### Built-in Analytics
- AI bot visit tracking
- Performance metrics
- Error rate monitoring
- Cache hit ratios

### Integration Points
- Cloudflare Analytics
- Workers Analytics
- Custom analytics via KV storage

## 🎨 Customization

### Adding New AI Platforms
1. Update bot detection in `smart-routing-worker.js`
2. Add platform-specific optimization in `advanced-seo-worker.js`
3. Update AI manifest in `ai-discovery-worker.js`

### Modifying Content Policy
1. Update `trust.txt` generation
2. Modify `llms.txt` content guidelines
3. Update AI manifest policies

### Custom API Endpoints
1. Add routes in `smart-routing-worker.js`
2. Implement handlers in `advanced-seo-worker.js`
3. Update OpenAPI specification

## 🐛 Troubleshooting

### Common Issues

**Workers Not Deploying**
- Check Wrangler authentication: `wrangler whoami`
- Verify zone permissions in Cloudflare dashboard
- Check for syntax errors in worker files

**Routes Not Working**
- Verify route priority in Cloudflare dashboard
- Check for conflicting routes
- Allow 5-10 minutes for propagation

**KV Namespace Issues**
- Ensure namespaces are created: `wrangler kv:namespace list`
- Check binding names in `wrangler.toml`
- Verify read/write permissions

### Debug Mode
Add debug parameters to test endpoints:
```
https://la.curations.cc/robots.txt?debug=1
https://la.curations.cc/ai-manifest.json?verbose=1
```

## 📞 Support

- **Technical Issues**: tech@curations.cc
- **AI Partnerships**: partnerships@curations.cc
- **General Questions**: la@curations.cc

## 📄 License

This worker suite is part of CurationsLA and follows the CC-BY-SA-4.0 license for training data and syndication. The workers themselves are proprietary to CurationsLA.

---

**Made with 💜 in Los Angeles**  
*Bringing Good Vibes to AI discovery since 2024*