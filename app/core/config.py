from pydantic import BaseSettings


class Settings(BaseSettings):
    app_title: str = 'Бронирование переговорок'
    app_description: str = (
        'Сервис по бронированию переговорок обеспечивает удобный '
        'онлайн-доступ к календарю переговорных комнат, позволяя '
        'пользователям легко забронировать необходимое пространство для '
        'проведения встреч и совещаний.'
    )
    database_url: str

    class Config:
        env_file = '.env'


settings = Settings()
