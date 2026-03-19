"""
Handlers para monitoreo/vigilancia de marcas.
Comandos: /vigilar, /mis_vigilancias, /dejar_vigilar
"""

import logging
from telegram import Update
from telegram.ext import ContextTypes

from bot.db import agregar_vigilancia, eliminar_vigilancia, listar_vigilancias

logger = logging.getLogger(__name__)

MAX_VIGILANCIAS_POR_USUARIO = 10


async def cmd_vigilar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    /vigilar <nombre> [clase]
    Agrega una marca para monitorear periódicamente.

    Ejemplos:
        /vigilar MiMarca
        /vigilar MiMarca 42
    """
    if not context.args:
        await update.message.reply_text(
            "Usá: /vigilar <nombre> [clase]\n\n"
            "El bot chequeará periódicamente si aparecen nuevas marcas "
            "con ese nombre y te avisará.\n\n"
            "Ejemplos:\n"
            "  /vigilar MiStartup\n"
            "  /vigilar MiStartup 42\n\n"
            "Otros comandos:\n"
            "  /mis_vigilancias → ver las activas\n"
            "  /dejar_vigilar <nombre> → dejar de vigilar"
        )
        return

    user_id = update.effective_user.id

    # Verificar límite
    existentes = await listar_vigilancias(user_id)
    if len(existentes) >= MAX_VIGILANCIAS_POR_USUARIO:
        await update.message.reply_text(
            f"Ya tenés {MAX_VIGILANCIAS_POR_USUARIO} vigilancias activas (máximo).\n"
            "Eliminá alguna con /dejar_vigilar <nombre> para agregar otra."
        )
        return

    args = list(context.args)
    clase = -1

    if len(args) >= 2 and args[-1].isdigit():
        posible_clase = int(args[-1])
        if 1 <= posible_clase <= 45:
            clase = posible_clase
            args = args[:-1]

    nombre = " ".join(args).strip().upper()
    if not nombre:
        await update.message.reply_text("Tenés que poner un nombre para vigilar.")
        return

    agregado = await agregar_vigilancia(user_id, nombre, clase)

    if agregado:
        clase_txt = f" en clase {clase}" if clase != -1 else " en todas las clases"
        await update.message.reply_text(
            f"✅ Vigilancia activada para \"{nombre}\"{clase_txt}.\n\n"
            f"Te voy a avisar si aparecen nuevas marcas con ese nombre.\n"
            f"Chequeo cada 6 horas."
        )
    else:
        await update.message.reply_text(
            f"Ya estás vigilando \"{nombre}\". "
            f"Usá /mis_vigilancias para ver las activas."
        )


async def cmd_mis_vigilancias(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """/mis_vigilancias - Lista las vigilancias activas."""
    user_id = update.effective_user.id
    vigilancias = await listar_vigilancias(user_id)

    if not vigilancias:
        await update.message.reply_text(
            "No tenés vigilancias activas.\n"
            "Usá /vigilar <nombre> para empezar a monitorear una marca."
        )
        return

    lines = [f"Tus vigilancias activas ({len(vigilancias)}):\n"]
    for v in vigilancias:
        clase_txt = f"Clase {v['clase']}" if v['clase'] != -1 else "Todas las clases"
        check_txt = f" (último: {v['last_count']} resultados)" if v['last_count'] > 0 else ""
        lines.append(f"  • {v['denominacion']} [{clase_txt}]{check_txt}")

    lines.append(f"\nPara dejar de vigilar: /dejar_vigilar <nombre>")
    await update.message.reply_text("\n".join(lines))


async def cmd_dejar_vigilar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    /dejar_vigilar <nombre>
    Elimina una vigilancia activa.
    """
    if not context.args:
        await update.message.reply_text(
            "Usá: /dejar_vigilar <nombre>\n"
            "Ejemplo: /dejar_vigilar MiMarca\n\n"
            "Usá /mis_vigilancias para ver las activas."
        )
        return

    user_id = update.effective_user.id
    nombre = " ".join(context.args).strip().upper()

    eliminado = await eliminar_vigilancia(user_id, nombre)

    if eliminado:
        await update.message.reply_text(f"✅ Dejaste de vigilar \"{nombre}\".")
    else:
        await update.message.reply_text(
            f"No encontré una vigilancia para \"{nombre}\".\n"
            f"Usá /mis_vigilancias para ver las activas."
        )
