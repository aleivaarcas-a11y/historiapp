# Curiosidades de nivel (Historiapp)

Historiapp tiene 100 niveles. Cada vez que un alumno sube de nivel aparece un mensaje emergente con una curiosidad de historia del deporte y su foto. Las 100 curiosidades forman un viaje cronológico: el nivel 1 está en la Prehistoria y el 100 en el deporte actual. El alumno tiene 18-19 años y estudia 1.º de Ciencias de la Actividad Física y del Deporte (UCAM). La curiosidad debe sorprenderle y darle ganas de seguir subiendo.

Te toca un lote de 20 niveles con su reparto de épocas (te lo da el encargo). Dentro de cada época, ordena de más antiguo a más reciente.

## Qué es una buena curiosidad
- Un hecho verdadero, concreto y poco conocido, con un detalle que se recuerda (una cifra, un nombre, un objeto, una anécdota, una consecuencia inesperada). Que el alumno piense «no lo sabía».
- El enfoque de la asignatura es socio-funcional: mejor el hecho que dice algo de la sociedad de su tiempo (religión, guerra, poder, clase, género, dinero, nación) que el récord por el récord.
- Varía deportes, países y protagonistas. Que haya mujeres en cada lote y algo de España o del mundo hispano.
- Nada de necrológicas ni tragedias salvo hecho de primer orden, y entonces con tono sobrio.
- **Sin repetir** lo que ya está en «Tal día como hoy»: antes de dar por buena una curiosidad, busca sus palabras clave en `../../data/efemerides.json` (por ejemplo `grep -i "louis" ../../data/efemerides.json`). Si el mismo hecho ya está, busca otro. Un mismo personaje vale si el hecho es distinto.

## Fuentes
1. Web fiable: museos, Olympedia, COI, federaciones, universidades, revistas académicas, libros en Google Books con página. Wikipedia solo para localizar, nunca para citar. Nada de copias de archivo ni cachés.
2. Los libros de `~/mnt/LIBROS/` (PDF) si los tienes a mano.
3. **Nunca inventes un hecho, una fecha, una cifra, una fuente ni una página.** Si no puedes verificar algo, cambia de curiosidad. Si te queda una duda, dila en el campo `nota`.

## Texto (castellano y su traducción al inglés)
- `titulo`: gancho de 3 a 8 palabras, sin dos puntos (ejemplo: «El maratón que se corrió con vino»).
- `texto`: 40 a 70 palabras, una a tres frases, con la fecha o la época dentro, y la cita APA 7 entre paréntesis al final: «(Guttmann, 2004, p. 160)» o «(Olympedia, s. f.)».
- `fecha`: cómo se muestra la época, corta: «c. 3000 a. C.», «776 a. C.», «Siglo XII», «1896». En inglés: «c. 3000 BC», «776 BC», «12th century», «1896».
- Estilo obligatorio en los dos idiomas: sin guiones largos (—), sin «no es X, sino Y» ni variantes, sin «sino» fuera de cita, sin dos puntos seguidos de enumeración, sin «crucial», «fascinante», «clave», «cabe destacar», «sin duda», sin preguntas retóricas ni exclamaciones. Frases claras de historiador que cuenta bien; la emoción la pone el hecho. En `refs_en`: «n.d.», «In», «&».

## Foto
Una imagen de Wikimedia Commons ligada a la curiosidad, por este orden de preferencia: el hecho o una imagen de la época; el protagonista; el lugar u objeto (estadio, trofeo, cartel, pieza de museo); una imagen genérica del deporte en época parecida, con pie que diga con claridad qué muestra. Nada que induzca a error.
Licencias válidas: dominio público, CC0, CC BY, CC BY-SA. Nada de «fair use», no libres o con marcas de agua. Evita menores identificables.

Herramientas, en el ordenador de Alex con `mcp__remote-devices__device_bash` (cárgala con ToolSearch: `select:mcp__remote-devices__device_bash`). Cada llamada es un shell nuevo: empieza siempre con `cd "$HOME/mnt/ASIGNATURAS/Claude outputs/Historiapp/tools/curio"`. **No uses el Bash de la nube para Commons** (IP bloqueada, error 429).
- `python3 commons.py buscar "consulta" [n]` busca y muestra licencia, autor, fecha y descripción. Prueba en inglés y en el idioma del país.
- `python3 commons.py info "File:Nombre.jpg"` datos de un fichero.
- `python3 getimg.py NNN "File:Nombre.jpg"` descarga a `img/curio/NNN.jpg` (NNN = nivel con tres cifras: 001, 042, 100).
Commons limita las peticiones: como mucho cuatro búsquedas por curiosidad, `sleep 3` entre búsquedas, pocas búsquedas por llamada (cada llamada dura como mucho 120 s). Si aparece un 429, espera un minuto.

## Salida
Fichero `lote_N.json` en esta carpeta, guardado tras cada curiosidad terminada (no al final), lista JSON de objetos:
```json
{"n": 1, "era": {"es": "Prehistoria", "en": "Prehistory"},
 "fecha": {"es": "c. 7000 a. C.", "en": "c. 7000 BC"},
 "titulo": {"es": "…", "en": "…"},
 "texto": {"es": "… (Autor, año, p. X).", "en": "… (Author, year, p. X)."},
 "refs": ["APA 7 completa en castellano"], "refs_en": ["APA 7 completa en inglés"],
 "img": {"src": "img/curio/001.jpg", "pie": {"es": "Qué muestra la imagen según su ficha", "en": "…"},
         "autor": {"es": "Nombre o «Autor anónimo»", "en": "Name or «Anonymous»"},
         "licencia": "Dominio público | CC BY-SA 4.0 | …", "url": "https://commons.wikimedia.org/wiki/File:…",
         "tipo": "hecho | protagonista | lugar | genérica"},
 "nota": ""}
```
Si para una curiosidad no hay foto válida, pon `"img": null` y explícalo en `nota`.

Al terminar, comprueba con Python que el JSON carga, que están los 20 niveles, que cada `src` existe en `../../img/curio/` y que ningún texto contiene «—». Resumen final breve: niveles hechos, sin foto y dudas.
