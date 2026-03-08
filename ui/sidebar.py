import streamlit as st

from services.category_service import CategoryService


def render_top_filters() -> dict:
    """Renderiza filtros inline no corpo principal e retorna os filtros selecionados."""
    if "cat_svc" not in st.session_state:
        st.session_state.cat_svc = CategoryService()
    cat_svc = st.session_state.cat_svc

    categories = cat_svc.get_all_categories()

    col1, col2, col3 = st.columns(3)

    with col1:
        search = st.text_input(
            "🔍 Buscar",
            placeholder="Pesquisar por título ou descrição...",
            key="filter_search",
        )

    with col2:
        cat_options = {c["id"]: c["name"] for c in categories}
        selected_cats = st.multiselect(
            "📂 Categoria",
            options=list(cat_options.keys()),
            format_func=lambda x: cat_options[x],
            key="filter_cats",
        )

    with col3:
        selected_priorities = st.multiselect(
            "⚡ Prioridade",
            options=["alta", "media", "baixa"],
            format_func=lambda p: {
                "alta": "🔴 Alta",
                "media": "🟡 Média",
                "baixa": "🟢 Baixa",
            }[p],
            key="filter_priorities",
        )

    return {
        "search": search.strip() if search else None,
        "category_ids": selected_cats if selected_cats else None,
        "priorities": selected_priorities if selected_priorities else None,
    }