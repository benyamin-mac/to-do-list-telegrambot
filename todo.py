import telebot
from telebot import types

bot = telebot.TeleBot("8137510614:AAFQozZ_yTSYAzVaWM2V7oeEP-T0o1lKPHc")

# دیکشنری برای نگه‌داری وظایف هر کاربر
user_tasks = {}

# دکمه افزودن وظیفه
def get_main_markup():
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("افزودن یک وظیفه➕", callback_data="add_task"))
    return markup

# هندلر شروع
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "سلام\nبه ربات برنامه ریزی خوش اومدی!🗓📒")

# هندلر برنامه‌ریزی
@bot.message_handler(commands=['planning'])
def start_planning(message):
    bot.send_message(message.chat.id,
                     "تو اینجا میتونی کارهای خودتو اضافه کنی👇",
                     reply_markup=get_main_markup())

# دکمه‌ها رو برای هر کاربر می‌سازه
def build_tasks_markup(user_id):
    markup = types.InlineKeyboardMarkup(row_width=3)
    tasks = user_tasks.get(user_id, [])
    for idx, task in enumerate(tasks):
        status_btn = types.InlineKeyboardButton("✅" if task["done"] else "❌", callback_data=f"toggle_{idx}")
        task_btn = types.InlineKeyboardButton(task["text"], callback_data="ignore")
        delete_btn = types.InlineKeyboardButton("🗑", callback_data=f"delete_{idx}")
        markup.add(status_btn, task_btn, delete_btn)
    markup.add(types.InlineKeyboardButton("افزودن یک وظیفه➕", callback_data="add_task"))
    return markup

# وقتی کاربر دکمه‌ها رو فشار میده
@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    user_id = call.message.chat.id

    if call.data == "add_task":
        bot.send_message(user_id, "لطفاً وظیفه جدیدت رو تایپ کن:")
        bot.register_next_step_handler(call.message, add_task)
    
    elif call.data.startswith("toggle_"):
        idx = int(call.data.split("_")[1])
        if user_id in user_tasks and idx < len(user_tasks[user_id]):
            user_tasks[user_id][idx]["done"] = not user_tasks[user_id][idx]["done"]
        bot.edit_message_reply_markup(user_id, call.message.message_id, reply_markup=build_tasks_markup(user_id))

    elif call.data.startswith("delete_"):
        idx = int(call.data.split("_")[1])
        if user_id in user_tasks and idx < len(user_tasks[user_id]):
            user_tasks[user_id].pop(idx)
        bot.edit_message_reply_markup(user_id, call.message.message_id, reply_markup=build_tasks_markup(user_id))

    elif call.data == "ignore":
        bot.answer_callback_query(call.id, "✅ این فقط متن وظیفه است.")

# اضافه کردن وظیفه
def add_task(message):
    user_id = message.chat.id
    task_text = message.text.strip()
    if user_id not in user_tasks:
        user_tasks[user_id] = []
    user_tasks[user_id].append({"text": task_text, "done": False})
    bot.send_message(user_id, "وظیفه اضافه شد ✅", reply_markup=build_tasks_markup(user_id))

bot.infinity_polling()
