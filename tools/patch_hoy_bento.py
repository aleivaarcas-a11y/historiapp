import re
p="index.html"; s=open(p,encoding="utf-8").read()
# CSS
a=s.index(".hoy{display:flex"); b=s.index("\n",s.index(".hoy .dice{"))
css=""".hoy{display:grid;grid-template-columns:1fr 1fr;gap:10px}
.hoy .card{position:relative;overflow:hidden;text-align:left;border-radius:18px;padding:14px;display:flex;flex-direction:column;gap:6px;border:1px solid var(--line);background:#fff;box-shadow:var(--shadow);cursor:pointer;min-width:0}
.hoy .card small{position:relative;z-index:1;font-size:10.5px;text-transform:uppercase;letter-spacing:.06em;font-weight:800;color:var(--muted)}
.hoy .card b{position:relative;z-index:1;font-size:17px;color:var(--primary-2);line-height:1.2}
.hoy .reto{grid-column:1/-1;flex-direction:row;align-items:center;gap:14px;background:#fff8e1;border:2px solid var(--accent)}
.hoy .reto .ic{flex:0 0 52px;height:52px;border-radius:16px;background:var(--accent);display:flex;align-items:center;justify-content:center;font-size:28px}
.hoy .reto .tx{flex:1;display:flex;flex-direction:column;gap:3px;min-width:0}
.hoy .reto .tx span{font-size:12.5px;color:var(--ink);line-height:1.3}
.hoy .reto .xp{flex:0 0 auto;font-size:13px;font-weight:800;color:var(--primary-2);background:#fff;border:1.5px solid var(--accent);border-radius:999px;padding:6px 10px}
.hoy .dep,.hoy .pil{background:#0b2545 center/cover no-repeat;border:0;color:#fff}
.hoy .dep{min-height:200px;justify-content:flex-end}
.hoy .ov{position:absolute;inset:0;background:linear-gradient(180deg,rgba(0,0,0,.05) 25%,rgba(0,0,0,.78))}
.hoy .dep small,.hoy .pil small{color:#fff;opacity:.95;position:absolute;top:12px;left:12px;right:56px;text-shadow:0 1px 3px rgba(0,0,0,.6)}
.hoy .dep b,.hoy .pil b{color:#fff;font-size:18px;text-shadow:0 1px 4px rgba(0,0,0,.5)}
.hoy .dep .w{position:relative;z-index:1;font-size:12px;line-height:1.3;color:#f1f1f1;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden}
.hoy .dep .dice{position:absolute;z-index:2;top:8px;right:8px;width:40px;height:40px;font-size:20px;border-radius:12px;border:0;background:rgba(255,255,255,.92)}
.hoy .efe{min-height:200px;background:linear-gradient(170deg,#eaf1fb,#fff 60%)}
.hoy .efe .yr{font-size:34px;font-weight:800;color:var(--primary);line-height:1}
.hoy .efe .dd{font-size:12px;font-weight:700;color:var(--muted)}
.hoy .efe .tx{font-size:12.5px;line-height:1.35;color:var(--ink);display:-webkit-box;-webkit-line-clamp:5;-webkit-box-orient:vertical;overflow:hidden}
.hoy .pil{grid-column:1/-1;min-height:150px;flex-direction:row;align-items:flex-end;gap:12px}
.hoy .pil .pb{position:relative;z-index:1;flex:0 0 48px;height:48px;border-radius:50%;background:rgba(255,255,255,.95);color:#0b2545;display:flex;align-items:center;justify-content:center;font-size:20px;padding-left:3px}
.hoy .pil b{flex:1;align-self:center;margin-top:18px}
"""
s=s[:a]+css.rstrip("\n")+s[b:]
def rep(old,new):
    global s; assert s.count(old)==1,old[:60]; s=s.replace(old,new)
rep('''const rc=document.createElement("button"); rc.className="card reto";
  rc.innerHTML=`<small>☀️ ${t("dailyCard")}</small><b>${done?t("dailyScore",{a:d.correct,b:d.total}):t("daily")}</b><span>${t("dailySub")}</span><div class="ft"><span>${done?"✓":"×2 XP"}</span><span>›</span></div>`;
  rc.onclick=()=>nav({name:"daily"}); hoy.appendChild(rc);''',
'''const rc=document.createElement("button"); rc.className="card reto";
  rc.innerHTML=`<div class="ic" aria-hidden="true">${done?"✅":"☀️"}</div><div class="tx"><small>${t("dailyCard")}</small><b>${done?t("dailyScore",{a:d.correct,b:d.total}):t("dailyStart")}</b><span>${done?t("dailyBack"):t("dailySub")}</span></div><div class="xp">${done?"✓":"×2 XP"}</div>`;
  rc.onclick=()=>nav({name:"daily"}); hoy.appendChild(rc);
  const slot=c=>{ const x=document.createElement("div"); x.className="card "+c; x.style.display="none"; hoy.appendChild(x); return x; };
  const sDep=slot("dep"), sEfe=slot("efe"), sPil=slot("pil");''')
rep('''const e=encDaily(E); const c=document.createElement("div"); c.className="card";
    c.innerHTML=`<small>🏅 ${t("encCard")}</small><b>${esc(L(e.name))}</b><span>${md(L(e.cuando))}</span><div class="ft"><button class="dice" aria-label="${esc(t("encRand"))}">🎲</button><span>${t("open")} ›</span></div>`;''',
'''const e=encDaily(E); const c=sDep; c.setAttribute("role","button");
    if(e.img&&e.img.src) c.style.backgroundImage=`url('${e.img.src}')`;
    c.innerHTML=`<div class="ov"></div><small>🏅 ${t("encCard")}</small><b>${esc(L(e.name))}</b><span class="w">${plain(L(e.cuando))}</span><button class="dice" aria-label="${esc(t("encRand"))}">🎲</button>`; c.style.display="";''')
rep('''c.style.cursor="pointer"; hoy.appendChild(c); } }catch(e){}''','''} }catch(e){}''')
rep('''const f=F[k]; const c=document.createElement("button"); c.className="card";
    c.innerHTML=`<small>📅 ${t("efeCard")} · ${esc(fmtDay(k))}</small><b>${esc(String(f.year||""))}</b><span>${md(L(f))}</span><div class="ft"><span></span><span>${t("open")} ›</span></div>`;
    c.onclick=()=>nav({name:"efe"}); hoy.appendChild(c); } }catch(e){}''',
'''const f=F[k]; const c=sEfe; c.setAttribute("role","button");
    c.innerHTML=`<small>📅 ${t("efeCard")}</small><div class="yr">${esc(String(f.year||""))}</div><div class="dd">${esc(fmtDay(k))}</div><div class="tx">${md(L(f))}</div>`;
    c.onclick=()=>nav({name:"efe"}); c.style.display=""; } }catch(e){}''')
rep('''const p=vids[dayHash(todayKey()+"v")%vids.length]; const c=document.createElement("button"); c.className="card";
      c.innerHTML=`<small>▶ ${t("pilCard")} · ${t("tema")} ${p.num}</small><b>${esc(L(p.v.title))}</b><span>${t("pilSub")}</span><div class="ft"><span></span><span>${t("open")} ›</span></div>`;
      c.onclick=()=>nav({name:"mode",num:p.num,mode:"videos"}); hoy.appendChild(c); } }catch(e){}''',
'''const p=vids[dayHash(todayKey()+"v")%vids.length]; const c=sPil; c.setAttribute("role","button");
      if(p.v.poster) c.style.backgroundImage=`url('${L(p.v.poster)}')`;
      c.innerHTML=`<div class="ov"></div><small>🎬 ${t("pilCard")} · ${t("tema")} ${p.num}</small><div class="pb" aria-hidden="true">▶</div><b>${esc(L(p.v.title))}</b>`;
      c.onclick=()=>nav({name:"mode",num:p.num,mode:"videos"}); c.style.display=""; } }catch(e){}''')
s=re.sub(r'historiapp-v(\d+)',lambda m:'historiapp-v'+str(int(m.group(1))),s)
open(p,"w",encoding="utf-8").write(s); print("ok")
