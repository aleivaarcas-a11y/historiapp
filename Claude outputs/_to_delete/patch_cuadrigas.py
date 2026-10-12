# Juego del Tema 4, «Cuadrigas» (12-10-2026).
# El juego vive en juegos/cuadrigas.html (se genera fuera, en Juegos web/Codigo/cuadrigas con build.py --historiapp).
# Este parche añade su tarjeta en Inicio, junto a la del Pentatlón, y su botón en la página del Tema 4 cuando el tema
# esté publicado, y lo guarda para usarlo sin conexión. Los resultados y los fantasmas van al Apps Script del ranking (v4).
import pathlib, sys, shutil, re
root = pathlib.Path(__file__).resolve().parent.parent
p = root / "index.html"; s = p.read_text(encoding="utf-8")
if "juegos/cuadrigas.html" in s: sys.exit("ya aplicado")
shutil.copy(p, root / "tools/index_antes_cuadrigas.html")
def rep(a, b, n=1):
    global s
    c = s.count(a)
    if c != n: sys.exit(f"ERROR ({c}): {a[:90]}")
    s = s.replace(a, b)
rep('gameCard:"Juego del Tema 3",', 'game4Card:"Juego del Tema 4", game4Title:"Cuadrigas: carreras en el circo romano", game4Sub:"Dirige una cuadra en Tarraco, conduce bigas y cuadrigas y llega al Circo Máximo", gameCard:"Juego del Tema 3",')
rep('gameCard:"Unit 3 game",', 'game4Card:"Unit 4 game", game4Title:"Chariots: racing in the Roman circus", game4Sub:"Run a stable in Tarraco, drive bigae and quadrigae and reach the Circus Maximus", gameCard:"Unit 3 game",')
rep('gc.onclick=()=>{ location.href="juegos/pentatlon.html"; }; hoy.appendChild(gc); }',
    'gc.onclick=()=>{ location.href="juegos/pentatlon.html"; }; hoy.appendChild(gc); }\n'
    '  { const g4=document.createElement("button"); g4.className="card reto"; g4.innerHTML=`<div class="ic" aria-hidden="true">🏇</div><div class="tx"><small>${t("game4Card")}</small><b>${t("game4Title")}</b><span>${t("game4Sub")}</span></div><div class="xp">XP</div>`; g4.onclick=()=>{ location.href="juegos/cuadrigas.html"; }; hoy.appendChild(g4); }')
rep('if(String(num)==="3"){ const gb=document.createElement("button");',
    'if(String(num)==="4"){ const g4=document.createElement("button"); g4.className="mode wide"; g4.innerHTML=`<div class="ic">🏇</div><b>${t("game4Title")}</b><span>${t("game4Sub")}</span>`; g4.onclick=()=>{ location.href="juegos/cuadrigas.html"; }; g.appendChild(g4); }\n'
    '  if(String(num)==="3"){ const gb=document.createElement("button");')
p.write_text(s, encoding="utf-8")
w = root / "sw.js"; t = w.read_text(encoding="utf-8")
v = int(re.search(r'historiapp-v(\d+)', t).group(1))
t = t.replace(f'historiapp-v{v}"', f'historiapp-v{v+1}"').replace('"./juegos/pentatlon.html", ', '"./juegos/pentatlon.html", "./juegos/cuadrigas.html", ', 1)
w.write_text(t, encoding="utf-8")
print("aplicado, sw v", v + 1)
