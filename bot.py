from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Application, ContextTypes, ConversationHandler, CommandHandler, MessageHandler, filters
import sqlite3
from set import TOKEN_BOT
import random
from clinica import Procedure1, Procedure2, Procedure3

application = Application.builder().token(TOKEN_BOT).build()

conn = sqlite3.connect('mydb.db')
cursor = conn.cursor()
users = cursor.execute("SELECT user_name FROM USERS").fetchall()
names = [row[0] for row in users]
CHOICE, CHECK_SUM, RECEIVE_PROCEDURE = range(3)
button1 = "Информация о процедурах"
button2 = "Back"
button3 = "Exit"
button4 = "Export"
button5 = "Text"
keyboard1 = [[button1],[button3]]
keyboard2 = [[button2, button3]]
keyboard3 = [[button4], [button5],[button2, button3]]

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
     try:
          if int(update.message.text) == context.user_data["rand1"] + context.user_data["rand2"]:
               await update.message.reply_text(f'{update.effective_user.username}, выбирай, что хочешь!', 
                                        reply_markup = ReplyKeyboardMarkup(keyboard1, one_time_keyboard=True))
               return CHOICE
          else:
               await update.message.reply_text('Попробуй еще!')
     except ValueError:
          await update.message.reply_text('Попробуй еще!')

async def choice(update: Update, context: ContextTypes.DEFAULT_TYPE):
     if update.message.text == button1:
          await update.message.reply_text("В каком формате?",
                                          reply_markup = ReplyKeyboardMarkup(keyboard3))
          return RECEIVE_PROCEDURE

     if update.message.text == button3:
          await update.message.reply_text("Приходите еще!",
                                          reply_markup=ReplyKeyboardRemove())
          return ConversationHandler.END
 
async def receive_procedure(update: Update, context: ContextTypes.DEFAULT_TYPE):
     await update.message.reply_text(f"Процедуры:\n {Procedure1}\n{Procedure2}\n{Procedure3}",
                                     reply_markup = ReplyKeyboardMarkup(keyboard2, one_time_keyboard=True))
     
async def receive_procedure_csv(update: Update, context: ContextTypes.DEFAULT_TYPE):
     await update.message.reply_document(document='procedures.csv',
                                         reply_markup = ReplyKeyboardMarkup(keyboard2, one_time_keyboard=True))

async def exit(update: Update, context: ContextTypes.DEFAULT_TYPE):
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
                    filters.Regex('Информация о процедурах'), choice),
          ],
          RECEIVE_PROCEDURE: [
               MessageHandler(filters.Regex("Text"), receive_procedure),
               MessageHandler(filters.Regex("Export"), receive_procedure_csv),
               MessageHandler(filters.Regex("Back"), cheсk_users)
          ]
     },
     fallbacks=[MessageHandler(filters.Regex("Exit"), exit)],
     )

application.add_handler(handler)

# Запуск бота
application.run_polling()