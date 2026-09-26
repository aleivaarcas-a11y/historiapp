#!/bin/bash
# Historiapp: sube (o actualiza) la app en GitHub Pages con un solo comando.
# Uso, desde la Terminal del Mac:
#   bash "/Users/leiva/Mi unidad /UCAM/ASIGNATURAS/Claude outputs/Historiapp/subir.sh"
# La primera vez crea el repositorio y activa la página; las siguientes solo suben los cambios.

set -e
ORIGEN="$(cd "$(dirname "$0")" && pwd)"
DESTINO="$HOME/historiapp"
REPO="historiapp"

echo "==> Historiapp: publicar en GitHub Pages"

# 1. Herramientas
if ! command -v git >/dev/null 2>&1; then
  echo "Falta git. Instala las herramientas de Xcode con:  xcode-select --install   y vuelve a ejecutar este comando."; exit 1
fi
if ! command -v gh >/dev/null 2>&1; then
  if command -v brew >/dev/null 2>&1; then
    echo "==> Instalando la herramienta de GitHub (gh) con Homebrew…"; brew install gh
  else
    echo "Falta la herramienta de GitHub (gh). Descárgala de https://cli.github.com (botón Download for Mac), instálala y vuelve a ejecutar este comando."; exit 1
  fi
fi

# 2. Sesión de GitHub
if ! gh auth status >/dev/null 2>&1; then
  echo "==> Hay que iniciar sesión en GitHub (una sola vez). Se abrirá el navegador; acepta las opciones por defecto."
  gh auth login --web --git-protocol https
fi
USUARIO="$(gh api user --jq .login)"
echo "==> Usuario de GitHub: $USUARIO"

# 3. Copia de trabajo fuera de Google Drive
mkdir -p "$DESTINO"
rsync -a --delete --exclude ".git" --exclude ".DS_Store" --exclude "~\$*" --exclude "qr/" "$ORIGEN/" "$DESTINO/"
cd "$DESTINO"
if [ ! -d .git ]; then
  git init -b main >/dev/null
  git config user.name >/dev/null 2>&1 || git config user.name "$USUARIO"
  git config user.email >/dev/null 2>&1 || git config user.email "$USUARIO@users.noreply.github.com"
fi
git add -A
if git diff --cached --quiet; then
  echo "==> No hay cambios nuevos que subir."
else
  git commit -q -m "Historiapp $(date '+%Y-%m-%d %H:%M')"
fi

# 4. Repositorio remoto (se crea la primera vez)
if ! git remote get-url origin >/dev/null 2>&1; then
  if gh repo view "$USUARIO/$REPO" >/dev/null 2>&1; then
    git remote add origin "https://github.com/$USUARIO/$REPO.git"
  else
    echo "==> Creando el repositorio $USUARIO/$REPO…"
    gh repo create "$REPO" --public --source=. --remote=origin >/dev/null
  fi
fi
echo "==> Subiendo…"
git push -u origin main

# 5. GitHub Pages (se activa la primera vez)
if ! gh api "repos/$USUARIO/$REPO/pages" >/dev/null 2>&1; then
  echo "==> Activando GitHub Pages…"
  gh api -X POST "repos/$USUARIO/$REPO/pages" -f build_type=legacy -f "source[branch]=main" -f "source[path]=/" >/dev/null
fi

echo
echo "Listo. La app estará en uno o dos minutos en:"
echo "   https://$USUARIO.github.io/$REPO/"
echo "Guarda esa dirección: es la que comparten los alumnos y la que se usa para los QR."
