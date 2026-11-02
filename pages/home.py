import streamlit as st

from unisdb.i18n import t
from unisdb.ui import add_info_footer, societies_or_stop

societies = societies_or_stop()

st.title(t("app_title"))
countries = {s["country"] for s in societies if s["country"]}
st.caption(t("loaded_summary", societies=len(societies), countries=len(countries)))

st.info(t("coming_soon"))

add_info_footer()