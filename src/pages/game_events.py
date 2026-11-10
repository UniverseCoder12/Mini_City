from __future__ import annotations

import pandas as pd
import streamlit as st

from src.database import SessionLocal
from src.models import Building, City, GameEvent


def render() -> None:
    st.title("🎲 Eventos do jogo")

    with SessionLocal() as session:
        events = session.query(GameEvent).order_by(GameEvent.id.asc()).all()
        cities = session.query(City).order_by(City.id.asc()).all()

    if events:
        rows = [
            {
                "id": event.id,
                "cidade": event.city_id,
                "tipo": event.type,
                "dia": event.day,
                "duracao": event.duration,
                "ativo": event.active,
                "building_id": event.building_id,
                "mensagem": event.message,
            }
            for event in events
        ]
        st.dataframe(pd.DataFrame(rows), use_container_width=True)

    st.subheader("Adicionar evento")
    with st.form("create_game_event_form"):
        city_id = st.selectbox("Cidade", options=[city.id for city in cities], format_func=lambda value: next(city.name for city in cities if city.id == value))
        event_type = st.selectbox("Tipo", options=["fire", "power_failure", "festival", "boom"])
        day = st.number_input("Dia", min_value=1, max_value=99999, value=1, step=1)
        duration = st.number_input("Duração", min_value=1, max_value=9999, value=1, step=1)
        active = st.checkbox("Ativo", value=True)
        building_id = st.number_input("ID do prédio afetado", min_value=0, value=0, step=1)
        message = st.text_input("Mensagem", value="Evento na cidade")
        submitted = st.form_submit_button("Salvar evento")

    if submitted:
        with SessionLocal() as session:
            building = None
            if building_id:
                building = session.get(Building, int(building_id))

            event = GameEvent(
                city_id=int(city_id),
                type=event_type,
                day=int(day),
                duration=int(duration),
                active=active,
                building_id=building.id if building else None,
                message=message,
            )
            session.add(event)
            session.commit()
        st.success("Evento cadastrado com sucesso.")
        st.rerun()
