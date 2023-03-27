import os
from aiogram import Bot, types
from aiogram.utils import executor
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import sqlite3
from modules import config, body, basedate, generate
from google.cloud import dialogflow #Модуль DialogFlow

storage = MemoryStorage()
bot = Bot(token=config.TELEGRAM_API_KEY, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=storage)

path = 'servise_code.json'
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]=path #Относительный путь к json файлу приват-ключа

session_client = dialogflow.SessionsClient() #Сессия клиента
project_id = 'small-talk-ayte' #Айди проекта берём с json файла
session_id = 'sessions' #Указываем любое значение, в моём случае "sessions"
language_code = 'ru' #Язык русский
session = session_client.session_path(project_id, session_id) #Объявляем сессию по айди проекта и айди сессии

bd = basedate.BASADATA()

body.register_handlers(dp)
generate.register_handlers(dp)

@dp.message_handler() #Хендлер без блока commands
async def ch_dialogflow(message: types.Message): #Асинк функция с атрибутом message
    text_input = dialogflow.TextInput( #Текст запроса
            text=message.text, language_code=language_code)
    query_input = dialogflow.QueryInput(text=text_input) #Ввод запроса
    response = session_client.detect_intent( #Ответ бота
        session=session, query_input=query_input)
    if response.query_result.fulfillment_text: #Если ответ имеется
        await bot.send_message(message.chat.id, response.query_result.fulfillment_text) #Отправляем его пользователю
    else: #В обратном случае
        await bot.send_message(message.chat.id, "Прости меня,но я еще не до конца могу понимать все,что ты говоришь, ведь я ИИ. Попробуй сконцтруировать правильнее запрос и снова отправить его мне:)") #Я тебя не понимаю
        
if __name__ == '__main__':
    os.system('clear')
    os.system('cls')
    print('DELTA работает стабильно!')

executor.start_polling(dp)