"""
Handlers informativos: /start, /ayuda, /clase, /clases
"""

from telegram import Update
from telegram.ext import ContextTypes

from bot.utils.niza_classes import CLASES_NIZA, obtener_clase, buscar_clases_por_keyword


async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler para /start"""
    await update.message.reply_text(
        "Hola! Soy el bot de ARCA/INPI.\n\n"
        "Te ayudo a consultar marcas registradas en Argentina "
        "y a resolver dudas sobre trámites en ARCA.\n\n"
        "MARCAS:\n"
        "  /buscar <nombre> - Buscar marcas vigentes\n"
        "  /disponible <nombre> - Verificar disponibilidad\n"
        "  /registrar - Como registrar una marca\n"
        "  /clase <numero> - Info sobre una clase Niza\n"
        "  /clases <actividad> - Buscar clases por rubro\n\n"
        "ARCA / TRÁMITES:\n"
        "  /clavefiscal - Como obtener o recuperar tu clave\n"
        "  /inpi - Que es el INPI y como acceder\n"
        "  /monotributo - Info sobre monotributo\n"
        "  /factura - Como facturar electrónicamente\n"
        "  /tramites - Trámites disponibles online\n\n"
        "También podés escribir cualquier pregunta directamente "
        "y te respondo lo mejor que pueda.\n\n"
        "Ejemplo: \"como saco la clave fiscal?\""
    )


async def cmd_ayuda(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler para /ayuda"""
    await update.message.reply_text(
        "Guía del bot ARCA/INPI\n\n"
        "BUSCAR MARCAS:\n"
        "  /buscar DAMM --> marcas vigentes que contengan \"DAMM\"\n"
        "  /buscar DAMM 35 --> solo en clase 35\n"
        "  /disponible MiMarca --> nombre exacto disponible?\n"
        "  /disponible MiMarca 42 --> solo en clase 42\n"
        "  /buscar_todas DAMM --> incluye no vigentes\n\n"
        "CLASES NIZA (clasificación de marcas):\n"
        "  /clase 42 --> que cubre la clase 42\n"
        "  /clases software --> clases relacionadas con software\n\n"
        "CONSULTAS ARCA:\n"
        "  /clavefiscal --> como obtener/recuperar\n"
        "  /clavefiscal recuperar --> recuperar clave olvidada\n"
        "  /clavefiscal niveles --> niveles de seguridad\n"
        "  /inpi --> que es y como acceder al INPI\n"
        "  /registrar --> paso a paso para registrar marca\n"
        "  /monotributo --> info monotributo\n"
        "  /factura --> como facturar\n"
        "  /tramites --> tramites disponibles online\n\n"
        "TEXTO LIBRE:\n"
        "  Escribí cualquier pregunta y te respondo.\n"
        "  Ej: \"como adhiero un servicio en arca?\"\n"
        "  Ej: \"que necesito para registrar una marca?\"\n\n"
        "Si no tengo la respuesta, te mando el link oficial donde encontrarla.",
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
        await update.message.reply_text(
            f"Clase {numero} ({tipo}):\n{descripcion}"
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
        await update.message.reply_text("\n".join(lines))
    else:
        await update.message.reply_text(
            f"No encontré clases para \"{keyword}\".\n"
            "Probá con otra palabra o usá /clase <numero> para ver una clase específica."
        )
