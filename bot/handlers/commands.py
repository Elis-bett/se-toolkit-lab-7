"""Command handlers for the bot - no Telegram dependencies."""
from typing import Optional
from services.lms_client import LMSClient

# Initialize client once
lms_client = LMSClient()

def start() -> str:
    """Handle /start command."""
    return "👋 Welcome to SE Toolkit Lab Bot! I can help you check lab scores and backend status. Use /help to see available commands."

def help() -> str:
    """Handle /help command."""
    return """🤖 Available commands:

/start - Welcome message
/help - Show this help message
/health - Check backend health status
/labs - List all available labs
/scores <lab> - Show pass rates for a specific lab (e.g., /scores lab-04)

📝 Note: All commands require the backend to be running."""

def health() -> str:
    """Handle /health command."""
    is_healthy, message = lms_client.check_health()
    return message

def labs() -> str:
    """Handle /labs command."""
    try:
        labs_data = lms_client.get_labs()
        
        if not labs_data:
            return "📚 No labs found in the system. Please run ETL sync first."
        
        result = "📚 Available Labs:\n\n"
        for lab in labs_data:
            name = lab.get("name", "Unnamed")
            lab_id = lab.get("id", "unknown")
            description = lab.get("description", "No description")
            result += f"**{name}** (`{lab_id}`)\n"
            result += f"   {description}\n\n"
        
        return result.strip()
    except Exception as e:
        return f"❌ Error fetching labs: {str(e)}"

def scores(lab_name: str = "") -> str:
    """Handle /scores command."""
    if not lab_name:
        return "❌ Please specify a lab, e.g., /scores lab-04\n\nUse /labs to see available labs."
    
    try:
        pass_rates = lms_client.get_pass_rates(lab_name)
        
        if not pass_rates or "tasks" not in pass_rates:
            return f"📊 No score data available for {lab_name}. The lab may not have any submissions yet."
        
        result = f"📈 Pass Rates for {lab_name}:\n\n"
        
        for task in pass_rates.get("tasks", []):
            task_name = task.get("name", "Unnamed Task")
            pass_rate = task.get("pass_rate", 0)
            attempts = task.get("attempts", 0)
            result += f"• {task_name}: {pass_rate:.1f}% ({attempts} attempts)\n"
        
        return result.strip()
        
    except Exception as e:
        # Error already formatted in LMSClient, just return it
        return f"❌ {str(e)}"

def unknown() -> str:
    """Handle unknown commands."""
    return "❓ Unknown command. Use /help to see available commands."
