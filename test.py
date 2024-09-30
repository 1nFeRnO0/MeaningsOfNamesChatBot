import telebot
from telebot import types

# Токен, полученный от BotFather
API_TOKEN = '7508422440:AAHTcxW-T0hSYTYAIsapPhnrHrdivy_6c-8'

# Создаем экземпляр бота
bot = telebot.TeleBot(API_TOKEN)

# Словарь со значениями имен
name_meanings = {
    'Александр': 'Защитник людей',
    'Мария': 'Госпожа, любимая',
    'Дмитрий': 'Посвященный Деметре',
    'Анна': 'Благодать, милость',
}

# Функция обработки команды /start
@bot.message_handler(commands=['start'])
def start(message):
    # Создаем объект клавиатуры
    markup = types.InlineKeyboardMarkup()
    
    # Добавляем кнопки с именами
    for name in name_meanings.keys():
        markup.add(types.InlineKeyboardButton(text=name))

    # Отправляем приветственное сообщение с кнопками
    bot.send_message(
        message.chat.id,
        "Привет! Нажми на одно из имен или напиши свое имя для получения его значения.",
        reply_markup=markup
    )

# Функция для обработки текстовых сообщений (введенных имен)
@bot.message_handler(func=lambda message: True)
def send_name_meaning(message):
    name = message.text.strip()
    
    # Проверяем, есть ли введенное имя в словаре
    if name in name_meanings:
        meaning = name_meanings[name]
        bot.send_message(message.chat.id, f"Значение имени {name}: {meaning}")
    else:
        bot.send_message(message.chat.id, f"К сожалению, значение имени {name} не найдено.")

# Запуск бота
if __name__ == '__main__':
    bot.polling(none_stop=True)
