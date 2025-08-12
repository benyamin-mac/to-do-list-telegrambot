import telebot

bot = telebot.TeleBot("8137510614:AAFQozZ_yTSYAzVaWM2V7oeEP-T0o1lKPHc")

add_task_button = telebot.types.InlineKeyboardButton('افزودن یک وظیفه➕' , callback_data='add task')


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "سلام\nبه ربات برنامه ریزی خوش اومدی!🗓📒")

@bot.message_handler(commands=['planning'])
def start_planning(message):
    bot.reply_to(message , 'تو اینجا میتونی کارهای خودتو اضافه کنی👇')

bot.infinity_polling()
