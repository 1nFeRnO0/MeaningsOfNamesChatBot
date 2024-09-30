import telebot
from telebot import types


bot = telebot.TeleBot("7508422440:AAHTcxW-T0hSYTYAIsapPhnrHrdivy_6c-8", parse_mode=None)
names_meanings = {
    "Руслан":"Происхождение имени Руслан корнями уходит в героический иранский эпос о Рустаме, сыне Залазара (поэма «Шахнамэ» персидского поэта Фирдоуси). Тюркские народы воспели его уже как Арслана Зальзара, а затем в XVII веке у славянских народов он уже фигурирует как богатырь Еруслан Залазарович, или Лазаревич.",
    "Антон": "Имя Антон имеет латинские корни, происходит от римского родового имени Antonius (Антониус, Антоний). Это очень древнее римское родовое имя, поэтому точное значение не известно.",
    "Никита": "Имя Никита в переводе с греческого языка означает «победитель». В Западной Европе можно услышать и женский вариант этого имени, он идентичен мужскому звучанию – Никита. Женское имя Никита (с ударением на последний слог) появилось после известного фильма Люка Бессона «Никита» («Nikita», «La Femme Nikita»), где главная героиня взяла себе этот псевдоним.",
    "Александра": "Имя Александра в переводе с греческого означает «мужественная», «защитница». Парное мужское имя – Александр. В русском, украинском и белорусском языках это имя имеет различные формы: Лександра, Ляксандра, Олекса, Алекса, Алеся, Олеся, Леся."
}

# @bot.message_handler(content_types=['text'])
# def welcome_message(message):
#     # Если написали «Привет»
#     if message.text == "Привет":
#         # Пишем приветствие
#         bot.send_message(message.from_user.id, "Привет, сейчас я расскажу тебе кто ты по масти.")

@bot.message_handler(commands=['start', 'help'])
def create_buttons(message):
    keyboard = types.InlineKeyboardMarkup()
    # По очереди готовим текст и обработчик для каждого знака зодиака
    key_ruslan = types.InlineKeyboardButton(text='Руслан', callback_data='Руслан')
    # И добавляем кнопку на экран
    keyboard.add(key_ruslan)

    key_anton = types.InlineKeyboardButton(text='Антон', callback_data='Антон')
    keyboard.add(key_anton)

    key_nikita = types.InlineKeyboardButton(text='Никита', callback_data='Никита')
    keyboard.add(key_nikita)

    key_sasha = types.InlineKeyboardButton(text='Александра', callback_data='Александра')
    keyboard.add(key_sasha)

    # Показываем все кнопки сразу и пишем сообщение о выборе
    bot.send_message(message.from_user.id, text='Выбери, кто ты сегодня', reply_markup=keyboard)

# Обработчик нажатий на кнопки
@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):

    msg = names_meanings[call.data]
    # Отправляем текст в Телеграм
    bot.send_message(call.message.chat.id, msg)


# Запуск бота
if __name__ == '__main__':
    bot.polling(none_stop=True)
