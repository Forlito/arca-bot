"""
Base de conocimiento del bot ARCA/INPI.
Cada entrada tiene: keywords (para matching), respuesta, y link de referencia.
"""

# Cada tema tiene:
# - keywords: lista de palabras que activan esta respuesta
# - respuesta: texto de respuesta (profesional simple, sin jerga innecesaria)
# - link: URL de referencia oficial
# - comando: comando asociado (si tiene)

KNOWLEDGE_BASE = [
    # ===== CLAVE FISCAL =====
    {
        "id": "clave_fiscal_que_es",
        "keywords": ["clave fiscal", "que es clave fiscal", "clave fiscal que es", "contraseña arca", "password arca"],
        "respuesta": (
            "La Clave Fiscal es tu contraseña para operar en ARCA (ex AFIP). "
            "Te permite hacer trámites online: facturar, pagar impuestos, inscribirte en monotributo, "
            "adherir servicios como INPI, y más.\n\n"
            "Tiene niveles de seguridad (2, 3 y 4). Cuanto más alto el nivel, más trámites podés hacer.\n\n"
            "Para la mayoría de los trámites necesitás nivel 2 o 3."
        ),
        "link": "https://www.afip.gob.ar/clavefiscal/",
    },
    {
        "id": "clave_fiscal_obtener",
        "keywords": ["obtener clave fiscal", "sacar clave fiscal", "como saco la clave", "crear clave fiscal",
                     "clave fiscal nueva", "registrarme en arca", "como me registro", "no tengo clave fiscal",
                     "necesito clave fiscal", "quiero clave fiscal"],
        "respuesta": (
            "Hay 3 formas de obtener tu Clave Fiscal:\n\n"
            "1. Por la app ARCA (la más rápida)\n"
            "   Descargá la app ARCA, andá a Herramientas > Solicitud de clave fiscal. "
            "Escaneá tu DNI tarjeta y sacate una foto. Te da nivel 3.\n\n"
            "2. Por homebanking\n"
            "   Si tenés cuenta bancaria, desde tu homebanking podés generar clave fiscal nivel 2.\n\n"
            "3. Presencial en ARCA\n"
            "   Sacá turno web, andá con DNI a una dependencia de ARCA. Te registran datos biométricos (foto, firma, huella). Te da nivel 3.\n\n"
            "Requisitos: DNI argentino en formato tarjeta y ser mayor de edad."
        ),
        "link": "https://www.argentina.gob.ar/servicio/obtener-la-clave-fiscal",
    },
    {
        "id": "clave_fiscal_niveles",
        "keywords": ["nivel clave fiscal", "niveles de seguridad", "nivel 2", "nivel 3", "nivel 4",
                     "que nivel necesito", "diferencia niveles", "subir nivel"],
        "respuesta": (
            "Los niveles de Clave Fiscal determinan qué trámites podés hacer:\n\n"
            "Nivel 2: Lo básico. Alta de servicios para vos mismo. Se obtiene por homebanking.\n\n"
            "Nivel 3: El más usado. Podés adherir servicios, delegar a terceros, hacer casi todo. "
            "Se obtiene por la app ARCA o presencial.\n\n"
            "Nivel 4: Máxima seguridad. Requiere doble autenticación (token). "
            "Necesitás tener nivel 3 primero y tramitarlo presencial con turno.\n\n"
            "Para INPI y la mayoría de trámites, nivel 2 alcanza."
        ),
        "link": "https://www.afip.gob.ar/clavefiscal/ayuda/obtener-clave-fiscal.asp",
    },
    {
        "id": "clave_fiscal_recuperar",
        "keywords": ["recuperar clave fiscal", "olvide clave fiscal", "no me acuerdo la clave",
                     "blanquear clave", "resetear clave", "clave bloqueada", "me bloquee"],
        "respuesta": (
            "Si olvidaste tu Clave Fiscal podés recuperarla de 3 formas:\n\n"
            "1. Desde la app ARCA: Herramientas > Recupero de clave fiscal. Escaneá DNI y sacate selfie.\n\n"
            "2. Por homebanking: Tu banco te permite regenerarla.\n\n"
            "3. Presencial: Sacá turno web y andá a una dependencia de ARCA con tu DNI.\n\n"
            "Si te bloquearon la clave por intentos fallidos, esperá 30 minutos o hacé el recupero."
        ),
        "link": "https://www.afip.gob.ar/clavefiscal/ayuda/recupera-clave-fiscal.asp",
    },
    # ===== SERVICIOS / ADHERIR =====
    {
        "id": "adherir_servicio",
        "keywords": ["adherir servicio", "agregar servicio", "habilitar servicio", "activar servicio",
                     "como adhiero", "adherir inpi", "agregar inpi", "sumar servicio"],
        "respuesta": (
            "Para adherir un servicio (como INPI, Monotributo, etc.):\n\n"
            "1. Ingresá a www.arca.gob.ar con tu CUIT y clave fiscal\n"
            "2. Andá a \"Administrador de Relaciones de Clave Fiscal\" (en Servicios Administrativos)\n"
            "3. Hacé click en \"Adherir Servicio\"\n"
            "4. Buscá el organismo (ej: Instituto Nacional de la Propiedad Industrial para INPI)\n"
            "5. Confirmá\n\n"
            "Con nivel 2 podés adherir servicios para vos mismo. "
            "Para delegar a terceros necesitás nivel 3."
        ),
        "link": "https://servicioscf.afip.gob.ar/publico/abc/ABCpaso2.aspx?cat=2949",
    },
    {
        "id": "delegar_servicio",
        "keywords": ["delegar servicio", "delegar clave fiscal", "dar acceso a otro", "compartir acceso",
                     "contador acceso", "que otro opere", "usuario externo"],
        "respuesta": (
            "Para delegar un servicio a otra persona (ej: tu contador):\n\n"
            "1. Ingresá a ARCA con tu clave fiscal (necesitás nivel 3)\n"
            "2. Andá a \"Administrador de Relaciones de Clave Fiscal\"\n"
            "3. Elegí \"Nueva Relación\" (NO \"Adherir Servicio\")\n"
            "4. En \"Representado\" elegí tu CUIT\n"
            "5. Elegí el servicio a delegar\n"
            "6. En \"Representante\" poné el CUIT de la persona que va a operar\n"
            "7. Confirmá\n\n"
            "La persona delegada tiene que aceptar desde \"Aceptación de Designación\" con su propia clave fiscal."
        ),
        "link": "https://servicioscf.afip.gob.ar/publico/abc/ABCpaso2.aspx?cat=2949",
    },
    # ===== INPI / MARCAS =====
    {
        "id": "inpi_que_es",
        "keywords": ["que es inpi", "inpi que es", "registro de marcas", "propiedad industrial",
                     "para que sirve inpi", "marcas argentina"],
        "respuesta": (
            "El INPI (Instituto Nacional de la Propiedad Industrial) es el organismo argentino "
            "donde registrás marcas, patentes y modelos industriales.\n\n"
            "Lo que podés hacer en el INPI:\n"
            "- Registrar una marca (nombre, logo, o ambos)\n"
            "- Consultar marcas ya registradas\n"
            "- Renovar marcas existentes\n"
            "- Registrar patentes de invención\n"
            "- Registrar modelos de utilidad\n"
            "- Registrar diseños industriales\n"
            "- Transferir tecnología\n\n"
            "Para operar online necesitás clave fiscal y adherir el servicio INPI en ARCA."
        ),
        "link": "https://www.argentina.gob.ar/inpi",
    },
    {
        "id": "registrar_marca",
        "keywords": ["registrar marca", "como registro marca", "registro de marca", "quiero registrar",
                     "sacar marca", "patentar marca", "patentar nombre", "proteger marca",
                     "inscribir marca", "marca comercial"],
        "respuesta": (
            "Para registrar una marca en Argentina:\n\n"
            "1. Buscá si el nombre está disponible (usá /disponible <nombre> en este bot)\n"
            "2. Elegí la clase Niza correcta para tu actividad (usá /clases <actividad>)\n"
            "3. Ingresá a portaltramites.inpi.gob.ar con tu clave fiscal\n"
            "4. Completá el formulario de solicitud de marca\n"
            "5. Pagá el arancel (consultá montos actualizados en el portal)\n"
            "6. Hacé seguimiento del trámite con tu número de acta\n\n"
            "Tiempos: 12 meses (trámite simplificado) a 24 meses (trámite completo).\n\n"
            "Requisitos: CUIT/CUIL + Clave Fiscal nivel 2+ + servicio INPI adherido en ARCA."
        ),
        "link": "https://www.argentina.gob.ar/inpi/marcas/registrar-una-marca",
    },
    {
        "id": "inpi_adherir",
        "keywords": ["adherir inpi", "activar inpi", "habilitar inpi", "inpi arca", "inpi clave fiscal",
                     "como entro al inpi", "acceder inpi", "registrarme inpi"],
        "respuesta": (
            "Para acceder al portal de trámites del INPI:\n\n"
            "1. Necesitás tener clave fiscal nivel 2 o superior\n"
            "2. Ingresá a www.arca.gob.ar con tu CUIT y clave fiscal\n"
            "3. Andá a \"Administrador de Relaciones de Clave Fiscal\"\n"
            "4. Click en \"Adherir Servicio\"\n"
            "5. Buscá y seleccioná \"Instituto Nacional de la Propiedad Industrial\"\n"
            "6. Confirmá\n"
            "7. Ahora ingresá a portaltramites.inpi.gob.ar con tu clave fiscal\n"
            "8. Completá tus datos personales (nombre, domicilio, tipo de usuario: particular o agente)\n\n"
            "Listo, ya podés operar en el INPI online."
        ),
        "link": "https://www.argentina.gob.ar/inpi",
    },
    {
        "id": "marca_costo",
        "keywords": ["cuanto cuesta marca", "costo marca", "precio marca", "arancel marca",
                     "cuanto sale registrar", "tasa inpi", "cuanto cobran"],
        "respuesta": (
            "Los aranceles del INPI se actualizan periódicamente. "
            "Para consultar los montos vigentes, ingresá al portal del INPI.\n\n"
            "Ten en cuenta que el pago es por clase Niza. Si querés registrar la marca en varias clases, "
            "pagás por cada una."
        ),
        "link": "https://www.argentina.gob.ar/inpi/aranceles",
    },
    {
        "id": "seguir_tramite",
        "keywords": ["seguir tramite", "estado tramite", "como va mi tramite", "seguimiento",
                     "numero de acta", "consultar tramite", "ver tramite"],
        "respuesta": (
            "Para ver el estado de tu trámite de marca:\n\n"
            "1. Ingresá a portaltramites.inpi.gob.ar/marcasconsultas/busqueda\n"
            "2. En \"Seguimiento de Trámite\" poné tu Número de Acta\n"
            "3. Click en \"Buscar\"\n"
            "4. Hacé click en el icono a la derecha para ver el detalle del expediente\n\n"
            "No necesitás clave fiscal para esta consulta, es pública."
        ),
        "link": "https://www.argentina.gob.ar/inpi/marcas/seguir-el-tramite",
    },
    {
        "id": "renovar_marca",
        "keywords": ["renovar marca", "vencimiento marca", "marca vence", "renovacion marca",
                     "cuanto dura marca", "vencida marca"],
        "respuesta": (
            "Las marcas en Argentina tienen una vigencia de 10 años desde la fecha de concesión.\n\n"
            "Para renovar, tenés que iniciar el trámite dentro de los últimos 12 meses antes del vencimiento "
            "o hasta 6 meses después (con recargo).\n\n"
            "El trámite de renovación se hace online en portaltramites.inpi.gob.ar con tu clave fiscal."
        ),
        "link": "https://www.argentina.gob.ar/inpi/marcas/tramites-de-marcas",
    },
    # ===== MONOTRIBUTO =====
    {
        "id": "monotributo",
        "keywords": ["monotributo", "como me hago monotributista", "inscribir monotributo",
                     "alta monotributo", "categorias monotributo", "ser monotributista",
                     "que es monotributo", "que es el monotributo", "monotributista"],
        "respuesta": (
            "El Monotributo es un régimen simplificado para pequeños contribuyentes en Argentina. "
            "Incluye: impuesto integrado + aportes jubilatorios + obra social.\n\n"
            "Para inscribirte:\n"
            "1. Necesitás CUIT y clave fiscal\n"
            "2. Ingresá a www.arca.gob.ar\n"
            "3. Accedé al servicio \"Monotributo\"\n"
            "4. Elegí la categoría según tu facturación anual\n"
            "5. Completá los datos y confirmá\n\n"
            "Las categorías van de la A a la K, según ingresos brutos anuales."
        ),
        "link": "https://www.afip.gob.ar/monotributo/",
    },
    # ===== FACTURACIÓN =====
    {
        "id": "facturacion",
        "keywords": ["factura", "facturar", "como facturo", "factura electronica", "emitir factura",
                     "hacer factura", "comprobante", "factura a", "factura b", "factura c"],
        "respuesta": (
            "Para facturar electrónicamente:\n\n"
            "1. Necesitás CUIT + clave fiscal + estar inscripto (monotributo o responsable inscripto)\n"
            "2. Dar de alta un punto de venta en \"Registro Único Tributario\"\n"
            "3. Podés facturar desde:\n"
            "   - facturador.afip.gob.ar (web, la más simple)\n"
            "   - \"Comprobantes en línea\" en ARCA\n"
            "   - App ARCA Móvil\n\n"
            "Tipos de factura: A (a responsables inscriptos), B (a consumidor final), "
            "C (de monotributistas)."
        ),
        "link": "https://www.afip.gob.ar/facturacion/",
    },
    # ===== CUIT =====
    {
        "id": "cuit",
        "keywords": ["cuit", "obtener cuit", "sacar cuit", "que es cuit", "cuil",
                     "diferencia cuit cuil", "necesito cuit"],
        "respuesta": (
            "CUIT (Clave Única de Identificación Tributaria) es tu número de identificación fiscal.\n\n"
            "CUIL es para relación laboral, CUIT es para operar como contribuyente.\n\n"
            "Para obtener CUIT:\n"
            "1. Si sos empleado ya tenés CUIL (se convierte en CUIT)\n"
            "2. Si necesitás CUIT nuevo, sacá turno en ARCA y andá con DNI\n"
            "3. También se puede gestionar online con clave fiscal\n\n"
            "Lo necesitás para: facturar, inscribirte en monotributo, acceder a servicios de ARCA."
        ),
        "link": "https://www.argentina.gob.ar/obtener-cuit",
    },
    # ===== ARCA GENERAL =====
    {
        "id": "arca_que_es",
        "keywords": ["que es arca", "arca que es", "afip", "que es afip", "arca ex afip"],
        "respuesta": (
            "ARCA (antes llamada AFIP) es la Agencia de Recaudación y Control Aduanero de Argentina. "
            "Es el organismo que administra los impuestos nacionales.\n\n"
            "Desde ARCA podés:\n"
            "- Inscribirte en Monotributo o Régimen General\n"
            "- Facturar electrónicamente\n"
            "- Pagar impuestos\n"
            "- Adherir servicios de otros organismos (INPI, ANSES, etc.)\n"
            "- Delegar accesos a contadores o representantes\n"
            "- Consultar aportes jubilatorios\n"
            "- Cargar deducciones (SiRADIG)\n\n"
            "Para todo esto necesitás CUIT y Clave Fiscal."
        ),
        "link": "https://www.arca.gob.ar",
    },
    {
        "id": "tramites_web",
        "keywords": ["tramites online", "tramites web", "que puedo hacer online", "que tramites",
                     "servicios arca", "servicios disponibles", "que servicios hay"],
        "respuesta": (
            "Trámites que podés hacer online con ARCA y clave fiscal:\n\n"
            "Tributarios: Inscripción en monotributo, régimen general, pago de impuestos, "
            "declaraciones juradas, planes de pago, constancia de CUIT.\n\n"
            "Facturación: Emitir facturas electrónicas, dar de alta puntos de venta.\n\n"
            "Laboral: Consultar aportes, registrar personal doméstico.\n\n"
            "Deducciones: Cargar deducciones de Ganancias en SiRADIG.\n\n"
            "Otros organismos: INPI (marcas y patentes), ANSES, Bienes Personales.\n\n"
            "Servicios administrativos: Adherir servicios, delegar accesos, gestionar clave fiscal."
        ),
        "link": "https://servicioscf.afip.gob.ar/publico/abc/ABCPaso1.aspx",
    },
]

# Links de fallback por categoría
FALLBACK_LINKS = {
    "general": "https://servicioscf.afip.gob.ar/publico/abc/ABCPaso1.aspx",
    "clave_fiscal": "https://www.afip.gob.ar/clavefiscal/",
    "monotributo": "https://www.afip.gob.ar/monotributo/",
    "facturacion": "https://www.afip.gob.ar/facturacion/",
    "inpi": "https://www.argentina.gob.ar/inpi",
    "marcas": "https://www.argentina.gob.ar/inpi/marcas",
}


def buscar_respuesta(texto: str) -> dict | None:
    """
    Busca la mejor respuesta en la base de conocimiento para un texto dado.
    Devuelve el entry con mayor score de matching, o None si no hay match.
    """
    texto_lower = texto.lower().strip()
    mejor_score = 0
    mejor_entry = None

    for entry in KNOWLEDGE_BASE:
        score = 0
        for kw in entry["keywords"]:
            kw_lower = kw.lower()
            # Match exacto de keyword completa
            if kw_lower in texto_lower:
                # Bonus por largo del keyword (más específico = mejor)
                score += len(kw_lower.split())
            else:
                # Match parcial: cada palabra del keyword que aparezca
                palabras_kw = kw_lower.split()
                matches = sum(1 for p in palabras_kw if p in texto_lower)
                if matches > 0:
                    score += matches * 0.5

        if score > mejor_score:
            mejor_score = score
            mejor_entry = entry

    # Requiere un mínimo de relevancia
    if mejor_score >= 1.0:
        return mejor_entry
    return None


def obtener_fallback_link(texto: str) -> str:
    """Devuelve el link de fallback más relevante según el texto."""
    texto_lower = texto.lower()

    if any(p in texto_lower for p in ["marca", "inpi", "patente", "registrar nombre"]):
        return FALLBACK_LINKS["marcas"]
    if any(p in texto_lower for p in ["clave fiscal", "clave", "contraseña", "nivel"]):
        return FALLBACK_LINKS["clave_fiscal"]
    if any(p in texto_lower for p in ["monotributo", "categoria", "monotributista"]):
        return FALLBACK_LINKS["monotributo"]
    if any(p in texto_lower for p in ["factura", "facturar", "comprobante"]):
        return FALLBACK_LINKS["facturacion"]

    return FALLBACK_LINKS["general"]
