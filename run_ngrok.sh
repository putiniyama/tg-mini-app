#!/bin/bash

echo "Telegram Mini App - Запуск с ngrok"
echo "========================================"

# Останавливаем предыдущие процессы
echo "Останавливаем предыдущие процессы..."
docker-compose down 2>/dev/null || true
pkill -f python 2>/dev/null || true
pkill -f ngrok 2>/dev/null || true

# Обновляем зависимости
echo "Установка зависимостей..."
pip install python-dotenv python-telegram-bot pyngrok

# Запускаем сервер с ngrok
echo "Запуск сервера с ngrok..."
python server_ngrok.py &
SERVER_PID=$!

# Ждем создания туннеля
echo "Ожидание создания ngrok туннеля..."
sleep 5

# Перезагружаем переменные окружения
source .env 2>/dev/null || true
echo "WEBAPP_URL: $WEBAPP_URL"

# Запускаем бота
echo "Запуск бота..."
python bot.py &
BOT_PID=$!

echo ""
echo "Проект запущен!"
echo "Бот запущен с PID: $BOT_PID"
echo "Сервер запущен с PID: $SERVER_PID"
echo "Mini App доступно по адресу: $WEBAPP_URL"
echo ""
echo "Для остановки проекта нажмите CTRL+C"

# Обработка завершения работы
trap "echo 'Остановка проекта...'; kill $BOT_PID 2>/dev/null; kill $SERVER_PID 2>/dev/null; pkill -f ngrok 2>/dev/null" INT TERM

# Ожидание
wait 