#!/usr/bin/env python3
"""
CurationsLA Enhancements Validation Script
Validates the implementation of web scraping and specialized agents
"""

import os
import json
from pathlib import Path
import sys

def validate_agents():
    """Validate specialized agent deployment"""
    agents_dir = Path(__file__).parent.parent / "agents" / "specialized"
    
    print("🤖 Validating Specialized Agents...")
    print("=" * 50)
    
    if not agents_dir.exists():
        print("❌ Specialized agents directory not found")
        return False
    
    # Expected agent files
    expected_agents = [
        "agent_la_news_001_config.json",
        "agent_biz_realestate_002_config.json", 
        "agent_entertainment_003_config.json",
        "agent_eats_004_config.json",
        "agent_community_005_config.json",
        "agent_sports_recreation_006_config.json",
        "agent_events_activities_007_config.json",
        "agent_commercial_development_008_config.json",
        "agent_shopping_commercial_009_config.json",
        "agent_arts_culture_010_config.json"
    ]
    
    found_agents = 0
    total_sources = 0
    web_scraping_sources = 0
    
    for agent_file in expected_agents:
        agent_path = agents_dir / agent_file
        if agent_path.exists():
            found_agents += 1
            
            # Load and analyze agent config
            with open(agent_path, 'r') as f:
                config = json.load(f)
            
            sources = config.get('content_sources', [])
            total_sources += len(sources)
            web_scraping_sources += len([s for s in sources if s.get('type') == 'web_scraper'])
            
            print(f"✅ {config['name']} - {len(sources)} sources")
        else:
            print(f"❌ Missing: {agent_file}")
    
    # Check coordination system
    coord_file = agents_dir / "specialized_coordination_system.json"
    coord_exists = coord_file.exists()
    
    # Check deployment report  
    report_file = agents_dir / "deployment_report.json"
    report_exists = report_file.exists()
    
    print(f"\n📊 Agent Validation Results:")
    print(f"   ✅ Agents deployed: {found_agents}/10")
    print(f"   📡 Total sources: {total_sources}")
    print(f"   🕷️  Web scraping sources: {web_scraping_sources}")
    print(f"   🔄 Coordination system: {'✅' if coord_exists else '❌'}")
    print(f"   📋 Deployment report: {'✅' if report_exists else '❌'}")
    
    return found_agents == 10 and coord_exists and report_exists

def validate_web_scraper():
    """Validate web scraper implementation"""
    print("\n🕷️  Validating Web Scraper...")
    print("=" * 50)
    
    scripts_dir = Path(__file__).parent
    web_scraper_file = scripts_dir / "web_scraper.py"
    
    if not web_scraper_file.exists():
        print("❌ Web scraper file not found")
        return False
    
    try:
        # Try to import web scraper
        sys.path.append(str(scripts_dir))
        from web_scraper import WebScraper
        
        scraper = WebScraper()
        available_scrapers = list(scraper.scrapers.keys())
        
        print(f"✅ Web scraper imported successfully")
        print(f"📊 Available scrapers: {len(available_scrapers)}")
        
        for scraper_name in available_scrapers:
            print(f"   🔧 {scraper_name}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error importing web scraper: {str(e)}")
        return False

def validate_enhanced_content_generator():
    """Validate enhanced content generator"""
    print("\n🌴 Validating Enhanced Content Generator...")
    print("=" * 50)
    
    scripts_dir = Path(__file__).parent
    content_gen_file = scripts_dir / "content_generator.py"
    
    if not content_gen_file.exists():
        print("❌ Content generator not found")
        return False
    
    # Read content generator and check for enhancements
    with open(content_gen_file, 'r') as f:
        content = f.read()
    
    enhancements = {
        'web_scraper_import': 'from web_scraper import WebScraper' in content,
        'web_scraping_available': 'WEB_SCRAPING_AVAILABLE' in content,
        'fallback_method': 'fetch_with_scraping_fallback' in content,
        'scraper_mapping': 'scraper_mapping' in content
    }
    
    print("📋 Content Generator Enhancements:")
    for enhancement, present in enhancements.items():
        status = "✅" if present else "❌"
        print(f"   {status} {enhancement.replace('_', ' ').title()}")
    
    return all(enhancements.values())

def validate_documentation():
    """Validate updated documentation"""
    print("\n📚 Validating Documentation...")
    print("=" * 50)
    
    readme_file = Path(__file__).parent.parent / "README.md"
    
    if not readme_file.exists():
        print("❌ README.md not found")
        return False
    
    with open(readme_file, 'r') as f:
        content = f.read()
    
    documentation_elements = {
        'web_scraping_mention': 'Web Scraping' in content,
        'specialized_agents': 'Specialized Deployed Agents' in content,
        'deployment_instructions': 'Deployment Instructions' in content,
        'troubleshooting_guide': 'Troubleshooting Guide' in content,
        'enhanced_system': 'Enhanced System Components' in content,
        'rss_vs_scraping': 'RSS Feed vs Web Scraping' in content
    }
    
    print("📋 Documentation Updates:")
    for element, present in documentation_elements.items():
        status = "✅" if present else "❌"
        print(f"   {status} {element.replace('_', ' ').title()}")
    
    return all(documentation_elements.values())

def validate_file_structure():
    """Validate overall file structure"""
    print("\n📁 Validating File Structure...")
    print("=" * 50)
    
    base_dir = Path(__file__).parent.parent
    
    expected_structure = {
        'scripts/web_scraper.py': 'Web scraper implementation',
        'scripts/deploy_specialized_agents.py': 'Specialized agent deployment',
        'scripts/test_web_scraping.py': 'Web scraping test suite',
        'agents/specialized/': 'Specialized agents directory',
        'README.md': 'Updated documentation'
    }
    
    all_present = True
    
    for path, description in expected_structure.items():
        full_path = base_dir / path
        exists = full_path.exists()
        status = "✅" if exists else "❌"
        print(f"   {status} {path} - {description}")
        
        if not exists:
            all_present = False
    
    return all_present

def main():
    """Run all validation checks"""
    print("🧪 CurationsLA Enhancement Validation Suite")
    print("Validating web scraping and specialized agent implementation")
    print("=" * 60)
    
    results = {
        'agents': validate_agents(),
        'web_scraper': validate_web_scraper(), 
        'content_generator': validate_enhanced_content_generator(),
        'documentation': validate_documentation(),
        'file_structure': validate_file_structure()
    }
    
    print("\n🎯 Overall Validation Results:")
    print("=" * 40)
    
    passed = 0
    total = len(results)
    
    for component, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"   {status} {component.replace('_', ' ').title()}")
        if result:
            passed += 1
    
    print(f"\n📊 Final Score: {passed}/{total} ({passed/total*100:.1f}%)")
    
    if passed == total:
        print("🎉 All enhancements successfully implemented!")
        print("🚀 CurationsLA automation system is ready for enhanced operation")
    else:
        print("⚠️  Some enhancements need attention")
        
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)