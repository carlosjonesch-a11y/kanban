import streamlit as st
from datetime import datetime, date, time

from services.category_service import CategoryService
from services.task_service import TaskService


def _get_services():
    if "cat_svc" not in st.session_state:
        st.session_state.cat_svc = CategoryService()
    if "task_svc" not in st.session_state:
        st.session_state.task_svc = TaskService()
    return st.session_state.cat_svc, st.session_state.task_svc


# ──────────────────────────────────────────────
# Dialog: Criar nova task
# ──────────────────────────────────────────────
@st.dialog("Nova Tarefa", width="large")
def create_task_dialog():
    cat_svc, task_svc = _get_services()
    categories = cat_svc.get_all_categories()

    title = st.text_input("Título *", key="new_title")
    description = st.text_area("Descrição", key="new_desc", height=80)

    col1, col2 = st.columns(2)
    with col1:
        cat_options = {c["id"]: c["name"] for c in categories}
        selected_cat = st.selectbox(
            "Categoria *",
            options=list(cat_options.keys()),
            format_func=lambda x: cat_options[x],
            key="new_cat",
        )
    with col2:
        priority = st.selectbox(
            "Prioridade *",
            options=["alta", "media", "baixa"],
            format_func=lambda p: {"alta": "🔴 Alta", "media": "🟡 Média", "baixa": "🟢 Baixa"}[p],
            index=1,
            key="new_priority",
        )

    # Subcategoria (filtrada pela categoria selecionada)
    subcategories = cat_svc.get_subcategories(selected_cat) if selected_cat else []
    sub_options = {s["id"]: s["name"] for s in subcategories}
    selected_sub = None
    if sub_options:
        selected_sub = st.selectbox(
            "Subcategoria",
            options=[None] + list(sub_options.keys()),
            format_func=lambda x: "— Nenhuma —" if x is None else sub_options[x],
            key="new_subcat",
        )

    col3, col4 = st.columns(2)
    with col3:
        due_d = st.date_input("Data de prazo", value=None, key="new_due_date")
    with col4:
        due_t = st.time_input("Hora", value=time(23, 59), key="new_due_time")

    status = st.selectbox(
        "Coluna",
        options=["todo", "in_progress", "done"],
        format_func=lambda s: {"todo": "📋 A Fazer", "in_progress": "⚙️ Em Andamento", "done": "✅ Concluído"}[s],
        key="new_status",
    )

    if st.button("✅ Criar Tarefa", use_container_width=True, type="primary"):
        if not title.strip():
            st.error("O título é obrigatório.")
            return

        data = {
            "title": title.strip(),
            "description": description.strip(),
            "status": status,
            "priority": priority,
            "category_id": selected_cat,
        }
        if selected_sub:
            data["subcategory_id"] = selected_sub
        if due_d:
            due_datetime = datetime.combine(due_d, due_t)
            data["due_date"] = due_datetime.isoformat()

        task_svc.create_task(data)
        st.session_state["refresh_board"] = True
        st.rerun()


# ──────────────────────────────────────────────
# Dialog: Editar task existente
# ──────────────────────────────────────────────
@st.dialog("Editar Tarefa", width="large")
def edit_task_dialog(task: dict):
    cat_svc, task_svc = _get_services()
    categories = cat_svc.get_all_categories()
    task_id = task["id"]

    title = st.text_input("Título *", value=task["title"], key=f"edit_title_{task_id}")
    description = st.text_area(
        "Descrição",
        value=task.get("description", "") or "",
        height=80,
        key=f"edit_desc_{task_id}",
    )

    col1, col2 = st.columns(2)
    with col1:
        cat_options = {c["id"]: c["name"] for c in categories}
        cat_ids = list(cat_options.keys())
        current_cat_idx = cat_ids.index(task["category_id"]) if task["category_id"] in cat_ids else 0
        selected_cat = st.selectbox(
            "Categoria *",
            options=cat_ids,
            format_func=lambda x: cat_options[x],
            index=current_cat_idx,
            key=f"edit_cat_{task_id}",
        )
    with col2:
        prio_options = ["alta", "media", "baixa"]
        current_prio_idx = prio_options.index(task["priority"]) if task["priority"] in prio_options else 1
        priority = st.selectbox(
            "Prioridade *",
            options=prio_options,
            format_func=lambda p: {"alta": "🔴 Alta", "media": "🟡 Média", "baixa": "🟢 Baixa"}[p],
            index=current_prio_idx,
            key=f"edit_priority_{task_id}",
        )

    subcategories = cat_svc.get_subcategories(selected_cat) if selected_cat else []
    sub_options = {s["id"]: s["name"] for s in subcategories}
    selected_sub = None
    if sub_options:
        sub_ids = [None] + list(sub_options.keys())
        current_sub_idx = 0
        if task.get("subcategory_id") in sub_options:
            current_sub_idx = sub_ids.index(task["subcategory_id"])
        selected_sub = st.selectbox(
            "Subcategoria",
            options=sub_ids,
            format_func=lambda x: "— Nenhuma —" if x is None else sub_options[x],
            index=current_sub_idx,
            key=f"edit_subcat_{task_id}",
        )

    col3, col4 = st.columns(2)
    with col3:
        existing_date = None
        if task.get("due_date"):
            existing_date = datetime.fromisoformat(
                task["due_date"].replace("Z", "+00:00")
            ).date()
        due_d = st.date_input("Data de prazo", value=existing_date, key=f"edit_due_date_{task_id}")
    with col4:
        existing_time = time(23, 59)
        if task.get("due_date"):
            existing_time = datetime.fromisoformat(
                task["due_date"].replace("Z", "+00:00")
            ).time()
        due_t = st.time_input("Hora", value=existing_time, key=f"edit_due_time_{task_id}")

    c1, c2 = st.columns(2)
    with c1:
        if st.button("💾 Salvar", use_container_width=True, type="primary"):
            if not title.strip():
                st.error("O título é obrigatório.")
                return
            data = {
                "title": title.strip(),
                "description": description.strip(),
                "priority": priority,
                "category_id": selected_cat,
                "subcategory_id": selected_sub,
            }
            if due_d:
                data["due_date"] = datetime.combine(due_d, due_t).isoformat()
            else:
                data["due_date"] = None

            task_svc.update_task(task_id, data)
            st.session_state["refresh_board"] = True
            st.rerun()
    with c2:
        if st.button("🗑️ Excluir", use_container_width=True):
            task_svc.delete_task(task_id)
            st.session_state["refresh_board"] = True
            st.rerun()


# ──────────────────────────────────────────────
# Dialog: Gerenciar subcategorias
# ──────────────────────────────────────────────
@st.dialog("Gerenciar Subcategorias", width="large")
def manage_subcategories_dialog():
    cat_svc, _ = _get_services()
    categories = cat_svc.get_all_categories()

    cat_options = {c["id"]: c["name"] for c in categories}
    selected_cat = st.selectbox(
        "Categoria",
        options=list(cat_options.keys()),
        format_func=lambda x: cat_options[x],
        key="manage_sub_cat",
    )

    st.divider()

    # Criar nova subcategoria
    col_a, col_b = st.columns([3, 1])
    with col_a:
        new_sub_name = st.text_input("Nova subcategoria", key="new_sub_name", label_visibility="collapsed", placeholder="Nome da nova subcategoria...")
    with col_b:
        if st.button("➕ Criar", use_container_width=True):
            if new_sub_name.strip():
                cat_svc.create_subcategory(new_sub_name.strip(), selected_cat)
                st.rerun()
            else:
                st.error("Informe um nome.")

    # Listar subcategorias existentes
    subcategories = cat_svc.get_subcategories(selected_cat)
    if not subcategories:
        st.info("Nenhuma subcategoria cadastrada para esta categoria.")
    else:
        for sub in subcategories:
            col1, col2 = st.columns([4, 1])
            with col1:
                st.markdown(f"**{sub['name']}**")
            with col2:
                if st.button("🗑️", key=f"del_sub_{sub['id']}"):
                    cat_svc.delete_subcategory(sub["id"])
                    st.rerun()
