import streamlit as st
from pathlib import Path

from ui.sidebar import render_sidebar
from ui.board import render_board
from ui.dialogs import create_task_dialog, edit_task_dialog, manage_subcategories_dialog

# ─── Configuração da página ───
st.set_page_config(
    page_title="Kanban Board",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── CSS customizado ───
css_path = Path(__file__).parent / "styles" / "kanban.css"
if css_path.exists():
    st.markdown(f"<style>{css_path.read_text()}</style>", unsafe_allow_html=True)

# ─── Header ───
st.markdown("# 📋 Kanban Board")

# ─── Sidebar (filtros + ações) ───
filters = render_sidebar()

# ─── Board principal ───
render_board(filters)

# ─── Dialogs (abertos via session_state) ───
if st.session_state.get("open_create_dialog"):
    st.session_state["open_create_dialog"] = False
    create_task_dialog()

if st.session_state.get("edit_task"):
    task = st.session_state.pop("edit_task")
    edit_task_dialog(task)

if st.session_state.get("open_subcategories_dialog"):
    st.session_state["open_subcategories_dialog"] = False
    manage_subcategories_dialog()
