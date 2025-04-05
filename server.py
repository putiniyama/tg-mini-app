import http.server
import socketserver
import os
import time
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()

# Порт для локального сервера
PORT = 8000

class Handler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # Добавляем заголовки CORS для локальной разработки
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        http.server.SimpleHTTPRequestHandler.end_headers(self)

def main():
    print("Запуск HTTP сервера на порту", PORT)
    
    # В Docker используем внешний Nginx для HTTPS
    if os.environ.get("DOCKER_ENV"):
        print("Запущено в Docker с Nginx HTTPS прокси")
    else:
        print("Запущено локально без HTTPS")
        print("Для использования с Telegram Mini App требуется HTTPS.")
        print("Рекомендуется использовать Docker с Nginx или ngrok.")
    
    # Запускаем HTTP сервер
    with socketserver.TCPServer(("0.0.0.0", PORT), Handler) as httpd:
        print(f"Сервер запущен на порту {PORT}")
        print(f"Локальный URL: http://localhost:{PORT}")
        httpd.serve_forever()

if __name__ == "__main__":
    main() 