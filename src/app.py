from __future__ import annotations

import streamlit as st

from src.database import init_db
from src.pages.dashboard import render as dashboard_page
from src.pages.building_types import render as building_types_page
from src.pages.buildings import render as buildings_page
from src.pages.cities import render as cities_page
from src.pages.city_stats import render as city_stats_page
from src.pages.game_events import render as game_events_page
from src.pages.tiles import render as tiles_page

st.set_page_config(page_title="MiniCidade", page_icon="🏙️", layout="wide")

if "db_ready" not in st.session_state:
    init_db()
    st.session_state["db_ready"] = True

pages = {
    "Visão geral": [
        st.Page(dashboard_page, title="🏙️ Dashboard", icon="🏙️"),
    ],
    "Entidades": [
        st.Page(cities_page, title="🏘️ Cidades", icon="🏘️"),
        st.Page(tiles_page, title="🧩 Tiles", icon="🧩"),
        st.Page(building_types_page, title="🏗️ Tipos de prédio", icon="🏗️"),
        st.Page(buildings_page, title="🏢 Prédios", icon="🏢"),
        st.Page(city_stats_page, title="📊 Estatísticas", icon="📊"),
        st.Page(game_events_page, title="🎲 Eventos", icon="🎲"),
    ],
}

navigation = st.navigation(pages)
navigation.run()
