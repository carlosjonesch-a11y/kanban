import streamlit as st

from services.task_service import TaskService
from ui.card import render_card_html, STATUS_LABELS, STATUS_ICONS


COLUMNS = [
    ("todo", "A Fazer", "📋"),
    ("in_progress", "Em Andamento", "⚙️"),
    ("done", "Concluído", "✅"),
]

STATUS_OPTIONS = ["todo", "in_progress", "done"]


def _fetch_tasks(filters: dict) -> dict[str, list[dict]]:
    if "task_svc" not in st.session_state:
        st.session_state.task_svc = TaskService()
    task_svc = st.session_state.task_svc

    result = {"todo": [], "in_progress": [], "done": []}
    all_tasks = task_svc.get_tasks(search=filters.get("search"))

    cat_ids = filters.get("category_ids")
    priorities = filters.get("priorities")

    for t in all_tasks:
        if cat_ids and t["category_id"] not in cat_ids:
            continue
        if priorities and t["priority"] not in priorities:
            continue
        status = t.get("status", "todo")
        if status in result:
            result[status].append(t)

    return result


def render_board(filters: dict):
    tasks_by_status = _fetch_tasks(filters)
    cols = st.columns(3, gap="medium")

    for idx, (status_key, status_label, icon) in enumerate(COLUMNS):
        tasks = tasks_by_status.get(status_key, [])
        with cols[idx]:
            # Marcador para o CSS identificar e estilizar esta coluna
            st.markdown('<span class="board-col"></span>', unsafe_allow_html=True)
            st.markdown(
                f'<div class="kanban-column-header">'
                f'<h3>{icon} {status_label}</h3>'
                f'<div class="kanban-counter">{len(tasks)}</div></div>',
                unsafe_allow_html=True,
            )

            if not tasks:
                st.markdown(
                    '<p class="empty-col-text">Nenhuma tarefa</p>',
                    unsafe_allow_html=True,
                )

            for task in tasks:
                st.markdown(render_card_html(task), unsafe_allow_html=True)

                # Barra de ações: marker CSS + selectbox + botões compactos
                col_status, col_edit, col_del = st.columns([4, 1, 1], gap="small")

                with col_status:
                    # Marcador invisível usado pelo CSS :has() para estilizar a linha
                    st.markdown('<span class="card-action-marker"></span>', unsafe_allow_html=True)
                    current_idx = STATUS_OPTIONS.index(status_key)
                    new_status = st.selectbox(
                        "Status",
                        options=STATUS_OPTIONS,
                        format_func=lambda s: f"{STATUS_ICONS.get(s, '')} {STATUS_LABELS[s]}",
                        index=current_idx,
                        key=f"status_{task['id']}",
                        label_visibility="collapsed",
                    )
                    if new_status != status_key:
                        st.session_state.task_svc.move_task(task["id"], new_status)
                        st.rerun()

                with col_edit:
                    if st.button("✏️", key=f"edit_{task['id']}", help="Editar", use_container_width=True):
                        st.session_state["edit_task"] = task

                with col_del:
                    if st.button("🗑️", key=f"del_{task['id']}", help="Excluir", use_container_width=True):
                        st.session_state.task_svc.delete_task(task["id"])
                        st.rerun()

                st.markdown("<div style='margin-bottom:0.5rem'></div>", unsafe_allow_html=True)