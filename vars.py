import telebot
import gsheet
import redis
import os
from config import host, user, password, db_name


reminderMessage = 'Время ответить за скед!!'
notYourDayReminder = 'Вообще ты мог сегодня не писать, но раз уж написал - ответь за скед!'

google_sheet = 'rand'

time_timer = 0
all_users = {}

list_with_days = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье']

list_with_hours = {"6 часов": 6, "10 часов": 10, "12 часов": 12}

list_with_sked_hours = {"Обнови на 5" : 5, "Обнови на 6" : 6, "Обнови на 7" : 7, "Обнови на 8" : 8, "Обнови на 9" : 9, "Обнови на 10" : 10}



# getting our bots TOKEN


keyWords = ['#sked']

how_to_use_message = "Для начала зарегайтесь командой <b>/register.</b>\n " \
                     "Теперь задайте гугл таблицу <b>/add_gs 'link на таблицу'\n"\
                     "Потом настройте удобное вам время и дни недели командой <b>/settings</b>\n" \
                     "Дальше следует добавление ключевых слов, которые буду отслеживаться.\n" \
                     "#sked там уже есть. Для добавленя новых используйте команду <b>/keywords.</b>\n" \
                     "Для этого напишите\n<b>/keywords - слово, которое хотите добавить.</b>\n" \
                     "Вот и все. Бот настроен."

help_message = "Вот команды, которые вы можете использовать" \
               "\n\n" \
               "/start - включить бота\n" \
               "/help - открыть список всех команд\n" \
               "<b>/register - регистрация нового пользователя</b>\n" \
               "<b>/add_gs - добавить гугл таблицу</b>\n" \
               "/how_to_use - как использовать бота\n" \
               "/settings - настройкм\n" \
               "/time - изменить время полученмя напоминалок\n" \
               "/keywords - добавить новое ключевое слово"

dic = []
dict_with_mes_id = {}

pool = redis.ConnectionPool(host='127.0.0.1', port=6379, db=0)
redis = redis.Redis(connection_pool=pool)

bot = telebot.TeleBot('5681996034:AAFpFl2Lr4QucJF2GSgNfCFU19RE5xMR_zI')

import psycopg2

connection = psycopg2.connect(
    host=host,
    user=user,
    password=password,
    database=db_name
)


messages_need_to_answer = []
gs = gsheet.GoogleSheet()
