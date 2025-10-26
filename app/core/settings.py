from typing import Any, Optional, Dict
from xml.dom import NotFoundErr
from xmlrpc.client import boolean
from pydantic import InstanceOf, PostgresDsn, field_validator, validator
from pydantic_settings import BaseSettings
import os
from dotenv import load_dotenv
from sqlalchemy import Boolean


env_mode = os.getenv("ENV", "prod")

try:
    if env_mode == "dev" and os.path.exists(".env.dev"):
        load_dotenv(".env.dev")
    elif env_mode == "prod" and os.path.exists(".env.prod"):
        load_dotenv("env.prod")
    else:
        raise NotFoundErr("env files not found")
except (ImportError, ModuleNotFoundError):
    print("please check dot env module")


class Settings(BaseSettings):
    PROJECT_NAME: str = "Fast Api 1.0.0"
    VERSION: str = "1.0.0"
    DESCRIPTION: str = "Fast rest api"
    API_TAG: str = "/api"

    # data base
    POSTGRES_SERVER: str = os.getenv("POSTGRES_SERVER",)
    POSTGRES_USER: str = os.getenv("POSTGRES_USER", )
    POSTGRES_PASSWORD: str = os.getenv(
        "POSTGRES_PASSWORD",)
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", )
    POSTGRES_PORT: int = int(os.getenv("POSTGRES_PORT", 5432))
    SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn] = None
    DATABASE_ECHO:boolean = True # prod its false

    # data base url validator
    @field_validator("SQLALCHEMY_DATABASE_URI", mode="before")
    @classmethod
    def create_database_url(cls, v: Optional[str], info: dict):
        if v is not None:
            return v
        values = info.data
        return PostgresDsn.build(
            scheme="postgresql",
            username=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            host=values.get("POSTGRES_SERVER"),
            path=f"{values.get('POSTGRES_DB') or ''}",  # Added leading slash
            port=values.get("POSTGRES_PORT"),
        )
    class Config:
        case_sensitive = True
        env_file = [".env.prod", ".env.dev"]
        extra = "allow"  # allow extra fields in settings


settings = Settings()

