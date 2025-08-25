import telebot
from telebot import types
import json
import os

bot = telebot.TeleBot("8137510614:AAFQozZ_yTSYAzVaWM2V7oeEP-T0o1lKPHc")

# 📂 مسیر فایل ذخیره‌سازی
DATA_FILE = "tasks.json"

# 📌 بارگذاری داده‌ها از فایل (اگر وجود داشته باشه)
def load_tasks():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

# 📌 ذخیره‌سازی داده‌ها در فایل
def save_tasks():
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(user_tasks, f, ensure_ascii=False, indent=2)

# 📌 دیکشنری وظایف کاربران
user_tasks = load_tasks()


# ==============================
#   دکمه افزودن وظیفه
# ==============================
def get_main_markup():
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("افزودن یک وظیفه➕", callback_data="add_task"))
    return markup


# 📌 دستور start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "سلام\nبه ربات برنامه ریزی خوش اومدی!🗓📒")


# 📌 دستور planning
@bot.message_handler(commands=['planning'])
def start_planning(message):
    bot.send_message(message.chat.id,
                     "این لیست فعلی وظایف تو هست.\nمیتونی اگه چیزی خواستی از طریق دکمه ی آخر اضافه کنی.",
                     reply_markup=build_tasks_markup(message.chat.id))


# 📌 ساخت لیست دکمه‌های وظایف
def build_tasks_markup(user_id):
    markup = types.InlineKeyboardMarkup(row_width=3)
    tasks = user_tasks.get(str(user_id), [])  # کلیدها باید رشته باشن برای JSON
    for idx, task in enumerate(tasks):
        status_btn = types.InlineKeyboardButton("✅" if task["done"] else "❌", callback_data=f"toggle_{idx}")
        task_btn = types.InlineKeyboardButton(task["text"], callback_data="ignore")
        delete_btn = types.InlineKeyboardButton("🗑", callback_data=f"delete_{idx}")
        markup.add(status_btn, task_btn, delete_btn)
    markup.add(types.InlineKeyboardButton("افزودن یک وظیفه➕", callback_data="add_task"))
    return markup


# 📌 هندلر کلیک روی دکمه‌ها
@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    user_id = str(call.message.chat.id)

    if call.data == "add_task":
        bot.send_message(user_id, "لطفاً وظیفه جدیدت رو تایپ کن:")
        bot.register_next_step_handler(call.message, add_task)

    elif call.data.startswith("toggle_"):
        idx = int(call.data.split("_")[1])
        if user_id in user_tasks and idx < len(user_tasks[user_id]):
            user_tasks[user_id][idx]["done"] = not user_tasks[user_id][idx]["done"]
            save_tasks()
        bot.edit_message_reply_markup(user_id, call.message.message_id, reply_markup=build_tasks_markup(user_id))

    elif call.data.startswith("delete_"):
        idx = int(call.data.split("_")[1])
        if user_id in user_tasks and idx < len(user_tasks[user_id]):
            deleted_task = user_tasks[user_id][idx]['text']
            user_tasks[user_id].pop(idx)
            save_tasks()
            #نمایش alert برای کاربر پس از حذف یک وظیفه
            bot.answer_callback_query(call.id, f"🗑 وظیفه «{deleted_task}» حذف شد!" , show_alert=True)
        bot.edit_message_reply_markup(user_id, call.message.message_id, reply_markup=build_tasks_markup(user_id))

    elif call.data == "ignore":
        bot.answer_callback_query(call.id, "✅ این فقط متن وظیفه است.")


# 📌 اضافه کردن وظیفه
def add_task(message):
    user_id = str(message.chat.id)
    task_text = message.text.strip()
    if user_id not in user_tasks:
        user_tasks[user_id] = []
    user_tasks[user_id].append({"text": task_text, "done": False})
    save_tasks()
    bot.send_message(user_id, "وظیفه اضافه شد ✅", reply_markup=build_tasks_markup(user_id))

#تنظیمات مربوطه به اجرای ربات
if __name__ == "__main__":
    bot.remove_webhook()   # 🔴 1. وبهوک قبلی پاک میشه
    bot.infinity_polling(skip_pending=True) # ✅ 2. ربات به صورت مداوم شروع به polling میکنه
