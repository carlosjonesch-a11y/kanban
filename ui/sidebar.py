import streamlit as st

from services.category_service import CategoryService


def render_sidebar() -> dict:
    """Renderiza a sidebar com filtros e retorna os filtros selecionados."""
    if "cat_svc" not in st.session_state:
        st.session_state.cat_svc = CategoryService()
    cat_svc = st.session_state.cat_svc

    categories = cat_svc.get_all_categories()

    with st.sidebar:
        st.markdown("## 🔎 Filtros")

        # Busca por texto
        search = st.text_input(
            "Buscar",
            placeholder="Pesquisar por título ou descrição...",
            key="filter_search",
        )

        # Filtro de categoria
        cat_options = {c["id"]: c["name"] for c in categories}
        selected_cats = st.multiselect(
            "Categoria",
            options=list(cat_options.keys()),
            format_func=lambda x: cat_options[x],
            key="filter_cats",
        )

        # Filtro de prioridade
        selected_priorities = st.multiselect(
            "Prioridade",
            options=["alta", "media", "baixa"],
            format_func=lambda p: {
                "alta": "🔴 Alta",
                "media": "🟡 Média",
                "baixa": "🟢 Baixa",
            }[p],
            key="filter_priorities",
        )

        st.divider()

        # Botões de ação
        st.markdown("## ⚙️ Gerenciar")

        if st.button("📁 Subcategorias", use_container_width=True):
            st.session_state["open_subcategories_dialog"] = True

        if st.button("➕ Nova Tarefa", use_container_width=True, type="primary"):
            st.session_state["open_create_dialog"] = True

    return {
        "search": search.strip() if search else None,
        "category_ids": selected_cats if selected_cats else None,
        "priorities": selected_priorities if selected_priorities else None,
    }
