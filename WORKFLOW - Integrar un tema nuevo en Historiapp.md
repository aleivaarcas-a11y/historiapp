# Integrar un tema nuevo en Historiapp

Pasos para que un tema terminado (PPT definitivo y notas del orador revisadas) quede integrado del todo en la app. Está escrito para que lo siga cualquier sesión de Claude sin el historial de las anteriores. N es el número del tema; NN, el mismo número con dos cifras (03, 04…).

Todo se hace en el ordenador de Alex, en `ASIGNATURAS/Claude outputs/Historiapp/`, salvo lo que exija la nube (ver apartado 9). Antes de tocar `index.html`, guarda una copia en `tools/index_antes_<motivo>.html`. Nada se borra: lo sobrante va a `Claude outputs/_to_delete/`.

## 0. Material de partida

Antes de empezar hay que tener cuatro cosas.
- El PPT definitivo del tema (en `HISTORIA DEL DEPORTE/TEMAS NUEVOS/`). No se modifica nunca; solo se lee.
- El archivo «TEMA N - Notas del orador.md», con un bloque `### Diapositiva N · Título` por diapositiva.
- Su traducción al inglés con la misma estructura, en `tools/fuentes/tN_notas_en.md`. Si no existe, se traduce primero.
- Los títulos de apartado en inglés, que se añaden a `tools/secciones_en.json`.

## 1. Fichas (el manual de bolsillo)

1. En el Mac, con python-pptx: `python3 tools/extraer_ppt.py "<PPT>" tools/fuentes/tN_slides.json <carpeta_imagenes>`.
2. Elegir las imágenes que van a la app, copiarlas a `img/tN/` y registrarlas en `tools/imgmap.json` (sNN_K → nombre del archivo).
3. `python3 tools/construir_fichas.py tools/fuentes/tN_slides.json data/temaNN.json img/tN tools/imgmap.json "TEMA N - Notas del orador.md" tools/fuentes/tN_notas_en.md`. Rehace `sections`, `fichas` e `intro` y respeta el resto del JSON.
4. Comprobar códigos de ficha (HN·xx), apartados y fuentes APA. Las citas van en el texto, nunca en nota al pie.

## 2. Modos de estudio

Cada elemento lleva `es` y `en`, y su apartado en `sec`. Los modelos están en `data/tema02.json`.
- `cards` (análisis de imágenes, verdadero o falso). Las propuestas se preparan en `tools/tN_cards_nuevas.json`.
- `glossary`, `timeline`, `sources`, `match`, `myths` y `quiz`.
- `mapa`: se escribe en `tools/mapas.json` (clave "N") y el nivel 3 en `tools/mapa_x_temaNN.json`. Se vuelca con `tools/patch_mapa_examen.py` y `tools/patch_mapa_nivel3.py`.
- `videos`: lista en `tools/videos_tN.json`, con los mp4 y sus carteles en `videos/tN/` (`tN_XX_es.mp4`, `tN_XX_es.jpg`, y lo mismo en `_en`). Cada vídeo lleva `more` («Saber más») y `q` (pregunta). La pestaña Vídeos los mezcla sola con los de los demás temas.
- `podcast`: episodios en `tools/podcast.json` (clave "N") y audio en `audio/`; se vuelca con `tools/patch_podcast.py`.

Todo el contenido sale de las diapositivas y de las fichas de lectura del corpus. No se inventan datos, fechas ni páginas; las páginas se buscan con `LECTURAS DEPORTE/_corpus/02-citar.sh`. Se redacta con la skill lenguaje-alex.

## 3. Publicar el tema dentro de la app

1. En `data/temas.json`, poner el tema N en `"available": true` y actualizar `version` con la fecha.
2. En `index.html`, añadir la imagen de portada del tema a `TEMA_IMG` (busca `const TEMA_IMG=`), por ejemplo `3:"img/t3/<imagen>.jpg"`. Tiene que mostrar la práctica física del tema y estar en `img/tN/`.

El reto del día, el buscador global, las medallas por modo, los logros y la pantalla de carga leen los temas disponibles sin tocar nada más.

## 4. Palabra del día (wordle)

1. Sacar el texto del PPT (`~/enc/ppt/` en la VM o el extraído en el paso 1) y listar las palabras de cinco letras.
2. Elegir solo términos que aparezcan en las diapositivas del tema: entre 12 y 18 en castellano (sin tildes en la palabra) y entre 10 y 12 en inglés, también de cinco letras y del mismo contenido. Nada de términos que no estén en el PPT.
3. Escribir cada palabra con su definición breve, sacada de lo que dice la diapositiva, en `tools/wordle_palabras.js`, con `t:N`.
4. Volcar la lista en `index.html` sustituyendo el bloque `const WORDS={ … ]};` (el script que se usó está en el registro del 30-09; basta con un reemplazo del bloque entre `const WORDS={` y el primer `]};`).
5. Dar a Alex la lista en el chat para que la apruebe.

## 5. Enciclopedia del deporte

1. Repasar los deportes y juegos que aparecen en el tema. Si alguno no tiene ficha, se añade con el flujo de `tools/enc_tandas/INSTRUCCIONES.md` (fuente prioritaria, la federación internacional; Fernández Truan solo si no hay otra).
2. En las fichas de deportes que el tema trata, añadir el enlace `tema` (`[{"num":N,"f":"<id de la ficha>","t":{"es":…,"en":…}}]`) en la tanda correspondiente.
3. Ejecutar `python3 tools/enc_merge.py`. Integra también las descripciones «Qué es» (`tools/desc/desc_enciclopedia.json`) y los continentes (`tools/enciclopedia_continente.json`). Un deporte nuevo necesita su línea en esos dos ficheros: la descripción solo si no es olímpico ni muy conocido.
4. Si al cruzar la Enciclopedia con las diapositivas aparece alguna discrepancia, se anota en `HISTORIA DEL DEPORTE/Claude outputs/` para que Alex decida, como en «Diapositivas a revisar (detectado en la Enciclopedia, 29-09).md».

## 6. Tal día como hoy

Si el tema trae hechos con fecha exacta (día y mes) y fuente, se puede proponer a Alex sustituir la efeméride de ese día en `data/efemerides.json`, con `enc` si hay deporte enlazado o con `img` propia de Wikimedia Commons (`src` en `img/efe/MM-DD.jpg`, `pie` es/en, `autor`, `licencia`, `url`). Las herramientas están en `tools/efe_fotos/`.

## 7. QR de las fichas

`python3 tools/generar_qr.py https://aleivaarcas-a11y.github.io/historiapp/ data/temaNN.json qr/tN`. Deja un PNG por ficha y un `indice.csv` con las diapositivas que corresponden a cada uno.

## 8. Comprobación antes de publicar

1. `node --check` del JavaScript de `index.html` (extraer los bloques `<script>` a un fichero y comprobarlo).
2. Probar en un navegador con la vista de móvil (390 × 844), en castellano y en inglés, y con el modo oscuro.
   - Inicio, con la tarjeta del tema, su anillo de progreso y la imagen.
   - Cada modo del tema, la pestaña Vídeos, el buscador con un término del tema y la palabra del día.
   - Una ficha de la Enciclopedia enlazada con el tema.
3. Subir la versión del service worker en `sw.js` (`const VERSION = "historiapp-vNN"`), una por cada publicación.

## 9. Nube y ordenador

- Para probar en la nube (Playwright), los ficheros del Drive se copian antes a `Claude outputs/_to_delete/_prueba_x/`, se espera un minuto largo y se suben con stage; los enlaces del Drive fallan si se suben directamente.
- Wikimedia Commons bloquea la IP de la nube (error 429). Las búsquedas y descargas de imágenes se hacen desde el ordenador de Alex (`tools/efe_fotos/commons.py` y `getimg.py`).
- Si se lanzan agentes, con Sonnet para ahorrar cuota y preguntando antes a Alex.

## 10. Cierre

1. Alex publica con `bash "/Users/leiva/Mi unidad /UCAM/ASIGNATURAS/Claude outputs/Historiapp/subir.sh"`.
2. Añadir dos o tres líneas a `HISTORIA DEL DEPORTE/REGISTRO DE SESIONES.md` y al apartado 8 de la «HOJA DE RELEVO.md», y actualizar sus pendientes.
3. Decirle a Alex qué hay que revisar a mano (palabras del wordle, imágenes dudosas, discrepancias con las diapositivas).
