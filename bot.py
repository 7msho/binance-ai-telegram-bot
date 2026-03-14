import os
import logging
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

TOKEN = os.getenv("8655878252:AAFGMnWSDJCcyDEgCgfGCqDMuSbwSuxD-ls")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🚀 Binance AI Bot\n\n"
        "Commands:\n"
        "/start\n"
        "/btc\n"
        "/opportunity"
    )

async def btc(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        r = requests.get("https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT", timeout=10)
        r.raise_for_status()
        data = r.json()
        price = data.get("price")
        if not price:
            await update.message.reply_text(f"API problem: {data}")
            return
        await update.message.reply_text(f"BTC Price: ${price}")
    except Exception as e:
        logging.exception("BTC command failed")
        await update.message.reply_text(f"Error: {e}")

async def opportunity(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        r = requests.get("https://api.binance.com/api/v3/ticker/24hr", timeout=20)
        r.raise_for_status()
        data = r.json()

        if not isinstance(data, list):
            await update.message.reply_text(f"API problem: {data}")
            return

        pairs = []
        for item in data:
            try:
                symbol = item["symbol"]
                change = float(item["priceChangePercent"])
                volume = float(item["quoteVolume"])
                if symbol.endswith("USDT") and volume > 10000000:
                    pairs.append((symbol, change, volume))
            except Exception:
                continue

        pairs.sort(key=lambda x: x[1], reverse=True)

        if not pairs:
            await update.message.reply_text("No opportunities found.")
            return

        msg = "🔥 Top Opportunities Now\n\n"
        for symbol, change, volume in pairs[:5]:
            msg += f"{symbol}\nChange: {change:.2f}%\nVolume: {volume:,.0f}\n\n"

        await update.message.reply_text(msg)

    except Exception as e:
        logging.exception("Opportunity command failed")
        await update.message.reply_text(f"Error: {e}")

def main():
    if not TOKEN:
        raise ValueError("TOKEN is missing. Add it in Railway Variables.")

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("btc", btc))
    app.add_handler(CommandHandler("opportunity", opportunity))

    logging.info("Bot started")
    app.run_polling()

if __name__ == "__main__":
    main()
