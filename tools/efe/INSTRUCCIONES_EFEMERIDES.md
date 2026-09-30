# «Tal día como hoy»: instrucciones para redactar efemérides

Historiapp tendrá cada día una curiosidad de historia del deporte ligada a esa fecha del calendario. Se necesita **una efeméride por día**, en castellano y en inglés, verdadera y con fuente.

## Qué entregar
Un fichero `tools/efe/efe_MM.json` por cada mes asignado (MM = 01…12), lista JSON de objetos:
`{"d":"MM-DD","year":1891,"es":"…","en":"…","refs":["…APA 7…"],"refs_en":["…APA 7 inglés…"],"enc":"id-de-la-enciclopedia o null"}`
Guarda el fichero tras cada día terminado.

## Contenido
- Un hecho de historia del deporte ocurrido ese día del año (cualquier año): fundación de un deporte, un club o una federación, un primer partido, un reglamento, unos Juegos, un récord con valor histórico, un hito de las mujeres en el deporte, un momento del deporte español, etc. El enfoque de la asignatura es socio-funcional: mejor el hecho que dice algo sobre la sociedad que el mero récord.
- Texto de 35 a 70 palabras por idioma, una o dos frases, con el año al principio o dentro del texto, y la cita APA 7 entre paréntesis al final: «(Guttmann, 2004, p. 160)».
- Evita necrológicas y tragedias salvo que sean hechos históricos de primer orden, y entonces con tono sobrio.
- Varía épocas, deportes, países y protagonistas a lo largo del mes; que haya mujeres y que haya España.

## Fuentes, por este orden
1. **Hechos ya verificados en la app.** `tools/efe/cobertura_enciclopedia.json` indica, por fecha MM-DD, qué fichas de `data/enciclopedia.json` (o de `data/tema01.json` y `data/tema02.json`, con prefijo `T01:`/`T02:`) contienen un hecho con día, mes y año. Si tu día aparece ahí, usa ese hecho y la misma cita que trae la ficha, y pon su id en `enc`. Es la vía más barata y segura.
2. **Biblioteca**: `~/mnt/LIBROS/Historia Deporte/`, con Guttmann (2004) convertido como `~/enc/gut04.txt` (impresa = física − 17) y Levinson y Christensen (1999) como `lev99r` (impresa = física − 18); busca con `python3 ~/enc/busca.py <alias> "palabra"`. Vamplew (2021) y otros también están.
3. **Web**: federaciones, Olympedia, COI, organismos oficiales. Pocas búsquedas, una por día como máximo. **Nada de copias de archivo ni cachés.** Wikipedia solo para localizar, nunca para citar.
4. Nunca inventes un hecho, una fecha ni una página. Si para un día no encuentras un hecho verificable, déjalo fuera y dilo en tu resumen.
5. Evita a Fernández Truan salvo que no haya otra fuente.

## Estilo (obligatorio en los dos idiomas)
Sin guiones largos (—), sin «no es X, sino Y», sin «sino» fuera de cita, sin dos puntos seguidos de enumeración, sin «crucial», «fascinante», «clave», «cabe destacar». Tono sobrio de historiador. En `refs_en`, «n.d.», «In», «&».

## Resumen final
Días hechos, días sin hacer y cualquier dato dudoso.
