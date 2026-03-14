import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = 8655878252:AAFnf3Wjo7FDFPkR-PhHqgC9AVCs0YEYzlk

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🚀 Welcome to Binance Opportunity Bot")

async def btc(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT"
    data = requests.get(url).json()
    price = data["price"]

    await update.message.reply_text(f"BTC price: ${price}")

async def bnb(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = "https://api.binance.com/api/v3/ticker/price?symbol=BNBUSDT"
    data = requests.get(url).json()
    price = data["price"]

    await update.message.reply_text(f"BNB price: ${price}")

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("btc", btc))
app.add_handler(CommandHandler("bnb", bnb))

app.run_polling()
