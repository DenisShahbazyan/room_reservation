Запуск приложения:\
`main` - имя файла\
`app` - объект приложения FastAPI\
`--reload` - автоматическая перезагрузка сервера при изменении

```sh
uvicorn main:app --reload
uvicorn app.main:app --reload
```

Запуск программы стандартными средствами IDE:

```py
import uvicorn

if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)
```

Документация по написанному коду:\
Swagger http://127.0.0.1:8000/docs\
ReDoc http://127.0.0.1:8000/redoc
