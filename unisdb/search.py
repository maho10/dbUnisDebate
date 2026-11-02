from dataclasses import dataclass

from rapidfuzz import fuzz

from unisdb.text import compact, normalize

MIN_SCORE = 70


@dataclass
class Match:
    society: dict
    score: float
    matched: str


def _search_keys(society: dict) -> list[tuple[str, bool]]:
    short = [society["code"], society["society"]["acronym"], society["institution"]["acronym"]]
    long = [society["society"]["name"], society["institution"]["name"]]
    keys = [(k, True) for k in short if k] + [(k, False) for k in long if k]
    keys += [(a, len(compact(a)) <= 8) for a in society.get("aliases", [])]
    return keys


def _score(query: str, key: str, is_short: bool) -> float:
    if is_short:
        return fuzz.ratio(compact(query), compact(key))
    q, k = normalize(query, drop_stopwords=True), normalize(key, drop_stopwords=True)
    return max(fuzz.token_set_ratio(q, k), fuzz.ratio(q, k))


def search(query: str, societies: list[dict], limit: int = 20) -> list[Match]:
    if not normalize(query):
        return []
    matches = []
    for society in societies:
        best = max(((_score(query, key, short), key) for key, short in _search_keys(society)), default=(0, ""))
        if best[0] >= MIN_SCORE:
            matches.append(Match(society, best[0], best[1]))
    q = normalize(query)
    matches.sort(key=lambda m: (-m.score, -fuzz.ratio(q, normalize(m.society["society"]["name"]))))
    return matches[:limit]