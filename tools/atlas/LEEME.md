# Atlas de Historiapp

Pestaña «Atlas» de la app (`#atlas`), que abre `atlas/index.html` dentro de la propia app. Comparte mapa, proyección y estética con el juego Agón, pero es una herramienta de estudio, como la línea del tiempo.

## Cómo crece

- Cada tema tiene su archivo `tools/atlas/atlas_tN.json` con sus lugares (coordenadas en latitud y longitud, fecha, texto, fuente, referencias, preguntas, fichas, imágenes y vídeos de la app) y sus acontecimientos.
- `python3 tools/atlas/atlas_build.py` (desde la carpeta Historiapp) genera `data/atlas.json` y `data/atlas_mapa.json`, coloca cada lugar en el mapa y en su provincia, y avisa si una ficha, imagen o vídeo no existe.
- El Atlas solo enseña los temas marcados como disponibles en `data/temas.json`. El Tema 4 ya está preparado y aparecerá solo cuando se abra en la app (falta añadir sus fichas, imágenes y vídeos en `atlas_t4.json`).

## Formato de un lugar

`id`, `civ` (pre, his, fen, egi, per, ege, gre, etr, rom o una nueva definida en `civs`), `lat`, `lon`, `name`, `place`, `date` (textos `{es, en}`), `year` (número, negativo antes de Cristo), `text`, `src` (`type`: Material, Iconografía o Texto; `cap`), `ref`, `qs` (la primera opción es la correcta), `fichas` (ids de `data/temaNN.json`), `imgs` (rutas de imágenes de esas fichas), `vids` (ids de vídeo), `kw` (palabras clave opcionales) y, si hace falta forzarla, `prov`.

## Qué monta el script en la cartela

Además de lo anterior, `atlas_build.py` enlaza cada lugar con el tema. Saca los apartados y los nodos del mapa conceptual donde están sus fichas, un extracto de cada ficha, los hitos de `data/linea.json`, los términos del glosario que aparecen en sus textos y, junto a las preguntas propias, las del cuestionario, los mitos y las tarjetas del tema que contienen alguna palabra clave. Las palabras clave son el nombre del lugar y las de `kw`; casan al principio de palabra, de modo que «tiro» no se confunde con «tiro con arco» si se precisa en `kw`. Límites por lugar: tres nodos, cinco hitos, seis términos y diez preguntas.

## Mapa base

`mapa_base.json`: costas, lagos y ríos de Natural Earth y fronteras del Ancient World Mapping Center (AWMC, licencia ODbL, a partir del Barrington Atlas): provincias romanas hacia el 200 d. C., Imperio persa, Imperio de Alejandro y Roma hacia el 60 a. C. Las fuentes con que se reconstruyeron las provincias están en «Juegos web/Codigo/atlas/».
