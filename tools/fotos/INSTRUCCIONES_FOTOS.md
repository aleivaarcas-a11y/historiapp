# Revisión de las fotos de la Enciclopedia

Alex quiere que la imagen de cada ficha **muestre el deporte practicándose**: gente jugando, compitiendo o entrenando (fotografía, pintura, grabado, relieve o miniatura; las históricas son preferibles si muestran la práctica).

## Hay que sustituir la imagen cuando muestra
- un retrato de una persona (fundador, inventor, campeón posando, dirigente), aunque sea importante;
- un objeto o material suelto (pelota, bate, silla, casco, balones), un trofeo, un documento, un reglamento, una patente, una portada de libro, un cartel, un sello, una placa, un mapa;
- un edificio, una instalación vacía o un paisaje sin la práctica;
- una ceremonia, una entrega de premios o el público sin la práctica.
Una pintura o un grabado que muestre la práctica vale. Si no hay imagen (`img` vacío), búscala.

## Cómo
1. Tu lote de ids está en `tools/fotos/lote_N.json`. Para cada ficha de `data/enciclopedia.json`, lee `img.pie` y, si hace falta, la descripción de Commons del fichero (`python3 ~/enc/commons.py` busca; la API `imageinfo` con `extmetadata` da la descripción). Decide si cumple.
2. Si no cumple, busca en Commons una imagen de la práctica (`python3 ~/enc/commons.py "consulta"`), con licencia Dominio público, CC0, CC BY o CC BY-SA, y descárgala con `python3 ~/enc/getimg2.py <id> "<título del fichero>"` (sustituye a la anterior; si Commons la sirve en PNG, comprueba que la ruta de `img.src` coincide con la extensión real).
3. Rehaz `img` completo: `src`, `pie` ES/EN que describa lo que se ve (sin inventar), `autor` (texto limpio o `{"es":"Autor anónimo","en":"Anonymous"}`), `licencia` (`{"es":"Dominio público","en":"Public domain"}` o la sigla CC), `url` de Commons.
4. Si no encuentras ninguna imagen de la práctica con licencia válida, deja la que había y anótalo.
5. Commons limita las peticiones: haz pausas y pocas búsquedas por ficha. Nada de copias de archivo.

## Entrega
Escribe en `tools/enc_tandas/tanda_47_N.json` las fichas que cambies, **completas** (copia la ficha de `data/enciclopedia.json` y cambia solo `img`). Guarda tras cada una. No toques `data/enciclopedia.json` ni otros ficheros. Responde con una tabla breve: ficha, imagen antigua, imagen nueva, y las que no pudiste arreglar.
