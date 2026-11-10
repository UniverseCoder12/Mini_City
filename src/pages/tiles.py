from __future__ import annotations

import pandas as pd
import streamlit as st

from src.database import SessionLocal
from src.models import City, Tile


def render() -> None:
    st.title("🧩 Tiles")

    with SessionLocal() as session:
        cities = session.query(City).order_by(City.id.asc()).all()
        if not cities:
            st.info("Cadastre uma cidade antes de criar tiles.")
            return

        city_options = {city.name: city.id for city in cities}
        selected_city_name = st.selectbox("Cidade", options=list(city_options.keys()))
        selected_city_id = city_options[selected_city_name]

        tiles = session.query(Tile).filter_by(city_id=selected_city_id).order_by(Tile.y.asc(), Tile.x.asc()).all()
        if tiles:
            rows = [
                {
                    "id": tile.id,
                    "cidade": selected_city_name,
                    "x": tile.x,
                    "y": tile.y,
                    "terrain": tile.terrain,
                    "road": tile.road,
                    "zone": tile.zone,
                    "building_id": tile.building_id,
                    "near_road": tile.near_road,
                }
                for tile in tiles
            ]
            st.dataframe(pd.DataFrame(rows), use_container_width=True)

        st.subheader("Adicionar tile")
        with st.form("create_tile_form"):
            city_id = st.selectbox("Cidade", options=[city.id for city in cities], format_func=lambda value: next(city.name for city in cities if city.id == value))
            x = st.number_input("Coordenada X", min_value=0, value=0, step=1)
            y = st.number_input("Coordenada Y", min_value=0, value=0, step=1)
            terrain = st.selectbox("Terreno", options=["grass", "water", "forest"])
            road = st.checkbox("Tem estrada")
            zone = st.selectbox("Zona", options=["none", "residential", "commercial", "industrial"])
            near_road = st.checkbox("Próximo de estrada")
            submitted = st.form_submit_button("Salvar tile")

        if submitted:
            with SessionLocal() as session:
                tile = Tile(
                    city_id=int(city_id),
                    x=int(x),
                    y=int(y),
                    terrain=terrain,
                    road=road,
                    zone=zone,
                    building_id=None,
                    near_road=near_road,
                )
                session.add(tile)
                session.commit()
            st.success("Tile adicionado com sucesso.")
            st.rerun()
