"""
Handlers para búsqueda de marcas en el INPI y consulta de CUIT.
Comandos: /buscar, /disponible, /cuit
"""

import logging
from telegram import Update
from telegram.ext import ContextTypes

from bot.scrapers.inpi_marcas import buscar_marcas, verificar_disponibilidad, INPIError
from bot.scrapers.arca_padron import consultar_cuit, formatear_persona, PadronError
from bot.utils.formatter import formatear_resultados, formatear_disponibilidad
from bot.utils.validators import validar_cuit, formatear_cuit
from bot.utils.fonetica import encontrar_similares_foneticos

logger = logging.getLogger(__name__)


async def cmd_buscar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    /buscar <nombre> [clase]
    Busca marcas registradas que contengan el nombre.
    Opcionalmente filtra por clase Niza.

    Ejemplos:
        /buscar DAMM
        /buscar DAMM 35
    """
    if not context.args:
        await update.message.reply_text(
            "Usá: /buscar <nombre> [clase]\n\n"
            "Ejemplos:\n"
            "  /buscar DAMM\n"
            "  /buscar DAMM 35\n"
            "  /buscar COCA COLA 32"
        )
        return

    # Parsear argumentos: el último puede ser un número de clase
    args = context.args
    clase = None

    if len(args) >= 2 and args[-1].isdigit():
        posible_clase = int(args[-1])
        if 1 <= posible_clase <= 45:
            clase = posible_clase
            args = args[:-1]

    nombre = " ".join(args).strip()
    if not nombre:
        await update.message.reply_text("Tenés que poner un nombre para buscar.")
        return

    # Feedback inmediato
    msg = await update.message.reply_text(f"🔍 Buscando \"{nombre}\" en el INPI...")

    try:
        resultados = await buscar_marcas(
            denominacion=nombre,
            clase=clase,
            solo_vigentes=True,
            tipo_busqueda=1,  # contiene
        )

        texto = formatear_resultados(
            query=nombre,
            resultados=resultados,
            solo_vigentes=True,
        )

        await msg.edit_text(texto, parse_mode="MarkdownV2")

    except INPIError as e:
        await msg.edit_text(f"⚠️ {str(e)}")
    except Exception as e:
        logger.error(f"Error en /buscar: {e}", exc_info=True)
        await msg.edit_text(
            "❌ Algo falló al buscar. El INPI puede estar caído. "
            "Intentá de nuevo en unos minutos."
        )


async def cmd_disponible(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    /disponible <nombre> [clase]
    Verifica si un nombre de marca podría estar disponible.

    Ejemplos:
        /disponible MiMarca
        /disponible MiMarca 42
    """
    if not context.args:
        await update.message.reply_text(
            "Usá: /disponible <nombre> [clase]\n\n"
            "Ejemplos:\n"
            "  /disponible MiStartup\n"
            "  /disponible MiStartup 42"
        )
        return

    args = context.args
    clase = None

    if len(args) >= 2 and args[-1].isdigit():
        posible_clase = int(args[-1])
        if 1 <= posible_clase <= 45:
            clase = posible_clase
            args = args[:-1]

    nombre = " ".join(args).strip()
    if not nombre:
        await update.message.reply_text("Tenés que poner un nombre para verificar.")
        return

    msg = await update.message.reply_text(f"🔍 Verificando disponibilidad de \"{nombre}\"...")

    try:
        resultado = await verificar_disponibilidad(nombre=nombre, clase=clase)

        # Agregar análisis fonético
        todas = resultado["exactas"] + resultado["similares"]
        foneticos = encontrar_similares_foneticos(nombre, todas, umbral=0.7)
        resultado["foneticos"] = foneticos

        texto = formatear_disponibilidad(nombre, resultado)
        await msg.edit_text(texto, parse_mode="MarkdownV2")

    except INPIError as e:
        await msg.edit_text(f"⚠️ {str(e)}")
    except Exception as e:
        logger.error(f"Error en /disponible: {e}", exc_info=True)
        await msg.edit_text(
            "❌ Algo falló al verificar. El INPI puede estar caído. "
            "Intentá de nuevo en unos minutos."
        )


async def cmd_buscar_todas(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    /buscar_todas <nombre> [clase]
    Busca todas las marcas (incluyendo no vigentes).
    """
    if not context.args:
        await update.message.reply_text(
            "Usá: /buscar_todas <nombre> [clase]\n"
            "Igual que /buscar pero incluye marcas vencidas, abandonadas, etc."
        )
        return

    args = context.args
    clase = None

    if len(args) >= 2 and args[-1].isdigit():
        posible_clase = int(args[-1])
        if 1 <= posible_clase <= 45:
            clase = posible_clase
            args = args[:-1]

    nombre = " ".join(args).strip()
    msg = await update.message.reply_text(f"🔍 Buscando \"{nombre}\" (todas, incluso no vigentes)...")

    try:
        resultados = await buscar_marcas(
            denominacion=nombre,
            clase=clase,
            solo_vigentes=False,
            tipo_busqueda=1,
        )

        texto = formatear_resultados(
            query=nombre,
            resultados=resultados,
            solo_vigentes=False,
        )

        await msg.edit_text(texto, parse_mode="MarkdownV2")

    except INPIError as e:
        await msg.edit_text(f"⚠️ {str(e)}")
    except Exception as e:
        logger.error(f"Error en /buscar_todas: {e}", exc_info=True)
        await msg.edit_text("❌ Algo falló. Intentá de nuevo en unos minutos.")


async def cmd_cuit(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    /cuit <numero>
    Consulta datos públicos de un CUIT en ARCA.

    Ejemplos:
        /cuit 20-12345678-9
        /cuit 20123456789
    """
    if not context.args:
        await update.message.reply_text(
            "Usá: /cuit <numero>\n\n"
            "Ejemplos:\n"
            "  /cuit 20-12345678-9\n"
            "  /cuit 20123456789\n\n"
            "Consulta datos públicos del padrón de ARCA."
        )
        return

    cuit_input = "".join(context.args)
    es_valido, resultado = validar_cuit(cuit_input)

    if not es_valido:
        await update.message.reply_text(f"⚠️ {resultado}")
        return

    cuit_limpio = resultado
    cuit_formateado = formatear_cuit(cuit_limpio)
    msg = await update.message.reply_text(f"🔍 Consultando CUIT {cuit_formateado}...")

    try:
        data = await consultar_cuit(cuit_limpio)
        texto = formatear_persona(data)
        await msg.edit_text(texto)
    except PadronError as e:
        await msg.edit_text(f"⚠️ {str(e)}")
    except Exception as e:
        logger.error(f"Error en /cuit: {e}", exc_info=True)
        await msg.edit_text("❌ Algo falló al consultar ARCA. Probá de nuevo.")
