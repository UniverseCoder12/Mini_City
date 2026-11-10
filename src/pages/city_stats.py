from __future__ import annotations

import pandas as pd
import streamlit as st

from src.database import SessionLocal
from src.models import City, CityStats


def render() -> None:
    st.title("📊 Estatísticas da cidade")

    with SessionLocal() as session:
        stats = session.query(CityStats).order_by(CityStats.id.asc()).all()
        cities = session.query(City).order_by(City.id.asc()).all()

    if stats:
        rows = [
            {
                "id": stat.id,
                "cidade": stat.city_id,
                "population": stat.population,
                "working_age": stat.working_age,
                "residential_capacity": stat.residential_capacity,
                "jobs_commercial": stat.jobs_commercial,
                "jobs_industrial": stat.jobs_industrial,
                "jobs": stat.jobs,
                "workers": stat.workers,
                "unemployment": stat.unemployment,
                "demand_residential": stat.demand_residential,
                "happiness": stat.happiness,
                "power_produced": stat.power_produced,
                "power_consumed": stat.power_consumed,
                "blackout": stat.blackout,
                "road_tiles": stat.road_tiles,
                "income": stat.income,
                "expenses": stat.expenses,
                "balance": stat.balance,
            }
            for stat in stats
        ]
        st.dataframe(pd.DataFrame(rows), use_container_width=True)

    st.subheader("Adicionar estatística")
    with st.form("create_city_stats_form"):
        city_id = st.selectbox("Cidade", options=[city.id for city in cities], format_func=lambda value: next(city.name for city in cities if city.id == value))
        population = st.number_input("População", min_value=0, value=0, step=1)
        working_age = st.number_input("População em idade de trabalhar", min_value=0, value=0, step=1)
        residential_capacity = st.number_input("Capacidade residencial", min_value=0, value=0, step=1)
        jobs_commercial = st.number_input("Empregos comerciais", min_value=0, value=0, step=1)
        jobs_industrial = st.number_input("Empregos industriais", min_value=0, value=0, step=1)
        jobs = st.number_input("Total de empregos", min_value=0, value=0, step=1)
        workers = st.number_input("Trabalhadores", min_value=0, value=0, step=1)
        unemployment = st.number_input("Desemprego (%)", min_value=0.0, max_value=100.0, value=0.0, step=1.0)
        demand_residential = st.number_input("Demanda residencial", min_value=-100, max_value=100, value=0, step=1)
        demand_commercial = st.number_input("Demanda comercial", min_value=-100, max_value=100, value=0, step=1)
        demand_industrial = st.number_input("Demanda industrial", min_value=-100, max_value=100, value=0, step=1)
        happiness = st.number_input("Felicidade média", min_value=0, max_value=100, value=50, step=1)
        power_produced = st.number_input("Energia produzida", min_value=0, value=0, step=1)
        power_consumed = st.number_input("Energia consumida", min_value=0, value=0, step=1)
        blackout = st.checkbox("Em apagão", value=False)
        road_tiles = st.number_input("Tiles de estrada", min_value=0, value=0, step=1)
        income = st.number_input("Receita do mês", min_value=0, value=0, step=1)
        expenses = st.number_input("Despesas do mês", min_value=0, value=0, step=1)
        balance = st.number_input("Saldo do mês", value=0, step=1)
        submitted = st.form_submit_button("Salvar estatísticas")

    if submitted:
        with SessionLocal() as session:
            stat = CityStats(
                city_id=int(city_id),
                population=int(population),
                working_age=int(working_age),
                residential_capacity=int(residential_capacity),
                jobs_commercial=int(jobs_commercial),
                jobs_industrial=int(jobs_industrial),
                jobs=int(jobs),
                workers=int(workers),
                unemployment=float(unemployment),
                demand_residential=int(demand_residential),
                demand_commercial=int(demand_commercial),
                demand_industrial=int(demand_industrial),
                happiness=int(happiness),
                power_produced=int(power_produced),
                power_consumed=int(power_consumed),
                blackout=blackout,
                road_tiles=int(road_tiles),
                income=int(income),
                expenses=int(expenses),
                balance=int(balance),
            )
            session.add(stat)
            session.commit()
        st.success("Estatísticas cadastradas com sucesso.")
        st.rerun()
