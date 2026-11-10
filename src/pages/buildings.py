from __future__ import annotations

import pandas as pd
import streamlit as st

from src.database import SessionLocal
from src.models import Building, BuildingType, City


def render() -> None:
    st.title("🏢 Prédios")

    with SessionLocal() as session:
        buildings = session.query(Building).order_by(Building.id.asc()).all()
        cities = session.query(City).order_by(City.id.asc()).all()
        types = session.query(BuildingType).order_by(BuildingType.id.asc()).all()

    if buildings:
        rows = [
            {
                "id": building.id,
                "cidade": building.city_id,
                "tipo": building.type_id,
                "x": building.x,
                "y": building.y,
                "nivel": building.level,
                "ocupantes": building.occupants,
                "dia": building.built_day,
                "energia": building.powered,
                "conectado": building.connected,
                "felicidade": building.happiness,
            }
            for building in buildings
        ]
        st.dataframe(pd.DataFrame(rows), use_container_width=True)

    st.subheader("Adicionar prédio")
    with st.form("create_building_form"):
        city_id = st.selectbox("Cidade", options=[city.id for city in cities], format_func=lambda value: next(city.name for city in cities if city.id == value))
        type_id = st.selectbox("Tipo", options=[item.id for item in types], format_func=lambda value: next(item.name for item in types if item.id == value))
        x = st.number_input("Coordenada X", min_value=0, value=0, step=1)
        y = st.number_input("Coordenada Y", min_value=0, value=0, step=1)
        level = st.number_input("Nível", min_value=1, max_value=10, value=1, step=1)
        occupants = st.number_input("Ocupantes", min_value=0, max_value=1000, value=0, step=1)
        built_day = st.number_input("Dia de construção", min_value=1, max_value=99999, value=1, step=1)
        powered = st.checkbox("Com energia", value=True)
        connected = st.checkbox("Conectado à estrada", value=False)
        happiness = st.number_input("Felicidade", min_value=0, max_value=100, value=50, step=1)
        days_happy = st.number_input("Dias felizes", min_value=0, max_value=9999, value=0, step=1)
        days_unhappy = st.number_input("Dias infelizes", min_value=0, max_value=9999, value=0, step=1)
        on_fire = st.checkbox("Em chamas", value=False)
        abandoned = st.checkbox("Abandonado", value=False)
        submitted = st.form_submit_button("Salvar prédio")

    if submitted:
        with SessionLocal() as session:
            building = Building(
                city_id=int(city_id),
                type_id=str(type_id),
                x=int(x),
                y=int(y),
                level=int(level),
                occupants=int(occupants),
                built_day=int(built_day),
                powered=powered,
                connected=connected,
                happiness=int(happiness),
                days_happy=int(days_happy),
                days_unhappy=int(days_unhappy),
                on_fire=on_fire,
                abandoned=abandoned,
            )
            session.add(building)
            session.commit()
        st.success("Prédio cadastrado com sucesso.")
        st.rerun()
