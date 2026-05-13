"""
ADIM 1: GitHub'daki Python repolarından fonksiyonları topla.
Çalıştır: python3 1_collect_functions.py
"""
import ast
import json
import os
import requests
import time
from config import REPOS, FUNCTIONS_PER_REPO, OUTPUT_DIR

os.makedirs(OUTPUT_DIR, exist_ok=True)

GITHUB_API = "https://api.github.com"
HEADERS = {"Accept": "application/vnd.github.v3+json"}


def get_python_files(repo: str):
    """Repo'daki tüm .py dosyalarını getir."""
    url = f"{GITHUB_API}/repos/{repo}/git/trees/HEAD?recursive=1"
    r = requests.get(url, headers=HEADERS, timeout=15)
    if r.status_code != 200:
        print(f"  HATA: {repo} tree alınamadı ({r.status_code})")
        return []
    return [
        item for item in r.json().get("tree", [])
        if item["path"].endswith(".py")
        and "test" not in item["path"].lower()
        and item.get("size", 0) < 50000  # Çok büyük dosyaları atla
    ]


def get_file_content(repo: str, path: str):
    """Bir dosyanın içeriğini getir."""
    url = f"{GITHUB_API}/repos/{repo}/contents/{path}"
    r = requests.get(url, headers=HEADERS, timeout=15)
    if r.status_code != 200:
        return None
    import base64
    try:
        return base64.b64decode(r.json()["content"]).decode("utf-8")
    except Exception:
        return None


def extract_functions(source, filename):
    """Python kaynak kodundan sade, test edilebilir fonksiyonları çıkar."""
    try:
        tree = ast.parse(source)
    except SyntaxError:
        return []

    # Class içindeki metodları tespit etmek için class gövdelerini topla
    method_nodes = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            for item in ast.walk(node):
                if isinstance(item, ast.FunctionDef):
                    method_nodes.add(id(item))

    funcs = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.FunctionDef):
            continue
        if id(node) in method_nodes:
            continue  # class metodu, atla
        name = node.name
        if name.startswith("_"):
            continue
        if len(node.body) < 3:
            continue
        lines = source.splitlines()
        start = node.lineno - 1
        end = node.end_lineno
        func_src = "\n".join(lines[start:end])
        if len(func_src) < 50 or len(func_src) > 2000:
            continue
        funcs.append({
            "name": name,
            "filename": filename,
            "source": func_src,
            "lineno": node.lineno,
        })
    return funcs



def collect_for_repo(repo: str, n: int):
    print(f"\n[REPO] {repo} işleniyor...")
    py_files = get_python_files(repo)
    print(f"   {len(py_files)} Python dosyası bulundu")

    collected = []
    for f in py_files:
        if len(collected) >= n:
            break
        content = get_file_content(repo, f["path"])
        if not content:
            continue
        funcs = extract_functions(content, f["path"])
        for func in funcs:
            if len(collected) >= n:
                break
            func["repo"] = repo
            collected.append(func)
        time.sleep(0.3)  # GitHub rate limit'e saygı

    print(f"   OK {len(collected)} fonksiyon toplandı")
    return collected


if __name__ == "__main__":
    all_functions = []
    for repo in REPOS:
        funcs = collect_for_repo(repo, FUNCTIONS_PER_REPO)
        all_functions.extend(funcs)

    out_path = os.path.join(OUTPUT_DIR, "functions.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(all_functions, f, ensure_ascii=False, indent=2)

    print(f"\nTAMAMLANDI Toplam {len(all_functions)} fonksiyon kaydedildi → {out_path}")
