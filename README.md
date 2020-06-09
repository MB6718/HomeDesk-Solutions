# HomeDesk Solutions

![HomeDesk-Solutions]()

[![version](https://img.shields.io/badge/Version-BETA-BrightGreen)](https://github.com/MB6718/HomeDesk-Solutions)
[![python-version](https://img.shields.io/badge/Python-v3.8-blue)](https://www.python.org/downloads/release/python-383rc1/)
[![platform](https://img.shields.io/badge/platform-windows%20%7C%20linux%20%7C%20macos-LightGray)](https://ru.wikipedia.org/wiki/%D0%9A%D1%80%D0%BE%D1%81%D1%81%D0%BF%D0%BB%D0%B0%D1%82%D1%84%D0%BE%D1%80%D0%BC%D0%B5%D0%BD%D0%BD%D0%BE%D1%81%D1%82%D1%8C)
[![license](https://img.shields.io/badge/license-GPL_v3.0-yellow)](https://github.com/MB6718/HomeDesk-Solutions/blob/master/LICENSE)
[![framework](https://img.shields.io/badge/framework-Flask_1.1.12-ff69b4)](https://flask.palletsprojects.com/en/1.1.x/)

### Содержание
* [Краткое описание](#description)
* [Раздел с ТЗ и концептуальной частью](#concept)
* [Подготовка к запуску](#firstrun)
* [Формат описания API запросов/ответов](#apiformat)
	* [POST /auth/login](#login)
	* [POST /auth/logout](#logout)
* [Примеры API запросов](#example)
* [Построен с использованием](#build_with)
* [Авторы](#authors)
* [Лицензия](#license)

### Краткое описание <a name="description"></a>
Данное приложение HomeDesk Solutions, REST API cерверная часть сайта-сервиса для учёта и анализа личных финансов.

Приложение реализовано с помощью web-фреймворка Flask.

### Раздел с ТЗ и концептуальной частью <a name="consept"></a>
Техническое задание проекта:
`link here`

Концептуальная модель БД проекта:
`link here`

Логическая модель БД проекта:
`link here`

### Подготовка и запуск <a name="firstrun"></a>
Пошаговая инструкция по запуску приложения на локальном компьютере:
* под Windows
	1. Скачать архив с релизом приложения и распаковать в любую удобную папку
	2. создать и запустить виртуальное окружение в корне проекта, подтянуть необходимые зависимости
		```bash
		python -m venv .venv # создаём виртуальное окружение
		.venv\Scripts\activate.bat # активируем виртуальное окружение
		(.venv) python -V # проверяем версию интерпретатора Python, убеждаясь в работе окружения
		(.venv) pip install -r requirements.txt # устанавливаем необходимые пакеты и формируем зависимости
		(.venv) flask run # запустим локальный сервер Flask
		```


### Формат описания API запросов/ответов: <a name="apiformat"></a>
* запросы и ответы представлены в JSON-подобной структуре и описывают JSON-документы
* через двоеточие указываются типы полей
* запись вида type? обозначает, что поле необязательное и может отсутствовать
* запись вида [type] обозначает список значений типа type

<a name="login"></a> 
&#9660; Авторизация: вход и выход.  

**POST** &rArr; `/auth/login`  
Request:
```json
{
  "email": str,
  "password": str
}
```
<a name="logout"></a>
**POST** &rArr; `/auth/logout`

### Примеры API запросов <a name="example"></a>

  
### Построен с использованием <a name="build_with"></a>

* [Python 3.8.3](https://img.shields.io/badge/Python-v3.8-blue) - интерпретатор языка Python не ниже версии 3.8
* [Flask 1.1.12](https://img.shields.io/badge/framework-Flask_1.1.12-ff69b4) - фреймворк для создания веб-приложений на языке Python

Остальные зависимые модули и пакеты см. в файл [requirements.txt]()

### Авторы <a name="authors"></a>

* __Max [MB6718] Bee__
* __Gift-Dar__
* __Xandarel__

### Лицензия <a name="license"></a>

HomeDesk Solutions распространяется под лицензией GNU GPL v3.0. Смотрите LICENSE.md для получения более полных сведений.

&copy; 2020 White-Studio