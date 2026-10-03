# Historiapp

App web para preparar el examen de Historia del Deporte (Grado en CAFD, UCAM). Funciona como aplicación de móvil al añadirla a la pantalla de inicio y no necesita servidor: es un único `index.html` que lee su contenido de archivos JSON.

## Estructura

```
index.html        La app completa (interfaz, lógica, textos en ES y EN)
tools/            Scripts para generar contenido desde los PPT y las notas del orador (ver abajo)
manifest.json     Nombre, icono y colores para instalarla en el móvil
sw.js             Caché sin conexión (una vez abierta, funciona sin red)
data/temas.json   Índice de temas: cuáles están publicados y cuáles bloqueados
data/tema01.json  Contenido del tema 1
data/tema02.json  Contenido del tema 2
img/t1, img/t2    Imágenes de cada tema (máx. 1000 px, JPG)
icons/            Iconos de la app
fonts/            Carlito (gemela libre de Calibri, misma métrica) para los móviles que no la tienen
```

## Publicar en GitHub Pages

1. Crea un repositorio público en GitHub, por ejemplo `historiapp`.
2. Sube todo el contenido de esta carpeta a la raíz del repositorio (arrastrando los archivos en la web de GitHub sirve).
3. En el repositorio, entra en Settings, después en Pages, y en «Build and deployment» elige «Deploy from a branch», rama `main`, carpeta `/ (root)`. Guarda.
4. Al cabo de un minuto la app estará en `https://TU_USUARIO.github.io/historiapp/`.
5. Comparte esa dirección con los alumnos. En el iPhone: Safari, botón Compartir, «Añadir a pantalla de inicio». En Android: Chrome, menú, «Instalar aplicación».

## Fichas: el manual de bolsillo

La sección «Fichas» de cada tema se genera a partir del PPT y del archivo «TEMA N - Notas del orador.md». Cada ficha corresponde a una diapositiva (o a un grupo de diapositivas seguidas sobre lo mismo) y lleva su nota del orador como texto, las fuentes en APA, la frase «Para el ensayo» si la hay, el texto de la diapositiva desplegable y las imágenes. Cada ficha tiene un código corto (H2·10) y una dirección propia:

```
https://USUARIO.github.io/historiapp/#t2/f/la-fiesta-del-heb-sed
```

Esa dirección se puede poner como hipervínculo en el PDF de las diapositivas, como QR en la diapositiva proyectada, o simplemente escribir el código en el buscador de la app. Los QR se generan en lote:

```
pip install qrcode pillow
python3 tools/generar_qr.py https://USUARIO.github.io/historiapp/ data/tema02.json qr/t2
```

Deja un PNG por ficha (QR más código) y un `indice.csv` que dice a qué diapositivas corresponde cada uno.

## Regenerar las fichas de un tema

Cuando cambien las diapositivas o las notas del orador:

```
python3 tools/extraer_ppt.py "TEMA 2. Egipto, Persia y Fenicia.pptx" tools/fuentes/t2_slides.json
python3 tools/construir_fichas.py tools/fuentes/t2_slides.json data/tema02.json img/t2 tools/imgmap.json "TEMA 2 - Notas del orador.md" tools/fuentes/t2_notas_en.md
```

El último argumento, opcional, es la traducción al inglés de las notas con la misma estructura (en `tools/fuentes/` están las de los temas 1 y 2). Los títulos de apartado en inglés se leen de `tools/secciones_en.json`.

El primer script necesita `pip install python-pptx` y se ejecuta donde esté el PPT. El segundo conserva intactas las demás secciones del JSON (tarjetas, glosario, etc.) y solo rehace `sections`, `fichas` e `intro`. El archivo `tools/imgmap.json` dice qué imagen del PPT (sNN_K) se llama cómo en `img/`.

Las notas del orador se leen del Markdown con un bloque `### Diapositiva N · Título` por diapositiva, con sus apartados «Notas del orador» y «Fuente». Una diapositiva cuyo título empieza por un código de apartado (2.1.2.) abre un apartado nuevo y su nota pasa a ser la introducción de ese apartado; la nota de la portada es la presentación del tema.

## Añadir un tema nuevo

El procedimiento completo, con todos los puntos de la app que hay que tocar (fichas, modos, palabra del día, Enciclopedia, efemérides, QR y pruebas), está en «WORKFLOW - Integrar un tema nuevo en Historiapp.md». Lo que sigue es el resumen mínimo.


1. Crea `data/tema03.json` con la misma estructura que `tema02.json` (secciones `cards`, `glossary`, `timeline`, `sources`, `match`, `myths`, `quiz`, `videos`; cada texto lleva sus versiones `es` y `en`, y cada elemento su apartado en `sec`). Las fichas se generan con los scripts de arriba.
2. Copia sus imágenes a `img/t3/`.
3. En `data/temas.json`, cambia el tema 3 a `"available": true` y actualiza el campo `version` con la fecha.
4. Sube los archivos al repositorio. Los alumnos verán el tema nuevo la próxima vez que abran la app, sin reinstalar nada.

Para corregir una pregunta o un texto basta con editar el JSON correspondiente y volver a subirlo.

## Colores y tipografía

La interfaz usa la paleta de la plantilla PPT de la UCAM (azul 004379, azul oscuro 002060, naranja EDAB00 y FBAE40, texto 383838 sobre blanco) y Calibri. Como Calibri no existe en iPhone ni en Android, la app lleva Carlito, una fuente libre con exactamente las mismas medidas, que solo se usa cuando el dispositivo no tiene Calibri. Los colores se cambian en las variables de la cabecera de `index.html`.

## Vídeos

Cada tema tiene una lista `videos` con el identificador de YouTube y el título en los dos idiomas:

```json
"videos": [{"id": "XXXXXXXXXXX", "title": {"es": "El Heb-Sed en dos minutos", "en": "The Heb-Sed in two minutes"}}]
```

Conviene subirlos a YouTube como «no listados» y en formato vertical.

## Progreso de los alumnos

XP, niveles, rachas, insignias y cajas de repaso del glosario se guardan solo en el móvil de cada alumno (localStorage). No hay servidor ni datos personales. Desde Ajustes pueden cambiar de idioma o borrar su progreso.
