from __future__ import annotations

import random

import pandas as pd
import streamlit as st

from src.database import SessionLocal
from src.models import City, Tile


def _create_tiles_for_city(session, city: City) -> None:
    existing = session.query(Tile).filter_by(city_id=city.id).count()
    if existing:
        return

    width = city.width
    height = city.height
    center_start = max((width - 8) // 2, 0)
    center_end = min(center_start + 8, width)

    rng = random.Random(city.seed or 1)
    for y in range(height):
        for x in range(width):
            terrain = "grass"
            if x >= center_start and x < center_end and y >= center_start and y < center_end:
                terrain = "grass"
            else:
                roll = rng.random()
                if roll < 0.12:
                    terrain = "water"
                elif roll < 0.30:
                    terrain = "forest"

            tile = Tile(
                city_id=city.id,
                x=x,
                y=y,
                terrain=terrain,
                road=False,
                zone="none",
                building_id=None,
                near_road=False,
            )
            session.add(tile)

    session.commit()


def render() -> None:
    st.title("🏘️ Cidades")

    with SessionLocal() as session:
        cities = session.query(City).order_by(City.id.asc()).all()

    if cities:
        rows = [
            {
                "id": city.id,
                "nome": city.name,
                "seed": city.seed,
                "largura": city.width,
                "altura": city.height,
                "dinheiro": city.money,
                "dia": city.day,
                "taxa": city.tax_rate,
                "peak_population": city.peak_population,
            }
            for city in cities
        ]
        st.subheader("Lista de cidades")
        st.dataframe(pd.DataFrame(rows), use_container_width=True)

    st.subheader("Adicionar cidade")
    with st.form("create_city_form"):
        name = st.text_input("Nome da cidade", value="Minha Cidade")
        seed = st.number_input("Seed", min_value=0, max_value=999999, value=0, step=1)
        width = st.number_input("Largura", min_value=8, max_value=128, value=32, step=1)
        height = st.number_input("Altura", min_value=8, max_value=128, value=32, step=1)
        submitted = st.form_submit_button("Criar cidade")

    if submitted:
        with SessionLocal() as session:
            city = City(name=name, seed=int(seed), width=int(width), height=int(height))
            session.add(city)
            session.commit()
            session.refresh(city)
            _create_tiles_for_city(session, city)
        st.success(f"Cidade '{name}' criada com sucesso.")
        st.rerun()
