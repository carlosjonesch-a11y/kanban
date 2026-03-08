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

if "current_filters" not in st.session_state:
    st.session_state["current_filters"] = {"search": None, "category_ids": None, "priorities": None}

tab_board, tab_filters, tab_subcats = st.tabs(["📋 Board", "🔎 Filtros", "📁 Subcategorias"])

with tab_board:
    render_board(st.session_state["current_filters"])

with tab_filters:
    st.markdown("### 🔎 Filtros de Tarefas")
    st.markdown("Configure os filtros e volte para a aba **Board** para ver os resultados.")
    st.divider()
    filters = render_top_filters()
    st.session_state["current_filters"] = filters
    st.divider()
    st.info("💡 Os filtros são aplicados automaticamente ao Board.")

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