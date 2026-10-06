# Historiapp: barra del pódcast completa (06-10-2026): -15, play/pausa, +30, velocidad, cerrar y barra de progreso.
# Tocar el título abre el reproductor grande si el episodio está en la lista; si no, va al pódcast del tema.
import re, pathlib, shutil
root = pathlib.Path(__file__).resolve().parent.parent
idx = root/"index.html"; sw = root/"sw.js"
bak = root/"tools"/"index_antes_podbar.html"
if not bak.exists(): shutil.copy(idx, bak)
h = idx.read_text(encoding="utf-8")
def rep(a, b):
    global h
    if b in h: return
    assert h.count(a) == 1, a[:70]
    h = h.replace(a, b)
rep('<button id="pbB">−15</button><button id="pbP">▶</button><button id="pbX">✕</button></div>',
    '<button id="pbB" aria-label="-15 s">−15</button><button id="pbP" class="pp">▶</button><button id="pbF" aria-label="+30 s">+30</button><button id="pbS" class="sp">1×</button><button id="pbX" aria-label="Cerrar">✕</button><i id="pbL"></i></div>')
rep('  document.getElementById("pbT").onclick=()=>{ if(POD.tema) nav({name:"mode",num:POD.tema,mode:"podcast"}); };',
    '''  document.getElementById("pbF").onclick=()=>{ a.currentTime=Math.min((a.duration||1e9)-1,a.currentTime+30); };
  document.getElementById("pbS").onclick=()=>{ if(!POD.ep) return; const st=podState(POD.ep.id), r=[0.75,1,1.25,1.5,1.75], n=r[(r.indexOf(st.rate||1)+1)%r.length]; st.rate=n; a.playbackRate=n; save(); podUI(); };
  document.getElementById("pbT").onclick=()=>{ const it=(typeof PD_L!=="undefined"&&POD.ep)?PD_L.find(x=>x&&x.ep&&x.ep.id===POD.ep.id):null; if(it){ pdOpenFull(it); return; } if(POD.tema) nav({name:"mode",num:POD.tema,mode:"podcast"}); };''')
rep('''    document.getElementById("pbP").textContent=a.paused?"▶":"❚❚"; }''',
    '''    document.getElementById("pbP").textContent=a.paused?"▶":"❚❚";
    const r0=podState(POD.ep.id).rate||1; document.getElementById("pbS").textContent=String(r0).replace(".",S.lang==="es"?",":".")+"×";
    const dd=a.duration||POD.ep.dur||0; document.getElementById("pbL").style.width=(dd?Math.min(100,a.currentTime/dd*100):0)+"%"; }''')
CSS = """/* podbar-INI */
#podbar{gap:6px;overflow:hidden;padding:8px 8px 10px}
#podbar button{width:36px;height:36px;font-size:13px;flex-shrink:0;padding:0}
#podbar .pp{width:40px;height:40px;background:#fff;color:#002060;font-size:15px}
#podbar .sp{width:auto;min-width:40px;padding:0 8px;background:#EDAB00;color:#002060}
#pbL{position:absolute;left:0;bottom:0;height:3px;width:0;background:#FBAE40;transition:width .3s linear}
@media (max-width:420px){#podbar img{display:none}}
/* podbar-FIN */
"""
if "podbar-INI" not in h:
    i = h.index("</style>"); h = h[:i] + CSS + h[i:]
idx.write_text(h, encoding="utf-8")
s = sw.read_text(encoding="utf-8"); m = re.search(r'historiapp-v(\d+)', s)
sw.write_text(s.replace(m.group(0), f"historiapp-v{int(m.group(1))+1}", 1), encoding="utf-8")
print("ok", f"sw v{int(m.group(1))+1}")
