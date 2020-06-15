# HomeDesk-Solutions

[![version](https://img.shields.io/badge/Version-BETA-BrightGreen)](https://github.com/MB6718/HomeDesk-Solutions/)
[![python-version](https://img.shields.io/badge/Python-v3.8-blue)](https://www.python.org/downloads/release/python-383rc1/)
[![platform](https://img.shields.io/badge/platform-windows%20%7C%20linux%20%7C%20macos-LightGray)](https://ru.wikipedia.org/wiki/%D0%9A%D1%80%D0%BE%D1%81%D1%81%D0%BF%D0%BB%D0%B0%D1%82%D1%84%D0%BE%D1%80%D0%BC%D0%B5%D0%BD%D0%BD%D0%BE%D1%81%D1%82%D1%8C)
[![license](https://img.shields.io/badge/license-GPL_v3.0-yellow)](https://github.com/MB6718/HomeDesk-Solutions/blob/master/LICENSE)
[![framework](https://img.shields.io/badge/framework-Flask_1.1.12-ff69b4)](https://flask.palletsprojects.com/en/1.1.x/)

### Содержание
* [Краткое описание](#description)
* [Техническое задание и концепция проекта](#concept)
* [Подготовка к запуску](#firstrun)
* [Спецификация (Формат описания API запросов/ответов)](#apispec)
	* [POST /auth/login](#login)
	* [POST /auth/logout](#logout)
* [Примеры API запросов](#example)
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
	1. Скачать архив с релизом приложения и распаковать в любую удобную папку
	2. ...

### Спецификация (Формат описания API запросов/ответов): <a name="apispec"></a>
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

Состав команды __White Studio:__
* ![contrib_images](https://avatars2.githubusercontent.com/u/61043468?s=400&v=4){:height="24px" width="24px"}
[__Max [MB6718] Bee__](https://github.com/MB6718) (Belkin Maxim)
* ![contrib_images](https://avatars3.githubusercontent.com/u/64541060?s=400&v=4){:height="24px" width="24px"}
[__Gift-Dar__](https://github.com/Gift-Dar) (Варганова Дарья)
* ![contrib_images](https://avatars1.githubusercontent.com/u/44629770?s=400&v=4){:height="24px" width="24px"}
[__Xandarel__](https://github.com/Xandarel) (Бордюг Александр)

### Лицензия <a name="license"></a>

HomeDesk-Solutions распространяется под лицензией GNU GPL v3.0. Смотрите [LICENSE.md](https://github.com/MB6718/HomeDesk-Solutions/blob/master/LICENSE) для получения более полных сведений.

&copy; 2020 White Studio