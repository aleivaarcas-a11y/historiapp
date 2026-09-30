# Fotos para «Tal día como hoy» (Historiapp)

Cada día del año tiene una efeméride de historia del deporte. Tu lote (`dias_N.json` en esa carpeta) trae días sin foto: `dia` (MM-DD), `year`, el texto `es` y sus fuentes. Hay que ponerle a cada uno **una imagen de Wikimedia Commons ligada al acontecimiento**.

## Qué imagen vale, por este orden de preferencia
1. El acontecimiento mismo (el partido, la carrera, la ceremonia) o una imagen de la época del hecho.
2. El protagonista (deportista, fundador, club, equipo); aquí sí vale un retrato.
3. El lugar (estadio, pista, ciudad sede) o un objeto directamente ligado (trofeo, cartel, medalla de esos Juegos).
4. Si nada de eso existe con licencia válida, una imagen del deporte practicándose en una época parecida.
Nada de imágenes que puedan inducir a error: no pongas la foto de otro partido o de otra edición como si fuera la del hecho; si usas una imagen genérica (caso 3 o 4), el pie debe decir con claridad qué muestra.

## Licencias
Solo Dominio público (PD, Public domain), CC0, CC BY o CC BY-SA (cualquier versión). Descarta las «fair use», las no libres y las que tengan marcas de agua. Evita fotos de menores identificables.

## Dónde trabajas
Todo se hace en el ordenador de Alex con la herramienta `mcp__remote-devices__device_bash` (cárgala antes con ToolSearch: `select:mcp__remote-devices__device_bash`). Cada llamada es un shell nuevo: empieza siempre con `cd "$HOME/mnt/ASIGNATURAS/Claude outputs/Historiapp/tools/efe_fotos"`. No uses el Bash de la nube para Commons: su IP está bloqueada por Commons (error 429).

## Herramientas (en esa carpeta)
- `python3 commons.py buscar "consulta" [n]` busca ficheros y muestra licencia, autor, fecha y descripción. Prueba consultas en inglés y en el idioma del país.
- `python3 commons.py info "File:Nombre.jpg"` muestra los datos de un fichero concreto.
- `python3 getimg.py MM-DD "File:Nombre.jpg"` descarga la imagen a `Historiapp/img/efe/MM-DD.jpg` (JPEG, 1200 px).
Commons limita las peticiones: pocas búsquedas por día (máximo cuatro), una llamada de herramienta cada vez y `sleep 2` entre búsquedas. Si ves un error 429, espera un minuto antes de seguir. Cada llamada a device_bash dura como mucho 120 s: no encadenes muchas búsquedas en una sola llamada. Nada de copias de archivo ni de otras webs.

## Salida
Escribe `fotos_N.json` en esa misma carpeta de forma incremental (guarda tras cada día), un objeto:
```json
{"12-13": {"src": "img/efe/12-13.jpg",
  "pie": {"es": "Qué se ve, con lugar y fecha si constan", "en": "…"},
  "autor": "Nombre limpio o «Autor anónimo»/«Anonymous» como {\"es\":…,\"en\":…}",
  "licencia": "Dominio público o la sigla CC", "url": "https://commons.wikimedia.org/wiki/File:…",
  "tipo": "hecho | protagonista | lugar | genérica"}}
```
El `pie` describe solo lo que muestra la imagen según su ficha de Commons, sin inventar; castellano llano, sin «—», sin «sino» y sin dos puntos seguidos de enumeración. Si para un día no encuentras nada válido, ponlo con `"src": null` y una `nota`.

Al terminar, comprueba con Python que el JSON carga, que están todos los días del lote y que existe `../../img/efe/MM-DD.jpg` para cada `src`. Resumen final de una línea: cuántos por tipo y cuántos sin foto.
