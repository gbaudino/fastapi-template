"""
Settings module to load the application settings.
The settings are loaded from the environment file.

Please, create a <env_file> file, with the settings
needed to run the application. Use the following format:
```
app_name=my_app
app_description=my_description
app_version=0.1.0
```
"""
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "myapp"
    app_description: str = "My FastAPI application."
    app_version: str = "0.1.0"
    host: str = "0.0.0.0"
    port: int = 8000
    debug: bool = True

    class Config:
        env_file = 'configs/prod.env'
        env_file_encoding = 'utf-8'
