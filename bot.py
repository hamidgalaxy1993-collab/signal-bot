# -*- coding: utf-8 -*-
import re
import telebot

TOKEN = "8836214472:AAHSQ_pU9NXd-R4jhkEI6ZQSxenYuffZ0RY"

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "سلام! متن سیگنال رو بفرست تا به فرمت ربات تریدر تبدیل کنم.")

@bot.message_handler(func=lambda m: True)
def handle_message(message):
    text = message.text

    # استخراج اطلاعات از متن فارسی
    symbol = re.search(r'رمزارز\s*([^\n]+)', text)
    symbol = symbol.group(1).strip() if symbol else "BTC"

    # تشخیص جهت (Buy/Sell)
    if "شورت" in text:
        side = "Sell"
    elif "لانگ" in text:
        side = "Buy"
    else:
        side = "Buy"  # پیش‌فرض

    # استخراج قیمت ورود
    entry = re.search(r'نقطه\s*([\d.]+)', text)
    entry = entry.group(1) if entry else "0"

    # استخراج تارگت‌ها (اولین تارگت رو به عنوان TP اصلی انتخاب می‌کنیم)
    targets = re.search(r'تارگت\s*:\s*([\d.\-]+)', text)
    if targets:
        tp_list = targets.group(1).strip().split('-')
        tp = tp_list[0] if tp_list else "0"
    else:
        tp = "0"

    # استخراج استاپ لاس
    stop = re.search(r'استاپ\s*([\d.]+)', text)
    stop = stop.group(1) if stop else "0"

    # ساخت خروجی به فرمت ربات تریدر
    result = f"{side} {symbol} {entry} TP {tp} SL {stop}"

    bot.reply_to(message, result)

print("ربات برای تریدر روشن شد!")
bot.infinity_polling()