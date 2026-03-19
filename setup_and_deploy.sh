#!/bin/bash
# =============================================================
# ARCA-BOT: Script de setup y deploy
# Corre esto desde la carpeta arca-bot en tu Mac
# =============================================================

echo ""
echo "========================================="
echo "  ARCA-BOT: Setup y Deploy"
echo "========================================="
echo ""

# 1. Verificar que estamos en la carpeta correcta
if [ ! -f "bot/main.py" ]; then
    echo "ERROR: No estás en la carpeta correcta."
    echo "Corré: cd /ruta/a/arca-bot"
    echo "Y después: bash setup_and_deploy.sh"
    exit 1
fi

echo "[1/6] Carpeta correcta"

# 2. Crear virtual environment e instalar dependencias
echo "[2/6] Instalando dependencias..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi
source venv/bin/activate
pip install -r requirements.txt -q
if [ $? -ne 0 ]; then
    echo "ERROR: Falló la instalación de dependencias"
    exit 1
fi
echo "      Dependencias instaladas (venv)"

# 3. Test rápido del parser
echo "[3/6] Testeando parser..."
python3 tests/test_parser.py
if [ $? -ne 0 ]; then
    echo "ERROR: Falló el test del parser"
    exit 1
fi

# 4. Verificar token
if [ ! -f ".env" ]; then
    echo "ERROR: No existe el archivo .env"
    echo "Crealo con: echo 'TELEGRAM_BOT_TOKEN=tu_token' > .env"
    exit 1
fi
echo "[4/6] .env encontrado"

# 5. Inicializar git y subir a GitHub
echo "[5/6] Configurando Git..."
if [ ! -d ".git" ]; then
    git init
    git add -A
    git commit -m "Initial commit: arca-bot v1"

    echo ""
    echo "Ahora necesitás crear el repo en GitHub:"
    echo "  1. Andá a https://github.com/new"
    echo "  2. Nombre: arca-bot"
    echo "  3. Dejá todo default y hacé click en 'Create repository'"
    echo "  4. Copiá la URL del repo (ej: https://github.com/TU_USUARIO/arca-bot.git)"
    echo ""
    read -p "Pegá la URL del repo acá: " REPO_URL

    git remote add origin "$REPO_URL"
    git branch -M main
    git push -u origin main
    echo "      Código subido a GitHub"
else
    echo "      Git ya inicializado"
    git add -A
    git commit -m "Update arca-bot" 2>/dev/null
    git push 2>/dev/null
fi

# 6. Info para Railway
echo ""
echo "[6/6] Deploy en Railway"
echo ""
echo "========================================="
echo "  ÚLTIMO PASO: Conectar Railway"
echo "========================================="
echo ""
echo "  1. Andá a https://railway.app"
echo "  2. Logueate con tu cuenta de GitHub"
echo "  3. Click en 'New Project'"
echo "  4. Elegí 'Deploy from GitHub repo'"
echo "  5. Seleccioná 'arca-bot'"
echo "  6. En Settings > Variables, agregá:"
echo "     TELEGRAM_BOT_TOKEN = (tu token de BotFather)"
echo "  7. Railway lo deploya automáticamente"
echo ""
echo "  Listo! El bot va a estar corriendo 24/7."
echo ""
echo "========================================="
echo ""

# Ofrecer correr local mientras tanto
read -p "Querés correr el bot local mientras tanto? (s/n): " CORRER
if [ "$CORRER" = "s" ] || [ "$CORRER" = "S" ]; then
    echo ""
    echo "Arrancando bot... (Ctrl+C para parar)"
    echo ""
    python3 -m bot.main
fi
