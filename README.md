# HomeDesk-Solutions <a name="top"></a>

![HomeDesk-Solutions](logo/hds-beta-logo.png)

[![version](https://img.shields.io/badge/Version-BETA-BrightGreen)](https://github.com/MB6718/HomeDesk-Solutions/)
[![python-version](https://img.shields.io/badge/Python-v3.8-blue)](https://www.python.org/downloads/release/python-383rc1/)
[![platform](https://img.shields.io/badge/platform-windows%20%7C%20linux%20%7C%20macos-LightGray)](https://ru.wikipedia.org/wiki/%D0%9A%D1%80%D0%BE%D1%81%D1%81%D0%BF%D0%BB%D0%B0%D1%82%D1%84%D0%BE%D1%80%D0%BC%D0%B5%D0%BD%D0%BD%D0%BE%D1%81%D1%82%D1%8C)
[![license](https://img.shields.io/badge/license-GPL_v3.0-yellow)](https://github.com/MB6718/HomeDesk-Solutions/blob/master/LICENSE)
[![framework](https://img.shields.io/badge/framework-Flask_1.1.12-ff69b4)](https://flask.palletsprojects.com/en/1.1.x/)
[![database](https://img.shields.io/badge/database-SQLite-Green)](https://www.sqlite.org/index.html)

### Содержание
* [Краткое описание](#description)
* [Техническое задание и концепция проекта](#concept)
* [Подготовка к запуску](#firstrun)
* [Спецификация (Формат описания API запросов/ответов)](#apispec)
	* [POST /auth/login](#login)
	* [POST /auth/logout](#logout)
	* [POST /users](#user_registration)
	* [GET /categories](#get_category)
	* [GET /categories/&lt;int:category_id&gt;](#get_category_id)
	* [POST /categories](#add_category)
	* [PATCH /categories/&lt;int:category_id&gt;](#edit_category_id)
	* [DELETE /categories/&lt;int:category_id&gt;](#del_category_id)
	* [POST /transactions](#posttrans)
	* [GET /transactions/&lt;int:transaction_id&gt;](#get_transaction_id)
	* [PATCH /transactions/&lt;int:transaction_id&gt;](#patchtrans_id)
	* [DELETE /transactions/&lt;int:transaction_id&gt;](#deltrans_id)
	* [GET /report](#get_report)
* [Примеры API запросов и Тесты](#examples)
* [Построен с использованием](#build_with)
* [Авторы](#authors)
* [Лицензия](#license)

### Краткое описание <a name="description"></a>
Данное приложение HomeDesk-Solutions, REST API серверная часть сайта-сервиса для учёта и анализа личных финансов.

Приложение реализовано с помощью web-фреймворка Flask.

### Техническое задание и концепция проекта <a name="concept"></a>
[Техническое задание и Спецификация API v1.0](https://docs.google.com/document/d/1s0gNeP3KrxJHMbYMV39MfNtt7Q3iOBBALYNGqWocjwA)  
[Концептуальная модель БД](https://app.creately.com/diagram/Q8o4micJQkM/view)  
[Логическая модель БД](https://dbdesign.online/model/TYq7nwh1XueR)

### Подготовка и запуск <a name="firstrun"></a>
Пошаговая инструкция по запуску приложения на локальном компьютере:
* под Windows
	1. Скачать архив с исходным кодом и распаковать в любую удобную папку
	2. В корне проекта создать файл .env, содержащий четыре строки:
		```bash
		PYTHONPATH=src # путь к исходнику проекта
		DB_FILE=db.sqlite # путь к файлу базы данных SQLite
		SECRET_KEY=1234567890 # секретный ключ (!) заменить на свой
		```
	3. Выполнить скрипт для создания пустой БД
		```bash
		python create_db.py # после выполнения появится файл БД с именем "db.sqlite"
		```
	4. Создать и запустить виртуальное окружение в корне проекта, подтянуть необходимые зависимости
		```bash
		python -m venv .venv # создаём виртуальное окружение
		.venv\Scripts\activate.bat # активируем виртуальное окружение
		(.venv) python -V # проверяем версию интерпретатора Python, убеждаясь в работе окружения
		(.venv) pip install -r requirements.txt # устанавливаем необходимые пакеты
		(.venv) flask run # запустим локальный сервер Flask
		```
	5. Можно приступать к тестированию API функционала приложения
* под Linux (Ubuntu 20.04)
	1. Скачать архив с исходным кодом и распаковать в любую удобную папку
	2. В корне проекта создать файл .env, содержащий четыре строки:
		```bash
		PYTHONPATH=src # путь к исходнику проекта
		DB_FILE=db.sqlite # путь к файлу базы данных SQLite
		SECRET_KEY=1234567890 # секретный ключ (!) заменить на свой
		```
	3. Выполнить скрипт для создания пустой БД
		```bash
		python3 create_db.py # после выполнения появится файл БД с именем "db.sqlite"
		```
	4. Создать и запустить виртуальное окружение в корне проекта, подтянуть необходимые зависимости
		```bash
		python3 -m venv .venv # создаём виртуальное окружение
		source .venv/bin/activate # активируем виртуальное окружение
		(.venv) python -V # проверяем версию интерпретатора Python, убеждаясь в работе окружения
		(.venv) pip install -r requirements.txt # устанавливаем необходимые пакеты
		(.venv) flask run # запустим локальный сервер Flask
		```
	5. Можно приступать к тестированию API функционала приложения
<p align="right"><a href="#top">[ Наверх ]</a></p>

### Спецификация (Формат описания API запросов/ответов): <a name="apispec"></a>
* запросы и ответы представлены в JSON-подобной структуре и описывают JSON-документы
* через двоеточие указываются типы полей
* запись вида ?type обозначает, что поле необязательное и может отсутствовать
* запись вида [type] обозначает список значений типа type

<a name="login"></a> 
&#9660; Аутентификация: вход и выход.  

**POST** &rArr; `/auth/login`  
Request:
```
{
  "email" : str,
  "password" : str
}
```
Response code:
> **200** - Вход произведён успешно  
> **400** - Не задано обязательное поле в JSON запросе  
> **403** - Неверный пароль или Логин не зарегистрирован в системе

<a name="logout"></a>
**POST** &rArr; `/auth/logout`  
Response code:
> **200** - Выход произведён успешно
<p align="right"><a href="#top">[ Наверх ]</a></p>

<a name="user_registration"></a>
&#9660; Регистрация нового пользователя в системе.  

**POST** &rArr; `/users`  
Request:
```
{
  "first_name" : str,
  "last_name" : str,
  "email" : str,
  "password" : str
}
```
Response:
```
{
  "id" : int, 
  "first_name" : str,
  "last_name" : str,
  "email" : str
}
```
Response code:
> **201** - Пользователь успешно зарегистрирован  
> **400** - Не задано обязательное поле в JSON запросе  
> **409** - Логин `email` уже существует (зарегистрирован) в системе
<p align="right"><a href="#top">[ Наверх ]</a></p>

<a name="get_category"></a>
&#9660; Получение информации о всех имеющихся категориях пользователя по его ID в текущей сессии. Доступно только аутентифицированному пользователю.  

**GET** &rArr; `/categories`  
Response:
```
[
  {
    "id" : int,
    "name" : str,
    "subcategory" : [
      {
        "id" : int,
        "name" : str,
        "subcategory" : [ ]
      },
      {
        … n …
      }
    ],
  },
  {
    … n …
  }
]
```
Response code:
> **200** - Категория/дерево категорий получено успешно
> **403** - Получение категорий невозможно, пользователь не аутентифицирован
<p align="right"><a href="#top">[ Наверх ]</a></p>

<a name="get_category_id"></a>
&#9660; Возвращаем полное дерево категорий начиная с категории "category_id". Если категория не содержит дочерних категорий, выводим только её.  

**GET** &rArr; `/categories/<int:category_id>`  
Response:
```
{
  "id" : int, <category_id>
  "name" : str,
  "subcategory" : [
    {
      "id" : int,
      "name" : str,
      "subcategory" : [ ]
    },
    {
      … n …
    }
  ]
}
```
Response code:
> **200** - Категория/дерево категорий получено успешно  
> **403** - Тек. пользователь не является владельцем `category_id` категории    
> **404** - Категория `category_id` не существует
<p align="right"><a href="#top">[ Наверх ]</a></p>

<a name="add_category"></a>
&#9660; Добавление категории, если категория удачно создана или уже существует, то возвращаем полное дерево категорий начиная с родителя (если передан в request) и заканчивая "name" категорией. Доступно только аутентифицированному пользователю.  

**POST** &rArr; `/categories`  
Request:
```
{
  "name" : str,
  "parent_id" : ?int 
}
```
Response (Если указан "parent_id"):
```
{
  "id" : int,
  "name" : str,
  "subcategory" : 
  {
    "id" : int,
    "name" : str
  }
}
```
Response (в иных случаях):
```
{
  "id" : int,
  "name" : str
}
```
Response code:
> **200** - Категория создана успешно  
> **400** - Не задано обязательное поле `name` в JSON запросе  
> **403** - Тек. пользователь не является владельцем `parent_id` категории  
> **404** - Категория `parent_id` не существует  
> **409** - Категория с именем `name` уже существует
<p align="right"><a href="#top">[ Наверх ]</a></p>

<a name="edit_category_id"></a>
&#9660; Редактирование существующей категории. Обновляем имя "name" категории и/или значение "parent_id" связи, если в request пришёл "id" нового родителя. Редактировать категорию может только владелец (пользователь, создавший её). Доступно только аутентифицированному пользователю.  

**PATCH** &rArr; `/categories/<int:category_id>`  
Request:
```
{
  "name" : ?str,
  "parent_id" : ?int 
}
```
Response (Если указан "parent_id"):
```
{
  "id" : int,
  "name" : str,
  "subcategory" : 
  {
    "id" : int,
    "name" : str
  }
}
```
Response (в иных случаях):
```
{
  "id" : int,
  "name" : str
}
```
Response code:
> **200** - Категория изменена успешно  
> **403** - Тек. пользователь не является владельцем `parent_id` категории  
> **404** - Категория `parent_id` не существует  
> **409** - Категория с именем `name` уже существует
<p align="right"><a href="#top">[ Наверх ]</a></p>

<a name="del_category_id"></a>
&#9660; Удаление категории. Удаляем категорию и каскадно все наследующие от нее категории (связи). Удалить категорию может только владелец (пользователь, создавший её). Доступно только аутентифицированному пользователю.  

**DELETE** &rArr; `/categories/<int:category_id>`
Response code:
> **204** - Категория удалена успешно  
> **403** - Тек. пользователь не является владельцем `category_id` категории  
> **404** - Категория `category_id` не существует
<p align="right"><a href="#top">[ Наверх ]</a></p>

<a name="posttrans"></a>
&#9660; Добавление финансовой операции. Доступно только аутентифицированному пользователю.  

**POST** &rArr; `/transactions`  
Request:
```
{
  "type" : str,
  "amount" : str, (дробное число типа 189945,56)
  "comment" : ?str,
  "date" : ?int, (timestamp, default=current_date/time)
  "category_id" : ?int
}
```
Response:
```
{
  "id" : int,
  "type" : str, (expenses - расходы; income - доходы)
  "amount" : str, (дробное число типа 189945,56)
  "comment" : ?str,
  "date" : ?int, <timestamp>
  "category_id" : ?int 
}
```
Response code:
> **200** - Операция создана успешно  
> **400** - Не задано обязательное поле в JSON запросе  
> **403** - Тек. пользователь не является владельцем `category_id` категории  
> **404** - Категория `category_id` не существует
<p align="right"><a href="#top">[ Наверх ]</a></p>

<a name="get_transaction_id"></a>
&#9660; Получение информации об указанной финансовой операций по "transaction_id". Доступно только аутентифицированному пользователю.  

**GET** &rArr; `/transactions/<int:transaction_id>`  
Response:
```
{
  "id" : int,
  "type" : str, (expenses - расходы; income - доходы)
  "amount" : str, (дробное число типа 189945,56)
  "comment" : ?str,
  "date" : int, <timestamp>
  "category_id" : int
}
```
Response code:
> **200** - Операция получена успешно  
> **403** - Тек. пользователь не является владельцем `transaction_id` операции    
> **404** - Операция `transaction_id` не существует
<p align="right"><a href="#top">[ Наверх ]</a></p>

<a name="patchtrans_id"></a>
&#9660; Редактирование финансовой операции. Редактировать операцию может только владелец (пользователь, создавший её). Доступно только аутентифицированному пользователю.  

**PATCH** &rArr; `/transactions/<int:transaction_id>`  
Request:
```
{
  "type" : ?str, (expenses - расходы; income - доходы)
  "amount" : ?str, (дробное число типа 189945,56)
  "comment" : ?str,
  "date" : ?str, <timestamp>
  "category_id" : ?int
}
```
Response:
```
{
  "id" : int,
  "type : str, (expenses - расходы; income - доходы)
  "amount" : str, (дробное число типа 189945,56)
  "comment" : ?str,
  "date" : str, <timestamp>
  "category_id" : ?int
}
```
Response code:
> **200** - Операция изменена успешно  
> **403** - Тек. пользователь не является владельцем `transaction_id` операции    
> **404** - Операция `transaction_id` не существует
<p align="right"><a href="#top">[ Наверх ]</a></p>

<a name="deltrans_id"></a>
&#9660; Удаление операции. Удалить операцию может только владелец (пользователь, создавший её). Доступно только аутентифицированному пользователю.  

**DELETE** &rArr; `/transactions/<int:transaction_id>`  
Response code:
> **204** - Операция удалена успешно  
> **403** - Тек. пользователь не является владельцем `transaction_id` операции    
> **404** - Операция `transaction_id` не существует
<p align="right"><a href="#top">[ Наверх ]</a></p>

<a name="get_report"></a>
&#9660; Получение отчета. Параметры: начальная дата, конечная дата и категория являются необязательными. Если категория не указана, то в отчет включаются все операции за указанный период. Для каждой операции отдается дата, сумма, описание и категория (вместе со всеми родительскими категориями). Список отсортирован по дате и отдается с пагинацией.

**GET** &rArr; `/report`  
Request:
```
Query params:
  from = ?str,
  to = ?str,
  type = ?str, (expenses - расходы; income - доходы)
  category_id = ?int,
  page_size = ?int, (default = 20)
  page = ?int (default = 1)
```
Response:
```
{
  "page_count" : int,
  "page" : int,
  "page_size" : int,
  "item_count" : int,
  "total" : str, (дробное число типа 189945,56)
  "transactions" : [
    {
      "id" : int,
      "amount" : str, (дробное число типа 189945,56)
      "comment" : ?str,
      "type" : str, (expenses - расходы; income - доходы)
      "date" : str, <timestamp>
      "category" : [
        {
          "id" : int,
          "name" : str      
        },
        {
          … n …	
        }
      ]
    },
    {
      … n …	  
    }
  ]
} 
```
Response code:
<p align="right"><a href="#top">[ Наверх ]</a></p>

### Примеры API запросов и Тесты <a name="examples"></a>
Для тестирования сервиса, используем утилиту [Postman](https://www.postman.com/).  
Для утилиты прилагается файл [HomeDesk Solutions - API Test Collection.postman_collection](https://github.com/MB6718/HomeDesk-Solutions/blob/dev/tests/HomeDesk%20Solutions%20-%20API%20Test%20Collection.postman_collection.json) с коллекцией тестов (см. директорию tests/)  
Так же для выполнения тестов потребуется тестовая (проинициализированная, заполненная тестовыми данными) БД.
Для создания тестовой базы предназначен скрипт `create_test_db.py` (см. директорию `tests/`), выполнив который, получим файл БД `test-db.sqlite`.  

Краткая инструкция по тестированию:
* Запустить скрипт `create_test_db.py` и сгенерировать тестовую БД
* В файле .env в переменной `DB_FILE` указать путь к тестовой БД (пример: `DB_FILE=tests/test-db.sqlite`)
* Запустить/перезапустить локальный Flask сервер
* Запустить утилиту Postman и импортировать в неё коллекцию тестов из папки `tests/`
* В утилите, протестировать каждый отдельно взятый случай или все в порядке их очереди (в авто режиме)

__Примечание!__ Если пробовать тестировать на чистой БД, будут ошибки в тестах, это нормально и происходит из за отсутствия первичных данных в ней.
<p align="right"><a href="#top">[ Наверх ]</a></p>

### Построен с использованием <a name="build_with"></a>

* [Python 3.8.3](https://www.python.org/downloads/release/python-383rc1/) - интерпретатор языка Python не ниже версии 3.8
* [Flask 1.1.12](https://flask.palletsprojects.com/en/1.1.x/) - фреймворк для создания веб-приложений на языке Python
* [SQLite 3.X.X](https://www.sqlite.org/index.html) - компактная встраиваемая СУБД версии 3.Х и выше

Остальные зависимые модули и пакеты см. в файл [requirements.txt](https://github.com/MB6718/HomeDesk-Solutions/blob/dev/requirements.txt)  
<p align="right"><a href="#top">[ Наверх ]</a></p>

### Авторы <a name="authors"></a>

Состав команды __White Studio:__
* <img src="https://avatars2.githubusercontent.com/u/61043468?s=400&v=4" width="24" height="24"/> [__Max [MB6718] Bee__](https://github.com/MB6718) (Belkin Maxim)
* <img src="https://avatars3.githubusercontent.com/u/64541060?s=400&v=4" width="24" height="24"/> [__Gift-Dar__](https://github.com/Gift-Dar) (Варганова Дарья)
* <img src="https://avatars1.githubusercontent.com/u/44629770?s=400&v=4" width="24" height="24"/> [__Xandarel__](https://github.com/Xandarel) (Бордюг Александр)
<p align="right"><a href="#top">[ Наверх ]</a></p>

### Лицензия <a name="license"></a>

HomeDesk-Solutions распространяется под лицензией GNU GPL v3.0. Смотрите [LICENSE.md](https://github.com/MB6718/HomeDesk-Solutions/blob/master/LICENSE) для получения более полных сведений.

&copy; 2020 White Studio