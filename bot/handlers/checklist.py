"""
Handler para checklists interactivos.
Comando: /checklist <tramite>
"""

import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from bot.utils.checklists import obtener_checklist, listar_checklists, formatear_checklist

logger = logging.getLogger(__name__)


async def cmd_checklist(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    /checklist <tramite>
    Muestra un checklist paso a paso para un trámite.

    Ejemplos:
        /checklist registro_marca
        /checklist clave_fiscal
        /checklist monotributo_alta
        /checklist facturacion
        /checklist adherir_inpi
    """
    if not context.args:
        texto = listar_checklists()
        await update.message.reply_text(texto, disable_web_page_preview=True)
        return

    checklist_id = context.args[0].lower()
    checklist = obtener_checklist(checklist_id)

    if not checklist:
        texto = f"No encontré el checklist '{checklist_id}'.\n\n" + listar_checklists()
        await update.message.reply_text(texto, disable_web_page_preview=True)
        return

    texto = formatear_checklist(checklist)

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("Menú principal", callback_data="menu_inpi"
            if "inpi" in checklist_id or "marca" in checklist_id
            else "menu_arca")],
    ])

    await update.message.reply_text(
        texto,
        reply_markup=keyboard,
        disable_web_page_preview=True,
    )
