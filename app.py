import streamlit as st

from unisdb.i18n import LANGUAGES, init_language, t

st.set_page_config(page_title="Instituciones de Debate", page_icon=":material/account_balance:", layout="wide")
init_language()

with st.sidebar:
    lang = st.segmented_control(t("language"), options=list(LANGUAGES), format_func=LANGUAGES.get,
                                default=st.session_state.lang)
    if lang and lang != st.session_state.lang:
        st.session_state.lang = lang
        st.rerun()

pages = [
    st.Page("pages/home.py", title=t("nav_home"), icon=":material/search:", default=True),
    st.Page("pages/suggest.py", title=t("nav_suggest"), icon=":material/add_circle:"),
    st.Page("pages/admin.py", title=t("nav_admin"), icon=":material/lock:"),
]
st.navigation(pages).run()