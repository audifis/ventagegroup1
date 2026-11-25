#!/usr/bin/env python3
"""Ajoute ?v=<empreinte> aux CSS/JS appelés par les pages HTML.
Chaque modification d'un fichier change son adresse : le navigateur recharge
la nouvelle version tout de suite au lieu de garder l'ancienne en cache.
À lancer avant chaque commit :  python3 tools/stamp.py"""
import hashlib, pathlib, re
root = pathlib.Path(__file__).resolve().parent.parent
def h(rel):
    f = root / rel
    return hashlib.md5(f.read_bytes()).hexdigest()[:8] if f.exists() else None
pat = re.compile(r'((?:href|src)=")((?:css|js)/[\w.-]+\.(?:css|js))(?:\?v=[0-9a-f]+)?(")')
for page in sorted(root.glob("*.html")):
    s = page.read_text()
    n = pat.sub(lambda m: f"{m.group(1)}{m.group(2)}?v={h(m.group(2))}{m.group(3)}" if h(m.group(2)) else m.group(0), s)
    if n != s: page.write_text(n); print("versionné :", page.name)
