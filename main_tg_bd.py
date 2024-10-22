import sqlite3
import telebot
from telebot import types
import constants

# Создание экземпляра бота с токеном (замени на свой токен)
TOKEN = constants.TG_API_TOKEN
bot = telebot.TeleBot(TOKEN)

# Логин администратора
ADMIN_LOGIN = constants.ADMIN_LOGIN

# Функция для подключения к базе данных
def connect_db():
    conn = sqlite3.connect('names.db')
    return conn

# Команда /start
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    about_btn = types.KeyboardButton("О боте")
    name_meaning_btn = types.KeyboardButton("Узнать значение имени")

    web_app = types.WebAppInfo(url="https://1nferno0.github.io/MeaningsOfNamesChatBot/")
    web_app_btn = types.KeyboardButton(text="Значение", web_app=web_app)

    markup.add(about_btn, name_meaning_btn, web_app_btn)
    bot.send_message(message.chat.id, "Привет! Выберите действие:", reply_markup=markup)

# Обработка нажатия кнопки "О боте"
@bot.message_handler(func=lambda message: message.text == "О боте")
def about_bot(message):
    bot.send_message(message.chat.id, "Этот бот позволяет узнать значения имен. Вы можете выбрать имя и получить его значение.")

# Обработка нажатия кнопки "Узнать значение имени"
@bot.message_handler(func=lambda message: message.text == "Узнать значение имени")
def get_names(message):
    # Получаем список имен из базы данных
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM names")
    names = cursor.fetchall()
    conn.close()

    # Создаем инлайн-кнопки с именами
    markup = types.InlineKeyboardMarkup()
    for name in names:
        markup.add(types.InlineKeyboardButton(text=name[0], callback_data=name[0]))
    
    bot.send_message(message.chat.id, "Выберите имя:", reply_markup=markup)

# Обработка нажатия на инлайн-кнопку с именем
@bot.callback_query_handler(func=lambda call: True)
def query_name(call):
    name = call.data

    # Получаем значение имени из базы данных
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT meaning FROM names WHERE name=?", (name,))
    result = cursor.fetchone()
    conn.close()

    if result:
        bot.send_message(call.message.chat.id, f"Значение имени {name}: {result[0]}")
    else:
        bot.send_message(call.message.chat.id, "Значение имени не найдено.")

# Функция проверки админа
def is_admin(message):
    return message.from_user.username == ADMIN_LOGIN

# Добавление имени (только для админа)
@bot.message_handler(commands=['addname'])
def add_name(message):
    if is_admin(message):
        msg = bot.send_message(message.chat.id, "Введите имя, которое хотите добавить:")
        bot.register_next_step_handler(msg, process_add_name)
    else:
        bot.send_message(message.chat.id, "У вас нет прав для выполнения этой команды.")

def process_add_name(message):
    name = message.text
    msg = bot.send_message(message.chat.id, "Введите значение имени:")
    bot.register_next_step_handler(msg, lambda msg: save_name(name, msg))

def save_name(name, message):
    meaning = message.text
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO names (name, meaning) VALUES (?, ?)", (name, meaning))
    conn.commit()
    conn.close()
    bot.send_message(message.chat.id, f"Имя '{name}' успешно добавлено.")

# Удаление имени (только для админа)
@bot.message_handler(commands=['deletename'])
def delete_name(message):
    if is_admin(message):
        msg = bot.send_message(message.chat.id, "Введите имя, которое хотите удалить:")
        bot.register_next_step_handler(msg, process_delete_name)
    else:
        bot.send_message(message.chat.id, "У вас нет прав для выполнения этой команды.")

def process_delete_name(message):
    name = message.text
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM names WHERE name=?", (name,))
    conn.commit()
    conn.close()
    bot.send_message(message.chat.id, f"Имя '{name}' успешно удалено.")

@bot.message_handler(content_types='web_app_data')
def buy_process(web_app_message): 
    DISC = {
        "1":"Происхождение имени Руслан корнями уходит в героический иранский эпос о Рустаме, сыне Залазара (поэма «Шахнамэ» персидского поэта Фирдоуси). Тюркские народы воспели его уже как Арслана Зальзара, а затем в XVII веке у славянских народов он уже фигурирует как богатырь Еруслан Залазарович, или Лазаревич.",
        "2": "Имя Антон имеет латинские корни, происходит от римского родового имени Antonius (Антониус, Антоний). Это очень древнее римское родовое имя, поэтому точное значение не известно.",
        "3": "Имя Никита в переводе с греческого языка означает «победитель». В Западной Европе можно услышать и женский вариант этого имени, он идентичен мужскому звучанию – Никита. Женское имя Никита (с ударением на последний слог) появилось после известного фильма Люка Бессона «Никита» («Nikita», «La Femme Nikita»), где главная героиня взяла себе этот псевдоним.",
        "4": "Имя Александра в переводе с греческого означает «мужественная», «защитница». Парное мужское имя – Александр. В русском, украинском и белорусском языках это имя имеет различные формы: Лександра, Ляксандра, Олекса, Алекса, Алеся, Олеся, Леся."
    }
    print(web_app_message)
    bot.send_message(web_app_message.chat.id, DISC[f'{web_app_message.web_app_data.data}']) 

# Запуск бота
bot.polling(none_stop=True)