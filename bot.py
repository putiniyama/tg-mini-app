import logging
import os
from dotenv import load_dotenv
from telegram import Update, WebAppInfo, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters

# Загружаем переменные окружения из .env файла
load_dotenv()

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Получаем токен и URL из переменных окружения
BOT_TOKEN = os.getenv('BOT_TOKEN')
WEBAPP_URL = os.getenv('WEBAPP_URL')

# Проверяем, является ли URL HTTPS
is_https = WEBAPP_URL.startswith("https://")

# Функция обработки команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if is_https:
        # Создаем кнопку для запуска мини-приложения
        keyboard = [
            [InlineKeyboardButton("Запустить приложение", web_app=WebAppInfo(url=WEBAPP_URL))]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            "Привет! Нажмите на кнопку ниже, чтобы открыть мини-приложение:",
            reply_markup=reply_markup
        )
    else:
        # Если URL не HTTPS, отправляем сообщение с инструкцией
        await update.message.reply_text(
            f"Привет! Mini App требует HTTPS URL.\n\n"
            f"Текущий URL: {WEBAPP_URL}\n\n"
            f"Пожалуйста, настройте ngrok, добавив ваш токен в .env файл:\n"
            f"NGROK_AUTHTOKEN=ваш_токен_ngrok\n\n"
            f"Получить токен можно на: https://dashboard.ngrok.com/get-started/your-authtoken"
        )

# Функция обработки текстовых сообщений
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await start(update, context)

def main():
    # Создаем экземпляр приложения, передаем токен бота
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    
    # Регистрируем обработчики команд
    app.add_handler(CommandHandler("start", start))
    
    # Регистрируем обработчик для всех текстовых сообщений
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    
    # Запускаем бота
    print("Бот запущен")
    print(f"WEBAPP_URL: {WEBAPP_URL}")
    print(f"HTTPS URL: {'Да' if is_https else 'Нет (Mini App требует HTTPS URL)'}")
    app.run_polling()

if __name__ == '__main__':
    main() 