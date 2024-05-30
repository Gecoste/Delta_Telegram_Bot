import os
from aiogram import Bot, types
from aiogram.utils import executor
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import sqlite3
from modules import body, basedate, generate
from google.cloud import dialogflow #Модуль DialogFlow
import openai
from aiogram import md
from dotenv import load_dotenv

load_dotenv()
storage = MemoryStorage()
bot = Bot(token=os.getenv("TELEGRAM_API_KEY"), parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=storage)

#path = 'servise_code.json'
#os.environ["GOOGLE_APPLICATION_CREDENTIALS"]=path #Относительный путь к json файлу приват-ключа

NUMBERS_ROWS = 6

API_KEY_GPT = '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'
openai.api_key = API_KEY_GPT

body.register_handlers(dp)
generate.register_handlers(dp)

@dp.message_handler() #Хендлер без блока commands
async def ch_chatgpt(message: types.Message): #Асинк функция с атрибутом message
    if f"{message.chat.id}.txt" not in os.listdir('users'):
        with open(f"users/{message.chat.id}.txt", "x") as f:
            f.write('')

    with open(f'users/{message.chat.id}.txt', 'r', encoding='utf-8') as file:
        oldmes = file.read()

    if message.text == '/clear':
        with open(f'users/{message.chat.id}.txt', 'w', encoding='utf-8') as file:
            file.write('')
        return bot.send_message(chat_id=message.chat.id, text='История очищена!')

    try:
        send_message = await bot.send_message(chat_id=message.chat.id, text='Обрабатываю запрос, пожалуйста подождите!')
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-0301",
            messages=[{"role": "user", "content": oldmes},
                      {"role": "user", "content": f'Предыдущие сообщения: {oldmes}; Запрос: {message.text}'}],
            presence_penalty=0.6)

        await bot.edit_message_text(text=completion.choices[0].message["content"], chat_id=message.chat.id,
                              message_id=send_message.message_id)

        with open(f'users/{message.chat.id}.txt', 'a+', encoding='utf-8') as file:
            file.write(message.text.replace('\n', ' ') + '\n' + completion.choices[0].message["content"].replace('\n',
                                                                                                                 ' ') + '\n')

        with open(f'users/{message.chat.id}.txt', 'r', encoding='utf-8') as f:
            lines = f.readlines()

        if len(lines) >= NUMBERS_ROWS + 1:
            with open(f'users/{message.chat.id}.txt', 'w', encoding='utf-8') as f:
                f.writelines(lines[2:])

    except Exception as e:
        bot.send_message(chat_id=message.chat.id, text=e)

if __name__ == '__main__':
    os.system('clear')
    os.system('cls')
    print('DELTA started | version 1.0')

executor.start_polling(dp)