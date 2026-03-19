"""
Consulta pública del padrón de ARCA (ex AFIP).
Endpoint: GET https://soa.afip.gob.ar/sr-padron/v2/persona/{CUIT}
No requiere autenticación.
"""

import asyncio
import requests
import logging

logger = logging.getLogger(__name__)

PADRON_URL = "https://soa.afip.gob.ar/sr-padron/v2/persona/{cuit}"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; ARCABot/1.0)",
    "Accept": "application/json",
}


class PadronError(Exception):
    """Error al consultar el padrón."""
    pass


def _consultar_cuit_sync(cuit: str) -> dict:
    """Consulta sincrónica al padrón público."""
    try:
        resp = requests.get(
            PADRON_URL.format(cuit=cuit),
            headers=HEADERS,
            timeout=10,
        )

        if resp.status_code == 404:
            raise PadronError(f"No se encontró el CUIT {cuit}.")

        if resp.status_code != 200:
            raise PadronError(f"Error HTTP {resp.status_code} al consultar ARCA.")

        data = resp.json()

        if not data.get("success", True):
            error_msg = data.get("error", {}).get("mensaje", "CUIT no encontrado")
            raise PadronError(error_msg)

        return data.get("data", data)

    except requests.exceptions.Timeout:
        raise PadronError("ARCA no responde. Probá de nuevo en unos minutos.")
    except requests.exceptions.ConnectionError:
        raise PadronError("No se puede conectar a ARCA ahora mismo.")
    except PadronError:
        raise
    except Exception as e:
        logger.error(f"[PADRON] Error inesperado: {type(e).__name__}: {e}")
        raise PadronError(f"Error inesperado: {type(e).__name__}")


async def consultar_cuit(cuit: str) -> dict:
    """Wrapper async."""
    return await asyncio.to_thread(_consultar_cuit_sync, cuit)


def formatear_persona(data: dict) -> str:
    """Formatea los datos del padrón para mostrar en Telegram."""
    tipo = data.get("tipoClave", "")
    tipo_persona = data.get("tipoPersona", "")

    if tipo_persona == "FISICA":
        nombre = f"{data.get('apellido', '')} {data.get('nombre', '')}".strip()
    else:
        nombre = data.get("razonSocial", data.get("nombre", "Sin nombre"))

    cuit = data.get("idPersona", "")
    estado = data.get("estadoClave", "")

    # Domicilio fiscal
    domicilio = data.get("domicilioFiscal", {})
    provincia = domicilio.get("descripcionProvincia", "")
    localidad = domicilio.get("localidad", "")

    # Actividades
    actividades = data.get("actividades", [])
    act_principal = ""
    if actividades:
        act_principal = actividades[0].get("descripcionActividad", "")

    # Impuestos
    impuestos = data.get("impuestos", [])
    imp_nombres = [i.get("descripcionImpuesto", "") for i in impuestos[:5]]

    # Monotributo
    es_monotributo = any("MONOTRIBUTO" in i.get("descripcionImpuesto", "").upper() for i in impuestos)
    categoria = data.get("categoriaMonotributo", {})
    cat_id = categoria.get("idCategoria", "") if categoria else ""

    lines = [f"Datos de CUIT {cuit}:\n"]

    if tipo_persona == "FISICA":
        lines.append(f"  Persona Física")
    else:
        lines.append(f"  Persona Jurídica")

    lines.append(f"  Nombre: {nombre}")
    lines.append(f"  Estado: {estado}")

    if provincia:
        ubicacion = f"{localidad}, {provincia}" if localidad else provincia
        lines.append(f"  Domicilio fiscal: {ubicacion}")

    if act_principal:
        lines.append(f"  Actividad principal: {act_principal}")

    if es_monotributo:
        cat_text = f" (Categoría {cat_id})" if cat_id else ""
        lines.append(f"  Monotributista{cat_text}")

    if imp_nombres:
        lines.append(f"\n  Impuestos inscriptos:")
        for imp in imp_nombres:
            lines.append(f"    - {imp}")
        if len(impuestos) > 5:
            lines.append(f"    ...y {len(impuestos) - 5} más")

    return "\n".join(lines)
