from __future__ import annotations

import sys
from pathlib import Path

import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.database import init_db
from src.pages.cities import render as leaderboard_page

st.set_page_config(page_title="MiniCidade | Leaderboard", page_icon="🏙️", layout="wide")

try:
    init_db()
except Exception:
    st.title("Leaderboard MiniCidade")
    st.error(
        "Não foi possível conectar ao banco de dados. Confira os segredos MySQL "
        "no Streamlit ou a configuração SQLite local."
    )
    st.stop()

navigation = st.navigation(
    [st.Page(leaderboard_page, title="Leaderboard", url_path="leaderboard")],
    position="hidden",
)
navigation.run()
