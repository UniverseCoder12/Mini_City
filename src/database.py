from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.models import Base

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")


def get_database_url() -> str:
    mysql_host = os.getenv("MYSQL_HOST")
    mysql_user = os.getenv("MYSQL_USER", "mini_city")
    mysql_password = os.getenv("MYSQL_PASSWORD", "mini_city")
    mysql_database = os.getenv("MYSQL_DATABASE", "mini_city")
    mysql_port = os.getenv("MYSQL_PORT", "3306")

    if mysql_host:
        return (
            f"mysql+pymysql://{mysql_user}:{mysql_password}@{mysql_host}:{mysql_port}/{mysql_database}"
        )

    return f"sqlite:///{BASE_DIR / 'mini_city.db'}"


engine = create_engine(get_database_url(), future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


def init_db() -> None:
    Base.metadata.create_all(bind=engine)
    from src.seed_data import seed_building_types

    with SessionLocal() as session:
        seed_building_types(session)


__all__ = ["Base", "SessionLocal", "engine", "get_database_url", "init_db"]
