"""
Servicio de monitoreo de marcas.
Chequea periódicamente las vigilancias activas y notifica cambios.
"""

import logging
from telegram.ext import ContextTypes

from bot.db import obtener_todas_vigilancias, actualizar_vigilancia
from bot.scrapers.inpi_marcas import buscar_marcas, INPIError

logger = logging.getLogger(__name__)


async def chequear_vigilancias(context: ContextTypes.DEFAULT_TYPE):
    """
    Job que se ejecuta periódicamente para chequear vigilancias.
    Registrar con: job_queue.run_repeating(chequear_vigilancias, interval=21600)
    """
    try:
        vigilancias = await obtener_todas_vigilancias()
    except Exception as e:
        logger.error(f"[MONITOR] Error obteniendo vigilancias: {e}")
        return

    if not vigilancias:
        return

    logger.info(f"[MONITOR] Chequeando {len(vigilancias)} vigilancias...")

    for vig in vigilancias:
        try:
            clase = vig["clase"] if vig["clase"] != -1 else None
            resultados = await buscar_marcas(
                denominacion=vig["denominacion"],
                clase=clase,
                solo_vigentes=True,
                tipo_busqueda=1,
            )

            count_actual = len(resultados)
            count_anterior = vig["last_count"]

            # Actualizar siempre
            await actualizar_vigilancia(vig["id"], count_actual)

            # Notificar solo si hay cambios (y no es el primer chequeo)
            if count_anterior > 0 and count_actual != count_anterior:
                diff = count_actual - count_anterior
                clase_txt = f" (clase {vig['clase']})" if vig["clase"] != -1 else ""

                if diff > 0:
                    texto = (
                        f"⚠️ Alerta de vigilancia: \"{vig['denominacion']}\"{clase_txt}\n\n"
                        f"Se encontraron {diff} marca(s) nueva(s) "
                        f"(antes: {count_anterior}, ahora: {count_actual}).\n\n"
                        f"Usá /buscar {vig['denominacion']} para ver los detalles."
                    )
                else:
                    texto = (
                        f"ℹ️ Vigilancia: \"{vig['denominacion']}\"{clase_txt}\n\n"
                        f"Hubo cambios en los resultados "
                        f"(antes: {count_anterior}, ahora: {count_actual})."
                    )

                try:
                    await context.bot.send_message(
                        chat_id=vig["telegram_id"],
                        text=texto,
                    )
                except Exception as e:
                    logger.error(f"[MONITOR] Error enviando notificación a {vig['telegram_id']}: {e}")

        except INPIError as e:
            logger.warning(f"[MONITOR] Error INPI para '{vig['denominacion']}': {e}")
        except Exception as e:
            logger.error(f"[MONITOR] Error procesando vigilancia {vig['id']}: {e}")
