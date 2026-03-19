"""
Handlers informativos: /start, /ayuda, /clase, /clases
"""

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from bot.utils.niza_classes import CLASES_NIZA, obtener_clase, buscar_clases_por_keyword


async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler para /start - muestra menú principal con botones."""
    texto = (
        "Hola! Soy el bot de ARCA/INPI.\n\n"
        "Te ayudo a consultar marcas registradas, datos de CUIT, "
        "calcular monotributo y resolver dudas sobre trámites en ARCA.\n\n"
        "Elegí un tema o usá los comandos de abajo:"
    )

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("INPI (Marcas y Patentes)", callback_data="menu_inpi")],
        [InlineKeyboardButton("Clave Fiscal", callback_data="menu_clavefiscal")],
        [InlineKeyboardButton("ARCA (ex AFIP)", callback_data="menu_arca")],
        [InlineKeyboardButton("Monotributo", callback_data="menu_monotributo")],
        [InlineKeyboardButton("Facturación Electrónica", callback_data="menu_factura")],
        [InlineKeyboardButton("Consultar CUIT", callback_data="tool_cuit")],
        [InlineKeyboardButton("Calculadora Monotributo", callback_data="tool_monotributo_calc")],
        [InlineKeyboardButton("Vencimientos Fiscales", callback_data="tool_vencimientos")],
    ])

    await update.message.reply_text(
        texto,
        reply_markup=keyboard,
    )


async def cmd_ayuda(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler para /ayuda"""
    await update.message.reply_text(
        "Guía del bot ARCA/INPI\n\n"
        "MENÚS INTERACTIVOS:\n"
        "  /inpi → Marcas, patentes, diseños industriales\n"
        "  /clavefiscal → Obtener, recuperar, niveles\n"
        "  /arca → Todo sobre ARCA (ex AFIP)\n"
        "  /monotributo → Inscripción, categorías, facturación\n"
        "  /factura → Facturación electrónica\n\n"
        "BUSCAR MARCAS:\n"
        "  /buscar DAMM → Marcas vigentes que contengan \"DAMM\"\n"
        "  /buscar DAMM 35 → Solo en clase 35\n"
        "  /disponible MiMarca → Disponible? (con análisis fonético)\n"
        "  /buscar_todas DAMM → Incluye no vigentes\n\n"
        "HERRAMIENTAS:\n"
        "  /cuit 20123456789 → Datos públicos de un CUIT\n"
        "  /monotributo_calc 5000000 → Calculadora de categoría\n"
        "  /vencimientos → Próximos vencimientos fiscales\n"
        "  /vencimientos 3 → Para CUIT terminado en 3\n"
        "  /costos_marca → Aranceles del INPI\n"
        "  /checklist registro_marca → Checklist paso a paso\n\n"
        "CLASES NIZA:\n"
        "  /clase 42 → Que cubre la clase 42\n"
        "  /clases software → Clases para tu actividad\n\n"
        "MODO INLINE:\n"
        "  Escribí @arcafaq_bot <consulta> en cualquier chat\n\n"
        "TEXTO LIBRE:\n"
        "  Escribí cualquier pregunta y te respondo.\n\n"
        "Tocá los botones en los mensajes para navegar entre temas.",
        disable_web_page_preview=True,
    )


async def cmd_clase(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    /clase <numero>
    Muestra la descripción de una clase Niza.
    """
    if not context.args or not context.args[0].isdigit():
        await update.message.reply_text(
            "Usá: /clase <numero>\n"
            "Ejemplo: /clase 42\n\n"
            "Las clases van del 1 al 45.\n"
            "Clases 1-34 = productos. Clases 35-45 = servicios."
        )
        return

    numero = int(context.args[0])
    descripcion = obtener_clase(numero)

    if descripcion:
        tipo = "Productos" if numero <= 34 else "Servicios"
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("Registrar una marca", callback_data="inpi_registrar")],
            [InlineKeyboardButton("Ver todas las clases Niza", callback_data="inpi_clases_niza")],
            [InlineKeyboardButton("Menú INPI", callback_data="menu_inpi")],
        ])
        await update.message.reply_text(
            f"Clase {numero} ({tipo}):\n{descripcion}",
            reply_markup=keyboard,
        )
    else:
        await update.message.reply_text(
            f"No existe la clase {numero}. Las clases van del 1 al 45."
        )


async def cmd_clases(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    /clases <palabra>
    Busca clases Niza relacionadas con una actividad.
    """
    if not context.args:
        await update.message.reply_text(
            "Usá: /clases <actividad>\n\n"
            "Ejemplos:\n"
            "  /clases software\n"
            "  /clases restaurant\n"
            "  /clases ropa"
        )
        return

    keyword = " ".join(context.args)
    resultados = buscar_clases_por_keyword(keyword)

    if resultados:
        lines = [f"Clases relacionadas con \"{keyword}\":\n"]
        for num, desc in resultados:
            tipo = "P" if num <= 34 else "S"
            lines.append(f"  [{tipo}] Clase {num}: {desc}")

        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("Registrar una marca", callback_data="inpi_registrar")],
            [InlineKeyboardButton("Costos y aranceles", callback_data="inpi_costos")],
            [InlineKeyboardButton("Menú INPI", callback_data="menu_inpi")],
        ])
        await update.message.reply_text(
            "\n".join(lines),
            reply_markup=keyboard,
        )
    else:
        await update.message.reply_text(
            f"No encontré clases para \"{keyword}\".\n"
            "Probá con otra palabra o usá /clase <numero> para ver una clase específica."
        )
