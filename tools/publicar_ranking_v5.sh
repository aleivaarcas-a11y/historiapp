#!/bin/bash
# Publica la v5 del ranking (Cuadrigas + clasificación de los juegos) y Historiapp con un solo comando (12-10-2026).
#   bash "$HOME/Mi unidad /UCAM/ASIGNATURAS/Claude outputs/Historiapp/tools/publicar_ranking_v5.sh"
# 1. Copia tools/ranking/Codigo_v5.js al proyecto de clasp (~/historiapp-ranking/Código.js), guardando antes la versión que hubiera.
# 2. Lo sube a la MISMA dirección de siempre (las acciones de Cuadrigas y del ranking no cambian).
# 3. Publica la app en GitHub Pages con subir.sh (juegos/pentatlon.html con el modo carrera ya está en la copia maestra).
set -e
DEPLOY="AKfycbzjxo9QvXjWabkFGm3MtbgTJWV1OMT372TAD7n-iTSoSR7av2KMpYBb3LhRfXvWt36GeA"
AQUI="$(cd "$(dirname "$0")" && pwd)"
echo "==> 1/3 · Copia de seguridad y v5"
cp "$HOME/historiapp-ranking/Código.js" "$HOME/historiapp-ranking/Código_antes_v5.js.bak"
cp "$AQUI/ranking/Codigo_v5.js" "$HOME/historiapp-ranking/Código.js"
echo "==> 2/3 · Apps Script del ranking (v5)"
if ! command -v clasp >/dev/null 2>&1; then echo "==> Instalando clasp…"; npm install -g @google/clasp; fi
[ -f "$HOME/.clasprc.json" ] || { echo "==> Inicia sesión en Google con la cuenta de la UCAM"; clasp login; }
cd "$HOME/historiapp-ranking"
clasp push -f
clasp deploy -i "$DEPLOY" -d "v5 · Cuadrigas + juegos $(date '+%Y-%m-%d')"
echo "==> 3/3 · Historiapp en GitHub Pages"
bash "$HOME/Mi unidad /UCAM/ASIGNATURAS/Claude outputs/Historiapp/subir.sh"
echo
echo "Listo. La clasificación del Pentatlón se guarda en la pestaña «Juegos» de la hoja del ranking."
