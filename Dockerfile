FROM python:3.11-slim

WORKDIR /app

# Копируем необходимые файлы
COPY requirements.txt .
COPY index.html .
COPY bot.py .
COPY server.py .
COPY .env .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Создаем директорию для сертификатов
RUN mkdir -p /app/certs

# Порт для нашего веб-сервера
EXPOSE 8000

# Запускаем сервер и бота
CMD ["python", "server.py"] 