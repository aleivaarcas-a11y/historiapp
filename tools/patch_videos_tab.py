#!/usr/bin/env python3
"""Pestaña «Vídeos»: todas las píldoras de los temas publicados, en orden aleatorio y en modo feed.
El feed registra vistos y tests en el tema de cada vídeo. Uso: python3 tools/patch_videos_tab.py"""
import os,re
R=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..'); p=os.path.join(R,'index.html'); s=open(p,encoding='utf-8').read()
if 'function openMixFeed(' in s: print('ya aplicado'); raise SystemExit
a=s.index('function openFeed(tema,idxs,start,onClose){'); b=s.index('\nfunction modeVideos(')
f=s[a:b]; o=f
f=f.replace('const answered=()=>S.prog.seen[tema.id+".videoq"]||{};','const TT=v=>(v&&v._t)||tema; const answered=v=>S.prog.seen[TT(v).id+".videoq"]||{};')
f=f.replace('answered()[v.id]','answered(v)[v.id]')
f=f.replace('${t("tema")} ${tema.num} · ${n+1}','${t("tema")} ${TT(v).num} · ${n+1}')
f=f.replace('const seen=S.prog.seen[tema.id+".videos"]||{}; if(!seen[v.id]) markSeen(tema.id,"videos",v.id);','const seen=S.prog.seen[TT(v).id+".videos"]||{}; if(!seen[v.id]) markSeen(TT(v).id,"videos",v.id);')
f=f.replace('videoAnswer(tema,v,','videoAnswer(TT(v),v,')
assert f.count('TT(v)')>=4 and 'answered()' not in f, f.count('TT(v)')
s=s[:a]+f+'''
async function openMixFeed(){
  try{ const idx=await getIndex(); const all=[];
    for(const m of idx.temas){ if(!m.available) continue; const tm=await getTema(m.num); modeIdxs(tm,"videos").forEach(i=>all.push(Object.assign({},tm.videos[i],{_t:tm}))); }
    if(!all.length){ toast(t("noVideos"),2200); return; }
    for(let i=all.length-1;i>0;i--){ const j=Math.floor(Math.random()*(i+1)); [all[i],all[j]]=[all[j],all[i]]; }
    track("videos/mezcla","Vídeos (pestaña)",true);
    openFeed({id:"mix",num:"",videos:all},all.map((_,i)=>i),0,()=>updateTabbar());
  }catch(e){ toast(t("loadError"),2200); }
}
'''+s[b:]
s=s.replace('const TABS=[["home","🏠","tabHome"],["temas","📚","tabTemas"],["enc","📖","tabEnc"],["exam","🎓","tabExam"],["settings","⚙️","tabSet"]];',
            'const TABS=[["home","🏠","tabHome"],["temas","📚","tabTemas"],["videos","▶️","tabVid"],["enc","📖","tabEnc"],["exam","🎓","tabExam"],["settings","⚙️","tabSet"]];')
s=s.replace('const k=b.dataset.k; nav(k==="settings"','const k=b.dataset.k; if(k==="videos"){ openMixFeed(); return; } nav(k==="settings"')
s=s.replace('tabTemas:"Temas", ','tabTemas:"Temas", tabVid:"Vídeos", ',1).replace('tabTemas:"Units", ','tabTemas:"Units", tabVid:"Videos", ',1)
s=s.replace('#tabbar button{flex:1;display:flex;flex-direction:column;align-items:center;gap:2px;padding:6px 0 4px;border-radius:12px;color:var(--muted);font-size:11px;',
            '#tabbar button{flex:1;min-width:0;display:flex;flex-direction:column;align-items:center;gap:2px;padding:6px 0 4px;border-radius:12px;color:var(--muted);font-size:10.5px;letter-spacing:-.01em;')
assert 'tabVid:"Vídeos"' in s and '["videos","▶️","tabVid"]' in s and 'openMixFeed(); return;' in s
open(p,'w',encoding='utf-8').write(s)
sw=os.path.join(R,'sw.js'); w=open(sw).read(); w=re.sub(r'historiapp-v(\d+)',lambda m:'historiapp-v%d'%(int(m.group(1))+1),w,1); open(sw,'w').write(w)
print('ok',re.search(r'historiapp-v\d+',w).group(0))
