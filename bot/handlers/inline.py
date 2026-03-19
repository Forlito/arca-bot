"""
Handler para modo inline de Telegram.
Permite usar @arcafaq_bot <consulta> desde cualquier chat.
"""

import logging
from uuid import uuid4

from telegram import Update, InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import ContextTypes

from bot.knowledge import buscar_respuesta, get_topic, get_menu, KEYWORD_MAP
from bot.utils.niza_classes import buscar_clases_por_keyword, obtener_clase

logger = logging.getLogger(__name__)

# Resultados por defecto cuando no hay query
DEFAULT_RESULTS = [
    InlineQueryResultArticle(
        id="help_marcas",
        title="Buscar marcas",
        description="Usá /buscar <nombre> en el chat directo con el bot",
        input_message_content=InputTextMessageContent(
            "Para buscar marcas, hablame directo: @arcafaq_bot\n"
            "Y usá /buscar <nombre>"
        ),
    ),
    InlineQueryResultArticle(
        id="help_clave",
        title="Clave Fiscal",
        description="Info sobre cómo obtener y usar la clave fiscal",
        input_message_content=InputTextMessageContent(
            "Clave Fiscal: es tu contraseña para operar en ARCA (ex AFIP). "
            "Obtenerla por la app ARCA es lo más rápido (te da nivel 3). "
            "Más info: https://www.afip.gob.ar/clavefiscal/"
        ),
    ),
    InlineQueryResultArticle(
        id="help_monotributo",
        title="Monotributo",
        description="Info sobre el régimen simplificado",
        input_message_content=InputTextMessageContent(
            "Monotributo: régimen simplificado para pequeños contribuyentes. "
            "Unifica impuesto + jubilación + obra social en una cuota mensual. "
            "Más info: https://www.afip.gob.ar/monotributo/"
        ),
    ),
]


async def handle_inline_query(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler para InlineQuery (@arcafaq_bot <consulta>)."""
    query = update.inline_query.query.strip()

    if not query:
        await update.inline_query.answer(DEFAULT_RESULTS, cache_time=300)
        return

    results = []

    # Buscar en clases Niza
    clases = buscar_clases_por_keyword(query)
    if clases:
        for num, desc in clases[:3]:
            tipo = "Productos" if num <= 34 else "Servicios"
            results.append(InlineQueryResultArticle(
                id=f"clase_{num}",
                title=f"Clase {num} ({tipo})",
                description=desc[:100],
                input_message_content=InputTextMessageContent(
                    f"Clase Niza {num} ({tipo}):\n{desc}"
                ),
            ))

    # Buscar en knowledge base
    entry = buscar_respuesta(query)
    if entry:
        target = entry["target"]

        if target.startswith("menu_"):
            menu = get_menu(target[5:])
            if menu:
                results.append(InlineQueryResultArticle(
                    id=f"menu_{target}",
                    title=target[5:].upper().replace("_", " "),
                    description=menu["texto"][:100],
                    input_message_content=InputTextMessageContent(
                        menu["texto"]
                    ),
                ))
        else:
            topic = get_topic(target)
            if topic:
                texto = topic["texto"]
                link = topic.get("link", "")
                if link:
                    texto += f"\n\nMás info: {link}"
                results.append(InlineQueryResultArticle(
                    id=f"topic_{target}",
                    title=_titulo_legible(target),
                    description=topic["texto"][:100],
                    input_message_content=InputTextMessageContent(texto),
                ))

    if not results:
        results.append(InlineQueryResultArticle(
            id="no_result",
            title="No encontré resultados",
            description=f"Probá con otras palabras clave",
            input_message_content=InputTextMessageContent(
                f"No encontré resultados para '{query}'. "
                "Probá hablándome directo: @arcafaq_bot"
            ),
        ))

    await update.inline_query.answer(results[:10], cache_time=60)


def _titulo_legible(target: str) -> str:
    """Convierte un target ID a título legible."""
    reemplazos = {
        "cf_": "Clave Fiscal: ",
        "inpi_": "INPI: ",
        "arca_": "ARCA: ",
        "mono_": "Monotributo: ",
        "fact_": "Facturación: ",
    }
    for prefijo, titulo in reemplazos.items():
        if target.startswith(prefijo):
            return titulo + target[len(prefijo):].replace("_", " ").capitalize()
    return target.replace("_", " ").capitalize()
