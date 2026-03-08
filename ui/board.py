import streamlit as st

from services.task_service import TaskService
from ui.card import render_card_html, STATUS_LABELS, STATUS_ICONS


COLUMNS = [
    ("todo", "A Fazer", "📋"),
    ("in_progress", "Em Andamento", "⚙️"),
    ("done", "Concluído", "✅"),
]


def _fetch_tasks(filters: dict) -> dict[str, list[dict]]:
    """Busca tasks do banco agrupadas por status."""
    if "task_svc" not in st.session_state:
        st.session_state.task_svc = TaskService()
    task_svc = st.session_state.task_svc

    result = {"todo": [], "in_progress": [], "done": []}

    all_tasks = task_svc.get_tasks(
        search=filters.get("search"),
    )

    # Aplicar filtros locais para multi-select
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
    """Renderiza o board Kanban com 3 colunas."""
    tasks_by_status = _fetch_tasks(filters)

    cols = st.columns(3, gap="medium")

    for idx, (status_key, status_label, icon) in enumerate(COLUMNS):
        tasks = tasks_by_status.get(status_key, [])
        with cols[idx]:
            # Header da coluna
            st.markdown(
                f"""
                <div class="kanban-column-header">
                    <h3>{icon} {status_label}</h3>
                    <div class="kanban-counter">{len(tasks)}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            if not tasks:
                st.markdown(
                    '<p style="color:#555; text-align:center; padding:2rem 0; font-size:0.85rem;">'
                    "Nenhuma tarefa</p>",
                    unsafe_allow_html=True,
                )

            for task in tasks:
                # Renderiza HTML do card
                st.markdown(render_card_html(task), unsafe_allow_html=True)

                # Botões de ação
                btn_cols = st.columns([1, 1, 1, 1])

                # Botão mover para esquerda
                if status_key != "todo":
                    prev_status = "todo" if status_key == "in_progress" else "in_progress"
                    prev_label = STATUS_ICONS.get(prev_status, "◀")
                    with btn_cols[0]:
                        if st.button(
                            f"◀ {prev_label}",
                            key=f"left_{task['id']}",
                            help=f"Mover para {STATUS_LABELS[prev_status]}",
                        ):
                            st.session_state.task_svc.move_task(task["id"], prev_status)
                            st.rerun()

                # Botão editar
                with btn_cols[1]:
                    if st.button("✏️", key=f"edit_{task['id']}", help="Editar"):
                        st.session_state["edit_task"] = task

                # Botão excluir
                with btn_cols[2]:
                    if st.button("🗑️", key=f"del_{task['id']}", help="Excluir"):
                        st.session_state.task_svc.delete_task(task["id"])
                        st.rerun()

                # Botão mover para direita
                if status_key != "done":
                    next_status = "in_progress" if status_key == "todo" else "done"
                    next_label = STATUS_ICONS.get(next_status, "▶")
                    with btn_cols[3]:
                        if st.button(
                            f"{next_label} ▶",
                            key=f"right_{task['id']}",
                            help=f"Mover para {STATUS_LABELS[next_status]}",
                        ):
                            st.session_state.task_svc.move_task(task["id"], next_status)
                            st.rerun()

                st.markdown("<div style='margin-bottom:0.3rem'></div>", unsafe_allow_html=True)
