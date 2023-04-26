# «API Сервис заказа товаров для розничных сетей».

## Описание

Приложение предназначено для автоматизации закупок в розничной сети. Пользователи сервиса — покупатель (менеджер торговой сети, который закупает товары для продажи в магазине) и поставщик товаров. [Тех. задание](./README_DEV.md)

**Клиент (покупатель):**

- Менеджер закупок через API делает ежедневные закупки по каталогу, в котором
  представлены товары от нескольких поставщиков.
- В одном заказе можно указать товары от разных поставщиков — это
  повлияет на стоимость доставки.
- Пользователь может авторизироваться, регистрироваться и восстанавливать пароль через API.
    
**Поставщик:**

- Через API информирует сервис об обновлении прайса.
- Может включать и отключать прием заказов.
- Может получать список оформленных заказов (с товарами из его прайса).

### Установка 

1. Установить зависимости:
- через `pip`:

```bash
pip install -r requirements.txt
```

- или `Poetry`:
```bash
poetry install
```

2. Настроть БД или использовать [Docker-file](./Docker-compose.yml) проекта

3. Установить переменные окружения и переименовать [.dev_temp](./orders/orders/.env_dev) в .env

4. Выполнить команду:

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```


### endpoint

- register: регистрация пользователя
- activation: подтверждение email
- get-token
- user
- contacts
- orders
- orders_shop
- products
- product
- shops


**register**
Регистрация пользователя. Активация пользователя требует подтверждения email.
Автоматически отправляется письмо на email пользователя, со ссылкой для активации.
Not Authenticated.
POST

**activation**
Подтверждение email пользователя по ссылке из письма.
Not Authenticated.
PUT

**get-token**
Получение токена авторизации пользователя.
GET

**user**
Данные авторизованного пользователя
GET, PUT

**contacts**
View-set
- list: список контактов авторизованного пользователя.
- detail: данные контакта авторизованного пользователя.
GET, POST, PUT, DELETE

**basket**
View-set
- list: список товаров в корзине авторизованного пользователя
- detail: данные товара в корзине авторизованного пользователя
GET, POST, PUT, DELETE

**order_new**
Подтверждение заказа пользователем (state=new).
Проверка заказа на: Контакт, корректность товаров и их кол-ва.
Обязательно передать {'contact': <id>}
Рассылка по email магазинов в заказе.
PUT

**orders**
View-set
- list: список заказов авторизованного пользователя.
- detail: данные заказа авторизованного пользователя.
GET

**orders_shop**
View-set
- list: список заказов магазина авторизованного пользователя.
- detail: данные заказа магазина, фильтр по позициям магазина.
Только для пользователей со state=shop
GET, POST, PUT, DELETE

**category**
View-set
- list: список категорий.
- detail: данные категорий.
GET

**products**
View-set
- list: список наименований товаров.
- detail: данные наименований товаров.
GET

**product**
View-set
- list: список товаров.
- detail: данные товаров.
GET

**shops**
View-set
- list: список магазинов
- detail: данные магазина
user=buyer GET
user=shop GET, POST, PUT, DELETE

**load**
Загрузка данных магазина и товаров в БД.
С помощью файла или ссылки позиции создаются или обновляются.
user=shop POST
