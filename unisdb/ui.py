import streamlit as st

from unisdb.data import load_societies
from unisdb.i18n import t

SUGGEST_PAGE = "pages/suggest.py"


def societies_or_stop() -> list[dict]:
    try:
        return load_societies()
    except Exception:
        st.error(t("db_error"))
        st.stop()


def add_info_footer():
    st.divider()
    left, right = st.columns([3, 1], vertical_alignment="center")
    left.caption(t("add_info_hint"))
    if right.button(t("add_info"), icon=":material/add:", width="stretch"):
        st.switch_page(SUGGEST_PAGE)