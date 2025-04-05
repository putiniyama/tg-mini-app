# Размещение Telegram Mini App на GitHub Pages

Эта инструкция поможет вам разместить ваше Telegram Mini App на GitHub Pages, чтобы получить публичный HTTPS URL.

## Шаг 1: Создание репозитория на GitHub

1. Войдите в свой аккаунт GitHub (или зарегистрируйтесь на [github.com](https://github.com))
2. Создайте новый репозиторий, нажав на "+" в правом верхнем углу
3. Укажите имя репозитория (например, `telegram-mini-app`)
4. Выберите "Public" (публичный)
5. Нажмите "Create repository"

## Шаг 2: Загрузка файлов в репозиторий

### Вариант 1: Через Git CLI

```bash
# Клонируем репозиторий
git clone https://github.com/ваш_юзернейм/telegram-mini-app.git

# Копируем файл index.html
cp index.html telegram-mini-app/

# Переходим в директорию репозитория
cd telegram-mini-app

# Добавляем файлы в Git
git add .

# Коммитим изменения
git commit -m "Initial commit"

# Отправляем на GitHub
git push origin main
```

### Вариант 2: Через веб-интерфейс GitHub

1. Откройте свой репозиторий на GitHub
2. Нажмите "Add file" → "Upload files"
3. Перетащите файл `index.html` в браузер
4. Нажмите "Commit changes"

## Шаг 3: Настройка GitHub Pages

1. Откройте настройки репозитория (вкладка "Settings")
2. В левом меню выберите "Pages"
3. В секции "Source", выберите ветку "main" и папку "/ (root)"
4. Нажмите "Save"
5. Подождите несколько минут, пока GitHub Pages будет активирован

После активации, вы получите URL вида:
```
https://ваш_юзернейм.github.io/telegram-mini-app/
```

## Шаг 4: Обновление URL в боте

Отредактируйте файл `.env` и установите:

```
WEBAPP_URL=https://ваш_юзернейм.github.io/telegram-mini-app/
```

Теперь запустите бота:

```bash
python bot.py
```

И мини-приложение будет доступно через бота с публичным HTTPS URL. 