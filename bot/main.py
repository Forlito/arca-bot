"""
arca-bot: Bot de Telegram para consultar marcas en el INPI Argentina
y resolver dudas sobre ARCA/AFIP.

Para correrlo:
    1. Copiá .env.example a .env y poné tu token de BotFather
    2. pip install -r requirements.txt
    3. python -m bot.main
"""

import os
import sys
import logging
from pathlib import Path

# Logging ANTES de todo para ver errores
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


def main():
    """Arranca el bot."""
    print("[1/5] Cargando configuración...")

    project_dir = Path(__file__).parent.parent
    env_file = project_dir / ".env"

    try:
        from dotenv import load_dotenv
        if env_file.exists():
            load_dotenv(env_file)
            print(f"[2/5] .env cargado desde {env_file}")
        else:
            load_dotenv()
            print(f"[2/5] .env cargado desde directorio actual")
    except ImportError:
        print("[2/5] AVISO: python-dotenv no instalado, buscando variable de entorno directo")

    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token:
        print("\n❌ ERROR: No se encontró TELEGRAM_BOT_TOKEN")
        print(f"   Buscó en: {env_file}")
        print(f"   ¿Existe el archivo? {env_file.exists()}")
        print("   Asegurate de tener un archivo .env con:")
        print("   TELEGRAM_BOT_TOKEN=tu_token_de_botfather")
        return

    print(f"[3/5] Token encontrado ({token[:10]}...)")

    try:
        from telegram.ext import Application, CommandHandler, MessageHandler, filters
    except ImportError:
        print("\n❌ ERROR: python-telegram-bot no está instalado")
        print("   Corré: pip install python-telegram-bot")
        return

    print("[4/5] Registrando comandos...")

    from bot.handlers.search import cmd_buscar, cmd_disponible, cmd_buscar_todas
    from bot.handlers.info import cmd_start, cmd_ayuda, cmd_clase, cmd_clases
    from bot.handlers.faq import (
        cmd_consulta, cmd_clavefiscal, cmd_monotributo, cmd_factura,
        cmd_inpi, cmd_tramites, cmd_registrar, handle_texto_libre,
    )

    app = Application.builder().token(token).build()

    # Comandos de búsqueda de marcas
    app.add_handler(CommandHandler("start", cmd_start))
    app.add_handler(CommandHandler("ayuda", cmd_ayuda))
    app.add_handler(CommandHandler("help", cmd_ayuda))
    app.add_handler(CommandHandler("buscar", cmd_buscar))
    app.add_handler(CommandHandler("disponible", cmd_disponible))
    app.add_handler(CommandHandler("buscar_todas", cmd_buscar_todas))
    app.add_handler(CommandHandler("clase", cmd_clase))
    app.add_handler(CommandHandler("clases", cmd_clases))

    # Comandos de FAQ / consultas
    app.add_handler(CommandHandler("consulta", cmd_consulta))
    app.add_handler(CommandHandler("clavefiscal", cmd_clavefiscal))
    app.add_handler(CommandHandler("monotributo", cmd_monotributo))
    app.add_handler(CommandHandler("factura", cmd_factura))
    app.add_handler(CommandHandler("inpi", cmd_inpi))
    app.add_handler(CommandHandler("tramites", cmd_tramites))
    app.add_handler(CommandHandler("registrar", cmd_registrar))

    # Texto libre (va ÚLTIMO, es el fallback para cualquier mensaje)
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_texto_libre))

    print("[5/5] Bot arrancando... (presioná Ctrl+C para parar)")
    print("      Abrí Telegram y escribile /start a tu bot\n")

    app.run_polling(drop_pending_updates=True)


if __name__ == "__main__":
    main()
