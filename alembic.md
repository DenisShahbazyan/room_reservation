1. Устанавливаем Alembic

```sh
pip install alembic==1.7.7
```

2. Инициализируем: (пишем асинхронный код, поэтому в команде следует указать, что Alembic должен использовать асинхронный шаблон `--template async`)

```sh
alembic init --template async alembic
```

```
(venv) ...room_reservation$ alembic init -t async alembic
Creating directory ...room_reservation\alembic ...  done
Creating directory ...room_reservation\alembic\versions ...  done
Generating ...room_reservation\alembic.ini ...  done
Generating ...room_reservation\alembic\env.py ...  done
Generating ...room_reservation\alembic\README ...  done
Generating ...room_reservation\alembic\script.py.mako ...  done
Please edit configuration/connection/logging settings
in '...room_reservation/alembic.ini' before proceeding.
```

3. В структуре проекта появилась директория /alembic и файл alembic.ini

```
room_reservation/
    ├── alembic/                 <-- Новая директория с файлами Alembic.
    |   ├── versions/            <-- Здесь будут храниться файлы миграций.
    |   ├── env.py               <-- Скрипт со служебными функциями Alembic.
    |   ├── README               <-- README для Alembic.
    |   └── script.py.mako       <-- Шаблон для файлов миграций.
    ├── app/
    ├── venv/
    ├── .env
    └── alembic.ini              <-- Файл настроек.
```

В последней строке логов Alembic предлагает установить настройки в файле alembic.ini:

```
Please edit configuration/connection/logging settings
in '...room_reservation/alembic.ini' before proceeding.
```

Подробно можно почитать в [документации](https://alembic.sqlalchemy.org/en/latest/tutorial.html#editing-the-ini-file)

Alembic умеет работать с переменными окружения и может прочесть значение DATABASE_URL из .env. Для этого нужно добавить несколько строк в файл alembic/env.py.\
В листинге все добавленные строки отмечены комментариями на русском языке. Внимательно прочтите код листинга и внесите изменения в свой файл alembic/env.py:

```py
# alembic/env.py

import asyncio
# Импортируем модуль стандартной библиотеки для работы с ОС.
import os
from logging.config import fileConfig

# Импортируем функцию для чтения файлов с переменными окружения
# из библиотеки python-dotenv. Эта библиотека была установлена
# вместе с uvicorn.
from dotenv import load_dotenv
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from sqlalchemy.ext.asyncio import AsyncEngine

from alembic import context

# Загрузим файл .env в переменные окружения.
# Библиотека python-dotenv умеет находить файл в «вышестоящих» каталогах,
# поэтому полный путь указывать не обязательно.
load_dotenv('.env')

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Установим для переменной sqlalchemy.url значение из нашего .env файла.
config.set_main_option('sqlalchemy.url', os.environ['DATABASE_URL'])

...  # Остальное содержимое файла.
```

Настройки, которые вы добавили в файл alembic/env.py, перезапишут дефолтное значение, указанное в alembic.ini, так что никакие изменения в значение переменной sqlalchemy.url в файле alembic.ini вносить не нужно.\
Теперь Alembic будет подключаться к той базе данных, которая указана в .env, а чувствительные данные будут в безопасности.
