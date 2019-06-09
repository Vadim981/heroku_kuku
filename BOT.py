#!/usr/bin/env python
# Для того, щоб виконати код пайтона в командній строці потрібно зайти в папку даного файла
#  а потім ввести наступний код: python *.py
#import requests  # подключаємо бібліотеку реквест
import types
import pickle # бібліотека,щоб зберігати дані при перезапуску бота
# даний модуль небезпечний, так як дані, які сюди попадають і серіалізуються покищо не є небезпечними,
# але якщо при десеріалізації там буде небезпечний код, то він виконається, злоумишленник може туди розмістити небезпечний код, який тоді зможе отримати доступ до вашого телеграму
import telebot
import random
import constants
from telebot.types import Message # дана конструкція потрібна для реалізації type-notation
#TOKEN = '879369668:AAFnvJ5_LomiaWhjL9ylMTMrFD7rJnTT68w'
# = f'https://api.telegram.org/bot{TOKEN}'  # Главная ссилка, тут використовується нова можливість пітона 3.5
# так звані f- стрінги
"""
payload = {
    'chat_id': 387198245,
    'text': 'И тебе привет, Вадимка',
    'reply_to_message_id':477
}
"""
# Код описаний вижче полне фуфло, так як все це вже реалізоване в бібліотеці telebot
# r = requests.post(f'{MAIN_URL}/sendMessage',data=payload)
#print(r.json())  # ответ ми получим в джейсоне
"""
{'ok': True, 'result': [{'update_id': 582540005, 'message': {'message_id': 477,
                                                             'from': {'id': 387198245, 'is_bot': False,
                                                                      'first_name': 'Хвост', 'last_name': 'Вадим',
                                                                      'username': 'Vadim_Hvost', 'language_code': 'ru'},
                                                             'chat': {'id': 387198245, 'first_name': 'Хвост',
                                                                      'last_name': 'Вадим', 'username': 'Vadim_Hvost',
                                                                      'type': 'private'}, 'date': 1559931611,
                                                             'text': '/start', 'entities': [
        {'offset': 0, 'length': 6, 'type': 'bot_command'}]}}]}
"""
# у JAVA все статично фіксовано, питон роботає динамічно
bot = telebot.TeleBot(constants.TOKEN)
USERS = set()
@bot.message_handler(commands=['start','help'])
def command_handler (message:Message):
    bot.reply_to(message,'There is no answer =(')
@bot.message_handler(content_types=['text']) # декоратор: реагуємо тільки на текст
@bot.edited_message_handler( content_types =['text'])
def echo_digits(message: Message): # тут описується анотація типов type аnotation
    if 'Vadim' in message.text:# якщо в коді повідомлення буде зазначений текст то виконати наступну строчку кода
        bot.send_message(message.from_user.id,'Good name !!!')
        return # команда повернення д основного коду
    reply = str(random.random()) # фрагмент кода де ми перетворюємо у строку рандомне число
    if message.from_user.id in USERS: # якщо ідентифікатор юзера вже є у масиві юзерс виконуємо код представлений у тілі іфа
        reply+= f" {message.from_user.id}, hello again" # додаємо до вмісту реплая ідентифікатор юзера і смс
    bot.reply_to(message,reply)# відсилаємо сформоване смс
    USERS.add(message.from_user.id)# фрагмент кода де ідентифікатор користувача додається в  масив юзерс

@bot.message_handler(content_types=['sticker'])
def sticker_handler(message:Message):
    bot.send_sticker(message.chat.id,constants.STICKER_ID)
# Inline mode -------спеціальний режим використання бота через строку бота,якого ми використовуємо
# Наступний блок потрібний для отримання інформації про погоду з інтерфейса бота
@bot.inline_handler(lambda query:query.query =='text')
def query_text(inline_query):
    print(inline_query)
    try:
            r = types.InlineQueryResultArticle('1','Result',types.InputTextMessageContent('Result message'))
            r2 = types.InlineQueryResultArticle('2','Result2',types.InputTextMessageContent('Result message2.'))
            bot.answer_inline_query(inline_query.id,[r,r2])
    except Exception as e:
        print (e)

bot.polling(timeout=60)

