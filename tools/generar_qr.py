#!/usr/bin/env python3
"""Genera un PNG con QR y código corto por cada ficha, para pegar en la diapositiva que corresponda.

Uso: python3 generar_qr.py https://USUARIO.github.io/historiapp/ data/tema02.json qr/t2
Necesita: pip install qrcode pillow
Escribe también qr/t2/indice.csv con código, diapositivas de origen, título y enlace.
"""
import sys, json, os, csv
import qrcode
from PIL import Image, ImageDraw, ImageFont

base, tema_path, out = sys.argv[1].rstrip("/") + "/", sys.argv[2], sys.argv[3]
os.makedirs(out, exist_ok=True)
tema = json.load(open(tema_path))
font = small = None
for cand in ["/Library/Fonts/Microsoft/Calibri.ttf", "/Applications/Microsoft PowerPoint.app/Contents/Resources/DFonts/Calibri.ttf",
             "/usr/share/fonts/truetype/crosextra/Carlito-Bold.ttf", "/System/Library/Fonts/Supplemental/Arial Bold.ttf", "/System/Library/Fonts/Helvetica.ttc"]:
    try:
        font = ImageFont.truetype(cand, 48); small = ImageFont.truetype(cand, 26); break
    except Exception:
        continue
if font is None:
    font = small = ImageFont.load_default()
rows = []
for f in tema["fichas"]:
    url = f"{base}#t{tema['num']}/f/{f['id']}"
    qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_M, box_size=10, border=2)
    qr.add_data(url); qr.make(fit=True)
    q = qr.make_image(fill_color="#1f4e79", back_color="white").convert("RGB")
    W = q.width; H = q.height + 110
    im = Image.new("RGB", (W, H), "white"); im.paste(q, (0, 0)); d = ImageDraw.Draw(im)
    d.text((W // 2, q.height + 20), f["code"], fill="#1f4e79", font=font, anchor="mt")
    d.text((W // 2, q.height + 72), "Historiapp", fill="#888888", font=small, anchor="mt")
    name = f"{f['code'].replace('·', '-')}_{f['id']}.png"
    im.save(os.path.join(out, name))
    rows.append([f["code"], " ".join(str(x) for x in f["slides"]), f["title"]["es"], url, name])
with open(os.path.join(out, "indice.csv"), "w", newline="") as fh:
    w = csv.writer(fh); w.writerow(["codigo", "diapositivas", "titulo", "enlace", "archivo"]); w.writerows(rows)
print(len(rows), "QR en", out)
