from telethon import TelegramClient, events
import mysql.connector
from threading import Lock
import constants

# Настройки подключения к MySQL
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'name_meanings'
}

# Подключение к базе данных с потокобезопасностью
lock = Lock()
try:
    db_connection = mysql.connector.connect(**DB_CONFIG)
    print("Успешное подключение к базе данных.")
except mysql.connector.Error as err:
    print(f"Ошибка подключения к базе данных: {err}")
    exit(1)

# Настройки Telethon
API_ID = constants.TG_API_ID
API_HASH = constants.TG_API_HASH
BOT_TOKEN = constants.TG_API_TOKEN

client = TelegramClient('name_meanings_bot', API_ID, API_HASH).start(bot_token=BOT_TOKEN)

@client.on(events.NewMessage(pattern='/start'))
async def start(event):
    await event.reply("Привет! Я бот, который расскажет значение имени.\nВведите имя, чтобы узнать его значение. Вы также можете добавить новое имя с помощью команды /add.")

@client.on(events.NewMessage(pattern='/add'))
async def add_name_prompt(event):
    await event.reply("Введите имя и значение через запятую (например, Иван, Добрый).")

    @client.on(events.NewMessage(from_users=event.sender_id))
    async def add_name_to_db(new_event):
        try:
            name, meaning = map(str.strip, new_event.text.split(",", 1))
            with lock:
                cursor = db_connection.cursor()
                cursor.execute("INSERT INTO names (name, meaning) VALUES (%s, %s)", (name, meaning))
                db_connection.commit()
                cursor.close()
            await new_event.reply(f"Имя '{name}' добавлено в базу данных со значением '{meaning}'.")
        except Exception as e:
            await new_event.reply(f"Произошла ошибка: {e}")
        finally:
            client.remove_event_handler(add_name_to_db)

@client.on(events.NewMessage)
async def get_name_meaning(event):
    name = event.text.strip()
    with lock:
        cursor = db_connection.cursor()
        cursor.execute("SELECT meaning FROM names WHERE name = %s", (name,))
        result = cursor.fetchone()
        cursor.close()
    if result:
        await event.reply(f"Значение имени '{name}': {result[0]}")
    else:
        await event.reply(f"Извините, я не знаю значения имени '{name}'. Вы можете добавить его с помощью команды /add.")

print("Бот запущен...")
client.run_until_disconnected()
