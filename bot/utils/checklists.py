"""
Checklists interactivos para trámites de ARCA/INPI.
Cada checklist es una lista de pasos que el usuario puede ir tildando.
"""

CHECKLISTS = {
    "registro_marca": {
        "titulo": "Checklist: Registrar una Marca",
        "pasos": [
            "Elegir el nombre de la marca",
            "Verificar disponibilidad (/disponible <nombre>)",
            "Identificar la clase Niza correcta (/clases <actividad>)",
            "Tener CUIT activo",
            "Tener Clave Fiscal nivel 2+",
            "Adherir servicio INPI en ARCA",
            "Completar perfil en portaltramites.inpi.gob.ar",
            "Preparar logo (si es marca mixta o figurativa)",
            "Completar solicitud en el portal INPI",
            "Pagar arancel (se paga por clase)",
            "Anotar número de acta para seguimiento",
        ],
        "link": "https://www.argentina.gob.ar/inpi/marcas/registrar-una-marca",
        "notas": "Tiempo estimado: 12-24 meses. Vigencia: 10 años renovables.",
    },
    "clave_fiscal": {
        "titulo": "Checklist: Obtener Clave Fiscal",
        "pasos": [
            "Tener DNI tarjeta vigente",
            "Descargar la app ARCA (Play Store / App Store)",
            "Abrir la app > Herramientas > Solicitud de Clave Fiscal",
            "Escanear DNI (frente y dorso)",
            "Sacarse selfie para validación biométrica",
            "Elegir contraseña segura",
            "Verificar acceso en www.arca.gob.ar",
        ],
        "link": "https://www.argentina.gob.ar/servicio/obtener-la-clave-fiscal",
        "notas": "Por la app obtenés nivel 3 directamente.",
    },
    "monotributo_alta": {
        "titulo": "Checklist: Inscribirse en Monotributo",
        "pasos": [
            "Tener CUIT activo",
            "Tener Clave Fiscal nivel 2+",
            "Adherir servicio 'Monotributo' en ARCA",
            "Determinar categoría según ingresos (/monotributo_calc)",
            "Ingresar a ARCA > Monotributo > Alta",
            "Completar actividad económica",
            "Elegir obra social",
            "Confirmar inscripción",
            "Dar de alta punto de venta para facturar",
            "Configurar medio de pago (débito automático recomendado)",
        ],
        "link": "https://www.afip.gob.ar/monotributo/",
        "notas": "La cuota vence el 20 de cada mes.",
    },
    "facturacion": {
        "titulo": "Checklist: Empezar a Facturar",
        "pasos": [
            "Tener CUIT + Clave Fiscal",
            "Estar inscripto (monotributo o resp. inscripto)",
            "Adherir servicio 'Comprobantes en Línea' en ARCA",
            "Dar de alta punto de venta en ARCA",
            "Ingresar a facturador.afip.gob.ar",
            "Emitir primera factura de prueba",
        ],
        "link": "https://www.afip.gob.ar/facturacion/",
        "notas": "Monotributistas emiten Factura C. Resp. Inscriptos emiten A o B.",
    },
    "adherir_inpi": {
        "titulo": "Checklist: Adherir servicio INPI en ARCA",
        "pasos": [
            "Tener CUIT + Clave Fiscal nivel 2+",
            "Ingresar a www.arca.gob.ar con clave fiscal",
            "Ir a 'Administrador de Relaciones de Clave Fiscal'",
            "Click en 'Adherir Servicio'",
            "Buscar 'Instituto Nacional de la Propiedad Industrial'",
            "Seleccionar y confirmar",
            "Ingresar a portaltramites.inpi.gob.ar",
            "Completar perfil (nombre, domicilio, tipo usuario)",
        ],
        "link": "https://portaltramites.inpi.gob.ar",
        "notas": "Una vez adherido, ya podés operar en el INPI online.",
    },
}


def obtener_checklist(checklist_id: str) -> dict | None:
    """Retorna un checklist por su ID."""
    return CHECKLISTS.get(checklist_id)


def listar_checklists() -> str:
    """Lista todos los checklists disponibles."""
    lines = ["Checklists disponibles:\n"]
    for cid, data in CHECKLISTS.items():
        lines.append(f"  /checklist {cid}")
        lines.append(f"    {data['titulo']}\n")
    return "\n".join(lines)


def formatear_checklist(checklist: dict) -> str:
    """Formatea un checklist para Telegram (texto plano con checkboxes)."""
    lines = [f"{checklist['titulo']}:\n"]

    for i, paso in enumerate(checklist["pasos"], 1):
        lines.append(f"  {i}. {paso}")

    if checklist.get("notas"):
        lines.append(f"\n{checklist['notas']}")

    if checklist.get("link"):
        lines.append(f"\nMás info: {checklist['link']}")

    return "\n".join(lines)
