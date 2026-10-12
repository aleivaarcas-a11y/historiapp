# Atlas: mapa político por épocas con las civilizaciones coloreadas (12-10-2026). Idempotente.
import os,sys
H=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','..')
P=os.path.join(H,'atlas','index.html'); s=open(P,encoding='utf-8').read()
if 'ERBY' in s: print('ya aplicado'); sys.exit()
def rep(a,b):
    global s
    assert s.count(a)==1,(s.count(a),a[:80]); s=s.replace(a,b)
rep("GEO:{prov:M.prov,layers:M.layers}","GEO:{prov:M.prov,layers:M.layers,eras:M.eras||[],ecol:M.ecol||{}}")
# textos
rep("provSites:'Lugares del temario en esta provincia',","provSites:'Lugares del temario en esta provincia',L_era:'Mapa político hacia el {y}',L_eraS:'Fronteras aproximadas',polSites:'Lugares del temario en este territorio',polNone:'Ningún lugar del temario cae dentro de este territorio.',polNote:'Fronteras aproximadas de historical-basemaps (A. Ourednik), un mapa mundial de trabajo que conviene contrastar con un atlas histórico. Los pueblos sin Estado llevan un sombreado tenue.',polChip:'Hacia el {y}',")
rep("provSites:'Places of the syllabus in this province',","provSites:'Places of the syllabus in this province',L_era:'Political map around {y}',L_eraS:'Approximate borders',polSites:'Places of the syllabus in this territory',polNone:'No place of the syllabus lies in this territory.',polNote:'Approximate borders from historical-basemaps (A. Ourednik), a working world map that should be checked against a historical atlas. Peoples without a state have a faint shading.',polChip:'Around {y}',")
rep("credit:'Fronteras: AWMC, ODbL · Costas y ríos: Natural Earth',","credit:'Fronteras: historical-basemaps (Ourednik, GPL-3.0) y AWMC (ODbL) · Costas y ríos: Natural Earth',")
rep("credit:'Borders: AWMC, ODbL · Coasts and rivers: Natural Earth',","credit:'Borders: historical-basemaps (Ourednik, GPL-3.0) and AWMC (ODbL) · Coasts and rivers: Natural Earth',")
# datos
rep("const PROVCOL=[","const ECOL=GEO.ecol;const ERAS=GEO.eras.map(e=>({id:e.id,from:e.from,to:e.to,pols:e.pols.map((p,i)=>({f:p.f,n:p.n,lab:p.lab,a:p.a,i,path:P2(p.d)}))}));const ERBY={};ERAS.forEach(e=>ERBY[e.id]=e);\nconst eraY=id=>id.startsWith('bc')?-(+id.slice(2)):+id;const ROMT=['#B6402C','#C9583C','#A23527','#D06A48','#B44A36'];let selPol=null;\nconst eraOf=l=>l&&l.startsWith('e:')?ERBY[l.slice(2)]:null;\nconst PROVCOL=[")
rep("function layerAt(y){if(y==null)return null;if(y>=-550&&y<-334)return'persia';if(y>=-334&&y<-300)return'alejandro';if(y>=-146&&y<-27)return'roma60';if(y>=-27&&y<=476)return'prov';return'none'}",
    "function layerAt(y){if(y==null)return ERBY['200']?'e:200':null;if(y<-3000)return'none';const e=ERAS.find(e=>y>=e.from&&y<=e.to);return e?'e:'+e.id:'none'}")
rep("function renderLayer(){const l=layerAt(Y),e=$('layer');if(!l){e.hidden=true;return}e.hidden=false;\n  e.innerHTML=`${t('L_'+l)}<small>${t('L_'+l+'S')}${l!=='none'?' · '+t('credit'):''}</small>`}",
    "function renderLayer(){const l=Y==null?null:layerAt(Y),e=$('layer');if(!l){e.hidden=true;return}e.hidden=false;const E=eraOf(l);\n  e.innerHTML=E?`${t('L_era',{y:fmtY(eraY(E.id))})}<small>${t('L_eraS')} · ${t('credit')}</small>`:`${t('L_'+l)}<small>${t('L_'+l+'S')}</small>`;if(openState&&openState.t==='q'&&openState.era!==(E&&E.id))closePanel()}")
# pintura
rep("  if(lay==='prov'||lay==null){for(const p of PROV){g.fillStyle=hexA(PROVCOL[(p.i*7)%PROVCOL.length],lay==='prov'?.40:.32);g.fill(p.path,'evenodd')}}\n  else if(lay&&lay!=='none'){",
    "  const E=eraOf(lay),wp=E&&E.id==='200';\n  if(E){for(const pass of[0,1])for(const p of E.pols){if((p.f==='pue')!==(pass===0))continue;if(wp&&p.f==='rom')continue;const c=ECOL[p.f]||'#777777';\n      if(p.f==='pue'){g.fillStyle=hexA(c,.13);g.fill(p.path,'evenodd');g.setLineDash([4/k,4/k]);g.strokeStyle=hexA(c,.5);g.lineWidth=1/k;g.stroke(p.path);g.setLineDash([]);continue}\n      g.fillStyle=hexA(c,.46);g.fill(p.path,'evenodd');g.save();g.clip(p.path,'evenodd');g.strokeStyle=hexA(c,.6);g.lineWidth=9/k;g.stroke(p.path);g.restore();g.strokeStyle=hexA(c,1);g.lineWidth=1.5/k;g.stroke(p.path)}\n    if(wp)for(const p of PROV){g.fillStyle=hexA(ROMT[(p.i*3)%ROMT.length],.5);g.fill(p.path,'evenodd')}}\n  else if(lay==='prov'||lay==null){for(const p of PROV){g.fillStyle=hexA(PROVCOL[(p.i*7)%PROVCOL.length],lay==='prov'?.40:.32);g.fill(p.path,'evenodd')}}\n  else if(lay&&lay!=='none'&&LAY[lay]){")
rep("  if(lay==='prov'||lay==null){g.strokeStyle='rgba(60,36,18,.7)';g.lineWidth=1.1/k;for(const p of PROV)g.stroke(p.path)}",
    "  if(wp||lay==='prov'||lay==null){g.strokeStyle=wp?'rgba(90,20,12,.75)':'rgba(60,36,18,.7)';g.lineWidth=1.1/k;for(const p of PROV)g.stroke(p.path)}")
# selección de territorio
rep("  if(hov&&hov.startsWith('p:')){","  {const E=eraOf(lay);if(E&&selPol!=null&&E.pols[selPol]){ctx.fillStyle='rgba(242,213,140,.30)';ctx.fill(E.pols[selPol].path,'evenodd');ctx.strokeStyle='#f6d27a';ctx.lineWidth=3/k;ctx.stroke(E.pols[selPol].path)}\n   if(E&&hov&&hov.startsWith('q:')){const p=E.pols[+hov.slice(2)];if(p){ctx.fillStyle='rgba(255,245,210,.16)';ctx.fill(p.path,'evenodd')}}}\n  if(hov&&hov.startsWith('p:')){")
# rótulos
rep("  if(lay==='prov'||(lay==null&&k>1.6)){for(const p of PROV){",
    "  const LE=eraOf(lay),LWP=LE&&LE.id==='200';\n  if(LE){ctx.textBaseline='middle';for(const p of LE.pols){if(LWP&&p.f==='rom')continue;const pa=p.a*67.5*k*k,pue=p.f==='pue';if(pa<(pue?16000:3500)&&selPol!==p.i)continue;const[x,y]=sc(p.lab);if(x<-120||x>VW+120||y<-40||y>VH+40)continue;\n      const fs=Math.max(pue?9:10.5,Math.min(pue?14:21,Math.sqrt(pa)/(pue?13:9)));ctx.font=`${pue?'italic ':'600 '}${fs}px ${serif}`;const nm=L(p.n).toUpperCase();ctx.lineWidth=3;ctx.lineJoin='round';ctx.strokeStyle='rgba(246,236,210,.75)';\n      const w=[...nm].reduce((a,ch)=>a+ctx.measureText(ch).width+fs*.14,-fs*.14);ctx.strokeText(nm,x,y);ctx.fillStyle=pue?'rgba(80,70,55,.7)':'rgba(38,24,12,.9)';ctx.fillText(nm,x,y)}}\n  if(LWP&&k>1.3||lay==='prov'||(lay==null&&k>1.6)){for(const p of PROV){")
rep("  else if(lay&&lay!=='none'){const[x,y]=sc(LAY[lay].lab);","  else if(LE){}\n  else if(lay&&lay!=='none'&&LAY[lay]){const[x,y]=sc(LAY[lay].lab);")
# elegir territorio
rep("  for(const p of PROV)if(hit.isPointInPath(p.path,mx,my,'evenodd'))return{t:'p',id:p.id};return null}",
    "  const E=eraOf(layerAt(Y));if(E&&E.id==='200'||!E){for(const p of PROV)if(hit.isPointInPath(p.path,mx,my,'evenodd'))return{t:'p',id:p.id}}\n  if(E){let b=null;for(const p of E.pols){if(E.id==='200'&&p.f==='rom')continue;if(hit.isPointInPath(p.path,mx,my,'evenodd')&&(!b||(b.f==='pue'&&p.f!=='pue')||(b.f==='pue')===(p.f==='pue')&&p.a<b.a))b=p}if(b)return{t:'q',id:b.i}}return null}")
rep("function pick(sx,sy){const h=pickTarget(sx,sy);if(!h){closePanel();return}if(h.t==='s')openSite(h.id,false);else openProv(h.id)}",
    "function pick(sx,sy){const h=pickTarget(sx,sy);if(!h){closePanel();return}if(h.t==='s')openSite(h.id,false);else if(h.t==='q')openPol(h.id);else openProv(h.id)}")
rep("function closePanel(){$('panel').hidden=true;selSite=null;selProv=null;","function closePanel(){$('panel').hidden=true;selSite=null;selProv=null;selPol=null;")
rep("else if(o.t==='e')openEvent(o.i,true)}","else if(o.t==='e')openEvent(o.i,true);else if(o.t==='q')openPol(o.id,true)}")
rep("function openEvent(i,keep){","""function openPol(i,keep){const E=eraOf(layerAt(Y));if(!E||!E.pols[i])return;const p=E.pols[i];openState={t:'q',id:i,era:E.id};selPol=i;selProv=null;selSite=null;
  const inside=S.filter(s=>vis(s)&&hit.isPointInPath(p.path,s.xy[0],s.xy[1],'evenodd')).sort((a,b)=>a.year-b.year);
  let h=`<div class="hero"><div class="chips"><span class="chip">${esc(t('polChip',{y:fmtY(eraY(E.id))}))}</span></div><h2>${esc(L(p.n))}</h2></div>`;
  h+=`<div class="st">${esc(t('polSites'))}</div>`;
  h+=inside.length?`<div class="pl">${inside.map(s=>`<button data-s="${s.id}">${shapeSVG(s.g,20)}<span><b>${esc(L(s.name))}</b><br><small class="note">${esc(t('tema',{n:s.tema}))}</small></span><span class="dd">${esc(L(s.date))}</span></button>`).join('')}</div>`:`<div class="c note">${esc(t('polNone'))}</div>`;
  h+=`<div class="note">${esc(t('polNote'))}</div>`;pc.innerHTML=h;showPanel();
  pc.querySelectorAll('[data-s]').forEach(b=>b.onclick=()=>openSite(b.dataset.s,true));
  if(!keep)flyTo(p.lab[0],p.lab[1],Math.max(cam.k,Math.min(4,1.2+40/Math.sqrt(p.a*67.5+1))));dirty=true}
function openEvent(i,keep){""")
open(P,'w',encoding='utf-8').write(s); print('ok')
# atlas_build: incorpora las épocas
B=os.path.join(os.path.dirname(os.path.abspath(__file__)),'atlas_build.py'); b=open(B,encoding='utf-8').read()
if 'atlas_eras.json' not in b:
    a="mp = {k: v for k, v in mapa.items() if k != 'proj'}"
    assert b.count(a)==1
    b=b.replace(a,a+"\n_er = os.path.join(BASE, 'atlas_eras.json')\nif os.path.exists(_er): mp.update(json.load(open(_er, encoding='utf8')))  # mapa político por épocas (eras_build.py)")
    open(B,'w',encoding='utf-8').write(b); print('atlas_build ok')
