#!/usr/bin/env python3
"""Margen superior seguro: mide env(safe-area-inset-top) al arrancar y, si iOS lo devuelve a 0 en la app
instalada (la barra de estado y la isla dinámica tapan la cabecera), aplica el valor del modelo de iPhone.
Uso: python3 tools/patch_safe.py"""
import os
R = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
p = os.path.join(R, 'index.html'); s = open(p, encoding='utf-8').read()
if 'function fixSafeTop' in s:
    print('ya aplicado'); raise SystemExit
JS = r'''/* --- margen superior seguro (iPhone) --- */
function fixSafeTop(){ try{
  const d=document.createElement("div"); d.style.cssText="position:fixed;top:0;left:0;width:1px;height:env(safe-area-inset-top,0px);visibility:hidden;pointer-events:none";
  document.body.appendChild(d); let h=d.getBoundingClientRect().height; d.remove();
  const ios=/iPad|iPhone|iPod/.test(navigator.userAgent)||(navigator.platform==="MacIntel"&&navigator.maxTouchPoints>1);
  const standalone=navigator.standalone===true||matchMedia("(display-mode: standalone)").matches;
  const portrait=innerHeight>innerWidth, H=Math.max(screen.height,screen.width);
  if(ios&&standalone&&portrait&&h<20) h = H>=874?62 : H>=852?59 : H>=812?50 : 20;
  document.documentElement.style.setProperty("--safe-top",h+"px");
}catch(e){} }
fixSafeTop(); addEventListener("orientationchange",()=>setTimeout(fixSafeTop,300)); addEventListener("resize",()=>setTimeout(fixSafeTop,300));
'''
anchor = '/* ============ boot ============ */'
assert anchor in s
s = s.replace(anchor, JS + anchor, 1)
open(p, 'w', encoding='utf-8').write(s)
print('ok')
