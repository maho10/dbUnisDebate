"""MongoDB connection shared by the app and the scripts."""
import tomllib
from pathlib import Path

from pymongo import MongoClient

SECRETS_FILE = Path(__file__).resolve().parent.parent / ".streamlit" / "secrets.toml"


def read_local_secrets() -> dict:
    """Secrets for scripts run outside Streamlit (the app uses st.secrets instead)."""
    with open(SECRETS_FILE, "rb") as f:
        return tomllib.load(f)


def connect(uri: str, db_name: str):
    if "<db_username>" in uri or "<db_password>" in uri:
        raise ValueError(f"Fill in the username and password in {SECRETS_FILE}")
    client = MongoClient(uri, serverSelectionTimeoutMS=10_000)
    client.admin.command("ping")
    return client[db_name]