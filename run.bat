@echo off

REM Установка зависимостей
pip install -r requirements.txt

REM Запуск веб-сервера с ngrok в отдельном окне
echo Запуск веб-сервера с ngrok...
start cmd /k python server.py

REM Ждем запуска сервера и создания туннеля
echo Ожидание создания ngrok туннеля...
timeout /t 5 /nobreak > nul

REM Запуск бота
echo Запуск Telegram бота...
python bot.py

REM Остановка ngrok при завершении
echo Остановка ngrok...
taskkill /f /im ngrok.exe > nul 2>&1 