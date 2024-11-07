from typing import Optional

from pydantic import BaseSettings, EmailStr


class Settings(BaseSettings):
    env_app_title: str = 'QRKot'
    env_app_description: str = 'Вместе мы спасем мохнатых друзей!'
    env_database_url: str = 'sqlite+aiosqlite:///./fastapi.db'
    env_secret: str = 'bananas'
    env_first_superuser_email: EmailStr = 'root@admin.ru'
    env_first_superuser_password: str = 'root'
    type: Optional[str] = None
    project_id: Optional[str] = None
    private_key_id: Optional[str] = None
    private_key: Optional[str] = None
    client_email: Optional[str] = None
    client_id: Optional[str] = None
    auth_uri: Optional[str] = None
    token_uri: Optional[str] = None
    auth_provider_x509_cert_url: Optional[str] = None
    client_x509_cert_url: Optional[str] = None
    email: Optional[str] = None

    class Config:
        env_file = '.env'


settings = Settings()
