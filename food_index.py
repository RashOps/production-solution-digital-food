""" Retrieve the real url using index"""
import re
import unicodedata
import difflib
import requests
from bs4 import BeautifulSoup

BASE_URL = "https://www.infocalories.fr/calories/"

# Pages candidates pour l'index
INDEX_URLS = [
    f"{BASE_URL}/index.php",
    f"{BASE_URL}/calories/",
    f"{BASE_URL}/",
]

_food_cache: dict[str, str] = {}   # cache manuel 

def normalize(text: str) -> str:
    nfd = unicodedata.normalize("NFD", text)
    return "".join(c for c in nfd if unicodedata.category(c) != "Mn").lower().strip()

def aggressive_normalize(text: str) -> str:
    # 1. Passage en minuscule et retrait des accents
    text = "".join(
        c for c in unicodedata.normalize("NFD", text.lower())
        if unicodedata.category(c) != "Mn"
    )
    # 2. RegEx : Retire les stop words (le, la, de, du, aux, etc.) et les caractères non-alphanumériques
    stop_words_pattern = r'\b(le|la|les|de|des|du|au|aux|en|un|une|avec|pour|et|a)\b'
    text = re.sub(stop_words_pattern, ' ', text)
    # 3. Retire tout ce qui n'est pas une lettre (chiffres à la fin des URLs, etc.)
    text = re.sub(r'[^a-z\s]', ' ', text)
    # 4. Nettoyage des espaces doubles
    return " ".join(text.split())

def _href_to_full_url(href: str) -> str:
    if href.startswith("http"):
        return href
    if href.startswith("/"):
        return BASE_URL + href
    return BASE_URL + "/" + href.lstrip("./")

def build_food_index(headers: dict) -> dict[str, str]:
    global _food_cache
    if _food_cache: return _food_cache

    food_map: dict[str, str] = {}
    # On itère sur les pages d'index
    for index_url in INDEX_URLS:
        try:
            r = requests.get(index_url, headers=headers, timeout=15)
            soup = BeautifulSoup(r.content, "html.parser")
            
            for a in soup.find_all("a", href=True):
                href = a["href"]
                # Accepte tout ce qui contient 'calories-' et finit par '.php'
                if "calories-" in href and href.endswith(".php"):
                    full_url = _href_to_full_url(href)
                    # Extraction du nom du lien (ex: 'calories-fruit-de-la-passion' -> 'fruit passion')
                    slug = href.split('/')[-1].replace('calories-', '').replace('.php', '').replace('-', ' ')
                    # Stockage de la version propre
                    clean_key = aggressive_normalize(slug)
                    food_map[clean_key] = full_url
                    # Stocke aussi le texte visible du lien pour doubler les chances
                    link_text = aggressive_normalize(a.get_text())
                    if link_text:
                        food_map[link_text] = full_url

        except Exception as e:
            print(f"Erreur sur {index_url}: {e}")
            continue
            
    _food_cache = food_map
    return food_map

def _fallback_urls(food_name: str) -> list[str]:
    """
    Génère les URLs candidates à tester quand l'index ne trouve rien.
    Couvre les cas : simple, -fruit, suffixe numérique.
    """
    slug = aggressive_normalize(food_name).replace(" ", "-")
    return [
        f"{BASE_URL}/calories/calories-{slug}.php",
        f"{BASE_URL}/calories/calories-{slug}-fruit.php",
        f"{BASE_URL}/calories/calories-{slug}-1.php",
        f"{BASE_URL}/calories/calories-{slug}-legume.php",
    ]

def find_food_url(food_name: str, headers: dict, cutoff: float = 0.55) -> str:
    index = build_food_index(headers)
    query = aggressive_normalize(food_name)
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
