#!/usr/bin/env python3
"""Construye la sección «Fichas» de un tema a partir del PPT y de las notas del orador.

Uso:
  python3 extraer_ppt.py "TEMA 2. Egipto.pptx" t2_slides.json          (en el Mac, con python-pptx)
  python3 construir_fichas.py t2_slides.json data/tema02.json img/t2 imgmap.json "TEMA 2 - Notas del orador.md" [notas_en.md]

Reglas:
- Una diapositiva cuyo título empieza por un código de apartado (2.1.2. …) abre un apartado nuevo.
  Su nota del orador pasa a ser la introducción del apartado.
- Cada diapositiva con título genera una ficha; los títulos con (II), (III) continúan la ficha anterior;
  las diapositivas sin título (solo imágenes) se añaden a la ficha anterior.
- El cuerpo de la ficha son las notas del orador de sus diapositivas (archivo Markdown con un bloque
  «### Diapositiva N · …» por diapositiva, «Notas del orador» y «Fuente»). Si no hay nota, se usa el
  texto de la diapositiva. Los párrafos que empiezan por «Para el ensayo» se marcan aparte.
- El texto de la diapositiva se conserva en «slide» como apoyo, y sus referencias APA en «refs».
"""
import sys, os, json, re, unicodedata

def slug(s):
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()
    s = re.sub(r"[^a-zA-Z0-9]+", "-", s).strip("-").lower()
    return s[:40].strip("-") or "ficha"

SEC_RE = re.compile(r"^(\d+(?:\.\d+)+)\.?\s+(.*)$")
CONT_RE = re.compile(r"\s*\((II|III|IV|V)\)\s*$")
YEAR = r"\((1[89]\d\d|20\d\d)[a-z]?\)"
REF_RE = re.compile(r"^(?:[A-ZÁÉÍÓÚÑ][\w'’\- ]{1,40},\s+[A-ZÁÉÍÓÚ]\.|[A-ZÁÉÍÓÚÑ][^.()]{2,50}\.\s+" + YEAR + r")")
LAYOUT_RE = re.compile(r"^(Imagen (izquierda|derecha|abajo|arriba)|Dos imágenes|Destacado \d+.*|Jerarquía de Viñetas|Portada.*|[Íí]ndice.*|Cierre.*|Texto.*|Comparación.*|Título.*|Base|En blanco|Solo imagen.*)$")

def is_ref(p):
    return bool(REF_RE.match(p)) and re.search(YEAR, p) is not None and len(p) > 40

def parse_notes(path):
    """Devuelve {n_diapositiva: {"title":…, "notes":[párrafos], "refs":[…]}}"""
    out = {}
    if not path:
        return out
    txt = open(path, encoding="utf-8").read()
    blocks = re.split(r"^### Diapositiva (\d+)\s*·\s*(.*)$", txt, flags=re.M)
    for k in range(1, len(blocks), 3):
        n = int(blocks[k]); head = blocks[k + 1].strip(); body = blocks[k + 2]
        parts = [p.strip() for p in head.split("·")]
        title = re.sub(r"\s+", " ", parts[-1].strip())
        if LAYOUT_RE.match(title) or title.startswith("("):
            title = ""
        def grab(label):
            m = re.search(r"\*\*`" + label + r"`\*\*[^\n]*\n(.*?)(?=\n\*\*`|\n---|\n## |\Z)", body, flags=re.S)
            if not m:
                return []
            paras, cur = [], []
            for line in m.group(1).split("\n"):
                line = line.strip()
                if line.startswith(">"):
                    line = line[1:].strip()
                if line:
                    cur.append(line)
                else:
                    if cur: paras.append(" ".join(cur)); cur = []
            if cur: paras.append(" ".join(cur))
            return [p for p in paras if p and p.lower() != "no procede."]
        notes = grab("Notas del orador")
        refs = []
        for r in grab("Fuente"):
            refs.extend([x.strip() for x in re.split(r"(?<=\.)\s+(?=[A-ZÁÉÍÓÚÑ][\w'’\- ]+,\s[A-Z]\.)", r) if x.strip()])
        out[n] = {"title": title, "notes": notes, "refs": refs}
    return out

def main(slides_path, tema_path, img_dir, imgmap_path, notes_path=None, notes_en_path=None):
    slides = json.load(open(slides_path))
    tema = json.load(open(tema_path))
    imgmap = json.load(open(imgmap_path))
    notes = parse_notes(notes_path)
    notes_en = parse_notes(notes_en_path)
    sec_en = {}
    try:
        sec_en = json.load(open(os.path.join(os.path.dirname(__file__) or ".", "secciones_en.json")))
    except Exception:
        pass
    m = imgmap.get(tema["id"], {})
    cap = {c["img"]: c.get("caption", {}) for c in tema.get("cards", [])}
    sections, fichas = [], []
    cur_sec = None
    n = len(slides)
    if 1 in notes and notes[1]["notes"]:
        tema["intro"] = {"es": notes[1]["notes"], "en": notes_en.get(1, {"notes": []})["notes"]}
    for s in slides:
        i = s["slide"]
        title = (s.get("title") or "").strip()
        paras = [p.strip() for p in s.get("paras", []) if p and len(p.strip()) > 3]
        nt = notes.get(i, {"title": "", "notes": [], "refs": []})
        ne = notes_en.get(i, {"title": "", "notes": [], "refs": []})
        if i == 1 or i == n:
            continue
        mt = SEC_RE.match(title)
        if mt and not paras:
            cur_sec = mt.group(1)
            sections.append({"code": cur_sec, "title": {"es": mt.group(2).strip(), "en": sec_en.get(cur_sec, "")},
                             "intro": {"es": nt["notes"], "en": ne["notes"]}, "refs": nt["refs"]})
            continue
        if not title and paras and all(SEC_RE.match(p) or len(p) < 4 for p in paras):
            continue  # índice
        if paras and sum(is_ref(p) for p in paras) >= max(3, len(paras) - 1):
            continue  # bibliografía
        imgs = []
        for src, name in m.items():
            if src.startswith(f"s{i:02d}_"):
                p = f"{img_dir}/{name}.jpg"
                imgs.append({"src": p, "caption": cap.get(p, {})})
        if not title and nt["title"] and (paras or imgs) and not CONT_RE.search(nt["title"]):
            # diapositiva sin título propio: se usa el de las notas del orador
            title = nt["title"]
            if paras and paras[0].lower() == title.lower(): paras = paras[1:]
        if not title and paras and len(paras[0]) < 75 and not paras[0].endswith(".") and sum(len(x) for x in paras) > 250:
            title = paras[0]; paras = paras[1:]
        cont = bool(CONT_RE.search(title)) or (not title)
        if cont and fichas:
            f = fichas[-1]
            f["slides"].append(i); f["images"].extend(imgs); f["_paras"].extend(paras)
            f["_notes"].extend(nt["notes"]); f["_nrefs"].extend(nt["refs"]); f["_notes_en"].extend(ne["notes"])
            continue
        if not title:
            continue
        clean = re.sub(r"\s+", " ", CONT_RE.sub("", title)).rstrip(":.").strip()
        title_en = ne["title"] if (ne["title"] and not ne["title"].startswith("(")) else ""
        fichas.append({"id": slug(clean), "sec": cur_sec or "", "title": {"es": clean, "en": re.sub(r"\s+", " ", CONT_RE.sub("", title_en)).rstrip(":.").strip()},
                       "slides": [i], "images": imgs, "_paras": list(paras),
                       "_notes": list(nt["notes"]), "_nrefs": list(nt["refs"]), "_notes_en": list(ne["notes"])})
    seen = set()
    for k, f in enumerate(fichas, 1):
        nts = f.pop("_notes"); paras = f.pop("_paras"); nrefs = f.pop("_nrefs"); nen = f.pop("_notes_en")
        base = f["id"]; j = 2
        while f["id"] in seen:
            f["id"] = f"{base}-{j}"; j += 1
        seen.add(f["id"])
        f["code"] = f"H{tema['num']}·{k:02d}"
        f["source"] = "notas" if nts else "diapositiva"
        body = nts if nts else [p for p in paras if not is_ref(p)]
        f["essay"] = {"es": [p for p in body if p.startswith("Para el ensayo")], "en": [p for p in nen if p.startswith("For the essay")]}
        f["body"] = {"es": [p for p in body if not p.startswith("Para el ensayo")], "en": [p for p in nen if not p.startswith("For the essay")]}
        f["slide"] = {"es": [p for p in paras if not is_ref(p)] if nts else [], "en": []}
        refs, u = [], set()
        for r in nrefs + [p for p in paras if is_ref(p)]:
            key = re.sub(r"\W+", "", r.lower())[:60]
            if key not in u:
                u.add(key); refs.append(r)
        f["refs"] = refs
        u2, out = set(), []
        for im in f["images"]:
            if im["src"] not in u2:
                u2.add(im["src"]); out.append(im)
        f["images"] = out
    tema["sections"] = sections
    tema["fichas"] = fichas
    json.dump(tema, open(tema_path, "w"), ensure_ascii=False, indent=1)
    print(f"{tema_path}: {len(sections)} apartados, {len(fichas)} fichas, "
          f"{sum(len(f['images']) for f in fichas)} imágenes, "
          f"{sum(1 for f in fichas if f['source']=='notas')} con notas del orador, "
          f"{sum(len(f['body']['es']) for f in fichas)} párrafos, {sum(1 for f in fichas if f['body']['en'])} con versión en inglés")

if __name__ == "__main__":
    main(*sys.argv[1:7])
