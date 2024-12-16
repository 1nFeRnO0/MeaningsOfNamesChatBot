import asyncio
from telethon import TelegramClient, events
from constants import *

token_bot1 = '8028350096:AAEktNUqQcuXfVV9okLhJ9eVFazg7EBp6vE'
token_bot2 = '6248951480:AAEe0L7u2PGTezN7QIUPKKgkhs1CsBoQrHU'
api_id = TG_API_ID
api_hash = TG_API_HASH


# Введите данные для двух ботов
api_id_1 = api_id
api_hash_1 = api_hash
session_name_1 = 'SESSION_NAME_1'
bot_token_1 = token_bot1

api_id_2 = api_id
api_hash_2 =api_hash
session_name_2 = 'SESSION_NAME_2'
bot_token_2 = token_bot2

# Создаем клиентов для двух ботов
client1 = TelegramClient(session_name_1, api_id_1,
api_hash_1).start(bot_token=bot_token_1)
client2 = TelegramClient(session_name_2, api_id_2,
api_hash_2).start(bot_token=bot_token_2)


@client1.on(events.NewMessage)
async def handler1(event):
# Если сообщение в групповом чате и содержит текст "Привет от второго бота!",
 # то отправляем ответное сообщение с помощью второго клиента
    if 'Привет от второго бота!' in event.raw_text:
        await client2.send_message(event.chat_id, 'Привет от первого бота!')

@client2.on(events.NewMessage)
async def handler2(event):
	if 'Привет от первого бота!' in event.raw_text:
		await client1.send_message(event.chat_id, 'Привет от второго бота!')

# Запускаем клиенты
loop = asyncio.get_event_loop()
client1.run_until_disconnected()
loop.run_until_complete(client2.run_until_disconnected())
