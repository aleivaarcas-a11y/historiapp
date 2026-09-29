# Enciclopedia del deporte de Historiapp: instrucciones para redactar una tanda

Historiapp es la app de la asignatura Historia del Deporte (1.º CAFD, UCAM) del profesor Alejandro Leiva Arcas. La Enciclopedia tiene una ficha por deporte, en castellano y en inglés, sobre **cuándo, dónde y cómo surge** cada deporte y cómo llega a su forma moderna. Lo que importa por encima de todo es que la información sea correcta.

## Dónde está todo (ordenador de Alex, con device_bash)
- App: `~/mnt/ASIGNATURAS/Claude outputs/Historiapp/`
- Lista maestra: `tools/enciclopedia_lista.json` (id, nombre ES/EN, bloque, `ft` = tiene entrada en Fernández Truan, `tipo` completa o breve).
- Ejemplos de fichas terminadas: `data/enciclopedia.json` (léelo antes de empezar; copia su estructura exacta).
- Apuntes de la asignatura: `data/tema01.json` y `data/tema02.json` (campo `fichas`, cada una con `id`, `title`, `body`).
- Fernández Truan, tomo IV, en texto por páginas: `~/enc/ft4.txt`. Buscar: `python3 ~/enc/busca.py ft4 "palabra" 200 10`; leer páginas: `python3 ~/enc/pg.py ft4 268 270`. El número de página física coincide con el impreso.
- Libros académicos: `~/mnt/LIBROS/Historia Deporte/` (Deportes/, Obras Generales/, Épocas/, Regiones/) y artículos en `~/mnt/ARTÍCULOS/` (con tilde; usa `ls -d ~/mnt/ART*`). Para buscar dentro de un PDF: `bash ~/enc/pages.sh "<ruta.pdf>" <alias>` y después `busca.py <alias> ...`. Guttmann (2004) ya está convertido como `gut04` (página impresa = física − 17).
- Imágenes de Wikimedia Commons (la red del ordenador sí llega a Commons): buscar con `python3 ~/enc/commons.py "consulta 1" "consulta 2"`; descargar con `python3 ~/enc/getimg2.py <id> "<título del fichero>"`, que imprime el crédito.
- Web (desde la nube): WebSearch y WebFetch.

## Fuentes, por este orden
1. **La federación internacional del deporte**, en su página oficial de historia (World Athletics, FIBA, UWW, World Aquatics, etc.). Es la fuente prioritaria y la que se cita por defecto. Si no hay federación internacional, la federación nacional más representativa o el organismo que rige el deporte (por ejemplo, la federación española o regional en juegos tradicionales).
2. **Si la federación no da el dato de origen, lo da mal o choca con lo establecido**, completa o corrige con un libro o artículo académico de la biblioteca, con página, o con Fernández Truan (con página). Cuando haya contradicción, la ficha da el dato mejor documentado y dice en una frase que existe la otra versión.
3. **Fernández Truan** sirve como mapa y solo se cita si se usa, siempre con página. Tiene errores frecuentes: no copies nada sin contrastarlo y nunca copies su redacción.
4. **Wikipedia nunca se cita ni se copia.** Puede servir para localizar la federación o una fecha que después compruebas en otra fuente.
5. **Nunca inventes una fuente, una fecha, una cita ni una página.** Si un dato no se puede comprobar, no lo pongas.

Cita en APA 7 dentro del texto, entre paréntesis, con el autor corporativo: (World Athletics, s. f.). Referencia en `refs`: `World Athletics. (s. f.). *History*. Recuperado el 29 de septiembre de 2026 de https://...`; en `refs_en`: `World Athletics. (n.d.). *History*. Retrieved September 29, 2026, from https://...`. Con libros: (Guttmann, 2004, p. 94). En `refs_en` cambia «s. f.» por «n.d.», «En» por «In» y «y» por «&» entre autores.

## Coherencia con los apuntes
Si el deporte o sus antecedentes aparecen en los temas 1 o 2 (busca con grep en `data/tema01.json` y `data/tema02.json`), la ficha no puede contradecir lo que dicen esas fichas: usa sus mismos datos y fuentes y añade el enlace en `tema`: `[{"num":2,"f":"<id de la ficha>","t":{"es":"<título>","en":"<título EN>"}}]`.

## Contenido de cada ficha
- `cuando`: una línea, lugar y fecha de origen (y de la forma moderna si difiere). ES y EN.
- `body`: ficha **completa**, tres párrafos de 80-150 palabras (origen y antecedentes; nacimiento de la forma moderna, reglas y primeras instituciones; difusión, federación internacional, entrada olímpica si la hay, y rasgo social relevante como distinción, identidad o género). Ficha **breve**, un solo párrafo. Las mismas ideas en ES y EN.
- Enfoque de la asignatura: socio-funcional (para qué servía el deporte y a quién), sin listas de récords ni de campeones.
- `img`: una imagen de Commons con licencia Dominio público, CC0, CC BY o CC BY-SA, a ser posible histórica y relacionada con el origen; si no la hay, una actual del deporte. `pie` ES/EN describiendo lo que se ve, `autor` (texto limpio; si es «Unknown author» pon `{"es":"Autor anónimo","en":"Anonymous"}`), `licencia` (`{"es":"Dominio público","en":"Public domain"}` o la sigla CC tal cual), `url` (la de Commons). Si no encuentras ninguna imagen adecuada, deja `img` vacío `{}` y dilo.

## Estilo (obligatorio, en los dos idiomas)
- Prosa de ensayo universitario en castellano, frases largas bien articuladas, tono sobrio, sin adornos, sin preguntas retóricas ni cierres con efecto.
- Prohibido el guion largo (—) y el semilargo como inciso: usa comas o paréntesis.
- Prohibida la construcción «no es X, sino Y» y sus variantes; no uses «sino» salvo en una cita.
- Prohibidos los dos puntos seguidos de una enumeración.
- «Conviene», «puesto que» y «dado que» se pueden usar con moderación.
- Nada de «genuinamente», «honestamente», «fascinante», «crucial», «clave», «en definitiva», «cabe destacar».
- Cursiva con *asteriscos* para términos en otra lengua y títulos.

## Qué entregar
- Escribe tu tanda en `tools/enc_tandas/tanda_NN.json` (NN = tu número) como lista JSON de fichas con exactamente estos campos: `id`, `name`, `bloque`, `tipo` (los tres copiados de la lista maestra), `cuando`, `body` {es:[...],en:[...]}, `tema` (lista, puede ir vacía), `img`, `refs`, `refs_en`. Guarda el fichero después de cada ficha terminada, para no perder trabajo.
- No toques `data/enciclopedia.json`, `index.html` ni ningún otro fichero. No borres nada.
- Al terminar, responde con un resumen breve: ids hechos, ids que no pudiste hacer y por qué, y cualquier dato dudoso o contradicción entre fuentes que Alex deba conocer.

## Reglas de acceso a la web (añadidas tras las primeras tandas)
- **Prohibido usar copias de archivo, caché o espejos** (web.archive.org, archive.today, cachés de buscadores) para leer una web a la que no se llega directamente. Si una web no se puede abrir con WebFetch, se da por no disponible y se usa otra fuente. Los libros antiguos de dominio público digitalizados (por ejemplo, un libro de 1909 en archive.org) sí se pueden usar, porque no sustituyen a una web bloqueada.
- **Las búsquedas web son limitadas y compartidas entre todos los redactores.** Haz como máximo una o dos búsquedas por deporte y ve directo a la página de historia de la federación. Si WebSearch deja de funcionar, no insistas: termina con la biblioteca las fichas que se puedan hacer con garantías y deja el resto sin hacer, explicándolo en el resumen.
