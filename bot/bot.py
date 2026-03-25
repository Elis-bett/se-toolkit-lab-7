import sys
import argparse
from handlers.commands import (
    start,
    help,
    health,
    labs,
    scores,
    unknown,
    process_natural_query,
)
from config import Config


def get_handler_response(command: str, args: str = "") -> str:
    handlers = {
        "/start": start,
        "/help": help,
        "/health": health,
        "/labs": labs,
        "/scores": lambda: scores(args.strip()) if args else scores(""),
    }
    handler = handlers.get(command)
    if handler:
        return handler()
    return unknown()


def run_test_mode():
    parser = argparse.ArgumentParser()
    parser.add_argument("--test", help="Command or query to test")
    args = parser.parse_args()

    if not args.test:
        print("❌ Please provide a command or query with --test")
        sys.exit(1)

    if args.test.startswith("/"):
        parts = args.test.split(maxsplit=1)
        command = parts[0]
        argument = parts[1] if len(parts) > 1 else ""
        response = get_handler_response(command, argument)
    else:
        response = process_natural_query(args.test)

    print(response)
    sys.exit(0)


def run_telegram_mode():
    if not Config.BOT_TOKEN:
        print("❌ BOT_TOKEN not found")
        sys.exit(1)

    try:
        from telegram.ext import Application, CommandHandler, MessageHandler, filters
        from telegram import ReplyKeyboardMarkup, KeyboardButton

        keyboard = [
            [KeyboardButton("/start"), KeyboardButton("/help")],
            [KeyboardButton("/labs"), KeyboardButton("/health")],
            [
                KeyboardButton("📚 What labs are available?"),
                KeyboardButton("📊 Show me scores for lab 04"),
            ],
            [
                KeyboardButton("📉 Which lab has the lowest pass rate?"),
                KeyboardButton("💬 Hello"),
            ],
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

        app = Application.builder().token(Config.BOT_TOKEN).build()

        app.add_handler(
            CommandHandler(
                "start",
                lambda u, c: u.message.reply_text(start(), reply_markup=reply_markup),
            )
        )
        app.add_handler(
            CommandHandler("help", lambda u, c: u.message.reply_text(help()))
        )
        app.add_handler(
            CommandHandler("health", lambda u, c: u.message.reply_text(health()))
        )
        app.add_handler(
            CommandHandler("labs", lambda u, c: u.message.reply_text(labs()))
        )
        app.add_handler(
            CommandHandler(
                "scores",
                lambda u, c: u.message.reply_text(
                    scores(u.message.text.replace("/scores", "").strip())
                ),
            )
        )

        async def handle_message(update, context):
            response = process_natural_query(update.message.text)
            await update.message.reply_text(response)

        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

        print("🤖 Bot started", file=sys.stderr)
        app.run_polling()

    except ImportError:
        print("❌ python-telegram-bot not installed")
        sys.exit(1)


if __name__ == "__main__":
    if "--test" in sys.argv:
        run_test_mode()
    else:
        run_telegram_mode()
