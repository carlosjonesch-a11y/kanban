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

                # Status dropdown + discrete action buttons
                col_status, col_edit, col_del = st.columns([3, 1, 1])

                with col_status:
                    st.markdown('<div class="card-status-select">', unsafe_allow_html=True)
                    current_idx = STATUS_OPTIONS.index(status_key)
                    new_status = st.selectbox(
                        "Mover",
                        options=STATUS_OPTIONS,
                        format_func=lambda s: f"{STATUS_ICONS.get(s, '')} {STATUS_LABELS[s]}",
                        index=current_idx,
                        key=f"status_{task['id']}",
                        label_visibility="collapsed",
                    )
                    st.markdown('</div>', unsafe_allow_html=True)
                    if new_status != status_key:
                        st.session_state.task_svc.move_task(task["id"], new_status)
                        st.rerun()

                with col_edit:
                    st.markdown('<div class="card-actions">', unsafe_allow_html=True)
                    if st.button("✏️", key=f"edit_{task['id']}", help="Editar"):
                        st.session_state["edit_task"] = task
                    st.markdown('</div>', unsafe_allow_html=True)

                with col_del:
                    st.markdown('<div class="card-actions">', unsafe_allow_html=True)
                    if st.button("🗑️", key=f"del_{task['id']}", help="Excluir"):
                        st.session_state.task_svc.delete_task(task["id"])
                        st.rerun()
                    st.markdown('</div>', unsafe_allow_html=True)

                st.markdown("<div style='margin-bottom:0.3rem'></div>", unsafe_allow_html=True)