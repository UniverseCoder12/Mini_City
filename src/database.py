from __future__ import annotations

import os
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv
from sqlalchemy import URL, create_engine
from sqlalchemy.orm import sessionmaker

from src.models import Base

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")


def get_database_url() -> URL:
    try:
        mysql_secrets = st.secrets.get("mysql", {})
    except FileNotFoundError:
        mysql_secrets = {}

    mysql_host = mysql_secrets.get("host") or os.getenv("MYSQL_HOST")

    if mysql_host:
        mysql_user = mysql_secrets.get("username") or os.getenv("MYSQL_USER")
        mysql_password = mysql_secrets.get("password") or os.getenv("MYSQL_PASSWORD")
        mysql_database = mysql_secrets.get("database") or os.getenv("MYSQL_DATABASE")
        mysql_port = mysql_secrets.get("port") or os.getenv("MYSQL_PORT", "3306")
        required = {
            "username": mysql_user,
            "password": mysql_password,
            "database": mysql_database,
        }
        missing = [key for key, value in required.items() if not value]
        if missing:
            raise ValueError(f"Configuração MySQL incompleta: {', '.join(missing)}")

        return URL.create(
            "mysql+pymysql",
            username=mysql_user,
            password=mysql_password,
            host=mysql_host,
            port=int(mysql_port),
            database=mysql_database,
        )

    return URL.create("sqlite", database=str(BASE_DIR / "mini_city.db"))


engine = create_engine(get_database_url(), future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


def init_db() -> None:
    Base.metadata.create_all(bind=engine)
    from src.seed_data import seed_building_types

    with SessionLocal() as session:
        seed_building_types(session)


__all__ = ["Base", "SessionLocal", "engine", "get_database_url", "init_db"]
