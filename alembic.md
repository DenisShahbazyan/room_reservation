### Миграции в FastAPI: библиотека Alembic

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

### Автоматическое создание миграций и применение

Создание файла миграции (файла со списком необходимых изменений); выполняется командой, для автогенерации нужно добавить флаг `--autogenerate`, для добавления сообщение есть флаг `-m`

```sh
# Создание файла миграции
alembic revision
# Автоматическое создание файла миграции
alembic revision --autogenerate -m "First migration"
```

Выполнение всех неприменённых миграций запускается командой:

```sh
alembic upgrade head
```

### Отмена миграций

Если что-то пошло не так — можно отменить миграции: одну, несколько или вообще все.\
Чтобы отменить все миграции, которые были в проекте, используется команда:

```sh
alembic downgrade base
```

### Полезные команды Alembic

По умолчанию имена файлов миграций начинаются с Revision ID, с ключа, который генерируется случайным образом. Поэтому в директории /versions файлы отображаются не в хронологическом порядке. \
В Alembic есть команда history, которая позволяет увидеть в терминале все миграции в хронологическом порядке. Выполните её:

```sh
alembic history
```

Вывод в терминале будет примерно такой:

```
466f1da3d4b1 -> befcaa650c3f (head), Add description to MeetingRoom
<base> -> 466f1da3d4b1, First migration
```

Хронологию можно вывести и в более подробном виде — при помощи ключа `--verbose` (или `-v` в короткой форме):

```
Rev: befcaa650c3f (head)
Parent: 466f1da3d4b1
Path: ...room_reservation\alembic\versions\befcaa650c3f_add_description_to_meetingroom.py

    Add description to MeetingRoom

    Revision ID: befcaa650c3f
    Revises: 466f1da3d4b1
    Create Date: 2022-04-09 14:17:28.908840

Rev: 466f1da3d4b1
Parent: <base>
Path: ...room_reservation\alembic\versions\466f1da3d4b1_first_migration.py

    First migration

    Revision ID: 466f1da3d4b1
    Revises:
    Create Date: 2022-04-09 13:53:53.047017
```

Посмотреть последнюю применённую миграцию можно при помощи команды `current`.

```sh
alembic current
```

В терминале последней строкой будет указан Revision ID миграции:

```
INFO  [alembic.runtime.migration] Context impl SQLiteImpl.
INFO  [alembic.runtime.migration] Will assume non-transactional DDL.
466f1da3d4b1
```

Если база находится в состоянии base, то есть не применена ни одна миграция, то третьей строчки в выводе не будет.\
При просмотре истории миграций можно вывести метку актуальной миграции: для этого надо указать ключ `-i` (или `--indicate-current` в полной форме):

```sh
alembic history -i
```

В выводе напротив строки с актуальной миграцией появится надпись `(current)`:

```
466f1da3d4b1 -> befcaa650c3f (head), Add description to MeetingRoom
<base> -> 466f1da3d4b1 (current), First migration

# Или так:

466f1da3d4b1 -> befcaa650c3f (head) (current), Add description to MeetingRoom
<base> -> 466f1da3d4b1, First migration

# Если БД находится в состоянии <base> и миграции не применены, надписи не будет:

466f1da3d4b1 -> befcaa650c3f (head), Add description to MeetingRoom
<base> -> 466f1da3d4b1, First migration
```

### Настройки имени файла миграций

По умолчанию миграции нумеруются случайным образом; причина в том, что `Alembic` поддерживает ветки миграций (это чем-то похоже на ветки Git и даёт пользователю большую гибкость в управлении структурой БД). При работе с ветками последовательная нумерация только запутает. Рассматривать ветки `Alembic` мы не будем, но знать о такой возможности нужно.

Миграциям можно задавать фиксированные Revision ID прямо в команде создания миграции; если их нумеровать по порядку, например, 01, 02, 03 — файлы в директории будут хронологически упорядочены.

Фиксированный Revision ID указывается в команде `revision` при помощи ключа `--rev-id`:

```
alembic revision --autogenerate -m "Initial structure" --rev-id 01

# Какие-то изменения в моделях.
alembic revision --autogenerate -m "Add new models" --rev-id 02
```

При выполнении этих команд файлы будут пронумерованы как задумано:

```
01_initial_structure.py
02_add_new_models.py
```

При желании можно добавить к названию файлов с миграциями дату и время их создания, поменяв в файле _alembic.ini_ значение по умолчанию; изначально в файле строка с переменной может быть закомментирована.

```
# Заменяем строку
file_template = %%(rev)s_%%(slug)s
# на такую:
file_template = %%(year)d_%%(month).2d_%%(day).2d_%%(hour).2d%%(minute).2d-%%(rev)s_%%(slug)s
```

Теперь имена файлов миграций будут выглядеть так:

```
2022_02_28_1235-e6bd2f1ce032_add_description_to_meetingroom.py
```

Шаблоны имён можно комбинировать как угодно, например, можно задать и такой шаблон:

```
file_template = %%(rev)s-%%(year)d_%%(month).2d_%%(day).2d_%%(hour).2d%%(minute).2d-%%(slug)s
```

Если теперь выполнить команду с указанием собственного Revision ID...

```
alembic revision -m "Initial structure" --rev-id 01
```

...то имя файла получится таким:

```
01-2022_02_28_1235-initial_structure.py
```

На просторах интернета можно найти решения, которые будут автоматически генерировать последовательные Revision ID для файлов миграций. Но мы не будем применять все эти настройки, оставим поведение по умолчанию.

### Гибкий запуск миграций

Команды `upgrade` и `downgrade` можно применять не только с параметрами `head` и `base`, но и с указанием конкретных Revision ID, до которых надо применить или откатить миграции.

Например, по команде `alembic upgrade befcaa650c3f` будут применены все миграции вплоть до миграции с указанным ID. Не обязательно писать ID целиком, достаточно указать первые несколько символов, которые не встречаются ни в какой другой миграции в проекте.

Можно выполнить `alembic upgrade be` или даже `alembic upgrade b`, если с буквы `b` начинается название только одного файла миграций. Если есть несколько таких файлов — команда не выполнится и будет выведено сообщение об ошибке.

Аналогично, команды `alembic downgrade 466f1da3d4b1`, `alembic downgrade 46`, или `alembic downgrade 4` откатят состояние до миграции с указанным ID.

Поддерживается относительное указание миграций: «выполнить две следующие миграции» или «откатить три предыдущие»; для этого после команд `upgrade` и `downgrade` нужно указать число со знаком плюс или минус: `alembic ugprade +2` или `alembic downgrade -3`
