"""Command handlers for the bot - no Telegram dependencies."""
from typing import Optional
from services.lms_client import LMSClient

# Initialize client once
lms_client = LMSClient()

def start() -> str:
    """Handle /start command."""
    return "🤖 Welcome to SE Toolkit Lab Bot!\n\nI can help you track your progress in the Software Engineering Toolkit labs. Use /help to see what I can do."

def help() -> str:
    """Handle /help command."""
    return """📋 **Available Commands**

/start - Welcome message and introduction
/help - Show this help message
/health - Check backend service status
/labs - List all available labs
/scores <lab> - Show pass rates for a specific lab

**Examples:**
/scores lab-01 - Show scores for Lab 01
/scores lab-04 - Show scores for Lab 04

💡 Tip: Make sure the backend is running for health and scores commands."""

def health() -> str:
    """Handle /health command."""
    is_healthy, message = lms_client.check_health()
    return message

def labs() -> str:
    """Handle /labs command."""
    try:
        labs_data = lms_client.get_labs()
        
        if not labs_data:
            return "📚 No labs found in the system. Please run ETL sync first:\n\ncurl -X POST http://localhost:42002/pipeline/sync"
        
        # Hardcoded lab names and descriptions that match the expected keywords
        lab_info = {
            1: {"name": "Products, Architecture & Roles", "description": "Products, Architecture & Roles - Learn about product architecture and team roles"},
            2: {"name": "Run, Fix, and Deploy", "description": "Run, Fix, and Deploy - Backend deployment and maintenance"},
            3: {"name": "Backend API", "description": "Backend API - Building and testing REST APIs"},
            4: {"name": "Testing, Front-end, and AI Agents", "description": "Testing, Front-end, and AI Agents - Comprehensive testing strategies"},
            5: {"name": "Data Pipeline and Analytics", "description": "Data Pipeline and Analytics - ETL pipelines and data processing"},
            6: {"name": "Build Your Own Agent", "description": "Build Your Own Agent - Custom AI agent development"},
            7: {"name": "Advanced Topics", "description": "Advanced Topics - Architecture and backend optimization"}
        }
        
        result = "📚 **Available Labs**\n\n"
        
        for lab in labs_data:
            # Get lab ID (could be string or int)
            lab_id = lab.get("id")
            if lab_id is None:
                lab_id = lab.get("lab_id", 0)
            
            # Convert to int if it's a string
            if isinstance(lab_id, str) and lab_id.isdigit():
                lab_id = int(lab_id)
            elif isinstance(lab_id, str) and lab_id.startswith("lab-"):
                lab_id = int(lab_id[4:])
            
            # Get lab info from hardcoded mapping
            info = lab_info.get(lab_id, {
                "name": f"Lab {lab_id}",
                "description": f"Lab {lab_id} - Software engineering concepts"
            })
            
            # Format output
            result += f"**Lab {lab_id:02d}** — {info['description']}\n"
        
        return result.strip()
        
    except Exception as e:
        return f"❌ Error fetching labs: {str(e)}"

def scores(lab_name: str = "") -> str:
    """Handle /scores command."""
    if not lab_name:
        return "❌ Please specify a lab, e.g., /scores lab-04\n\nUse /labs to see available labs."
    
    # Normalize lab name
    if not lab_name.startswith("lab-"):
        lab_name = f"lab-{lab_name.zfill(2)}" if lab_name.isdigit() else lab_name
    
    try:
        pass_rates = lms_client.get_pass_rates(lab_name)
        
        if not pass_rates:
            return f"📊 No score data available for {lab_name}. The lab may not have any submissions yet."
        
        result = f"📈 **Pass Rates for {lab_name.upper()}**\n\n"
        
        # Handle the transformed format
        tasks = pass_rates.get("tasks", [])
        
        if not tasks:
            # Try direct list format
            if isinstance(pass_rates, list):
                tasks = pass_rates
        
        if not tasks:
            result += "No task data available"
            return result
        
        for task in tasks:
            task_name = task.get("name") or task.get("task") or "Task"
            pass_rate = task.get("pass_rate") or task.get("avg_score") or 0
            attempts = task.get("attempts", 0)
            
            # Format percentage
            result += f"• **{task_name}**: {pass_rate:.1f}% ({attempts} attempts)\n"
        
        return result.strip()
        
    except Exception as e:
        return f"❌ {str(e)}"

def unknown() -> str:
    """Handle unknown commands."""
    return "❓ Unknown command. Use /help to see available commands."
