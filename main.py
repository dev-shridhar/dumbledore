from __future__ import annotations

import logging

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

from brain import build_messages, get_prompt_version
from config import config
from llm import chat
from memory import memory

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
logger = logging.getLogger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.message:
        return
    await update.message.reply_text(
        "ArchBot — System Design / DSA / Architecture Expert\n\n"
        "I challenge your thinking, I don't give easy answers.\n\n"
        "**How to use me:**\n"
        "• Reply to any message in this group — I'll probe the reasoning\n"
        "• `/ask <question>` — Direct expert answer\n"
        "• `/conclude` — Summarize discussion with the correct answer\n"
        "• `/clear` — Reset my memory of this group\n"
        "• `/status` — Show bot status\n"
        "• `/prompts` — Show current prompt versions"
    )


async def handle_ask(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.message:
        return
    if not context.args:
        await update.message.reply_text("Usage: `/ask <your question>`")
        return

    query = " ".join(context.args)
    chat_id = update.effective_chat
    if not chat_id:
        return

    ctx = memory.get_context(chat_id.id)
    messages = build_messages("ask", ctx, query)
    response = chat(messages)
    await update.message.reply_text(response)


async def handle_conclude(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.message:
        return
    chat_id = update.effective_chat
    if not chat_id:
        return

    ctx = memory.get_context(chat_id.id)
    if not ctx:
        await update.message.reply_text("No conversation history to conclude.")
        return

    messages = build_messages("conclude", ctx)
    response = chat(messages)
    await update.message.reply_text(response)


async def handle_clear(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.message or not update.effective_chat:
        return
    memory.clear(update.effective_chat.id)
    await update.message.reply_text("Memory cleared for this group.")


async def handle_status(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.message or not update.effective_chat:
        return
    count = memory.get_message_count(update.effective_chat.id)
    await update.message.reply_text(
        f"Messages in buffer: {count}\n"
        f"Prompt version: {get_prompt_version()}\n"
        f"Ollama model: {config.ollama_model}"
    )


async def handle_prompts(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.message:
        return
    await update.message.reply_text(f"Current prompt version: {get_prompt_version()}")


async def handle_group_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    msg = update.message
    if not msg or not msg.text or not msg.from_user or not msg.chat:
        return
    if msg.from_user.is_bot:
        return

    sender = msg.from_user.first_name or msg.from_user.username or "Unknown"
    memory.add_message(msg.chat.id, sender, msg.text, msg.message_id)

    if msg.reply_to_message and msg.reply_to_message.from_user:
        if not msg.reply_to_message.from_user.is_bot:
            ctx = memory.get_context(msg.chat.id)
            messages = build_messages("challenge", ctx, f"The last message says: {msg.text}")
            response = chat(messages)
            await msg.reply_text(response)


def main() -> None:
    if not config.telegram_token:
        raise ValueError("TELEGRAM_BOT_TOKEN not set")

    app = Application.builder().token(config.telegram_token).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", start))
    app.add_handler(CommandHandler("ask", handle_ask))
    app.add_handler(CommandHandler("conclude", handle_conclude))
    app.add_handler(CommandHandler("clear", handle_clear))
    app.add_handler(CommandHandler("status", handle_status))
    app.add_handler(CommandHandler("prompts", handle_prompts))

    app.add_handler(MessageHandler(
        filters.ChatType.GROUPS & filters.TEXT & ~filters.COMMAND,
        handle_group_message,
    ))

    logger.info("ArchBot starting...")
    app.run_polling()


if __name__ == "__main__":
    main()
