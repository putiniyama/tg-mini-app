import http.server
import socketserver
import os
import time
from dotenv import load_dotenv
from pyngrok import ngrok, conf

# Загружаем переменные окружения
load_dotenv()

# Порт для локального сервера
PORT = 8443

class Handler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # Добавляем заголовки CORS для локальной разработки
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        http.server.SimpleHTTPRequestHandler.end_headers(self)

def main():
    # Проверяем наличие токена ngrok
    ngrok_token = os.getenv('NGROK_AUTHTOKEN')
    
    if ngrok_token and ngrok_token != "ваш_токен_ngrok":
        # Устанавливаем токен авторизации для ngrok
        print(f"Настройка ngrok с токеном...")
        conf.get_default().auth_token = ngrok_token
        
        try:
            # Открываем HTTP туннель на порт 8000
            https_tunnel = ngrok.connect(PORT, "http")
            public_url = https_tunnel.public_url
            
            # Обновляем .env файл с новым URL
            with open('.env', 'r') as file:
                env_content = file.read()
            
            new_env_content = env_content.replace(
                f"WEBAPP_URL={os.getenv('WEBAPP_URL')}",
                f"WEBAPP_URL={public_url}"
            )
            
            with open('.env', 'w') as file:
                file.write(new_env_content)
            
            print(f"ngrok туннель создан: {public_url}")
            print(f"WEBAPP_URL обновлен в .env файле")
        except Exception as e:
            print(f"Ошибка при запуске ngrok: {str(e)}")
            print("Проверьте, что токен ngrok верный и не содержит специальных символов.")
            return
    else:
        print("NGROK_AUTHTOKEN не настроен или не указан.")
        print("Для работы Telegram Mini App требуется публичный HTTPS URL.")
        print("Получите токен на https://dashboard.ngrok.com/get-started/your-authtoken")
        print("и добавьте его в файл .env как NGROK_AUTHTOKEN=ваш_токен")
        return
    
    # Запускаем HTTP сервер
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"Сервер запущен на порту {PORT}")
        print(f"Локальный URL: http://localhost:{PORT}")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("Сервер остановлен.")
            ngrok.disconnect(public_url)
            print("ngrok туннель закрыт.")

if __name__ == "__main__":
    main() 