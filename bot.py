import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = "8655878252:AAEQHORz7LF9DhiaeMjeV7XKN-zJXdKprR0"

# Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "🚀 Binance AI Opportunity Bot\n\n"
        "Commands:\n"
        "/btc - BTC price\n"
        "/opportunity - Find hot coins\n"
    )
    await update.message.reply_text(text)

# BTC price
async def btc(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT"
    data = requests.get(url).json()
    price = data["price"]
    await update.message.reply_text(f"BTC Price: ${price}")

# Opportunity Radar
async def opportunity(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = "https://api.binance.com/api/v3/ticker/24hr"
    data = requests.get(url).json()

    # ترتيب العملات حسب نسبة الارتفاع
    coins = sorted(data, key=lambda x: float(x["priceChangePercent"]), reverse=True)

    message = "🔥 Top Opportunities Now\n\n"

    count = 0
    for coin in coins:
        symbol = coin["symbol"]
        change = float(coin["priceChangePercent"])
        volume = float(coin["quoteVolume"])

        if "USDT" in symbol and volume > 10000000:
            message += f"{symbol}\nChange: {change:.2f}%\nVolume: {volume:,.0f}\n\n"
            count += 1

        if count == 5:
            break

    await update.message.reply_text(message)


app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("btc", btc))
app.add_handler(CommandHandler("opportunity", opportunity))

app.run_polling()
