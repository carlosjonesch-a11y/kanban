import os
from collections.abc import Mapping

import streamlit as st
from supabase import create_client, Client


def _pick_nested_supabase_value(*keys: str) -> str | None:
    """Busca valor na secao [supabase] do st.secrets, aceitando aliases."""
    section = st.secrets.get("supabase")
    if not isinstance(section, Mapping):
        return None

    for key in keys:
        value = section.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip()
    return None


def _pick_flat_secret_or_env(*keys: str) -> str | None:
    """Busca valor em st.secrets (raiz) ou variavel de ambiente."""
    for key in keys:
        secret_value = st.secrets.get(key)
        if isinstance(secret_value, str) and secret_value.strip():
            return secret_value.strip()

        env_value = os.getenv(key)
        if isinstance(env_value, str) and env_value.strip():
            return env_value.strip()
    return None


def _resolve_supabase_credentials() -> tuple[str | None, str | None]:
    """Resolve credenciais aceitando formatos comuns local/cloud."""
    url = _pick_nested_supabase_value("url", "SUPABASE_URL")
    if not url:
        url = _pick_flat_secret_or_env("SUPABASE_URL", "supabase_url")

    key = _pick_nested_supabase_value("key", "anon_key", "SUPABASE_KEY", "SUPABASE_ANON_KEY")
    if not key:
        key = _pick_flat_secret_or_env(
            "SUPABASE_KEY",
            "SUPABASE_ANON_KEY",
            "supabase_key",
            "supabase_anon_key",
        )

    return url, key


def _show_missing_credentials_message() -> None:
    st.error("Configuracao do Supabase nao encontrada.")
    st.markdown("Configure as secrets no Streamlit com um destes formatos:")
    st.code(
        """[supabase]
url = "https://SEU-PROJETO.supabase.co"
key = "SUA_ANON_KEY"
""",
        language="toml",
    )
    st.code(
        """SUPABASE_URL = "https://SEU-PROJETO.supabase.co"
SUPABASE_KEY = "SUA_ANON_KEY"
""",
        language="toml",
    )
    st.caption("No Streamlit Cloud: app > Settings > Secrets")


@st.cache_resource
def get_supabase_client() -> Client:
    """Inicializa e retorna o cliente Supabase (singleton)."""
    url, key = _resolve_supabase_credentials()
    if not url or not key:
        _show_missing_credentials_message()
        st.stop()

    return create_client(url, key)
