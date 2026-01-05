import telebot
from telebot import types
import os
import random
from flask import Flask
from threading import Thread

# --- إعداد السيرفر لـ Render ---
app = Flask(__name__)
@app.route('/')
def home(): return "Botone is Online!"

def run():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run)
    t.start()

# --- إعداد البوت ---
TOKEN = os.getenv('BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)

# قائمة معلومات "هل تعلم"
facts = [
    "هل تعلم أن الحوت الأزرق هو أضخم حيوان على وجه الأرض؟",
    "هل تعلم أن قلب الإنسان ينبض حوالي 100 ألف مرة في اليوم؟",
    "هل تعلم أن العسل هو الطعام الوحيد الذي لا يفسد أبداً؟",
    "هل تعلم أن الأخطبوط لديه 3 قلوب و9 أدمغة؟"
]

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    btn1 = types.KeyboardButton('🆔 معلوماتي')
    btn2 = types.KeyboardButton('💡 هل تعلم؟')
    btn3 = types.KeyboardButton('✨ زخرفة اسمي')
    btn4 = types.KeyboardButton('📢 المطور')
    markup.add(btn1, btn2, btn3, btn4)
    
    bot.send_message(message.chat.id, "مرحباً بك في قائمة خدمات botone المحدثة! 🤖\nاختر خدمة من الأزرار بالأسفل:", reply_markup=markup)

@bot.message_handler(func=lambda message: True)
def handle_services(message):
    chat_id = message.chat.id
    text = message.text

    if text == '🆔 معلوماتي':
        user = message.from_user
        info = f"""
👤 معلوماتك الشخصية:
— — — — — — — — —
• اسمك: {user.first_name}
• يوزرك: @{user.username if user.username else 'لا يوجد'}
• آيديك: {user.id}
— — — — — — — — —
        """
        bot.send_message(chat_id, info, parse_mode="Markdown")

    elif text == '💡 هل تعلم؟':
        fact = random.choice(facts)
        bot.send_message(chat_id, f"💡 {fact}")

    elif text == '✨ زخرفة اسمي':
        name = message.from_user.first_name
        zakhrafa = [
            f"『{name}』", f"★{name}★", f"꧁{name}꧂", f"✨{name}✨"
        ]
        res = "إليك اسمك مزخرفاً بعدة أشكال:\n\n" + "\n".join(zakhrafa)
        bot.send_message(chat_id, res)

    elif text == '📢 المطور':
        bot.send_message(chat_id, "تم تطوير هذا البوت لخدمتك مجاناً.\nللتواصل: [  00967772786907]")

    else:
        bot.reply_to(message, "اختر خدمة من القائمة، أو انتظر تحديثات جديدة!")

if __name__ == "__main__":
    keep_alive()

    bot.infinity_polling()
