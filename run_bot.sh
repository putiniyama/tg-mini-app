#!/bin/bash

echo "Telegram Mini App - Запуск бота"
echo "========================================"

# Останавливаем предыдущие процессы
echo "Останавливаем предыдущие процессы..."
docker-compose down 2>/dev/null || true
pkill -f python 2>/dev/null || true

# Обновляем зависимости
echo "Установка зависимостей..."
pip install python-dotenv python-telegram-bot

echo "Укажите URL вашего размещенного Mini App (должен начинаться с https://):"
read webapp_url

if [[ ! "$webapp_url" =~ ^https:// ]]; then
  echo "Ошибка: URL должен начинаться с https://"
  exit 1
fi

# Обновляем .env файл с новым URL
echo "Обновление WEBAPP_URL в .env файле..."
sed -i "" "s#WEBAPP_URL=.*#WEBAPP_URL=$webapp_url#" .env

echo "WEBAPP_URL установлен: $webapp_url"

# Запускаем бота
echo "Запуск бота..."
python bot.py

echo ""
echo "Бот остановлен!" 