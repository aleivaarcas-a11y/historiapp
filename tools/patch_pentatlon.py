# Juego del Tema 3, «Pentatlón: de Élide a Olimpia» (11-10-2026).
# El juego vive en juegos/pentatlon.html (se genera fuera, en Juegos web) y lee su contenido de las fichas del Tema 3.
# Este parche añade su tarjeta en Inicio y su botón en la página del Tema 3, y lo guarda para usarlo sin conexión.
import pathlib, sys, shutil
root = pathlib.Path(__file__).resolve().parent.parent
p = root / "index.html"; s = p.read_text(encoding="utf-8")
if "juegos/pentatlon.html" in s: sys.exit("ya aplicado")
shutil.copy(p, root / "tools/index_antes_pentatlon.html")
def rep(a, b, n=1):
    global s
    c = s.count(a)
    if c != n: sys.exit(f"ERROR ({c}): {a[:90]}")
    s = s.replace(a, b)
rep('hoy:"Hoy"', 'hoy:"Hoy", gameCard:"Juego del Tema 3", gameTitle:"Pentatlón: de Élide a Olimpia", gameSub:"Viaja a Élide, supera la prueba de acceso y compite en Olimpia"')
rep('hoy:"Today"', 'hoy:"Today", gameCard:"Unit 3 game", gameTitle:"Pentathlon: from Elis to Olympia", gameSub:"Travel to Elis, pass the entry trial and compete at Olympia"')
rep('rc.onclick=()=>nav({name:"daily"}); hoy.appendChild(rc); rkHomeCard(hoy);',
    'rc.onclick=()=>nav({name:"daily"}); hoy.appendChild(rc); rkHomeCard(hoy);\n'
    '  { const gc=document.createElement("button"); gc.className="card reto"; gc.innerHTML=`<div class="ic" aria-hidden="true">🏛️</div><div class="tx"><small>${t("gameCard")}</small><b>${t("gameTitle")}</b><span>${t("gameSub")}</span></div><div class="xp">XP</div>`; gc.onclick=()=>{ location.href="juegos/pentatlon.html"; }; hoy.appendChild(gc); }')
rep('const g=document.getElementById("modes");',
    'const g=document.getElementById("modes");\n'
    '  if(String(num)==="3"){ const gb=document.createElement("button"); gb.className="mode wide"; gb.innerHTML=`<div class="ic">🏛️</div><b>${t("gameTitle")}</b><span>${t("gameSub")}</span>`; gb.onclick=()=>{ location.href="juegos/pentatlon.html"; }; g.appendChild(gb); }')
p.write_text(s, encoding="utf-8")
w = root / "sw.js"; t = w.read_text(encoding="utf-8")
import re
v = int(re.search(r'historiapp-v(\d+)', t).group(1))
t = t.replace(f'historiapp-v{v}"', f'historiapp-v{v+1}"').replace('"./index.html", ', '"./index.html", "./juegos/pentatlon.html", ', 1)
w.write_text(t, encoding="utf-8")
print("aplicado, sw v", v + 1)
