import streamlit as st

from unisdb.db import connect

CACHE_SECONDS = 600


@st.cache_resource
def get_db():
    secrets = st.secrets["mongo"]
    return connect(secrets["uri"], secrets["db"])


@st.cache_data(ttl=CACHE_SECONDS, show_spinner=False)
def load_societies() -> list[dict]:
    return list(get_db()["societies"].find({}, {"_id": 0}))


def refresh_societies():
    load_societies.clear()