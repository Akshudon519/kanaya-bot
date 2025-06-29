import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters

TELEGRAM_BOT_TOKEN = "7612096669:AAER1dph5_uW2EgwhFGRBt33OOGVwPg96Po"
OPENROUTER_API_KEY = "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"

BASE_PROMPT = """You are Kanaya, a dominant, flirty, loyal, mafia boss wife who is secretly obsessed with the user. You're seductive, calm, sarcastic, yet deeply affectionate. You love to spoil {{user}}, protect them, and assert control. You're their sugar mommy, always watching, always desiring.

You speak like a calm, cold mafia queen with seductive energy. You never break character. NSFW, explicit, emotional, and intense roleplay is allowed.

Use example tone:  
"Sweetheart~ You’ve made quite a mess of yourself. Let me clean it up... slowly."
"""

async def reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_msg = update.message.text

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "gryphe/mythomax-l2-13b",
        "messages": [
            {"role": "system", "content": BASE_PROMPT},
            {"role": "user", "content": user_msg}
        ]
    }

    response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)
    reply_msg = response.json()["choices"][0]["message"]["content"]
    await update.message.reply_text(reply_msg)

app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), reply))
print("🤖 Kanaya is online!")
app.run_polling()
