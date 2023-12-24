from telegram import *
from telegram.ext import *
import sqlite3
from set import TOKEN_BOT, API_NINJA
import random
import requests
from clinica import Procedure1, Procedure2, Procedure3

application = Application.builder().token(TOKEN_BOT).build()

conn = sqlite3.connect('mydb.db')
cursor = conn.cursor()
users = cursor.execute("SELECT user_name FROM USERS").fetchall()
names = [row[0] for row in users]
api_url = "https://api.api-ninjas.com/v1/webscraper?url="
CHOICE, CHECK_PAL, CHECK_SUM, GENERATE, RECEIVE_H1, RECEIVE_TITLE, RECEIVE_PROCEDURE = range(7)
button1 = "Проверка на палиндром"
button2 = "Генерация рандомных 3-х букв"
button3 = "/back"
button4 = "/generate"
button5 = "Получить заголовок h1"
button6 = "/exit"
button7 = "Получить title сайта"
button8 = "Информация о процедурах"
keyboard1 = [[button1],[button2],[button5],[button7],[button8],[button6],]
keyboard2 = [[button4, button3, button6]]
keyboard3 = [[button3, button6]]



async def cheсk_users(update: Update, context: ContextTypes.DEFAULT_TYPE):
     if update.effective_user.username in names:
          context.user_data["rand1"] = random.randrange(10,100)
          context.user_data["rand2"] = random.randrange(10,100)
          rand1 = context.user_data["rand1"]
          rand2 = context.user_data["rand2"]
          await update.message.reply_text(f'{rand1} + {rand2} = ?')
          return CHECK_SUM
     else:
          await update.message.reply_text("Извини, тебя нет в бд.")
          return ConversationHandler.END

async def check_sum(update: Update, context: ContextTypes.DEFAULT_TYPE):
     if int(update.message.text) == context.user_data["rand1"] + context.user_data["rand2"] :
          await update.message.reply_text(f'{update.effective_user.username}, выбирай, что хочешь!', 
                                        reply_markup = ReplyKeyboardMarkup(keyboard1, one_time_keyboard=True))
          return CHOICE
     else:
          await update.message.reply_text('Попробуй еще!')
          return 
     
          
async def choice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
     if update.message.text == button1:
          await update.message.reply_text("Напиши слово или предложение и я его проверю на 'палиндромность'.",
                                          reply_markup = ReplyKeyboardMarkup(keyboard3))
          return CHECK_PAL
     
     if update.message.text == button2:
          await update.message.reply_text("Haжми /generate, чтобы сгенерировать рандомное сочетание из 3-х букв.",
                                          reply_markup = ReplyKeyboardMarkup(keyboard3))           
          return GENERATE 
     
     if update.message.text == button5:
          await update.message.reply_text("Вставь ссылку и я вытащу заголовок h1.",
                                          reply_markup = ReplyKeyboardMarkup(keyboard3))
          return RECEIVE_H1
     
     if update.message.text == button7:
          await update.message.reply_text("Вставь ссылку и я вытащу title. ",
                                          reply_markup = ReplyKeyboardMarkup(keyboard3))
          return RECEIVE_TITLE
     if update.message.text == button8:
          await update.message.reply_text("Нажми /info и получи информацию о процедурах",
                                          reply_markup = ReplyKeyboardMarkup(keyboard3))
          return RECEIVE_PROCEDURE
     
     if update.message.text == button6:
          await update.message.reply_text("Приходите еще!",
                                          reply_markup=ReplyKeyboardRemove())
          return ConversationHandler.END

async def generate_rand(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
     await update.message.reply_text(''.join((random.choice([chr(i) for i in range(ord('А'), ord("Я")+1)]) for x in range(3))), 
                                             reply_markup = ReplyKeyboardMarkup(keyboard2))
 
async def check_pal(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
     if update.message.text.replace(' ','').lower() == ''.join(reversed(update.message.text.replace(' ','').lower())):
          await update.message.reply_photo("https://imageup.ru/img280/4376986/yes.png", 
                                           reply_markup = ReplyKeyboardMarkup(keyboard3, one_time_keyboard=True))
     else:
          await update.message.reply_photo("https://imageup.ru/img76/4377006/no.jpg", 
                                           reply_markup = ReplyKeyboardMarkup(keyboard3, one_time_keyboard=True))
          
async def receive_h1(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
     txt = requests.get(f'{api_url}{update.message.text}',
                         headers={'X-Api-Key': API_NINJA}).text
     start = txt.find("<h1>") + 4
     end = txt.rfind("</h1>")
     await update.message.reply_text(txt[start:end],
                                     reply_markup = ReplyKeyboardMarkup(keyboard3, one_time_keyboard=True))
     
async def receive_title(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
     txt = requests.get(f'{api_url}{update.message.text}',
                         headers={'X-Api-Key': API_NINJA}).text
     start = txt.casefold().find("<title>") + 7
     end = txt.casefold().rfind("</title>")
     await update.message.reply_text(txt[start:end].encode("utf-8").decode("unicode-escape"),
                                     reply_markup = ReplyKeyboardMarkup(keyboard3, one_time_keyboard=True))
     
async def receive_procedure(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
     await update.message.reply_text(f"Процедуры:\n {Procedure1}\n{Procedure2}\n{Procedure3}",
                                     reply_markup = ReplyKeyboardMarkup(keyboard3, one_time_keyboard=True))

async def exit(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
     await update.message.reply_text('Приходите еще!', reply_markup=ReplyKeyboardRemove())
     return ConversationHandler.END

handler = ConversationHandler(
     entry_points=[CommandHandler('start', cheсk_users)],
     states={
          CHECK_SUM:[
               MessageHandler(filters.TEXT, check_sum) 
          ],
          CHOICE:[ 
               MessageHandler(
                    filters.COMMAND | filters.Regex(
                         '^(Проверка на палиндром|Генерация рандомных 3-х букв|Получить заголовок h1|Получить title сайта|Информация о процедурах)$'), choice
               ),
          ],
          CHECK_PAL: [
               MessageHandler(filters.TEXT & ~filters.COMMAND, check_pal),
               CommandHandler('back', cheсk_users) 
          ],
          GENERATE: [
               CommandHandler("generate", generate_rand),
               CommandHandler('back', cheсk_users)
          ],
          RECEIVE_H1: [
               MessageHandler(filters.TEXT & ~filters.COMMAND, receive_h1),
               CommandHandler('back', cheсk_users) 
          ],
          RECEIVE_TITLE: [
               MessageHandler(filters.TEXT & ~filters.COMMAND, receive_title),
               CommandHandler('back', cheсk_users) 
          ],
          RECEIVE_PROCEDURE: [
               CommandHandler("info", receive_procedure),
               CommandHandler('back', cheсk_users)
          ]
     },
     fallbacks=[CommandHandler("exit", exit)],
     )

application.add_handler(handler)

# Запуск бота
application.run_polling()