"""
Handler de callbacks para botones inline (InlineKeyboardButton).
Maneja la navegación jerárquica de temas del bot.

Lógica:
- callback_data que empieza con "menu_" → muestra un menú con botones
- cualquier otro callback_data → muestra un topic detallado con sub-botones
"""

import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from bot.knowledge import get_topic, get_menu, TOPICS

logger = logging.getLogger(__name__)


def build_keyboard(botones: list[tuple[str, str]], columns: int = 1) -> InlineKeyboardMarkup:
    """
    Arma un InlineKeyboardMarkup a partir de una lista de (texto, callback_data).
    Por defecto 1 botón por fila para que sea legible.
    """
    keyboard = []
    for texto, callback_data in botones:
        keyboard.append([InlineKeyboardButton(texto, callback_data=callback_data)])
    return InlineKeyboardMarkup(keyboard)


async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handler principal para CallbackQuery (cuando el usuario toca un botón inline).
    """
    query = update.callback_query
    await query.answer()  # Acknowledge the callback (quita el loading del botón)

    data = query.data

    # Si es un menú (menu_xxx), mostrar el menú correspondiente
    if data.startswith("menu_"):
        menu_id = data[5:]  # quitar "menu_"
        await _mostrar_menu(query, menu_id)
        return

    # Herramientas que requieren input del usuario
    if data == "tool_cuit":
        await query.edit_message_text(
            "Para consultar un CUIT, usá el comando:\n\n"
            "  /cuit <numero>\n\n"
            "Ejemplo: /cuit 20-12345678-9"
        )
        return
    if data == "tool_monotributo_calc":
        await query.edit_message_text(
            "Para calcular tu categoría de monotributo, usá:\n\n"
            "  /monotributo_calc <facturación anual>\n\n"
            "Ejemplo: /monotributo_calc 5000000\n"
            "Ver todas: /monotributo_calc categorias"
        )
        return
    if data == "tool_vencimientos":
        await query.edit_message_text(
            "Para ver vencimientos fiscales:\n\n"
            "  /vencimientos → generales\n"
            "  /vencimientos 3 → para CUIT terminado en 3"
        )
        return

    # Si es un topic, mostrar detalle con sub-botones
    topic = get_topic(data)
    if topic:
        await _mostrar_topic(query, topic)
        return

    # Fallback: no se encontró el callback
    logger.warning(f"Callback no reconocido: {data}")
    await query.edit_message_text("No encontré esa opción. Probá con /start para ver los comandos.")


async def _mostrar_menu(query, menu_id: str):
    """Muestra un menú con botones inline."""
    menu = get_menu(menu_id)
    if not menu:
        await query.edit_message_text("Menú no encontrado. Probá con /start.")
        return

    keyboard = build_keyboard(menu["botones"])
    await query.edit_message_text(
        text=menu["texto"],
        reply_markup=keyboard,
        disable_web_page_preview=True,
    )


async def _mostrar_topic(query, topic: dict):
    """Muestra un topic detallado con link y sub-botones."""
    texto = topic["texto"]
    link = topic.get("link", "")

    if link:
        texto += f"\n\nMás info: {link}"

    botones = topic.get("botones", [])
    keyboard = build_keyboard(botones) if botones else None

    await query.edit_message_text(
        text=texto,
        reply_markup=keyboard,
        disable_web_page_preview=True,
    )


async def send_menu(update: Update, menu_id: str):
    """
    Envía un menú como mensaje nuevo (no como edit de callback).
    Usado por los comandos directos (/inpi, /clavefiscal, etc.)
    """
    menu = get_menu(menu_id)
    if not menu:
        await update.message.reply_text("Menú no encontrado.")
        return

    keyboard = build_keyboard(menu["botones"])
    await update.message.reply_text(
        text=menu["texto"],
        reply_markup=keyboard,
        disable_web_page_preview=True,
    )


async def send_topic(update: Update, topic_id: str):
    """
    Envía un topic como mensaje nuevo (no como edit de callback).
    Usado por texto libre y comandos que matchean directo a un topic.
    """
    topic = get_topic(topic_id)
    if not topic:
        await update.message.reply_text("Tema no encontrado.")
        return

    texto = topic["texto"]
    link = topic.get("link", "")

    if link:
        texto += f"\n\nMás info: {link}"

    botones = topic.get("botones", [])
    keyboard = build_keyboard(botones) if botones else None

    await update.message.reply_text(
        text=texto,
        reply_markup=keyboard,
        disable_web_page_preview=True,
    )
