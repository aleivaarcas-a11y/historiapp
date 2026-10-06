# Historiapp: formato iPad / tableta (06-10-2026). Añade un bloque CSS que solo actúa a partir de 768 px de ancho.
# Uso: python3 tools/patch_ipad.py   (idempotente: si el bloque ya está, lo sustituye)
import re, shutil, pathlib
root = pathlib.Path(__file__).resolve().parent.parent
idx = root/"index.html"; sw = root/"sw.js"
bak = root/"tools"/"index_antes_ipad.html"
if not bak.exists(): shutil.copy(idx, bak)
CSS = """/* iPad-INI */
/* Menú inferior fijo: que nada quede tapado (todas las pantallas) */
.deck{height:calc(100dvh - 340px - var(--safe-top) - var(--safe-bottom));min-height:300px}
.sheet .sq{display:flex;gap:10px;align-items:center;font-size:14px;line-height:1.4;font-style:italic;color:var(--muted);border-left:3px solid var(--accent);padding:2px 0 2px 10px;margin:0 0 10px}
.sheet .sq img{width:56px;height:56px;object-fit:cover;border-radius:8px;flex-shrink:0;font-style:normal}
body.podon main{padding-bottom:calc(156px + var(--safe-bottom))}
body.podon .deck{height:calc(100dvh - 406px - var(--safe-top) - var(--safe-bottom))}
@media (min-width:768px){
  #app{max-width:1100px}
  #tabbar{max-width:1100px}
  #podbar{max-width:640px}
  .sheet .in{max-width:640px}
  main{padding:24px 32px calc(100px + var(--safe-bottom))}
  main>*{width:100%;max-width:900px;margin-left:auto;margin-right:auto}
  .grid,.vlist,.tgrid{grid-template-columns:repeat(3,1fr);gap:16px}
  .lg-ach{grid-template-columns:repeat(3,1fr)}
  .ficha{max-width:760px}
  .deck,.swipe-btns,.swipe-hint{max-width:680px}
  .ficha h2{font-size:26px}
  .ficha .body p{font-size:17px;line-height:1.65}
  .vplayer{max-width:440px;margin-left:auto;margin-right:auto}
  .vplayer video{max-height:78vh}
  /* feed: botones y rótulo junto al vídeo vertical, no en los bordes de la pantalla */
  .fside{right:max(10px,calc(50% - 28.125dvh - 76px))}
  .fcap{left:max(14px,calc(50% - 28.125dvh + 14px));right:max(86px,calc(50% - 28.125dvh + 14px))}
}
@media (min-width:1100px){
  .grid,.vlist,.tgrid{grid-template-columns:repeat(4,1fr)}
  main>*{max-width:1000px}
}
/* iPad-FIN */
"""
h = idx.read_text(encoding="utf-8")
h = re.sub(r"/\* iPad-INI \*/.*?/\* iPad-FIN \*/\n", "", h, flags=re.S)
i = h.index("</style>")
h = h[:i] + CSS + h[i:]
# Enunciado (y miniatura) dentro de la hoja de respuesta, para no perderlo de vista
def rep(a,b):
    global h
    if b in h: return
    assert h.count(a)==1, a[:60]; h=h.replace(a,b)
rep('function sheet(ok,title,explain,xp,onNext){', 'function sheet(ok,title,explain,xp,onNext,q,qimg){')
rep('${esc(title)}</div>\n    <div class="exp">', '${esc(title)}</div>${q?`<div class="sq">${qimg?`<img src="${esc(qimg)}" alt="">`:""}<span>${esc(q)}</span></div>`:""}\n    <div class="exp">')
rep('L(it.explain), xp, ()=>{ pos++; if(pos>=order.length) finishRound(m,tema,mode,correct,order.length,()=>modeSwipe(tema,mode,m),opts); else draw(); });',
    'L(it.explain), xp, ()=>{ pos++; if(pos>=order.length) finishRound(m,tema,mode,correct,order.length,()=>modeSwipe(tema,mode,m),opts); else draw(); }, L(it.claim), it.img||"");')
rep('L(it.explain), xp, ()=>{ pos++; if(pos>=order.length) finishRound(m,tema,mode,correct,order.length,()=>modeChoice(tema,mode,m),opts); else draw(); }); };',
    'L(it.explain), xp, ()=>{ pos++; if(pos>=order.length) finishRound(m,tema,mode,correct,order.length,()=>modeChoice(tema,mode,m),opts); else draw(); }, L(mode==="sources"?it.question:it.q)); };')
# Velocidad 0,75x en el pódcast
h = h.replace("[1,1.25,1.5,1.75]", "[0.75,1,1.25,1.5,1.75]")
idx.write_text(h, encoding="utf-8")
s = sw.read_text(encoding="utf-8")
m = re.search(r'historiapp-v(\d+)', s)
s = s.replace(m.group(0), f"historiapp-v{int(m.group(1))+1}", 1)
sw.write_text(s, encoding="utf-8")
print("ok, sw", f"v{int(m.group(1))+1}")
