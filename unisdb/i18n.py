import streamlit as st

LANGUAGES = {"es": "Español", "en": "English"}
DEFAULT_LANG = "es"

STRINGS = {
    "es": {
        "app_title": "Instituciones de Debate",
        "nav_home": "Inicio",
        "nav_suggest": "Agregar información",
        "nav_admin": "Administración",
        "language": "Idioma",
        "add_info": "Agregar información",
        "add_info_hint": "¿Falta una sociedad, un código o un nombre alternativo?",
        "loaded_summary": "{societies} sociedades en {countries} países",
        "db_error": "No se pudo conectar a la base de datos. Intenta de nuevo en unos minutos.",
        "coming_soon": "Próximamente.",
    },
    "en": {
        "app_title": "Debate Institutions",
        "nav_home": "Home",
        "nav_suggest": "Add information",
        "nav_admin": "Admin",
        "language": "Language",
        "add_info": "Add information",
        "add_info_hint": "Missing a society, a code or an alternative name?",
        "loaded_summary": "{societies} societies in {countries} countries",
        "db_error": "Could not connect to the database. Please try again in a few minutes.",
        "coming_soon": "Coming soon.",
    },
}


def init_language():
    if "lang" not in st.session_state:
        lang = st.query_params.get("lang", DEFAULT_LANG)
        st.session_state.lang = lang if lang in LANGUAGES else DEFAULT_LANG
    # Re-set on every run: switching pages clears the URL's query params.
    st.query_params["lang"] = st.session_state.lang


def t(key: str, **kwargs) -> str:
    text = STRINGS[st.session_state.get("lang", DEFAULT_LANG)].get(key) or STRINGS[DEFAULT_LANG][key]
    return text.format(**kwargs) if kwargs else text