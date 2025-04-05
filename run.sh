#!/bin/bash

# Установка зависимостей
pip install -r requirements.txt

# Запуск веб-сервера в фоновом режиме
echo "Запуск веб-сервера с ngrok..."
python server.py &
SERVER_PID=$!

# Ждем запуска сервера и создания туннеля
echo "Ожидание создания ngrok туннеля..."
sleep 5

# Перезагрузка переменных окружения
source .env 2>/dev/null || true
echo "WEBAPP_URL: $WEBAPP_URL"

# Запуск бота
echo "Запуск Telegram бота..."
python bot.py

# Обработка завершения работы
function cleanup {
  echo "Завершение работы..."
  kill $SERVER_PID
  echo "Остановка ngrok туннеля..."
  pkill -f ngrok
  exit 0
}

# Перехват сигналов для корректного завершения
trap cleanup SIGINT SIGTERM

# Ожидание завершения
wait 