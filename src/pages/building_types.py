from __future__ import annotations

import pandas as pd
import streamlit as st

from src.database import SessionLocal
from src.models import BuildingType


def render() -> None:
    st.title("🏗️ Tipos de prédio")

    with SessionLocal() as session:
        types = session.query(BuildingType).order_by(BuildingType.id.asc()).all()

    if types:
        rows = [
            {
                "id": item.id,
                "nome": item.name,
                "categoria": item.category,
                "icon": item.icon,
                "largura": item.width,
                "altura": item.height,
                "custo": item.build_cost,
                "manutencao": item.upkeep,
                "capacidade": item.capacity,
                "unlock_population": item.unlock_population,
            }
            for item in types
        ]
        st.dataframe(pd.DataFrame(rows), use_container_width=True)

    st.subheader("Adicionar tipo de prédio")
    with st.form("create_building_type_form"):
        type_id = st.text_input("ID", value="school")
        name = st.text_input("Nome", value="Escola")
        category = st.selectbox("Categoria", options=["residential", "commercial", "industrial", "power", "service", "park"])
        icon = st.text_input("Ícone", value="🏫")
        width = st.number_input("Largura", min_value=1, max_value=10, value=1, step=1)
        height = st.number_input("Altura", min_value=1, max_value=10, value=1, step=1)
        build_cost = st.number_input("Custo de construção", min_value=0, value=0, step=1)
        upkeep = st.number_input("Manutenção mensal", min_value=0, value=0, step=1)
        capacity = st.number_input("Capacidade", min_value=0, value=0, step=1)
        power_consumption = st.number_input("Consumo de energia", min_value=0, value=0, step=1)
        power_production = st.number_input("Produção de energia", min_value=0, value=0, step=1)
        service_type = st.text_input("Tipo de serviço", value="education")
        effect_radius = st.number_input("Raio de efeito", min_value=0, value=0, step=1)
        happiness_effect = st.number_input("Efeito de felicidade", value=0, step=1)
        unlock_population = st.number_input("População mínima", min_value=0, value=0, step=1)
        submitted = st.form_submit_button("Salvar tipo")

    if submitted:
        with SessionLocal() as session:
            existing = session.get(BuildingType, type_id)
            if existing is not None:
                st.warning("Já existe um tipo com esse ID.")
                return

            new_type = BuildingType(
                id=type_id,
                name=name,
                category=category,
                icon=icon,
                width=int(width),
                height=int(height),
                build_cost=int(build_cost),
                upkeep=int(upkeep),
                capacity=int(capacity),
                power_consumption=int(power_consumption),
                power_production=int(power_production),
                service_type=service_type or None,
                effect_radius=int(effect_radius),
                happiness_effect=int(happiness_effect),
                unlock_population=int(unlock_population),
            )
            session.add(new_type)
            session.commit()
        st.success("Tipo cadastrado com sucesso.")
        st.rerun()
