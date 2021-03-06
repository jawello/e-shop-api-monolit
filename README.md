# E-SHOP example 

## Описание
Сервис интерент магазин. Содержит следующий набор сущностей: 
    
    • Пользователь
    • Товар
    • Магазин
    • Корзина
    • Заказ

![Схема БД](images/db_scheme.png)

API со следующим набором функций:

    • Авторизация на портале используя связку логин — пароль от лица одного из пользователей
    • Получение данных пользователя (имя, адрес эл. Почты и т.п.)
    • Просмотр истории заказов пользователя
    • Добавление нового заказа (N книг каждая из которых в M количестве)
    • Просмотр ассортимента определенного магазина
    • Деавторизация

Фреймворк для написания API — **aiohttp**. 

Библиотека для общения с базой данных — **sqlalchemy**. 

В качесве хранилища сессий используется **Redis**.

Сервис работает на **python 3.6**.

## Общая архитектура проекта
![Схема БД](images/api_service_arch.png)

### Архитектура сервиса API
![Схема БД](images/api_service_inner_arch.png)

## Getting started
Для запуска необходимо выполнить команду: `docker-compose up --build`

После запуска поднимуться следующие контейнеры:

    • Redis
    • PostgeSQL
    • Контейнер накатываня миграций на БД (по завршению контейнер закрывается)
    • Контейнер создания тестовых данных (по завршению контейнер закрывается) 
    • Контейнер веб приложения
    * Контейнер с описанием API (swagger)
Файл shop-api.postman_collection.json содержит примеры запросов на все API.
http://127.0.0.1:8080/ - поднят swagger (не закончена документация)

Все сущности в БД создаются случайным образом. Логины созданных пользователей выводятся в коммандной строке во время создания. 

**Доступ к БД:** 
- localhost:5432 
- db_name: postgres
- user: postgres 
- password: skytrack 

У всех пользователей пароль skytrack


<!--
## Что планируется
### По сервису e-shop
- Создать единый вид ошибок
- Создать единый способ формирования ошибок
- Создать документацию 
- Пересмотреть место получения данных и формирования ответа (унифицировать обработку)
- Добавить пагинацию
- Перейти на structlog и реализовать более подробное логирование
- Реализовать нагрузочное тестирование
- Узкие места перевести на асинхроную библиотеку доступа к БД 

### По архитектуре и деплою
- Добавить ELK и настроить логироание
- Разбить монолит на микросервисы
- Добавить proxy с поддержкой авторизации и "призмеления" https (н-р nginx)
- Добавить возможность масштабирования сервисов - добавить балансировщик (HAProxy)
- Мигрировать на docker stack
- Мигрировать на k8s 
-->