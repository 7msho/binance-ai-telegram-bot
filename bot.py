import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = os.getenv("TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🚀 Binance AI Bot\n\n"
        "Commands:\n"
        "/start - show commands\n"
        "/btc - BTC price\n"
        "/opportunity - hot USDT coins"
    )

async def btc(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        url = "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT"
        r = requests.get(url, timeout=10)
        data = r.json()

        if "price" not in data:
            await update.message.reply_text(f"API error: {data}")
            return

        await update.message.reply_text(f"BTC Price: ${data['price']}")
    except Exception as e:
        await update.message.reply_text(f"Error in /btc: {e}")

async def opportunity(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        url = "https://api.binance.com/api/v3/ticker/24hr"
        r = requests.get(url, timeout=15)
        data = r.json()

        if not isinstance(data, list):
            await update.message.reply_text(f"API error: {data}")
            return

        usdt_pairs = []
        for coin in data:
            try:
                symbol = coin["symbol"]
                change = float(coin["priceChangePercent"])
                volume = float(coin["quoteVolume"])

                if symbol.endswith("USDT") and volume > 10000000:
                    usdt_pairs.append((symbol, change, volume))
            except:
                pass

        usdt_pairs.sort(key=lambda x: x[1], reverse=True)

        if not usdt_pairs:
            await update.message.reply_text("No opportunities found.")
            return

        message = "🔥 Top Opportunities Now\n\n"
        for symbol, change, volume in usdt_pairs[:5]:
            message += f"{symbol}\nChange: {change:.2f}%\nVolume: {volume:,.0f}\n\n"

        await update.message.reply_text(message)

    except Exception as e:
        await update.message.reply_text(f"Error in /opportunity: {e}")

def main():
    if not TOKEN:
        print("TOKEN not found in environment variables")
        return

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("btc", btc))
    app.add_handler(CommandHandler("opportunity", opportunity))

    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
