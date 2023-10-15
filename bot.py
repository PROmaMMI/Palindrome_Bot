from telegram import *
from telegram.ext import *
import sqlite3
from set import TOKEN_BOT
import random

application = Application.builder().token(TOKEN_BOT).build()

conn = sqlite3.connect('mydb.db')
cursor = conn.cursor()
users = cursor.execute("SELECT user_name FROM USERS").fetchall()
names = [row[0] for row in users]
SET_KEYBOARD, CHOICE, CHECK, GENERATE = range(4)
button1 = "Проверка на палиндром"
button2 = "Генерация рандомных 3-х букв"
button3 = "/back"
button4 = "/generate"
keyboard1 = [[button1],[button2]]
keyboard2 = [[button4, button3]]
keyboard3 = [[button3]]

async def cheсk_users(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
     for i in names:
          if i == update.effective_user.username:
               await update.message.reply_text(f'{update.effective_user.username}, выбирай, что хочешь!', 
                                        reply_markup = ReplyKeyboardMarkup(keyboard1, one_time_keyboard=True))
               return CHOICE
          else:
               await update.message.reply_text("Извини, но тебя нет в базе данных.")
               return ConversationHandler.END
          
async def choice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
     if update.message.text == button1:
          await update.message.reply_text("Напиши слово или предложение и я его проверю на 'палиндромность'.")
          return CHECK
     if update.message.text == button2:
          await update.message.reply_text("Haжми /generate, чтобы сгенерировать рандомное сочетание из 3-х букв.")
          return GENERATE 

async def generate_rand(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
     await update.message.reply_text(''.join((random.choice([chr(i) for i in range(ord('А'), ord("Я")+1)]) for x in range(3))), 
                                             reply_markup = ReplyKeyboardMarkup(keyboard2))
 
async def check_pal(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
     if update.message.text.replace(' ','').lower() == ''.join(reversed(update.message.text.replace(' ','').lower())):
          await update.message.reply_photo("https://imageup.ru/img280/4376986/yes.png", reply_markup = ReplyKeyboardMarkup(keyboard3, one_time_keyboard=True))
     else:
          await update.message.reply_photo("https://imageup.ru/img76/4377006/no.jpg", reply_markup = ReplyKeyboardMarkup(keyboard3, one_time_keyboard=True))

handler = ConversationHandler(
     entry_points=[CommandHandler('start', cheсk_users)],
     states={
          CHOICE:[ 
               MessageHandler(
                    filters.COMMAND | filters.Regex('^(Проверка на палиндром|Генерация рандомных 3-х букв)$'), choice
               ),
          ],
          CHECK: [
               MessageHandler(filters.TEXT & ~filters.COMMAND, check_pal),
               CommandHandler('back', cheсk_users) 
          ],
          GENERATE: [
               CommandHandler("generate", generate_rand),
               CommandHandler("back", cheсk_users)
          ],
     },
     fallbacks=()
     )

application.add_handler(handler)

# Запуск бота
application.run_polling()
