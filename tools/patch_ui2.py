#!/usr/bin/env python3
"""Portada del tema cuadrada (Mapa arriba a todo lo ancho; Vídeos y Pódcast abajo a todo lo ancho)
y botón del modo scroll de los vídeos más claro.  Uso: python3 tools/patch_ui2.py"""
import os
R = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
p = os.path.join(R, 'index.html'); s = open(p, encoding='utf-8').read()
if '.mode.wide' in s:
    print('ya aplicado'); raise SystemExit

CSS = '''.mode.wide{grid-column:1/-1;display:grid;grid-template-columns:40px 1fr auto;column-gap:12px;row-gap:2px;align-items:center;min-height:0;padding:14px 16px}
.mode.wide .ic{grid-row:1/3;font-size:30px}
.mode.wide b,.mode.wide span:not(.pill){grid-column:2}
.mode.wide .pill{grid-column:3;grid-row:1/3;margin-top:0!important}
.mode.wide .prog{grid-column:1/-1;margin-top:8px}
.mode.wide .done{top:50%;transform:translateY(-50%);right:14px}
.mode.first{order:-1}
.vfeedbtn{width:100%;margin-bottom:14px;display:flex;flex-direction:row;align-items:center;gap:14px;background:linear-gradient(135deg,#002060,#004379);color:#fff;border:0;border-radius:var(--radius);padding:14px 16px;text-align:left;box-shadow:var(--shadow);cursor:pointer}
.vfeedbtn .vft{flex:1;display:flex;flex-direction:column;gap:3px}
.vfeedbtn .vft b{font-size:16px}
.vfeedbtn .vft small{font-size:12.5px;opacity:.88;line-height:1.35;font-weight:500}
.vfeedbtn .vfgo{font-size:26px;opacity:.9}
.vfph{display:block;position:relative;flex:0 0 auto;width:34px;height:58px;border:2.5px solid #fff;border-radius:9px;overflow:hidden}
.vfph i{position:absolute;left:4px;right:4px;height:22px;border-radius:4px;background:#FBAE40;animation:vfs 1.8s linear infinite}
.vfph i:nth-child(2){background:#fff;opacity:.75;animation-delay:-.9s}
.vfhand{position:absolute;right:-9px;bottom:-4px;font-size:18px;animation:vfh 1.8s ease-in-out infinite}
.vfwrap{display:block;position:relative;flex:0 0 auto;margin-right:6px}
@keyframes vfs{from{top:56px}to{top:-26px}}
@keyframes vfh{0%,100%{transform:translateY(4px)}50%{transform:translateY(-12px)}}
@media (prefers-reduced-motion:reduce){.vfph i,.vfhand{animation:none}.vfph i{top:14px}.vfph i:nth-child(2){display:none}}
</style>'''
assert s.count('</style>') == 1
s = s.replace('</style>', CSS, 1)

old = '''    const b=document.createElement("button"); b.className="mode";'''
assert old in s
s = s.replace(old, old + '''
    if(m==="mapa") b.classList.add("wide","first"); if(MEDIA.includes(m)) b.classList.add("wide");''', 1)

old = '''<button class="btn vfeedbtn" id="vFeed">${t("vFeed")}<small>${t("vFeedSub")}</small></button>'''
assert old in s
s = s.replace(old, '''<button class="vfeedbtn" id="vFeed"><span class="vfwrap"><span class="vfph"><i></i><i></i></span><span class="vfhand">👆</span></span><span class="vft"><b>${t("vFeed")}</b><small>${t("vFeedSub")}</small></span><span class="vfgo">›</span></button>''', 1)

s = s.replace('vFeed:"▶ Verlos seguidos", vFeedSub:"Desliza hacia arriba para pasar al siguiente"',
              'vFeed:"Modo scroll", vFeedSub:"Desliza hacia arriba y los vídeos pasan uno tras otro, como en TikTok o Reels"', 1)
s = s.replace('vFeed:"▶ Watch them in a row", vFeedSub:"Swipe up for the next one"',
              'vFeed:"Scroll mode", vFeedSub:"Swipe up and the videos play one after another, like TikTok or Reels"', 1)
assert 'Modo scroll' in s and 'Scroll mode' in s
open(p, 'w', encoding='utf-8').write(s)
print('ok')
