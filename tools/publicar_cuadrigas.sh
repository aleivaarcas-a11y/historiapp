#!/bin/bash
# Publica Cuadrigas en Historiapp con un solo comando (12-10-2026).
#   bash "/Users/leiva/Mi unidad /UCAM/ASIGNATURAS/Claude outputs/Historiapp/tools/publicar_cuadrigas.sh"
# 1. Sube el Apps Script del ranking en su versión 4 (resultados y fantasmas de Cuadrigas) a la MISMA dirección de siempre.
# 2. Publica la app en GitHub Pages con subir.sh (juegos/cuadrigas.html ya está en la copia maestra).
set -e
DEPLOY="AKfycbzjxo9QvXjWabkFGm3MtbgTJWV1OMT372TAD7n-iTSoSR7av2KMpYBb3LhRfXvWt36GeA"
echo "==> 1/2 · Apps Script del ranking (v4)"
if ! command -v clasp >/dev/null 2>&1; then echo "==> Instalando clasp…"; npm install -g @google/clasp; fi
[ -f "$HOME/.clasprc.json" ] || { echo "==> Inicia sesión en Google con la cuenta de la UCAM (se abrirá el navegador)"; clasp login; }
cd "$HOME/historiapp-ranking"
clasp push -f
clasp deploy -i "$DEPLOY" -d "v4 · Cuadrigas $(date '+%Y-%m-%d')"
echo "==> 2/2 · Historiapp en GitHub Pages"
bash "/Users/leiva/Mi unidad /UCAM/ASIGNATURAS/Claude outputs/Historiapp/subir.sh"
echo
echo "Listo. Los resultados de Cuadrigas llegan a la pestaña «Cuadrigas» de la hoja del ranking."
