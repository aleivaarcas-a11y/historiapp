# Atlas de Historiapp

Pestaña «Atlas» de la app (`#atlas`), que abre `atlas/index.html` dentro de la propia app. Comparte mapa, proyección y estética con el juego Agón, pero es una herramienta de estudio, como la línea del tiempo.

## Cómo crece

- Cada tema tiene su archivo `tools/atlas/atlas_tN.json` con sus lugares (coordenadas en latitud y longitud, fecha, texto, fuente, referencias, preguntas, fichas, imágenes y vídeos de la app) y sus acontecimientos.
- `python3 tools/atlas/atlas_build.py` (desde la carpeta Historiapp) genera `data/atlas.json` y `data/atlas_mapa.json`, coloca cada lugar en el mapa y en su provincia, y avisa si una ficha, imagen o vídeo no existe.
- El Atlas solo enseña los temas marcados como disponibles en `data/temas.json`. El Tema 4 ya está preparado y aparecerá solo cuando se abra en la app (falta añadir sus fichas, imágenes y vídeos en `atlas_t4.json`).

## Formato de un lugar

`id`, `civ` (pre, his, fen, egi, per, ege, gre, etr, rom o una nueva definida en `civs`), `lat`, `lon`, `name`, `place`, `date` (textos `{es, en}`), `year` (número, negativo antes de Cristo), `text`, `src` (`type`: Material, Iconografía o Texto; `cap`), `ref`, `qs` (la primera opción es la correcta), `fichas` (ids de `data/temaNN.json`), `imgs` (rutas de imágenes de esas fichas), `vids` (ids de vídeo) y, si hace falta forzarla, `prov`.

## Mapa base

`mapa_base.json`: costas, lagos y ríos de Natural Earth y fronteras del Ancient World Mapping Center (AWMC, licencia ODbL, a partir del Barrington Atlas): provincias romanas hacia el 200 d. C., Imperio persa, Imperio de Alejandro y Roma hacia el 60 a. C. Las fuentes con que se reconstruyeron las provincias están en «Juegos web/Codigo/atlas/».
