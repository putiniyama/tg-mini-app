#!/bin/bash

echo "Telegram Mini App - Запуск через Docker"
echo "========================================"

# Проверяем наличие Docker
if ! command -v docker &> /dev/null; then
    echo "Ошибка: Docker не установлен. Пожалуйста, установите Docker."
    exit 1
fi

# Проверяем наличие Docker Compose
if ! command -v docker-compose &> /dev/null; then
    echo "Ошибка: Docker Compose не установлен. Пожалуйста, установите Docker Compose."
    exit 1
fi

# Останавливаем предыдущие процессы
echo "Останавливаем предыдущие процессы..."
docker-compose down 2>/dev/null || true
pkill -f python 2>/dev/null || true
pkill -f ngrok 2>/dev/null || true

# Генерируем сертификаты, если они еще не созданы
if [ ! -f "certs/cert.pem" ] || [ ! -f "certs/key.pem" ]; then
    echo "Генерация SSL-сертификатов..."
    chmod +x generate-cert.sh
    ./generate-cert.sh
else
    echo "SSL-сертификаты уже существуют."
fi

# Запускаем проект с Docker Compose
echo "Запуск Docker-контейнеров..."
docker-compose up -d

# Ждем запуска контейнеров
echo "Ожидание запуска контейнеров..."
sleep 5

# Запускаем бота отдельно
echo "Запуск бота..."
python bot.py &
BOT_PID=$!

echo ""
echo "Проект запущен!"
echo "Бот запущен с PID: $BOT_PID"
echo "Mini App доступно по адресу: https://localhost"
echo ""
echo "Для остановки проекта нажмите CTRL+C"

# Обработка завершения работы
trap "echo 'Остановка проекта...'; kill $BOT_PID 2>/dev/null; docker-compose down" INT TERM

# Ожидание
wait 