# Reemplazos de curiosidades que ya están en los PPT (08-10-2026)

Algunas de las 100 curiosidades de nivel cuentan hechos que ya explican los PPT de la asignatura. Alex quiere que las curiosidades traigan cosas que el alumno NO ve en clase. Hay que sustituir esos niveles por curiosidades nuevas.

Lee primero `INSTRUCCIONES_CURIOSIDADES.md` (en esta carpeta): todo lo que dice sobre contenido, fuentes, estilo, foto, licencias y herramientas sigue valiendo.

## Comprobaciones adicionales antes de dar por buena una curiosidad
1. **Que no esté en los PPT.** El texto de los 11 PPT (diapositivas y notas del orador) está en `ppt_texto/T1.txt` … `T11.txt`. Busca sin tildes ni mayúsculas los nombres propios y palabras distintivas del hecho, por ejemplo:
   `python3 -c "import unicodedata,sys,glob;n=lambda s:''.join(c for c in unicodedata.normalize('NFD',s.lower()) if unicodedata.category(c)!='Mn');k=n(sys.argv[1]);[print(f,n(open(f).read()).count(k)) for f in sorted(glob.glob('ppt_texto/*.txt')) if k in n(open(f).read())]" "palabra"`
   Si el hecho (o su protagonista central) aparece, busca otro.
2. **Que no esté en «Tal día como hoy»** (`../../data/efemerides.json`).
3. **Que no repita otra curiosidad**: mira los títulos y textos de `lote_1.json` … `lote_5.json`.
4. **Que encaje en el hueco cronológico** que te dan (entre la curiosidad anterior y la siguiente). Usa en `era` el mismo nombre de época que llevan las curiosidades vecinas de su lote.

## Salida
No toques los `lote_N.json`. Escribe tu fichero `reemplazos_X.json` (X = la letra de tu encargo) en esta carpeta, con el mismo formato de objeto que los lotes y el mismo `n` del nivel que sustituyes, guardando tras cada curiosidad. La foto se descarga con `python3 getimg.py NNN "File:…"` y sustituye a la anterior en `img/curio/NNN.jpg`.
Al terminar, comprueba con Python que el JSON carga, que están todos tus niveles, que cada `src` existe y que no hay «—». Resumen breve: niveles hechos, sin foto y dudas.
