from datetime import datetime, timezone


PRIORITY_LABELS = {"alta": "🔴 Alta", "media": "🟡 Média", "baixa": "🟢 Baixa"}
STATUS_LABELS = {"todo": "A Fazer", "in_progress": "Em Andamento", "done": "Concluído"}
STATUS_ICONS = {"todo": "📋", "in_progress": "⚙️", "done": "✅"}


def due_date_badge(due_date_str: str | None) -> str:
    """Retorna HTML do badge de prazo com dias restantes e cor adequada."""
    if not due_date_str:
        return ""

    now = datetime.now(timezone.utc)
    due = datetime.fromisoformat(due_date_str.replace("Z", "+00:00"))
    delta = (due.date() - now.date()).days

    if delta < 0:
        label = f"Vencido há {abs(delta)}d"
        css_class = "badge-prazo-vencido"
    elif delta == 0:
        label = "Hoje!"
        css_class = "badge-prazo-hoje"
    elif delta <= 3:
        label = f"{delta}d restante{'s' if delta > 1 else ''}"
        css_class = "badge-prazo-alerta"
    else:
        label = f"{delta}d restante{'s' if delta > 1 else ''}"
        css_class = "badge-prazo-ok"

    return f'<span class="kanban-badge {css_class}">⏰ {label}</span>'


def render_card_html(task: dict) -> str:
    """Gera o HTML completo de um card do Kanban."""
    cat = task.get("categories") or {}
    subcat = task.get("subcategories") or {}
    cat_name = cat.get("name", "")
    cat_color = cat.get("color", "#6C63FF")
    subcat_name = subcat.get("name", "")
    priority = task.get("priority", "media")
    description = task.get("description", "") or ""

    # Badges
    badges = []
    badges.append(
        f'<span class="kanban-badge badge-category" style="background:{cat_color}">'
        f"{cat_name}</span>"
    )
    if subcat_name:
        badges.append(
            f'<span class="kanban-badge badge-subcategory">{subcat_name}</span>'
        )
    badges.append(
        f'<span class="kanban-badge badge-{priority}">'
        f'{PRIORITY_LABELS.get(priority, priority)}</span>'
    )
    prazo_html = due_date_badge(task.get("due_date"))
    if prazo_html:
        badges.append(prazo_html)

    desc_html = ""
    if description:
        safe_desc = description.replace("<", "&lt;").replace(">", "&gt;")
        desc_html = f'<div class="kanban-card-desc">{safe_desc}</div>'

    safe_title = task["title"].replace("<", "&lt;").replace(">", "&gt;")

    return f"""
    <div class="kanban-card" style="border-left-color: {cat_color};">
        <div class="kanban-card-title">{safe_title}</div>
        {desc_html}
        <div class="kanban-badges">
            {''.join(badges)}
        </div>
    </div>
    """
