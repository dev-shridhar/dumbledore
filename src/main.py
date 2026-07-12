from __future__ import annotations

import logging

from telegram import Update
from telegram.constants import ParseMode
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
        "<b>Dumbledore</b> — System Design / DSA / Architecture Expert\n\n"
        "I challenge your thinking, I don't give easy answers.\n\n"
        "<b>How to use me:</b>\n"
        "• Reply to any message in this group — I'll probe the reasoning\n"
        "• <code>/ask &lt;question&gt;</code> — Direct expert answer\n"
        "• <code>/conclude</code> — Summarize discussion with the correct answer\n"
        "• <code>/clear</code> — Reset my memory of this group\n"
        "• <code>/status</code> — Show bot status\n"
        "• <code>/prompts</code> — Show current prompt versions",
        parse_mode=ParseMode.HTML,
    )


async def handle_ask(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.message:
        return
    if not context.args:
        await update.message.reply_text(
            "Usage: <code>/ask &lt;your question&gt;</code>",
            parse_mode=ParseMode.HTML,
        )
        return

    query = " ".join(context.args)
    chat_id = update.effective_chat
    if not chat_id:
        return

    ctx = memory.get_context(chat_id.id)
    messages = build_messages("ask", ctx, query)
    response = chat(messages)
    await update.message.reply_text(response, parse_mode=ParseMode.HTML)


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
    await update.message.reply_text(response, parse_mode=ParseMode.HTML)


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
        f"<b>Bot Status</b>\n\n"
        f"• Messages in buffer: <code>{count}</code>\n"
        f"• Prompt version: <code>{get_prompt_version()}</code>\n"
        f"• Model: <code>{config.ollama_model}</code>",
        parse_mode=ParseMode.HTML,
    )


async def handle_prompts(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.message:
        return
    await update.message.reply_text(
        f"Current prompt version: <code>{get_prompt_version()}</code>",
        parse_mode=ParseMode.HTML,
    )


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
            await msg.reply_text(response, parse_mode=ParseMode.HTML)


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

    logger.info("Dumbledore starting...")
    app.run_polling()


if __name__ == "__main__":
    main()
