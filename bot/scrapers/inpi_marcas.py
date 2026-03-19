"""
Scraper para el buscador público de marcas del INPI Argentina.
Endpoint: POST https://portaltramites.inpi.gob.ar/MarcasConsultas/Grilla

Usa requests (sync) + asyncio.to_thread para no bloquear el bot.
requests es más compatible con sitios .gob.ar que httpx.
"""

import asyncio
import requests
from typing import Optional
import logging

from bot.scrapers.parser import MarcaResult, parsear_resultados

logger = logging.getLogger(__name__)

INPI_BASE_URL = "https://portaltramites.inpi.gob.ar"
INPI_SEARCH_PAGE = f"{INPI_BASE_URL}/marcasconsultas/busqueda"
INPI_SEARCH_URL = f"{INPI_BASE_URL}/MarcasConsultas/Grilla"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "es-AR,es;q=0.9,en;q=0.8",
}


class INPIError(Exception):
    """Error al comunicarse con el INPI."""
    pass


def _buscar_marcas_sync(
    denominacion: str,
    clase: Optional[int] = None,
    solo_vigentes: bool = True,
    tipo_busqueda: int = 1,
    tipo_resolucion: str = "",
) -> list[MarcaResult]:
    """Búsqueda sincrónica (se corre en un thread aparte)."""
    form_data = {
        "tipob": "1",
        "CboTipo": tipo_resolucion,
        "clase": str(clase) if clase else "-1",
        "TxtDenominacionTipoBusqueda": str(tipo_busqueda),
        "Denominacion": denominacion.upper(),
        "TxtTitularTipoBusqueda": "0",
        "Titular": "",
        "FechaIngresoDesde": "",
        "FechaIngresoHasta": "",
        "FechaResolucionDesde": "",
        "FechaResolucionHasta": "",
        "BtnBuscarAvanzada": "BUSCAR",
    }

    if solo_vigentes:
        form_data["SoloVigentes"] = "on"

    session = requests.Session()
    session.headers.update(HEADERS)

    try:
        # Paso 1: GET la página para obtener cookies de sesión
        logger.info(f"[INPI] GET {INPI_SEARCH_PAGE}")
        get_resp = session.get(INPI_SEARCH_PAGE, timeout=15, verify=True)
        logger.info(f"[INPI] GET status: {get_resp.status_code}, cookies: {len(session.cookies)}")

        # Paso 2: POST la búsqueda con las cookies
        logger.info(f"[INPI] POST buscando '{denominacion}'")
        post_resp = session.post(
            INPI_SEARCH_URL,
            data=form_data,
            headers={
                "Referer": INPI_SEARCH_PAGE,
                "Origin": INPI_BASE_URL,
            },
            timeout=20,
            verify=True,
        )
        logger.info(f"[INPI] POST status: {post_resp.status_code}, len: {len(post_resp.text)}")

        if post_resp.status_code != 200:
            raise INPIError(f"El INPI devolvió error HTTP {post_resp.status_code}")

        if "auth.afip" in post_resp.url:
            raise INPIError("El INPI redirigió al login. Probá de nuevo.")

        html = post_resp.text

    except requests.exceptions.Timeout:
        logger.error("[INPI] Timeout")
        raise INPIError("El INPI no responde. Probá de nuevo en unos minutos.")
    except requests.exceptions.SSLError as e:
        logger.error(f"[INPI] Error SSL: {e}")
        # Reintentar sin verificar SSL
        try:
            logger.info("[INPI] Reintentando sin SSL verify...")
            get_resp = session.get(INPI_SEARCH_PAGE, timeout=15, verify=False)
            post_resp = session.post(
                INPI_SEARCH_URL,
                data=form_data,
                headers={"Referer": INPI_SEARCH_PAGE, "Origin": INPI_BASE_URL},
                timeout=20,
                verify=False,
            )
            html = post_resp.text
        except Exception as e2:
            logger.error(f"[INPI] Falló también sin SSL: {e2}")
            raise INPIError("No se puede conectar al INPI (error SSL).")
    except requests.exceptions.ConnectionError as e:
        logger.error(f"[INPI] Error de conexión: {e}")
        raise INPIError("No se puede conectar al INPI ahora mismo.")
    except INPIError:
        raise
    except Exception as e:
        logger.error(f"[INPI] Error inesperado: {type(e).__name__}: {e}")
        raise INPIError(f"Error inesperado: {type(e).__name__}")

    resultados = parsear_resultados(html)
    logger.info(f"[INPI] Encontradas {len(resultados)} marcas")
    return resultados


async def buscar_marcas(
    denominacion: str,
    clase: Optional[int] = None,
    solo_vigentes: bool = True,
    tipo_busqueda: int = 1,
    tipo_resolucion: str = "",
) -> list[MarcaResult]:
    """Wrapper async que corre la búsqueda sync en un thread."""
    return await asyncio.to_thread(
        _buscar_marcas_sync,
        denominacion, clase, solo_vigentes, tipo_busqueda, tipo_resolucion,
    )


async def verificar_disponibilidad(
    nombre: str, clase: Optional[int] = None
) -> dict:
    """Verifica si un nombre de marca podría estar disponible."""
    similares = await buscar_marcas(
        denominacion=nombre,
        clase=clase,
        solo_vigentes=True,
        tipo_busqueda=1,
    )

    nombre_upper = nombre.upper().strip()
    exactas = [m for m in similares if m.denominacion.strip() == nombre_upper]
    parciales = [m for m in similares if m.denominacion.strip() != nombre_upper]

    return {
        "disponible": len(exactas) == 0,
        "exactas": exactas,
        "similares": parciales,
        "disclaimer": (
            "Esta búsqueda es orientativa. No reemplaza una búsqueda "
            "fonética profesional. El INPI puede denegar marcas por "
            "similitud fonética aunque el nombre exacto no esté registrado."
        ),
    }
