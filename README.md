mini-market
===========

Mini-market - небольшой интернет магазин с ограниченным функционалом:
* имеется поддержка каталогов, меток (тегов), корзины и оформлением заказа;
* регистрация/авторизация пользователей по email, профиль и отслеживание заказов;

- клиент написан на JavaScript и фреймворке Angular;
- сервер написан на языке Python и фреймворке Django
(djangorestframework для организации REST API, django-import-export для выгрузки данных заказов);
- для хранения данных используется sqlite;

superuser: test 12345qwerty
demo user: test@test.ru test@test.ru

Структура проекта
-----------------

Проект структурно состоит из 2х частей - клиентской и серверной.
Клиентские скрипты, шаблоны и стили размещены в публичной части системы (директория www), доступ к ним должен обеспечить веб сервер (nginx).
Серверная часть заключена в виде монолитного приложения на python и django (директория api_market), доступ к которому осуществляется посредством REST API.

```
mini-market
│
├─ api_market - django backend
└─ www - angular frontend
```

Описание REST Endpoint
----------------------

Роутинг по определенным точкам доступа для соответствующих обработчиков расположен в конфигурационном
файле серверного приложения ```api_market/backend/urls.py```

Установка
---------


#### Зависимости

Python 3.5 см. requirements.txt

#### Web server

Для работы приложения необходимо обеспечить доступ по домену (например www.mini-market.local)
и прописать этот домен в конфиурационных файлах системы.

##### hosts

    # Для доступа к клиентскому приложению, серверному приложению по REST API
    127.0.0.1 www.mini-market.local

##### nginx

Для работы доменов необходимо сконфигурировать веб сервер (например nginx).
Пример конфигурации для nginx
```
# public
server {
    listen 80;
    charset utf-8;
    root /path/to/mini-market/www;
    server_name www.mini-market.local;
    index index.html;
    client_max_body_size 5M;

    location / {
        try_files $uri /index.html;
    }

    location ~ \.(js|css|ico|htm|html|json)$ {
        try_files $uri =404;
    }

    location /_/ {
        proxy_pass_header Server;
        proxy_set_header Host $http_host;
        proxy_redirect off;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Scheme $scheme;
        proxy_pass http://mini_market_backends;
    }
}

# api
upstream mini_market_backends {
    server 127.0.0.1:8000;
}
```

где /path/to/mini-market/www - должен указывать на директорию www в приложении,
127.0.0.1:8000 - адрес и порт под которым работает django (значения по умолчанию для тестового сервера),
www.mini-market.local - тестовый домен.


#### Backend

В качестве СУБД используется sqlite, которая не требует отдельной конфигурации. Вместе с репозиторием поставляется база с тестовыми данными,
 пригодными для начала работы. Для начала самостоятельной работы с системой предлагается удалить
 существующую БД (расположение api_market/db.sqlite3) и провести стандартный ряд мероприятий по установке и
 конфигурированию БД, в соответствии с интрукцией по установке django.


#### Frontend

Настройка доступа к клиентским билиотекам осуществлятся в главном индексном файле ```www/index.html```
в большинстве внешние библиотеки подключаются через сторонние CDN а внутренние библиотеки системы имеют относительные пути.

Настроить доступ клиента к серверу можно главном модуле клиентского приложения angular ```www/system/app.js```
в нем необходимо удостовериться что параметры

        baseUrl: "http://www.mini-market.local/_",
        baseWWWUrl: "http://www.mini-market.local"

сконфигурированы в соответсвии с настройками веб сервера.
- baseUrl - базовый урл для API приложения
- baseWWWUrl - базовый урл для клиентских ресурсов приложения


python django angular sqlite