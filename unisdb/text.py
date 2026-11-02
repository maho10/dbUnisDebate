import re
import unicodedata


_INVISIBLE = dict.fromkeys(map(ord, "​‌‍⁠﻿­"), None)

STOPWORDS = {
    "universidad", "universitat", "universidade", "university", "uni",
    "sociedad", "sociedade", "society", "club", "circulo", "asociacion", "associacio",
    "debate", "debates", "debat", "debating", "oratoria", "argumentacion",
    "de", "del", "la", "las", "los", "el", "y", "e", "en", "of", "the", "and",
    "sd", "cd",
}


def clean(value) -> str:
    if value is None:
        return ""
    text = str(value).translate(_INVISIBLE)
    text = re.sub(r"\s+", " ", text).strip()
    return "" if text == "-" else text


def strip_accents(text: str) -> str:
    decomposed = unicodedata.normalize("NFKD", text)
    return "".join(c for c in decomposed if not unicodedata.combining(c))


def normalize(text: str, drop_stopwords: bool = False) -> str:
    text = strip_accents(clean(text)).lower()
    words = re.sub(r"[^a-z0-9]+", " ", text).split()
    if drop_stopwords:
        words = [w for w in words if w not in STOPWORDS] or words
    return " ".join(words)


def compact(text: str) -> str:
    return normalize(text).replace(" ", "")