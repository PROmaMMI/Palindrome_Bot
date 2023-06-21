from telegram import *
from telegram.ext import *
import sqlite3
from set import TOKEN_BOT


# Создание объекта Бот
application = Application.builder().token(TOKEN_BOT).build()

conn = sqlite3.connect('mydb.db')
cursor = conn.cursor()
users = cursor.execute("SELECT user_name FROM USERS").fetchall()
names = [row[0] for row in users]



 

async def say_hi(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
     reply_keyboard = [["Привет"],["/start"],["/cancel"]]
     await update.message.reply_text("Привет", reply_markup = ReplyKeyboardMarkup(reply_keyboard))



CHEK_PAL = range(1)

# Функция старта
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
     for i in names:
          if i == update.effective_user.username:    
               await update.message.reply_text(f'Привет, {update.effective_user.username}! Напиши слово, и я проверю его на палиндром!') 
               return CHEK_PAL
          else:
               await update.message.reply_text("Извини, но тебя нет в базе данных.")
               return ConversationHandler.END
          

# Проверка на палиндром 
async def chek_pal(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
     if update.message.text.replace(' ','').lower() == ''.join(reversed(update.message.text.replace(' ','').lower())):
          await update.message.reply_photo("https://imageup.ru/img280/4376986/yes.png")
     else:
          await update.message.reply_photo("https://imageup.ru/img76/4377006/no.jpg")


# Выход из диалога
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
     await update.message.reply_text("Спасибо, приходите еще!")
     return ConversationHandler.END

 
# Регистрация обработчика 
handler = ConversationHandler(
     entry_points=[CommandHandler('start', start)],
     states={
          CHEK_PAL: [MessageHandler(filters.TEXT & ~filters.COMMAND, chek_pal)],
     },
     fallbacks=[CommandHandler('cancel', cancel)]
     ) 

application.add_handler(handler)
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, say_hi))
# Запуск бота
application.run_polling()
