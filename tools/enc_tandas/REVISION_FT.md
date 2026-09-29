# Revisión: sustituir a Fernández Truan donde se pueda

Alex prefiere no usar el manual de Fernández Truan (tomo IV) como fuente. Tarea: repasar las fichas asignadas, que están en `data/enciclopedia.json`, y cambiar cada cita de Fernández Truan por otra fuente fiable **solo si se puede hacer bien**. Si no, se deja como está.

## Criterio
1. **Citas que sostienen un dato** («… (Fernández Truan, s. f., p. 123)»): busca el mismo dato en la federación (web oficial, abierta directamente), en un libro o artículo de la biblioteca (con página) o en una fuente institucional (UNESCO, ministerio, boletín oficial, museo). Si lo encuentras, cambia la cita. Si la otra fuente da un dato distinto, corrige el texto con la fuente fiable. Si no encuentras nada, deja la cita de Fernández Truan.
2. **Menciones que refutan o contrastan a Fernández Truan** («algún manual dice X, pero…», «Fernández Truan fecha en…, mientras la federación…»): se dejan, porque no lo usan como fuente. Puedes suprimirlas solo si la frase no aporta nada al alumno.
3. Si una ficha deja de citar a Fernández Truan, quita su referencia de `refs` y `refs_en`.
4. No cambies nada más: ni imagen, ni `tema`, ni el resto del texto. Lo que cambies en castellano, cámbialo igual en inglés.

## Reglas de siempre
Las de `INSTRUCCIONES.md` (léelo): nada de copias de archivo ni cachés, pocas búsquedas web (una o dos por dato), nada inventado, páginas comprobadas, estilo sin guiones largos, sin «sino» y sin dos puntos seguidos de enumeración. Biblioteca convertida en `~/enc/` (`lev99r` impresa = física − 18, `gut04` impresa = física − 17, y otras que encuentres allí). No toques `data/enciclopedia.json`.

## Entrega
Escribe las fichas que cambies, completas, en `tools/enc_tandas/tanda_32_N.json` (N = tu número), guardando tras cada una. Las que no cambies no hace falta escribirlas. Responde con una tabla breve: ficha, citas de Fernández Truan que había, cuántas has sustituido, y cualquier dato corregido.
