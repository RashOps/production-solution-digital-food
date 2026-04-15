# food_index.py — version corrigée
import re
import unicodedata
import difflib
import requests
from bs4 import BeautifulSoup

BASE_URL = "https://www.infocalories.fr"

# Pages candidates pour l'index (essayées dans l'ordre)
INDEX_URLS = [
    f"{BASE_URL}/index.php",
    f"{BASE_URL}/calories/",
    f"{BASE_URL}/",
]

_food_cache: dict[str, str] = {}   # cache manuel (lru_cache ne marche pas avec dict mutable)


def normalize(text: str) -> str:
    nfd = unicodedata.normalize("NFD", text)
    return "".join(c for c in nfd if unicodedata.category(c) != "Mn").lower().strip()


def _href_to_full_url(href: str) -> str:
    if href.startswith("http"):
        return href
    if href.startswith("/"):
        return BASE_URL + href
    return BASE_URL + "/" + href.lstrip("./")


def build_food_index(headers: dict) -> dict[str, str]:
    global _food_cache
    if _food_cache:
        return _food_cache

    food_map: dict[str, str] = {}

    for index_url in INDEX_URLS:
        try:
            r = requests.get(index_url, headers=headers, timeout=20)
            if r.status_code != 200:
                continue
        except Exception:
            continue

        soup = BeautifulSoup(r.content, "html.parser")

        for a in soup.find_all("a", href=True):
            href: str = a["href"]
            # Accepte toutes les variantes : /calories/calories-X.php, calories-X.php, etc.
            match = re.search(r"calories-(.+?)(?:-fruit)?\.php", href)
            if not match:
                continue

            slug = match.group(1)
            key = normalize(slug.replace("-", " "))
            food_map[key] = _href_to_full_url(href)

        if food_map:
            print(f"[food_index] {len(food_map)} aliments indexés depuis {index_url}")
            break   # on a ce qu'il faut

    if not food_map:
        print("[food_index] WARN : index vide — uniquement le fallback URL sera utilisé")

    _food_cache = food_map
    return food_map


def _fallback_urls(food_name: str) -> list[str]:
    """
    Génère les URLs candidates à tester quand l'index ne trouve rien.
    Couvre les cas : simple, -fruit, suffixe numérique.
    """
    slug = normalize(food_name).replace(" ", "-")
    return [
        f"{BASE_URL}/calories/calories-{slug}.php",
        f"{BASE_URL}/calories/calories-{slug}-fruit.php",
        f"{BASE_URL}/calories/calories-{slug}-1.php",
        f"{BASE_URL}/calories/calories-{slug}-legume.php",
    ]


def find_food_url(food_name: str, headers: dict, cutoff: float = 0.55) -> str:
    index = build_food_index(headers)
    query = normalize(food_name)

    # 1. Match exact dans l'index
    if query in index:
        return index[query]

    # 2. Fuzzy match dans l'index
    if index:
        matches = difflib.get_close_matches(query, list(index.keys()), n=1, cutoff=cutoff)
        if matches:
            print(f"[food_index] fuzzy match : '{food_name}' → '{matches[0]}'")
            return index[matches[0]]

    # 3. Fallback : on teste les URLs probables directement
    print(f"[food_index] index miss — tentative fallback pour '{food_name}'")
    for url in _fallback_urls(food_name):
        try:
            r = requests.head(url, headers=headers, timeout=10)
            if r.status_code == 200:
                print(f"[food_index] fallback OK : {url}")
                return url
        except Exception:
            continue

    raise ValueError(
        f"Aliment '{food_name}' introuvable (index + fallback). "
        f"Vérifie l'orthographe ou consulte infocalories.fr manuellement."
    )