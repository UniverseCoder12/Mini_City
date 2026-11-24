from __future__ import annotations

import pandas as pd
import streamlit as st
from sqlalchemy import func

from src.database import SessionLocal
from src.models import City, CityStats


def render() -> None:
    st.title("Leaderboard MiniCidade")

    with SessionLocal() as session:
        cities = (
            session.query(City, CityStats)
            .outerjoin(CityStats, CityStats.city_id == City.id)
            .order_by(
                func.coalesce(CityStats.population, 0).desc(),
                City.peak_population.desc(),
                City.day.desc(),
                City.name.asc(),
            )
            .all()
        )

    rows = [
        {
            "Posição": position,
            "Cidade": city.name,
            "População": stats.population if stats else 0,
            "Pico populacional": city.peak_population,
            "Dia": city.day,
            "Felicidade": stats.happiness if stats else 50,
            "Saldo": stats.balance if stats else 0,
        }
        for position, (city, stats) in enumerate(cities, start=1)
    ]

    leaderboard = pd.DataFrame(
        rows,
        columns=[
            "Posição",
            "Cidade",
            "População",
            "Pico populacional",
            "Dia",
            "Felicidade",
            "Saldo",
        ],
    )
    st.dataframe(
        leaderboard,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Posição": st.column_config.NumberColumn("#", format="%d"),
            "População": st.column_config.NumberColumn(format="%d"),
            "Pico populacional": st.column_config.NumberColumn(format="%d"),
            "Dia": st.column_config.NumberColumn(format="%d"),
            "Felicidade": st.column_config.NumberColumn(format="%d/100"),
            "Saldo": st.column_config.NumberColumn(format="%d"),
        },
    )
