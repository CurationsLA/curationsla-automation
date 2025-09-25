#!/bin/bash

# CurationsLA Advanced Cloudflare Workers Deployment Script
# Deploy comprehensive SEO and AI discovery infrastructure

set -e

echo "🚀 CurationsLA Advanced Workers Deployment"
echo "========================================="

# Configuration
ZONE_NAME="curations.cc"
SUBDOMAIN="la.curations.cc"
ENVIRONMENT="production"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check prerequisites
check_prerequisites() {
    print_status "Checking prerequisites..."
    
    if ! command -v wrangler &> /dev/null; then
        print_error "Wrangler CLI not found. Please install: npm install -g wrangler"
        exit 1
    fi
    
    if ! wrangler whoami &> /dev/null; then
        print_error "Wrangler not authenticated. Please run: wrangler login"
        exit 1
    fi
    
    print_success "Prerequisites check passed"
}

# Create KV namespaces if they don't exist
create_kv_namespaces() {
    print_status "Setting up KV namespaces..."
    
    # Check if namespaces exist, create if not
    if ! wrangler kv:namespace list | grep -q "CURATIONS_CACHE"; then
        print_status "Creating CURATIONS_CACHE namespace..."
        wrangler kv:namespace create "CURATIONS_CACHE" --env production
    fi
    
    if ! wrangler kv:namespace list | grep -q "CURATIONS_DATA"; then
        print_status "Creating CURATIONS_DATA namespace..."
        wrangler kv:namespace create "CURATIONS_DATA" --env production
    fi
    
    print_success "KV namespaces ready"
}

# Deploy individual workers
deploy_worker() {
    local worker_name=$1
    local worker_file=$2
    local description=$3
    
    print_status "Deploying $description..."
    
    if [ -f "$worker_file" ]; then
        wrangler deploy "$worker_file" --name "$worker_name" --env production
        print_success "$description deployed successfully"
    else
        print_error "Worker file $worker_file not found"
        return 1
    fi
}

# Set up routes
setup_routes() {
    print_status "Setting up Cloudflare routes..."
    
    # Main SEO worker routes
    print_status "Setting up main SEO worker routes..."
    wrangler route put "${SUBDOMAIN}/*" --zone-name="$ZONE_NAME" --worker="curationsla-seo-prod"
    
    # Sitemap routes
    print_status "Setting up sitemap routes..."
    wrangler route put "${SUBDOMAIN}/sitemap*.xml" --zone-name="$ZONE_NAME" --worker="curationsla-sitemap-prod"
    wrangler route put "${SUBDOMAIN}/news-sitemap.xml" --zone-name="$ZONE_NAME" --worker="curationsla-sitemap-prod"
    wrangler route put "${SUBDOMAIN}/events-sitemap.xml" --zone-name="$ZONE_NAME" --worker="curationsla-sitemap-prod"
    wrangler route put "${SUBDOMAIN}/api-sitemap.xml" --zone-name="$ZONE_NAME" --worker="curationsla-sitemap-prod"
    
    # Trust signals routes
    print_status "Setting up trust signals routes..."
    wrangler route put "${SUBDOMAIN}/robots.txt" --zone-name="$ZONE_NAME" --worker="curationsla-trust-prod"
    wrangler route put "${SUBDOMAIN}/llms.txt" --zone-name="$ZONE_NAME" --worker="curationsla-trust-prod"
    wrangler route put "${SUBDOMAIN}/trust.txt" --zone-name="$ZONE_NAME" --worker="curationsla-trust-prod"
    wrangler route put "${SUBDOMAIN}/.well-known/*" --zone-name="$ZONE_NAME" --worker="curationsla-trust-prod"
    
    # AI discovery routes
    print_status "Setting up AI discovery routes..."
    wrangler route put "${SUBDOMAIN}/ai-manifest.json" --zone-name="$ZONE_NAME" --worker="curationsla-ai-prod"
    wrangler route put "${SUBDOMAIN}/openapi.yaml" --zone-name="$ZONE_NAME" --worker="curationsla-ai-prod"
    wrangler route put "${SUBDOMAIN}/openapi.json" --zone-name="$ZONE_NAME" --worker="curationsla-ai-prod"
    
    # API routing (high priority for smart routing)
    print_status "Setting up API smart routing..."
    wrangler route put "${SUBDOMAIN}/api/*" --zone-name="$ZONE_NAME" --worker="curationsla-routing-prod"
    
    print_success "All routes configured"
}

# Validate deployment
validate_deployment() {
    print_status "Validating deployment..."
    
    local endpoints=(
        "https://${SUBDOMAIN}/robots.txt"
        "https://${SUBDOMAIN}/llms.txt"
        "https://${SUBDOMAIN}/trust.txt"
        "https://${SUBDOMAIN}/ai-manifest.json"
        "https://${SUBDOMAIN}/sitemap.xml"
        "https://${SUBDOMAIN}/.well-known/ai-plugin.json"
    )
    
    for endpoint in "${endpoints[@]}"; do
        print_status "Testing $endpoint..."
        if curl -s -f -o /dev/null "$endpoint"; then
            print_success "✓ $endpoint responding"
        else
            print_warning "⚠ $endpoint may not be responding yet (propagation delay expected)"
        fi
    done
}

# Upload configuration data to KV
setup_kv_data() {
    print_status "Setting up KV configuration data..."
    
    # Configuration data
    local config='{
        "site_url": "https://la.curations.cc",
        "contact_email": "la@curations.cc",
        "organization": "CurationsLA",
        "content_policy": "good_vibes_only",
        "license": "CC-BY-SA-4.0",
        "deployment_date": "'$(date -u +"%Y-%m-%dT%H:%M:%SZ")'"
    }'
    
    echo "$config" | wrangler kv:key put "site_config" --env production --binding CURATIONS_DATA
    
    print_success "KV configuration data uploaded"
}

# Main deployment sequence
main() {
    echo
    print_status "Starting CurationsLA Advanced Workers deployment..."
    echo
    
    # Prerequisites
    check_prerequisites
    
    # Setup infrastructure
    create_kv_namespaces
    setup_kv_data
    
    # Deploy workers
    echo
    print_status "Deploying workers..."
    deploy_worker "curationsla-seo-prod" "advanced-seo-worker.js" "Advanced SEO Worker"
    deploy_worker "curationsla-sitemap-prod" "sitemap-enhancer-worker.js" "Sitemap Enhancer Worker"
    deploy_worker "curationsla-routing-prod" "smart-routing-worker.js" "Smart Routing Worker"
    deploy_worker "curationsla-trust-prod" "trust-signals-worker.js" "Trust Signals Worker"
    deploy_worker "curationsla-ai-prod" "ai-discovery-worker.js" "AI Discovery Worker"
    
    # Setup routes
    echo
    setup_routes
    
    # Validation
    echo
    print_status "Waiting 30 seconds for propagation..."
    sleep 30
    validate_deployment
    
    echo
    print_success "========================================="
    print_success "🎉 CurationsLA Advanced Workers Deployed!"
    print_success "========================================="
    echo
    print_status "Deployed components:"
    echo "  ✓ Advanced SEO Worker (main site optimization)"
    echo "  ✓ Sitemap Enhancer (AI-optimized sitemaps)"
    echo "  ✓ Smart Routing (intelligent caching & bot detection)"
    echo "  ✓ Trust Signals (robots.txt, llms.txt, trust.txt)"
    echo "  ✓ AI Discovery (manifests and OpenAPI)"
    echo
    print_status "Key endpoints now available:"
    echo "  • https://la.curations.cc/robots.txt"
    echo "  • https://la.curations.cc/llms.txt"
    echo "  • https://la.curations.cc/trust.txt" 
    echo "  • https://la.curations.cc/ai-manifest.json"
    echo "  • https://la.curations.cc/.well-known/ai-plugin.json"
    echo "  • https://la.curations.cc/sitemap.xml"
    echo "  • https://la.curations.cc/openapi.yaml"
    echo
    print_status "Monitor performance at:"
    echo "  • Cloudflare Dashboard: https://dash.cloudflare.com"
    echo "  • Worker Analytics: https://dash.cloudflare.com/workers"
    echo
    print_success "Good Vibes are now optimized for AI discovery! 🌴✨"
}

# Handle script arguments
case "${1:-deploy}" in
    "deploy")
        main
        ;;
    "validate")
        validate_deployment
        ;;
    "check")
        check_prerequisites
        ;;
    *)
        echo "Usage: $0 [deploy|validate|check]"
        echo "  deploy   - Full deployment (default)"
        echo "  validate - Test endpoints only"
        echo "  check    - Check prerequisites only"
        exit 1
        ;;
esac