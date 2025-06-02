from typing import Optional
from functools import lru_cache
from pydantic_settings import BaseSettings,SettingsConfigDict

# class BaseConfig(BaseSettings):
#     class Config:
#         env_file:str = ".env"

class BaseConfig(BaseSettings):
    ENV_STATE: Optional[str] = None

    model_config = SettingsConfigDict(env_file=".env",extra="ignore")

# TELL PYDANTIC TO READ OUR .ENV FROM THE SETTINGS IMPORTED
# THEY STAND FOR DIFFERENT ENVIRONMENTS 
class GlobalConfig(BaseConfig):
    DATABASE_URL: Optional[str] = None
    DB_FORCE_ROLL_BACK: bool = False
    LOGTAIL_API_KEY = Optional[str] = None

class DevConfig(GlobalConfig):
    model_config = SettingsConfigDict(env_prefix="DEV_")

class ProdConfig(GlobalConfig):
    model_config = SettingsConfigDict(env_prefix="PROD_")

class TestConfig(GlobalConfig):
    DATABASE_URL: str = "sqlite:///test.db"
    DB_FORCE_ROLL_BACK: bool = True

    model_config = SettingsConfigDict(env_prefix="TEST_")



@lru_cache()
def get_config(env_state:str):
    configs = {"dev":DevConfig,"prod":ProdConfig,"test":TestConfig}
    return configs[env_state]()

config = get_config(BaseConfig().ENV_STATE)

