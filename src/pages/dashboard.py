from __future__ import annotations

import os

import streamlit as st
from sqlalchemy import func

from src.database import SessionLocal
from src.models import Building, City, CityStats, GameEvent


def render() -> None:
    st.title("🏙️ Dashboard do MiniCidade")

    with SessionLocal() as session:
        city_count = session.query(City).count()
        building_count = session.query(Building).count()
        event_count = session.query(GameEvent).count()
        total_population = session.query(func.coalesce(func.sum(CityStats.population), 0)).scalar() or 0
        total_money = session.query(func.coalesce(func.sum(City.money), 0)).scalar() or 0

    db_label = "MySQL" if os.getenv("MYSQL_HOST") else "SQLite"

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Cidades", city_count)
    col2.metric("Prédios", building_count)
    col3.metric("Eventos", event_count)
    col4.metric("População total", total_population)

    st.metric("Saldo consolidado", total_money)
    st.caption(f"Banco ativo: {db_label}")

    with SessionLocal() as session:
        cities = session.query(City).order_by(City.id.asc()).all()
        if not cities:
            st.info("Ainda não existem cidades cadastradas. Crie uma cidade na página de cidades.")
            return

        rows = []
        for city in cities:
            rows.append(
                {
                    "id": city.id,
                    "nome": city.name,
                    "seed": city.seed,
                    "largura": city.width,
                    "altura": city.height,
                    "dinheiro": city.money,
                    "dia": city.day,
                    "imposto": city.tax_rate,
                    "game_over": city.game_over,
                }
            )

        st.subheader("Cidades cadastradas")
        st.dataframe(rows, use_container_width=True)
