"""
Handler de preguntas frecuentes y texto libre.
Usa la base de conocimiento jerárquica con inline keyboards.
"""

import logging
from telegram import Update
from telegram.ext import ContextTypes

from bot.knowledge import buscar_respuesta, obtener_fallback_link
from bot.handlers.callbacks import send_menu, send_topic
from bot.utils.monotributo import (
    calcular_categoria, formatear_resultado_calculo, formatear_tabla_categorias,
)
from bot.utils.vencimientos import obtener_vencimientos_generales, obtener_vencimientos_por_terminacion

logger = logging.getLogger(__name__)


async def cmd_consulta(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    /consulta <tema>
    Busca en la base de conocimiento sobre ARCA/INPI.
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

    if len(texto) < 3:
        return

    await _responder_consulta(update, texto)


async def _responder_consulta(update: Update, texto: str):
    """Busca respuesta y la envía con inline keyboard si hay match."""
    entry = buscar_respuesta(texto)

    if entry:
        target = entry["target"]

        # Si el target es un menú, mostrar menú con botones
        if target.startswith("menu_"):
            menu_id = target[5:]
            await send_menu(update, menu_id)
        else:
            # Es un topic directo, mostrar con sub-botones
            await send_topic(update, target)
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


# Comandos directos — ahora muestran menús interactivos
async def cmd_clavefiscal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """/clavefiscal - Todo sobre clave fiscal."""
    if context.args:
        texto = "clave fiscal " + " ".join(context.args)
        await _responder_consulta(update, texto)
    else:
        await send_menu(update, "clavefiscal")


async def cmd_monotributo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """/monotributo - Info sobre monotributo."""
    if context.args:
        texto = "monotributo " + " ".join(context.args)
        await _responder_consulta(update, texto)
    else:
        await send_menu(update, "monotributo")


async def cmd_factura(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """/factura - Como facturar electronicamente."""
    if context.args:
        texto = "factura " + " ".join(context.args)
        await _responder_consulta(update, texto)
    else:
        await send_menu(update, "factura")


async def cmd_inpi(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """/inpi - Menu interactivo del INPI."""
    if context.args:
        texto = "inpi " + " ".join(context.args)
        await _responder_consulta(update, texto)
    else:
        await send_menu(update, "inpi")


async def cmd_arca(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """/arca - Menu principal de ARCA."""
    if context.args:
        texto = "arca " + " ".join(context.args)
        await _responder_consulta(update, texto)
    else:
        await send_menu(update, "arca")


async def cmd_tramites(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """/tramites - Trámites disponibles online."""
    await send_topic(update, "arca_tramites")


async def cmd_registrar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """/registrar - Como registrar una marca."""
    await send_topic(update, "inpi_registrar")


async def cmd_monotributo_calc(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    /monotributo_calc <facturacion_anual> [servicios|productos]
    Calcula la categoría de monotributo.

    Ejemplos:
        /monotributo_calc 5000000
        /monotributo_calc 15000000 productos
        /monotributo_calc categorias
    """
    if not context.args:
        await update.message.reply_text(
            "Usá: /monotributo_calc <facturación anual> [tipo]\n\n"
            "Ejemplos:\n"
            "  /monotributo_calc 5000000\n"
            "  /monotributo_calc 15000000 productos\n"
            "  /monotributo_calc categorias → ver todas\n\n"
            "Tipo: 'servicios' (default) o 'productos'"
        )
        return

    # Comando especial: mostrar tabla completa
    if context.args[0].lower() in ("categorias", "tabla", "todas"):
        texto = formatear_tabla_categorias()
        await update.message.reply_text(texto)
        return

    # Parsear monto
    monto_str = context.args[0].replace(".", "").replace(",", ".")
    try:
        ingreso_anual = float(monto_str)
    except ValueError:
        await update.message.reply_text(
            "No entendí el monto. Usá números, por ejemplo:\n"
            "  /monotributo_calc 5000000"
        )
        return

    # Parsear tipo
    tipo = "servicios"
    if len(context.args) >= 2 and context.args[1].lower().startswith("prod"):
        tipo = "productos"

    resultado = calcular_categoria(ingreso_anual, tipo)
    texto = formatear_resultado_calculo(ingreso_anual, tipo, resultado)
    await update.message.reply_text(texto)


async def cmd_vencimientos(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    /vencimientos [terminacion_cuit]
    Muestra los próximos vencimientos fiscales.

    Ejemplos:
        /vencimientos        → vencimientos generales
        /vencimientos 3      → para CUIT terminado en 3
    """
    if context.args:
        terminacion = context.args[0]
        if len(terminacion) == 1 and terminacion.isdigit():
            texto = obtener_vencimientos_por_terminacion(terminacion)
        else:
            texto = (
                "Usá la terminación de tu CUIT (un solo dígito).\n"
                "Ejemplo: /vencimientos 3"
            )
    else:
        texto = obtener_vencimientos_generales()

    await update.message.reply_text(texto, disable_web_page_preview=True)


async def cmd_costos(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """/costos_marca - Costos de registrar una marca en INPI."""
    await send_topic(update, "inpi_costos")
