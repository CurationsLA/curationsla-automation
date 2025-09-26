#!/usr/bin/env python3
"""
CurationsLA Specialized Agents Deployment
Creates and manages specialized content sourcing agents
"""

import os
import json
from pathlib import Path
from datetime import datetime
import sys

def create_agent_directory():
    """Create agents directory structure"""
    base_dir = Path(__file__).parent.parent
    agents_dir = base_dir / "agents" / "specialized"
    agents_dir.mkdir(parents=True, exist_ok=True)
    return agents_dir

def create_agent_config(agent_id, name, specialty, neighborhoods, sources, threshold=0.8):
    """Create agent configuration file"""
    config = {
        "agent_id": agent_id,
        "name": name,
        "specialty": specialty,
        "deployment_date": datetime.now().strftime("%Y-%m-%d"),
        "assigned_neighborhoods": neighborhoods,
        "content_sources": sources,
        "status": "active",
        "good_vibes_threshold": threshold,
        "success_metrics": {
            "content_items_target": 25,
            "good_vibes_score_minimum": threshold,
            "neighborhood_coverage": min(4, len(neighborhoods)),
            "source_diversity": min(4, len(sources))
        },
        "operational_guidelines": [
            "Focus on positive, community-oriented content only",
            "Exclude crime, politics, controversy, and rage-bait",
            "Prioritize new openings, celebrations, and achievements"
        ]
    }
    return config

def deploy_all_agents():
    """Deploy all 10 specialized agents"""
    print("🤖 Deploying CurationsLA Specialized Agents...")
    print("=" * 50)
    
    agents_dir = create_agent_directory()
    
    # Define agent configurations
    agents = [
        {
            "id": "agent_la_news_001",
            "name": "NewsNavigator",
            "specialty": "Breaking news, local developments, community updates",
            "neighborhoods": ["Downtown", "Hollywood", "Silver Lake", "Venice"],
            "sources": ["LAist", "LA Times", "LA Weekly", "The Eastsider LA"]
        },
        {
            "id": "agent_002",
            "name": "EatsExplorer", 
            "specialty": "Restaurant openings, food trucks, culinary events",
            "neighborhoods": ["Silver Lake", "Venice", "Downtown", "West Hollywood"],
            "sources": ["LA Eater", "LAist Food", "LA Times Food", "Infatuation LA"]
        },
        {
            "id": "agent_003",
            "name": "EventsEnthusiast",
            "specialty": "Concerts, festivals, art shows, community gatherings",
            "neighborhoods": ["Hollywood", "Arts District", "Mid-City", "Santa Monica"],
            "sources": ["LA Weekly Events", "Time Out LA", "Discover LA", "LAist Arts"]
        },
        {
            "id": "agent_004",
            "name": "CommunityConnector",
            "specialty": "Neighborhood initiatives, local heroes, community stories",
            "neighborhoods": ["Highland Park", "Boyle Heights", "Koreatown", "Little Tokyo"],
            "sources": ["The Eastsider LA", "Boyle Heights Beat", "Community News", "Local Voice"]
        },
        {
            "id": "agent_005",
            "name": "DevelopmentDetector",
            "specialty": "Urban planning, new construction, infrastructure updates",
            "neighborhoods": ["Downtown", "Hollywood", "Century City", "Playa Vista"],
            "sources": ["LA Downtown News", "Urbanize LA", "LA Business Journal", "Curbed LA"]
        },
        {
            "id": "agent_006",
            "name": "BusinessBeat",
            "specialty": "Startup launches, business openings, economic development",
            "neighborhoods": ["Santa Monica", "Culver City", "Venice", "Beverly Hills"],
            "sources": ["LA Business Journal", "Built In LA", "TechCrunch LA", "Voyage LA"]
        },
        {
            "id": "agent_007",
            "name": "EntertainmentExpert",
            "specialty": "Film premieres, TV shows, celebrity events, awards",
            "neighborhoods": ["Hollywood", "West Hollywood", "Beverly Hills", "Studio City"],
            "sources": ["Hollywood Reporter", "Variety", "Entertainment Weekly", "LA Times Entertainment"]
        },
        {
            "id": "agent_008",
            "name": "SportsSpotter",
            "specialty": "Lakers, Dodgers, Rams, Galaxy, Angels coverage",
            "neighborhoods": ["Downtown", "El Segundo", "Carson", "Anaheim"],
            "sources": ["ESPN LA", "LA Times Sports", "Lakers Nation", "Dodgers Nation"]
        },
        {
            "id": "agent_009",
            "name": "GoodiesGuru",
            "specialty": "Hidden gems, unique experiences, local secrets",
            "neighborhoods": ["Silver Lake", "Venice", "Los Feliz", "Manhattan Beach"],
            "sources": ["Secret Los Angeles", "Thrillist LA", "Atlas Obscura", "We Like LA"]
        },
        {
            "id": "agent_010",
            "name": "QualityControl",
            "specialty": "Content verification, fact-checking, Good Vibes scoring",
            "neighborhoods": ["System-wide quality assurance"],
            "sources": ["All agent outputs"],
            "threshold": 0.9
        }
    ]
    
    deployed_count = 0
    
    for agent in agents:
        config = create_agent_config(
            agent["id"],
            agent["name"],
            agent["specialty"],
            agent["neighborhoods"],
            agent["sources"],
            agent.get("threshold", 0.8)
        )
        
        config_path = agents_dir / f"{agent['id']}_config.json"
        
        try:
            with open(config_path, 'w') as f:
                json.dump(config, f, indent=2)
            
            print(f"✅ {agent['name']} ({agent['id']}) deployed successfully")
            deployed_count += 1
            
        except Exception as e:
            print(f"❌ Failed to deploy {agent['name']}: {str(e)}")
    
    # Create coordination system file
    coordination_config = {
        "system_name": "CurationsLA Specialized Agent Coordination",
        "deployment_timestamp": datetime.now().isoformat(),
        "total_agents": len(agents),
        "deployed_agents": deployed_count,
        "coordination_rules": {
            "duplicate_prevention": True,
            "content_sharing": True,
            "load_balancing": True,
            "quality_assurance": True
        },
        "performance_targets": {
            "total_content_items": 200,
            "geographic_coverage": 20,
            "category_balance": True,
            "average_good_vibes_score": 0.8,
            "web_scraping_success_rate": 0.8
        }
    }
    
    coordination_path = agents_dir / "specialized_coordination_system.json"
    
    try:
        with open(coordination_path, 'w') as f:
            json.dump(coordination_config, f, indent=2)
        print(f"✅ Coordination system configured")
    except Exception as e:
        print(f"❌ Failed to create coordination system: {str(e)}")
    
    print(f"\n🎯 Deployment Complete: {deployed_count}/{len(agents)} agents deployed")
    print(f"📁 Agent configs stored in: {agents_dir}")
    
    return deployed_count == len(agents)

def check_agent_status():
    """Check status of deployed agents"""
    print("📊 Agent Status Check")
    print("=" * 30)
    
    base_dir = Path(__file__).parent.parent
    agents_dir = base_dir / "agents" / "specialized"
    
    if not agents_dir.exists():
        print("❌ No agents directory found. Run deployment first.")
        return False
    
    config_files = list(agents_dir.glob("*_config.json"))
    
    if not config_files:
        print("❌ No agent configurations found")
        return False
    
    active_agents = 0
    total_agents = len(config_files)
    
    for config_file in config_files:
        try:
            with open(config_file, 'r') as f:
                config = json.load(f)
            
            status = config.get('status', 'unknown')
            name = config.get('name', 'Unknown')
            
            status_icon = "✅" if status == "active" else "❌"
            print(f"   {status_icon} {name}: {status}")
            
            if status == "active":
                active_agents += 1
                
        except Exception as e:
            print(f"   ❌ Error reading {config_file.name}: {str(e)}")
    
    print(f"\n📈 Summary: {active_agents}/{total_agents} agents active")
    return active_agents > 0

def reset_agents():
    """Reset all agents to active status"""
    print("🔄 Resetting Agent Status...")
    
    base_dir = Path(__file__).parent.parent
    agents_dir = base_dir / "agents" / "specialized"
    
    if not agents_dir.exists():
        print("❌ No agents directory found")
        return False
    
    config_files = list(agents_dir.glob("*_config.json"))
    reset_count = 0
    
    for config_file in config_files:
        try:
            with open(config_file, 'r') as f:
                config = json.load(f)
            
            config['status'] = 'active'
            config['last_reset'] = datetime.now().isoformat()
            
            with open(config_file, 'w') as f:
                json.dump(config, f, indent=2)
            
            reset_count += 1
            print(f"✅ Reset {config.get('name', 'Unknown')}")
            
        except Exception as e:
            print(f"❌ Failed to reset {config_file.name}: {str(e)}")
    
    print(f"\n🎯 Reset complete: {reset_count} agents")
    return reset_count > 0

def main():
    """Main deployment function"""
    if len(sys.argv) > 1:
        if sys.argv[1] == "--status":
            return check_agent_status()
        elif sys.argv[1] == "--reset":
            return reset_agents()
        elif sys.argv[1] == "--help":
            print("Usage:")
            print("  python deploy_specialized_agents.py         # Deploy all agents")
            print("  python deploy_specialized_agents.py --status  # Check agent status")
            print("  python deploy_specialized_agents.py --reset   # Reset all agents")
            return True
    
    return deploy_all_agents()

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)