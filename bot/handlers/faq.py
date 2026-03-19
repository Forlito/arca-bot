"""
Handler de preguntas frecuentes y texto libre.
Responde por keywords cuando el usuario escribe cualquier mensaje.
"""

import logging
from telegram import Update
from telegram.ext import ContextTypes

from bot.knowledge import buscar_respuesta, obtener_fallback_link

logger = logging.getLogger(__name__)


async def cmd_consulta(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    /consulta <tema>
    Busca en la base de conocimiento sobre ARCA/INPI.

    Ejemplos:
        /consulta clave fiscal
        /consulta como registro una marca
        /consulta monotributo
    """
    if not context.args:
        await update.message.reply_text(
            "Escribí tu consulta directamente. Por ejemplo:\n\n"
            "  /consulta como saco la clave fiscal\n"
            "  /consulta como registro una marca\n"
            "  /consulta que es el monotributo\n\n"
            "O simplemente escribí tu pregunta sin comando y te respondo."
        )
        return

    texto = " ".join(context.args)
    await _responder_consulta(update, texto)


async def handle_texto_libre(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handler para mensajes de texto libre (sin comando).
    Intenta responder buscando en la base de conocimiento.
    """
    if not update.message or not update.message.text:
        return

    texto = update.message.text.strip()

    # Ignorar mensajes muy cortos
    if len(texto) < 3:
        return

    await _responder_consulta(update, texto)


async def _responder_consulta(update: Update, texto: str):
    """Busca respuesta y la envía."""
    entry = buscar_respuesta(texto)

    if entry:
        respuesta = entry["respuesta"]
        link = entry.get("link", "")

        if link:
            respuesta += f"\n\nMás info: {link}"

        await update.message.reply_text(respuesta, disable_web_page_preview=True)
    else:
        # No encontró match: redirigir al link más relevante
        link = obtener_fallback_link(texto)
        await update.message.reply_text(
            f"No tengo una respuesta exacta para eso, pero probablemente encuentres "
            f"lo que necesitás acá:\n\n{link}\n\n"
            "También podés probar con palabras clave más específicas, por ejemplo:\n"
            "  clave fiscal\n"
            "  registrar marca\n"
            "  monotributo\n"
            "  facturar",
            disable_web_page_preview=True,
        )


# Comandos directos para los temas más comunes
async def cmd_clavefiscal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """/clavefiscal - Todo sobre clave fiscal."""
    if context.args:
        texto = "clave fiscal " + " ".join(context.args)
        await _responder_consulta(update, texto)
    else:
        await _responder_consulta(update, "que es clave fiscal obtener niveles")


async def cmd_monotributo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """/monotributo - Info sobre monotributo."""
    await _responder_consulta(update, "monotributo inscribir")


async def cmd_factura(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """/factura - Como facturar electronicamente."""
    await _responder_consulta(update, "facturar electronica")


async def cmd_inpi(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """/inpi - Que es el INPI y que podés hacer."""
    await _responder_consulta(update, "que es inpi registro marcas")


async def cmd_tramites(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """/tramites - Trámites disponibles online."""
    await _responder_consulta(update, "tramites online servicios disponibles")


async def cmd_registrar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """/registrar - Como registrar una marca."""
    await _responder_consulta(update, "registrar marca")
