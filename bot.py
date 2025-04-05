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
    user_first_name = update.effective_user.first_name
    
    if is_https:
        # Создаем кнопку для запуска мини-приложения
        keyboard = [
            [InlineKeyboardButton("Открыть приглашение 🍷", web_app=WebAppInfo(url=WEBAPP_URL))]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        # Отправляем приветствие с кнопкой для открытия мини-приложения
        await update.message.reply_text(
            f"Привет, {user_first_name}! У тебя новое приглашение:",
            reply_markup=reply_markup
        )
    else:
        # Если URL не HTTPS, отправляем сообщение с инструкцией
        await update.message.reply_text(
            f"Привет, {user_first_name}! Mini App требует HTTPS URL.\n\n"
            f"Текущий URL: {WEBAPP_URL}\n\n"
            f"Пожалуйста, разместите приложение на сервисе с HTTPS (GitHub Pages, Netlify и т.д.)"
        )

# Функция обработки текстовых сообщений
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await start(update, context)

# Обработчик данных от мини-приложения
async def handle_webapp_data(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = update.effective_message.web_app_data.data
    
    if data == "accepted":
        await update.message.reply_text("Отлично! Буду ждать тебя с вином! 🍷")
    else:
        await update.message.reply_text(f"Получены данные: {data}")

def main():
    # Создаем экземпляр приложения, передаем токен бота
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    
    # Регистрируем обработчики команд
    app.add_handler(CommandHandler("start", start))
    
    # Регистрируем обработчик для всех текстовых сообщений
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    
    # Регистрируем обработчик для данных от мини-приложения
    app.add_handler(MessageHandler(filters.StatusUpdate.WEB_APP_DATA, handle_webapp_data))
    
    # Запускаем бота
    print("Бот запущен")
    print(f"WEBAPP_URL: {WEBAPP_URL}")
    print(f"HTTPS URL: {'Да' if is_https else 'Нет (Mini App требует HTTPS URL)'}")
    app.run_polling()

if __name__ == '__main__':
    main() 