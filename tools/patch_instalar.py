#!/usr/bin/env python3
"""Guía de instalación por sistema y navegador (iPhone y Android, Safari, Chrome, Brave, Firefox, Edge, Samsung, Opera)."""
import os
p = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'index.html')
s = open(p, encoding='utf-8').read()

CSS = '''.ig{font-size:14.5px;line-height:1.5}
.ig .me{background:#EAF1F8;border-radius:14px;padding:12px 14px;margin:6px 0 12px}
.ig .me b{color:var(--primary-2)}
.ig ol{margin:6px 0 0;padding-left:22px} .ig li{margin:4px 0}
.ig h4{margin:14px 2px 6px;font-size:13px;letter-spacing:.06em;text-transform:uppercase;color:var(--muted)}
.ig details{border:1px solid #dde3ea;border-radius:12px;margin:6px 0;background:#fff}
.ig summary{padding:10px 12px;font-weight:700;cursor:pointer;color:var(--primary-2)}
.ig details ol{padding:0 14px 10px 34px}
.ig .tip{font-size:13px;color:var(--muted);margin:10px 2px}
.sheet .in.tall{max-height:88vh}
</style>'''

JS = r'''/* --- guía de instalación --- */
const IG={
es:{title:"Instalar Historiapp", yours:"Tu móvil", now:"Instalar ahora", others:"Otros móviles y navegadores", ios:"iPhone y iPad", and:"Android", pc:"Ordenador",
 after:"Cuando termines, abre Historiapp siempre desde su icono: tu progreso se guarda ahí. En iPhone, lo que hagas en Safari no pasa a la app instalada, así que conviene instalarla el primer día.",
 lost:"Si no encuentras la opción, abre la dirección en Safari (iPhone) o en Chrome (Android) y sigue sus pasos.",
 b:{
 ios_safari:["Safari",["Toca el botón Compartir (el cuadrado con una flecha hacia arriba). En iOS 26, si no lo ves, toca antes los tres puntos (···) junto a la dirección.","Desliza el menú hacia abajo y elige «Añadir a pantalla de inicio». Si no aparece, toca «Ver más» o «Editar acciones».","Si ves la opción de abrirla como app web, déjala activada. Pulsa «Añadir»."]],
 ios_chrome:["Chrome",["Toca el botón Compartir, arriba a la derecha junto a la dirección. También está en el menú de tres puntos, en «Compartir».","Elige «Añadir a pantalla de inicio». Si no aparece, toca «Ver más».","Pulsa «Añadir». Necesitas iOS 16.4 o posterior; con una versión anterior, usa Safari."]],
 ios_brave:["Brave",["Toca el menú de tres puntos (···) de la barra inferior y elige «Compartir».","Elige «Añadir a pantalla de inicio». Si no aparece, toca «Ver más».","Pulsa «Añadir». Necesitas iOS 16.4 o posterior; con una versión anterior, usa Safari."]],
 ios_firefox:["Firefox",["Toca el menú (tres rayas) y elige «Compartir».","Elige «Añadir a pantalla de inicio». Si no aparece, toca «Ver más».","Pulsa «Añadir». Necesitas iOS 16.4 o posterior; con una versión anterior, usa Safari."]],
 ios_edge:["Edge",["Toca el menú de tres puntos (···) de la barra inferior y elige «Compartir».","Elige «Añadir a pantalla de inicio». Si no aparece, toca «Ver más».","Pulsa «Añadir». Necesitas iOS 16.4 o posterior; con una versión anterior, usa Safari."]],
 and_chrome:["Chrome",["Si aparece el aviso «Instalar app» o «Añadir a pantalla de inicio», tócalo.","Si no, abre el menú de tres puntos (⋮, arriba a la derecha) y elige «Instalar aplicación» o «Añadir a pantalla de inicio».","Confirma con «Instalar». El icono aparece en tu pantalla de inicio o en el cajón de aplicaciones."]],
 and_samsung:["Samsung Internet",["Si en la barra de la dirección aparece un icono de descarga o de instalar, tócalo.","Si no, abre el menú (tres rayas, abajo a la derecha), elige «Añadir página a» y después «Pantalla de inicio».","Confirma con «Añadir» o «Instalar»."]],
 and_brave:["Brave",["Abre el menú de tres puntos (⋮, arriba o abajo a la derecha, según cómo tengas la barra).","Elige «Instalar aplicación» o «Añadir a pantalla de inicio».","Confirma con «Instalar» o «Añadir»."]],
 and_firefox:["Firefox",["Abre el menú de tres puntos (⋮).","Elige «Añadir a la pantalla de inicio» (en algunas versiones se llama «Instalar»).","Confirma con «Añadir»."]],
 and_edge:["Edge",["Abre el menú de la barra inferior (tres puntos o tres rayas).","Elige «Añadir al teléfono» o «Añadir a pantalla de inicio».","Confirma con «Instalar»."]],
 and_opera:["Opera",["Abre el menú de tres puntos (⋮).","Elige «Añadir a…» y después «Pantalla de inicio».","Confirma con «Añadir»."]],
 and_other:["Otros (Xiaomi, Huawei, DuckDuckGo…)",["Algunos navegadores de fábrica no instalan aplicaciones web.","Abre esta misma dirección en Chrome y sigue los pasos de Chrome."]],
 inapp:["Si abriste el enlace desde WhatsApp, Instagram, Teams, el correo o el Aula Virtual",["Esas aplicaciones abren la web en un navegador interno que no permite instalar.","Toca los tres puntos o el icono de la brújula y elige «Abrir en Safari», «Abrir en Chrome» o «Abrir en el navegador».","Después sigue los pasos de ese navegador."]],
 pc:["Chrome o Edge en el ordenador",["Pulsa el icono de instalar que aparece a la derecha de la barra de direcciones, o abre el menú y elige «Instalar Historiapp».","Para el móvil, abre esta misma dirección en el teléfono."]]
 }},
en:{title:"Install Historiapp", yours:"Your phone", now:"Install now", others:"Other phones and browsers", ios:"iPhone and iPad", and:"Android", pc:"Computer",
 after:"When you finish, always open Historiapp from its icon: your progress is saved there. On iPhone, what you do in Safari does not carry over to the installed app, so install it on day one.",
 lost:"If you cannot find the option, open the address in Safari (iPhone) or Chrome (Android) and follow their steps.",
 b:{
 ios_safari:["Safari",["Tap the Share button (the square with an upward arrow). On iOS 26, if you cannot see it, first tap the three dots (···) next to the address.","Scroll down the menu and choose 'Add to Home Screen'. If it is not there, tap 'View More' or 'Edit Actions'.","If you see the option to open it as a web app, leave it on. Tap 'Add'."]],
 ios_chrome:["Chrome",["Tap the Share button, top right next to the address. It is also in the three-dot menu, under 'Share'.","Choose 'Add to Home Screen'. If it is not there, tap 'View More'.","Tap 'Add'. You need iOS 16.4 or later; with an older version, use Safari."]],
 ios_brave:["Brave",["Tap the three-dot menu (···) in the bottom bar and choose 'Share'.","Choose 'Add to Home Screen'. If it is not there, tap 'View More'.","Tap 'Add'. You need iOS 16.4 or later; with an older version, use Safari."]],
 ios_firefox:["Firefox",["Tap the menu (three lines) and choose 'Share'.","Choose 'Add to Home Screen'. If it is not there, tap 'View More'.","Tap 'Add'. You need iOS 16.4 or later; with an older version, use Safari."]],
 ios_edge:["Edge",["Tap the three-dot menu (···) in the bottom bar and choose 'Share'.","Choose 'Add to Home Screen'. If it is not there, tap 'View More'.","Tap 'Add'. You need iOS 16.4 or later; with an older version, use Safari."]],
 and_chrome:["Chrome",["If an 'Install app' or 'Add to Home screen' prompt appears, tap it.","Otherwise open the three-dot menu (⋮, top right) and choose 'Install app' or 'Add to Home screen'.","Confirm with 'Install'. The icon appears on your home screen or in the app drawer."]],
 and_samsung:["Samsung Internet",["If a download or install icon appears in the address bar, tap it.","Otherwise open the menu (three lines, bottom right), choose 'Add page to' and then 'Home screen'.","Confirm with 'Add' or 'Install'."]],
 and_brave:["Brave",["Open the three-dot menu (⋮, top or bottom right, depending on your toolbar).","Choose 'Install app' or 'Add to Home screen'.","Confirm with 'Install' or 'Add'."]],
 and_firefox:["Firefox",["Open the three-dot menu (⋮).","Choose 'Add to Home screen' (called 'Install' in some versions).","Confirm with 'Add'."]],
 and_edge:["Edge",["Open the menu in the bottom bar (three dots or three lines).","Choose 'Add to phone' or 'Add to Home screen'.","Confirm with 'Install'."]],
 and_opera:["Opera",["Open the three-dot menu (⋮).","Choose 'Add to…' and then 'Home screen'.","Confirm with 'Add'."]],
 and_other:["Others (Xiaomi, Huawei, DuckDuckGo…)",["Some pre-installed browsers cannot install web apps.","Open this same address in Chrome and follow the Chrome steps."]],
 inapp:["If you opened the link from WhatsApp, Instagram, Teams, email or the Virtual Campus",["Those apps open the page in a built-in browser that cannot install.","Tap the three dots or the compass icon and choose 'Open in Safari', 'Open in Chrome' or 'Open in browser'.","Then follow the steps for that browser."]],
 pc:["Chrome or Edge on a computer",["Click the install icon at the right of the address bar, or open the menu and choose 'Install Historiapp'.","For your phone, open this same address on it."]]
 }}};
function detectBrowser(){
  const ua=navigator.userAgent, brave=!!navigator.brave;
  const inapp=/FBAN|FBAV|Instagram|WhatsApp|MicrosoftTeams|Line\/|LinkedInApp|Snapchat|TikTok|GSA\/|Outlook/i.test(ua)||(/Android/i.test(ua)&&/; wv\)/.test(ua));
  if(isIOS()){ const b=brave?"ios_brave":/CriOS/.test(ua)?"ios_chrome":/FxiOS/.test(ua)?"ios_firefox":/EdgiOS/.test(ua)?"ios_edge":"ios_safari"; return {os:"ios",key:inapp?"inapp":b}; }
  if(/Android/i.test(ua)){ const b=brave?"and_brave":/SamsungBrowser/.test(ua)?"and_samsung":/EdgA/.test(ua)?"and_edge":/OPR|Opera/.test(ua)?"and_opera":/Firefox/.test(ua)?"and_firefox":/MiuiBrowser|HuaweiBrowser|HeyTap|DuckDuckGo/.test(ua)?"and_other":"and_chrome"; return {os:"and",key:inapp?"inapp":b}; }
  return {os:"pc",key:"pc"};
}
function igSteps(k,L){ const [, st]=L.b[k]; return `<ol>${st.map(x=>`<li>${esc(x)}</li>`).join("")}</ol>`; }
function igBlock(k,L){ return `<details><summary>${esc(L.b[k][0])}</summary>${igSteps(k,L)}</details>`; }
async function installApp(){
  track("instalar","Instalar",true);
  if(isStandalone()){ toast(t("installed")); return; }
  const L=IG[S.lang==="en"?"en":"es"], d=detectBrowser();
  const osName={ios:L.ios,and:L.and,pc:L.pc}[d.os];
  const el=document.getElementById("sheet"), inn=document.getElementById("sheetIn"); el.className="sheet ok"; inn.classList.add("tall");
  inn.innerHTML=`<div class="verdict"><span class="dot">📲</span>${esc(L.title)}</div><div class="ig">
    ${deferredInstall?`<button class="btn" id="igNow">${esc(L.now)}</button>`:""}
    <div class="me"><b>${esc(L.yours)}: ${esc(osName)} · ${esc(L.b[d.key][0])}</b>${igSteps(d.key,L)}</div>
    <p class="tip">${esc(L.after)}</p>
    <h4>${esc(L.others)}</h4>
    <h4>${esc(L.ios)}</h4>${["ios_safari","ios_chrome","ios_brave","ios_firefox","ios_edge"].map(k=>igBlock(k,L)).join("")}
    <h4>${esc(L.and)}</h4>${["and_chrome","and_samsung","and_brave","and_firefox","and_edge","and_opera","and_other"].map(k=>igBlock(k,L)).join("")}
    <h4>WhatsApp, Instagram…</h4>${igBlock("inapp",L)}
    <h4>${esc(L.pc)}</h4>${igBlock("pc",L)}
    <p class="tip">${esc(L.lost)}</p></div>
    <button class="btn sec" id="sheetNext">${t("close")}</button>`;
  requestAnimationFrame(()=>el.classList.add("show"));
  document.getElementById("sheetNext").onclick=()=>{ el.classList.remove("show"); inn.classList.remove("tall"); };
  const nb=document.getElementById("igNow");
  if(nb) nb.onclick=async()=>{ const p=deferredInstall; if(!p) return; p.prompt(); try{ await p.userChoice; }catch(e){} deferredInstall=null; el.classList.remove("show"); inn.classList.remove("tall"); };
}
'''

a = s.index('async function installApp(){')
b = s.index('/* --- mapa conceptual --- */')
s = s[:a] + JS + '\n' + s[b:]
assert s.count('</style>') == 1
s = s.replace('</style>', CSS, 1)
open(p, 'w', encoding='utf-8').write(s)
print('ok')
