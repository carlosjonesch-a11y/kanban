import streamlit as st
from pathlib import Path

from ui.sidebar import render_top_filters
from ui.board import render_board
from ui.dialogs import create_task_dialog, edit_task_dialog, render_subcategories_manager

st.set_page_config(
    page_title="Kanban Board",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="collapsed",
)

css_path = Path(__file__).parent / "styles" / "kanban.css"
if css_path.exists():
    st.markdown(f"<style>{css_path.read_text()}</style>", unsafe_allow_html=True)

st.markdown(
    '<div class="kanban-header"><div>'
    "<h1>📋 Kanban Board</h1>"
    "<p>Gerencie suas tarefas de forma visual</p>"
    "</div></div>",
    unsafe_allow_html=True,
)

col_btn, col_spacer = st.columns([1, 3])
with col_btn:
    st.markdown('<div class="big-new-task-btn">', unsafe_allow_html=True)
    if st.button("➕ Nova Tarefa", use_container_width=True, type="primary"):
        st.session_state["open_create_dialog"] = True
    st.markdown("</div>", unsafe_allow_html=True)

tab_board, tab_subcats = st.tabs(["📋 Board", "📁 Subcategorias"])

with tab_board:
    filters = render_top_filters()
    st.divider()
    render_board(filters)

with tab_subcats:
    st.markdown("### 📁 Gerenciar Subcategorias")
    st.divider()
    render_subcategories_manager()

if st.session_state.get("open_create_dialog"):
    st.session_state["open_create_dialog"] = False
    create_task_dialog()

if st.session_state.get("edit_task"):
    task = st.session_state.pop("edit_task")
    edit_task_dialog(task)