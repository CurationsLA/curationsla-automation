#!/bin/bash

# CurationsLA Advanced Workers Validation Script
# Test all endpoints and functionality after deployment

set -e

DOMAIN="la.curations.cc"
BASE_URL="https://${DOMAIN}"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

print_status() {
    echo -e "${BLUE}[TEST]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[PASS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

print_error() {
    echo -e "${RED}[FAIL]${NC} $1"
}

# Test endpoint availability and response
test_endpoint() {
    local endpoint=$1
    local expected_content_type=$2
    local description=$3
    
    print_status "Testing $description at $endpoint"
    
    local response=$(curl -s -w "%{http_code}:%{content_type}" -o /tmp/response_body "$endpoint")
    local http_code=$(echo "$response" | cut -d':' -f1)
    local content_type=$(echo "$response" | cut -d':' -f2)
    
    if [ "$http_code" = "200" ]; then
        if [[ "$content_type" == *"$expected_content_type"* ]]; then
            print_success "$description - HTTP $http_code, Content-Type: $content_type"
            return 0
        else
            print_warning "$description - HTTP $http_code, but unexpected Content-Type: $content_type"
            return 1
        fi
    else
        print_error "$description - HTTP $http_code"
        return 1
    fi
}

# Test AI bot detection
test_ai_bot_detection() {
    print_status "Testing AI bot detection with GPTBot user agent"
    
    local response=$(curl -s -H "User-Agent: Mozilla/5.0 (compatible; GPTBot/1.0; +https://openai.com/gptbot)" \
                          -w "%{http_code}" \
                          -o /tmp/bot_response \
                          "$BASE_URL/")
    
    if [ "$response" = "200" ]; then
        if grep -q "AI Bot Detected" /tmp/bot_response 2>/dev/null; then
            print_success "AI bot detection working - GPTBot detected"
        else
            print_warning "AI bot detection may not be working - no detection signature found"
        fi
    else
        print_error "AI bot detection test failed - HTTP $response"
    fi
}

# Test schema validation
test_schema_validation() {
    print_status "Testing Schema.org markup presence"
    
    curl -s "$BASE_URL/" > /tmp/homepage_content
    
    if grep -q "application/ld+json" /tmp/homepage_content; then
        print_success "Schema.org JSON-LD markup found"
    else
        print_warning "Schema.org markup may be missing"
    fi
    
    if grep -q "CurationsLA" /tmp/homepage_content; then
        print_success "CurationsLA branding found in content"
    else
        print_warning "CurationsLA branding may be missing"
    fi
}

echo "🧪 CurationsLA Advanced Workers Validation"
echo "=========================================="
echo "Testing domain: $DOMAIN"
echo

# Core discovery files
print_status "Testing Core Discovery Files"
test_endpoint "$BASE_URL/robots.txt" "text/plain" "Robots.txt"
test_endpoint "$BASE_URL/llms.txt" "text/plain" "LLMs.txt"
test_endpoint "$BASE_URL/trust.txt" "text/plain" "Trust.txt"

echo

# AI discovery endpoints
print_status "Testing AI Discovery Endpoints"
test_endpoint "$BASE_URL/ai-manifest.json" "application/json" "AI Manifest"
test_endpoint "$BASE_URL/.well-known/ai-plugin.json" "application/json" "ChatGPT Plugin Manifest"
test_endpoint "$BASE_URL/openapi.yaml" "application/x-yaml" "OpenAPI Specification"

echo

# Sitemap endpoints
print_status "Testing Sitemap Endpoints"
test_endpoint "$BASE_URL/sitemap.xml" "application/xml" "Main Sitemap"
test_endpoint "$BASE_URL/sitemap-index.xml" "application/xml" "Sitemap Index"
test_endpoint "$BASE_URL/news-sitemap.xml" "application/xml" "News Sitemap"
test_endpoint "$BASE_URL/events-sitemap.xml" "application/xml" "Events Sitemap"
test_endpoint "$BASE_URL/api-sitemap.xml" "application/xml" "API Sitemap"

echo

# API endpoints
print_status "Testing API Endpoints"
test_endpoint "$BASE_URL/api/newsletter-today" "application/json" "Newsletter API"
test_endpoint "$BASE_URL/api/events" "application/json" "Events API"
test_endpoint "$BASE_URL/api/restaurants" "application/json" "Restaurants API"
test_endpoint "$BASE_URL/api/training-data" "application/json" "Training Data API"
test_endpoint "$BASE_URL/api/ai-context" "application/json" "AI Context API"

echo

# Well-known endpoints
print_status "Testing .well-known Endpoints"
test_endpoint "$BASE_URL/.well-known/security.txt" "text/plain" "Security.txt"
test_endpoint "$BASE_URL/.well-known/ai-plugin.json" "application/json" "AI Plugin Manifest"

echo

# Advanced functionality tests
print_status "Testing Advanced Functionality"
test_ai_bot_detection
test_schema_validation

echo

# Performance and header tests
print_status "Testing Performance Headers"
headers=$(curl -s -I "$BASE_URL/" | head -20)

if echo "$headers" | grep -q "X-AI-Optimized\|X-Bot-Detected\|X-Routing-Strategy"; then
    print_success "Advanced routing headers detected"
else
    print_warning "Advanced routing headers may not be present"
fi

if echo "$headers" | grep -q "Cache-Control"; then
    print_success "Cache-Control headers present"
else
    print_warning "Cache-Control headers may be missing"
fi

if echo "$headers" | grep -q "X-Content-Type-Options\|X-Frame-Options"; then
    print_success "Security headers present"
else
    print_warning "Security headers may be missing"
fi

echo

# Summary
echo "📊 Validation Summary"
echo "===================="
print_status "Core discovery files should be accessible for AI platforms"
print_status "API endpoints should provide structured data for training"
print_status "Sitemaps should enable comprehensive search engine discovery"
print_status "AI bot detection should optimize responses for different platforms"

echo
print_success "🎉 Validation complete! Check results above for any issues."
print_status "Monitor ongoing performance in Cloudflare Dashboard"
print_status "📧 Contact: la@curations.cc for any issues"

# Cleanup
rm -f /tmp/response_body /tmp/bot_response /tmp/homepage_content