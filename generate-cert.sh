#!/bin/bash

# Создаем директорию для сертификатов, если она еще не существует
mkdir -p certs

# Генерируем самоподписанный сертификат
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout certs/key.pem \
  -out certs/cert.pem \
  -subj "/C=RU/ST=Moscow/L=Moscow/O=TelegramMiniApp/CN=localhost" \
  -addext "subjectAltName = DNS:localhost,IP:127.0.0.1"

echo "Сертификаты созданы в директории certs/"
echo "cert.pem - публичный сертификат"
echo "key.pem - приватный ключ" 