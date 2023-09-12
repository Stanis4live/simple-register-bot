# Телеграм-бот для регистрации пользователей

## Обзор
Данный бот предназначен для регистрации пользователей. Пользователи могут вводить свои данные, такие как имя, фамилия 
и номер телефона. Также предусмотрена возможность редактирования этих данных.

## Функционал:
- Команда /start: начало работы с ботом, вывод пользовательского соглашения.
- Процесс регистрации: после принятия пользовательского соглашения бот запрашивает номер телефона, имя и фамилию пользователя.
- Меню редактирования: пользователи могут изменять введенные ранее данные.

## Установка и запуск:
1. Клонировать репозиторий.
2. Установить виртуальное окружение.
3. Активировать виртуальное окружение.
4. Установить необходимые зависимости.
5. Создайте файл .inv в корне проекта, а в файле переменную TELEGRAM_TOKEN
6. Применить миграции.
7. Запустить python3 bot.py
8. Запустить python3 manage.py runserver