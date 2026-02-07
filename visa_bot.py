import telebot
from flask import Flask, request
import os

TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(token=TOKEN)



@bot.message_handler(commands = ['start'], 
                     chat_types = ['private'])
def welcome(message):
    welcome_text = f"Dear {message.from_user.first_name} Welcome to our bot!"
    bot.send_message(chat_id=message.chat.id, text=welcome_text)

@bot.message_handler(func = lambda message : True, 
                     content_types = ['audio', 'photo', 'voice', 
                                      'video', 'document','text', 
                                      'location', 'contact', 'sticker'], 
                     chat_types = ['private'])
def reply_msg(message):
    if message.text != '/start':
        
        msg = f"""عزیز {message.from_user.first_name}

لطفاً برای هرگونه سوال درباره ویزای آمریکا یا شرایط عضویت در گروه، 
مستقیماً با ادمین گروه تماس بگیرید:

💬 @DrHemin

از توجه و همکاری شما سپاسگزاریم!
"""
        
        bot.reply_to(message, msg)

@bot.chat_join_request_handler()
def handle_join_request(join_request):
    req_welcome_text = f"Dear {join_request.from_user.first_name}"
    req_send_proof = """سلام و وقت بخیر 🌿
    
به گروه ویزای J ویژه پزشکان خوش آمدید 🙏🏻

برای تأیید عضویت شما و حفظ فضای تخصصی و امن گروه، لطفاً موارد زیر را با دقت بررسی و در اسرع وقت ارسال بفرمایید:

🔹 با توجه به اینکه این گروه صرفاً مخصوص پزشکان، دندانپزشکان و داروسازان می‌باشد، لطفاً برای احراز هویت حرفه‌ای خود، یکی از مدارک زیر را به‌صورت تصویر واضح ارسال نمایید:

1️⃣ کارت دانشجویی
یا
2️⃣ کارت نظام پزشکی
🔹 در صورتی که پروفایل تلگرام شما برای ادمین‌ها قابل مشاهده نیست، لطفاً آن را فعال نمایید.

❗️بدیهی است در صورت عدم ارسال مدارک فوق، امکان تأیید عضویت و یا ادامه فعالیت در گروه برای شما فراهم نخواهد بود.
🙏🏻 سپاس از همکاری شما در حفظ کیفیت و اعتبار این جمع تخصصی

لطفاً مدارک را به آیدی زیر ارسال بفرمایید:
@DrHemin

https://t.me/+4-las6zkqDZkNWNk """

    bot.send_message(chat_id=join_request.from_user.id,
                     text=f"{req_welcome_text}\n {req_send_proof}")
    
    msg = f"""New request: 
    first name: {join_request.from_user.first_name} 
    chat id: {join_request.from_user.id}"""
    
    bot.send_message(chat_id = admin, text = msg)


app = Flask(__name__)


@app.route(f"/{TOKEN}", methods=['POST'])
def webhook():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return "OK", 200


@app.route("/")
def index():
    return "Bot is running!", 200


# Set webhook

URL = f"https://visa-bot-tv1e.onrender.com/{TOKEN}"
bot.remove_webhook()
bot.set_webhook(url=URL)

# Start Flask server
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))












