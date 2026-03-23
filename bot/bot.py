import sys
import argparse
from telegram.ext import Application, CommandHandler
from handlers.commands import start, help, health, labs, scores, unknown
from config import Config


def get_handler_response(command: str, args: str = "") -> str:
    """Фабрика вызовов хендлеров для тестового режима"""
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
    """Запуск в режиме CLI тестирования"""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--test", help="Command to test, e.g., /start or /scores lab-04"
    )
    args = parser.parse_args()

    if not args.test:
        print("❌ Please provide a command with --test")
        sys.exit(1)

    parts = args.test.split(maxsplit=1)
    command = parts[0]
    argument = parts[1] if len(parts) > 1 else ""

    response = get_handler_response(command, argument)
    print(response)
    sys.exit(0)


def run_telegram_mode():
    """Запуск в режиме Telegram бота"""
    if not Config.BOT_TOKEN:
        print("❌ BOT_TOKEN not found in .env.bot.secret")
        sys.exit(1)

    app = Application.builder().token(Config.BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", lambda u, c: u.message.reply_text(start())))
    app.add_handler(CommandHandler("help", lambda u, c: u.message.reply_text(help())))
    app.add_handler(
        CommandHandler("health", lambda u, c: u.message.reply_text(health()))
    )
    app.add_handler(CommandHandler("labs", lambda u, c: u.message.reply_text(labs())))
    app.add_handler(
        CommandHandler(
            "scores", lambda u, c: scores(u.message.text.replace("/scores", "").strip())
        )
    )

    app.run_polling()


if __name__ == "__main__":
    if "--test" in sys.argv:
        run_test_mode()
    else:
        run_telegram_mode()
