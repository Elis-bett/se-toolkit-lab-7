def start() -> str:
    return "👋 Welcome to the SE Toolkit Lab Bot! Use /help to see available commands."


def help() -> str:
    return """Available commands:
/start - Welcome message
/help - Show this help
/health - Check backend health
/labs - List available labs
/scores <lab> - Get score for a specific lab
"""


def health() -> str:
    return "✅ Bot is running (placeholder — backend check coming soon)"


def labs() -> str:
    return "📚 Available labs: lab-01, lab-02, lab-03, lab-04, lab-05"


def scores(lab_name: str = "") -> str:
    if not lab_name:
        return "❌ Please specify a lab, e.g., /scores lab-04"
    return f"📊 Score for {lab_name}: Not implemented yet"


def unknown() -> str:
    return "❓ Unknown command. Use /help to see available commands."
