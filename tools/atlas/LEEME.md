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

## Mapa político por épocas (12-10-2026)

- `tools/atlas/eras_build.py` (necesita shapely y pyproj) lee los GeoJSON de historical-basemaps (A. Ourednik, GPL-3.0; https://github.com/aourednik/historical-basemaps), recorta y proyecta cada época al mapa del Atlas, agrupa las entidades por civilización con su nombre en castellano e inglés y escribe `tools/atlas/atlas_eras.json`. `atlas_build.py` lo copia dentro de `data/atlas_mapa.json`.
- Épocas: 3000, 2000, 1000, 700, 500, 400, 323, 300, 200 y 100 a. C.; cambio de era (Augusto a 99 d. C.); 200 d. C. (de 100 a 299, con las provincias romanas del AWMC); 300, 400 y 500 d. C. Antes del 3000 a. C. no se dibujan fronteras. «Todas las épocas» enseña el mapa hacia el 200 d. C.
- Colores por civilización, iguales a los de los lugares del temario donde existen (Egipto oro, Persia azul, Fenicia y Cartago morado, Etruria verde, Roma rojo, Grecia terracota, Macedonia y los reinos helenísticos malva, seléucidas verde azulado). Los pueblos sin Estado van con sombreado tenue y borde discontinuo. Cada territorio se puede pulsar y muestra los lugares del temario que caen dentro.
- Correcciones a la fuente: el Imperio parto de la capa del 300 d. C. se rotula como sasánida; los hititas del 1000 y el 700 a. C., como reinos neohititas; las «ciudades griegas» de esas dos capas, como pueblos griegos; se retira el resto del Imperio de Occidente de la capa del 500 d. C.
- Límites conocidos de la fuente: es un mapa mundial de trabajo y su autor pide contrastarlo; no trae Micenas ni las colonias fenicias, y la capa del 1500 a. C. repite la del 1000, por eso no se usa.
