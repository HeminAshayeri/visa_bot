import telebot
from flask import Flask, request
import os

TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(token=TOKEN)


@bot.message_handler(commands=['start'])
def welcome(message):
    welcome_text = f"user {message.from_user.first_name} Welcome to our bot!"
    bot.send_message(chat_id=message.chat.id, text=welcome_text)


# @bot.group_join_request()
@bot.chat_join_request_handler()
def handle_join_request(join_request):
    req_welcome_text = f"User: {join_request.from_user.first_name}"
    req_send_proof = """سلام وقت بخیر

جهت عضویت شما در گروه ویزای جی پزشکان موارد زیر رو بررسی بفرمایید تا در اسرع وقت عضویت شما مورد تایید قرار بگیرد 

* باتوجه به اینکه این گروه  مخصوص پزشکان، دندانپزشکان و داروسازان میباشد، ممنون میشم با 
فرستادن تصویر واضح از

۱- کارت دانشجويي
  و یا 
۲-  كارت نظام پزشکی 

بهمون اطمینان بدین پزشک، داروساز یا دندان پزشک هستین، 

۳- پروفايلتون هم اگر فعال نيست براي ادمين ها فعال كنيد 

در غیر اینصورت از عضویت و یا ادامه فعالیت شما در این گروه معذوریم
🙏

لطفا مدارک فوق رو به ای دی زیر ارسال بفرمایید:
@DrHemin

https://t.me/+4-las6zkqDZkNWNk """

    bot.send_message(chat_id=join_request.from_user.id,
                     text=f"{req_welcome_text}\n {req_send_proof}")


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
URL = f"https://visa_bot.onrender.com/{TOKEN}"
bot.remove_webhook()
bot.set_webhook(url=URL)

# Start Flask server
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
