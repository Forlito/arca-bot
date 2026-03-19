"""
Base de conocimiento JERÁRQUICA del bot ARCA/INPI.

Estructura:
- MENUS: definen los menús de botones inline (nivel padre)
- TOPICS: respuestas detalladas para cada sub-tema (nivel hijo)
- Cada topic puede tener sub-botones propios para seguir profundizando

Diseñado para drill-down interactivo vía inline keyboards de Telegram.
Preparado para futura integración de login ARCA (clave fiscal/CUIT).
"""

# =====================================================================
# MENÚS PRINCIPALES (lo que muestra cada comando)
# Cada menú tiene: texto introductorio + lista de botones
# =====================================================================

MENUS = {
    # ---- /inpi ----
    "inpi": {
        "texto": (
            "El INPI (Instituto Nacional de la Propiedad Industrial) es donde "
            "registrás marcas, patentes y diseños industriales en Argentina.\n\n"
            "Elegí qué querés saber:"
        ),
        "botones": [
            ("Registrar una marca", "inpi_registrar"),
            ("Consultar marcas existentes", "inpi_consultar"),
            ("Renovar una marca", "inpi_renovar"),
            ("Seguir un trámite", "inpi_seguir"),
            ("Costos y aranceles", "inpi_costos"),
            ("Patentes de invención", "inpi_patentes"),
            ("Modelos de utilidad", "inpi_modelos"),
            ("Diseños industriales", "inpi_disenos"),
            ("Cómo acceder al INPI online", "inpi_acceder"),
            ("Transferencia de tecnología", "inpi_transferencia"),
        ],
    },
    # ---- /clavefiscal ----
    "clavefiscal": {
        "texto": (
            "La Clave Fiscal es tu contraseña para operar en ARCA (ex AFIP). "
            "Sin ella no podés hacer trámites online.\n\n"
            "Elegí qué necesitás:"
        ),
        "botones": [
            ("Qué es la Clave Fiscal", "cf_que_es"),
            ("Cómo obtenerla", "cf_obtener"),
            ("Niveles de seguridad (2, 3, 4)", "cf_niveles"),
            ("Recuperar clave olvidada", "cf_recuperar"),
            ("Subir de nivel", "cf_subir_nivel"),
            ("Adherir un servicio con clave fiscal", "cf_adherir"),
            ("Delegar acceso a otro (ej: contador)", "cf_delegar"),
        ],
    },
    # ---- /arca ----
    "arca": {
        "texto": (
            "ARCA (ex AFIP) es la Agencia de Recaudación y Control Aduanero. "
            "Administra impuestos, facturación y servicios tributarios.\n\n"
            "Elegí un tema:"
        ),
        "botones": [
            ("Qué es ARCA", "arca_que_es"),
            ("Trámites disponibles online", "arca_tramites"),
            ("Monotributo", "arca_monotributo"),
            ("Facturación electrónica", "arca_facturacion"),
            ("CUIT / CUIL", "arca_cuit"),
            ("Clave Fiscal", "menu_clavefiscal"),
            ("INPI (Marcas y Patentes)", "menu_inpi"),
        ],
    },
    # ---- /monotributo ----
    "monotributo": {
        "texto": (
            "El Monotributo es el régimen simplificado para pequeños contribuyentes. "
            "Incluye impuesto + jubilación + obra social.\n\n"
            "Elegí qué querés saber:"
        ),
        "botones": [
            ("Qué es y para quién es", "mono_que_es"),
            ("Cómo inscribirse", "mono_inscribir"),
            ("Categorías y montos", "mono_categorias"),
            ("Cómo facturar siendo monotributista", "mono_facturar"),
            ("Recategorización", "mono_recategorizacion"),
            ("Dar de baja", "mono_baja"),
        ],
    },
    # ---- /factura ----
    "factura": {
        "texto": (
            "La facturación electrónica es obligatoria para todos los contribuyentes.\n\n"
            "Elegí qué necesitás:"
        ),
        "botones": [
            ("Cómo facturar (paso a paso)", "fact_como"),
            ("Tipos de factura (A, B, C, E)", "fact_tipos"),
            ("Dar de alta punto de venta", "fact_punto_venta"),
            ("Facturar desde el celular", "fact_movil"),
            ("Nota de crédito / débito", "fact_notas"),
        ],
    },
}

# =====================================================================
# TOPICS: respuestas detalladas para cada callback_data
# Cada topic puede tener sub-botones para seguir navegando
# =====================================================================

TOPICS = {
    # ===== INPI SUB-TOPICS =====
    "inpi_registrar": {
        "texto": (
            "Registrar una marca en Argentina - Paso a paso:\n\n"
            "1. Verificá disponibilidad del nombre\n"
            "   Usá /disponible <nombre> en este bot, o buscá en el portal del INPI.\n\n"
            "2. Elegí la clase Niza correcta\n"
            "   Las marcas se registran por clase de actividad (1-45). "
            "Usá /clases <actividad> para encontrar la tuya.\n\n"
            "3. Ingresá al portal de trámites del INPI\n"
            "   portaltramites.inpi.gob.ar (necesitás clave fiscal + servicio INPI adherido)\n\n"
            "4. Completá la solicitud\n"
            "   Elegí tipo de marca (denominativa, mixta, figurativa), "
            "cargá el nombre y logo si aplica.\n\n"
            "5. Pagá el arancel\n"
            "   Se paga por clase. El monto se actualiza periódicamente.\n\n"
            "6. Hacé seguimiento\n"
            "   Con tu número de acta podés ver el estado en cualquier momento.\n\n"
            "Tiempos: 12 meses (simplificado) a 24 meses (con oposiciones).\n"
            "Vigencia: 10 años renovables.\n\n"
            "Requisitos: CUIT/CUIL + Clave Fiscal nivel 2+ + servicio INPI adherido."
        ),
        "link": "https://www.argentina.gob.ar/inpi/marcas/registrar-una-marca",
        "botones": [
            ("Verificar disponibilidad ahora", "inpi_consultar"),
            ("Buscar mi clase Niza", "inpi_clases_niza"),
            ("Cómo acceder al portal INPI", "inpi_acceder"),
            ("Costos actualizados", "inpi_costos"),
            ("Volver al menú INPI", "menu_inpi"),
        ],
    },
    "inpi_consultar": {
        "texto": (
            "Consultar marcas registradas:\n\n"
            "Desde este bot:\n"
            "  /buscar <nombre> → Marcas vigentes que contengan ese nombre\n"
            "  /buscar <nombre> <clase> → Filtrado por clase Niza\n"
            "  /disponible <nombre> → Verifica si el nombre parece disponible\n"
            "  /buscar_todas <nombre> → Incluye marcas vencidas/abandonadas\n\n"
            "Desde la web del INPI:\n"
            "  Ingresá a portaltramites.inpi.gob.ar/MarcasConsultas\n"
            "  Podés buscar por denominación, titular, número de acta, etc.\n"
            "  Esta consulta es pública, no necesitás clave fiscal.\n\n"
            "Datos que muestra cada resultado:\n"
            "  Nro Acta, Titular, Clase, Estado, Vencimiento, Tipo de marca."
        ),
        "link": "https://portaltramites.inpi.gob.ar/MarcasConsultas",
        "botones": [
            ("Registrar una marca", "inpi_registrar"),
            ("Clases Niza explicadas", "inpi_clases_niza"),
            ("Volver al menú INPI", "menu_inpi"),
        ],
    },
    "inpi_renovar": {
        "texto": (
            "Renovar una marca registrada:\n\n"
            "Las marcas tienen vigencia de 10 años desde la fecha de concesión.\n\n"
            "Cuándo renovar:\n"
            "  Podés iniciar la renovación en los últimos 12 meses antes del vencimiento.\n"
            "  Si se te pasó, tenés hasta 6 meses después (con recargo).\n\n"
            "Cómo renovar:\n"
            "1. Ingresá a portaltramites.inpi.gob.ar con clave fiscal\n"
            "2. Andá a \"Trámites de marcas\" > \"Renovación\"\n"
            "3. Ingresá el número de acta de tu marca\n"
            "4. Verificá los datos y confirmá\n"
            "5. Pagá el arancel de renovación\n\n"
            "Si la marca venció hace más de 6 meses, perdés el derecho y "
            "tenés que hacer un registro nuevo.\n\n"
            "Requisitos: CUIT + Clave Fiscal + servicio INPI adherido."
        ),
        "link": "https://www.argentina.gob.ar/inpi/marcas/tramites-de-marcas",
        "botones": [
            ("Ver vencimiento de mi marca", "inpi_seguir"),
            ("Cómo acceder al portal", "inpi_acceder"),
            ("Volver al menú INPI", "menu_inpi"),
        ],
    },
    "inpi_seguir": {
        "texto": (
            "Seguir el estado de un trámite de marca:\n\n"
            "1. Ingresá a portaltramites.inpi.gob.ar/MarcasConsultas\n"
            "2. Usá la opción \"Seguimiento de Trámite\"\n"
            "3. Poné tu Número de Acta (lo recibiste al hacer la solicitud)\n"
            "4. Hacé click en \"Buscar\"\n"
            "5. Clickeá el ícono de la derecha para ver el detalle del expediente\n\n"
            "Esta consulta es pública, no necesitás clave fiscal.\n\n"
            "Estados posibles:\n"
            "  EN TRÁMITE → Se está procesando\n"
            "  PUBLICADA → Está en el Boletín de Marcas (período de oposiciones)\n"
            "  CONCEDIDA → Marca registrada exitosamente\n"
            "  DENEGADA → Fue rechazada (podés apelar)\n"
            "  ABANDONADA → No se completó el trámite\n"
            "  VENCIDA → Pasaron 10 años y no se renovó"
        ),
        "link": "https://portaltramites.inpi.gob.ar/MarcasConsultas",
        "botones": [
            ("Renovar una marca", "inpi_renovar"),
            ("Registrar una marca nueva", "inpi_registrar"),
            ("Volver al menú INPI", "menu_inpi"),
        ],
    },
    "inpi_costos": {
        "texto": (
            "Costos y aranceles del INPI:\n\n"
            "Los aranceles se actualizan periódicamente. Consultá siempre el valor "
            "vigente en el portal oficial antes de iniciar un trámite.\n\n"
            "Cosas a tener en cuenta:\n"
            "  - El arancel se paga por cada clase Niza (si registrás en 3 clases, pagás 3 veces)\n"
            "  - La renovación tiene su propio arancel\n"
            "  - Si renovás fuera de término (hasta 6 meses después), hay recargo\n"
            "  - Las oposiciones y recursos tienen costos adicionales\n"
            "  - El pago se realiza electrónicamente desde el portal de trámites\n\n"
            "Para ver los montos actualizados, ingresá al portal de aranceles del INPI."
        ),
        "link": "https://www.argentina.gob.ar/inpi/aranceles",
        "botones": [
            ("Registrar una marca", "inpi_registrar"),
            ("Volver al menú INPI", "menu_inpi"),
        ],
    },
    "inpi_patentes": {
        "texto": (
            "Patentes de invención en el INPI:\n\n"
            "Una patente protege una invención técnica nueva, con actividad inventiva "
            "y aplicación industrial. Dura 20 años (no renovable).\n\n"
            "Qué se puede patentar:\n"
            "  Productos, procesos, composiciones, dispositivos, mejoras técnicas.\n\n"
            "Qué NO se puede patentar:\n"
            "  Descubrimientos, teorías, métodos matemáticos, software puro, "
            "plantas, animales, métodos quirúrgicos.\n\n"
            "Cómo se tramita:\n"
            "1. Hacer una búsqueda de antecedentes (recomendado)\n"
            "2. Preparar la solicitud (descripción, reivindicaciones, resumen, dibujos)\n"
            "3. Presentar en el portal del INPI con clave fiscal\n"
            "4. Pagar arancel de presentación\n"
            "5. Examen de forma y fondo (puede llevar años)\n\n"
            "Se recomienda asesoramiento profesional (agente de propiedad industrial)."
        ),
        "link": "https://www.argentina.gob.ar/inpi/patentes",
        "botones": [
            ("Modelos de utilidad", "inpi_modelos"),
            ("Diseños industriales", "inpi_disenos"),
            ("Cómo acceder al portal", "inpi_acceder"),
            ("Volver al menú INPI", "menu_inpi"),
        ],
    },
    "inpi_modelos": {
        "texto": (
            "Modelos de utilidad en el INPI:\n\n"
            "Protegen mejoras funcionales de objetos ya existentes "
            "(\"pequeñas invenciones\"). Duran 10 años (no renovable).\n\n"
            "Diferencia con patente:\n"
            "  Patente = invención completamente nueva\n"
            "  Modelo de utilidad = mejora práctica de algo existente\n\n"
            "Ejemplos: un mango ergonómico, un cierre mejorado, "
            "un envase con mejor dosificación.\n\n"
            "Trámite similar a patentes pero más rápido y económico.\n"
            "Se presenta en el portal del INPI con clave fiscal."
        ),
        "link": "https://www.argentina.gob.ar/inpi/modelos-de-utilidad",
        "botones": [
            ("Patentes de invención", "inpi_patentes"),
            ("Diseños industriales", "inpi_disenos"),
            ("Volver al menú INPI", "menu_inpi"),
        ],
    },
    "inpi_disenos": {
        "texto": (
            "Diseños industriales en el INPI:\n\n"
            "Protegen la apariencia estética (forma, configuración, ornamentación) "
            "de un producto industrial. Duran 5 años, renovables hasta 15.\n\n"
            "Qué se protege: el aspecto visual, no la función.\n"
            "Ejemplos: diseño de una silla, packaging, interfaz de producto.\n\n"
            "Cómo se tramita:\n"
            "1. Preparar representaciones gráficas del diseño (fotos o dibujos)\n"
            "2. Presentar solicitud en el portal del INPI\n"
            "3. Pagar arancel\n"
            "4. El INPI examina y publica\n\n"
            "Se presenta online en portaltramites.inpi.gob.ar con clave fiscal."
        ),
        "link": "https://www.argentina.gob.ar/inpi/disenos-industriales",
        "botones": [
            ("Patentes de invención", "inpi_patentes"),
            ("Modelos de utilidad", "inpi_modelos"),
            ("Volver al menú INPI", "menu_inpi"),
        ],
    },
    "inpi_acceder": {
        "texto": (
            "Cómo acceder al portal online del INPI:\n\n"
            "1. Tener CUIT (si no tenés, sacalo en ARCA)\n\n"
            "2. Tener Clave Fiscal nivel 2 o superior\n"
            "   (si no tenés, obtenerla por app ARCA, homebanking, o presencial)\n\n"
            "3. Adherir el servicio INPI en ARCA:\n"
            "   a. Ingresá a www.arca.gob.ar con CUIT y clave fiscal\n"
            "   b. Andá a \"Administrador de Relaciones de Clave Fiscal\"\n"
            "   c. Click en \"Adherir Servicio\"\n"
            "   d. Buscá \"Instituto Nacional de la Propiedad Industrial\"\n"
            "   e. Seleccioná y confirmá\n\n"
            "4. Ingresá al portal de trámites:\n"
            "   a. Andá a portaltramites.inpi.gob.ar\n"
            "   b. Logueate con tu clave fiscal\n"
            "   c. Completá tus datos de perfil (nombre, domicilio, tipo: particular/agente)\n\n"
            "Listo, ya podés operar en el INPI online."
        ),
        "link": "https://portaltramites.inpi.gob.ar",
        "botones": [
            ("Qué es la Clave Fiscal", "cf_que_es"),
            ("Cómo obtener Clave Fiscal", "cf_obtener"),
            ("Registrar una marca", "inpi_registrar"),
            ("Volver al menú INPI", "menu_inpi"),
        ],
    },
    "inpi_transferencia": {
        "texto": (
            "Transferencia de tecnología en el INPI:\n\n"
            "Si vas a celebrar contratos de licencia, franquicia, o transferencia "
            "de tecnología con una empresa extranjera, tenés que registrarlo en el INPI.\n\n"
            "Esto incluye:\n"
            "  - Contratos de licencia de patentes o marcas\n"
            "  - Contratos de asistencia técnica\n"
            "  - Contratos de transferencia de tecnología\n"
            "  - Contratos de franquicia comercial\n\n"
            "El registro es requisito para poder girar regalías al exterior "
            "y deducirlas impositivamente.\n\n"
            "Se tramita online en el portal del INPI con clave fiscal."
        ),
        "link": "https://www.argentina.gob.ar/inpi/transferencia-de-tecnologia",
        "botones": [
            ("Cómo acceder al portal", "inpi_acceder"),
            ("Volver al menú INPI", "menu_inpi"),
        ],
    },
    "inpi_clases_niza": {
        "texto": (
            "Clases Niza (Clasificación Internacional de Marcas):\n\n"
            "Las marcas se registran por clase. Hay 45 clases:\n"
            "  Clases 1 a 34 → Productos\n"
            "  Clases 35 a 45 → Servicios\n\n"
            "Cada clase cubre un rubro específico. Algunos ejemplos:\n"
            "  Clase 25 → Ropa, calzado\n"
            "  Clase 35 → Publicidad, gestión de negocios\n"
            "  Clase 42 → Software, tecnología, diseño\n"
            "  Clase 43 → Restaurantes, hotelería\n\n"
            "Para buscar tu clase, usá:\n"
            "  /clases <actividad> → ej: /clases software\n"
            "  /clase <numero> → ej: /clase 42\n\n"
            "Si tu marca abarca varias actividades, podés necesitar registrar "
            "en múltiples clases (se paga por cada una)."
        ),
        "link": "https://www.argentina.gob.ar/inpi/marcas/clasificacion-de-niza",
        "botones": [
            ("Registrar una marca", "inpi_registrar"),
            ("Costos por clase", "inpi_costos"),
            ("Volver al menú INPI", "menu_inpi"),
        ],
    },

    # ===== CLAVE FISCAL SUB-TOPICS =====
    "cf_que_es": {
        "texto": (
            "La Clave Fiscal es tu contraseña digital para operar en ARCA (ex AFIP).\n\n"
            "Con ella podés:\n"
            "  - Facturar electrónicamente\n"
            "  - Pagar impuestos\n"
            "  - Inscribirte en monotributo\n"
            "  - Adherir servicios (INPI, ANSES, etc.)\n"
            "  - Delegar accesos a tu contador\n"
            "  - Consultar aportes jubilatorios\n\n"
            "Tiene niveles de seguridad (2, 3 y 4). Cuanto más alto el nivel, "
            "más trámites podés hacer. Para la mayoría, nivel 2 o 3 alcanza.\n\n"
            "Sin Clave Fiscal no podés hacer ningún trámite online en ARCA."
        ),
        "link": "https://www.afip.gob.ar/clavefiscal/",
        "botones": [
            ("Cómo obtenerla", "cf_obtener"),
            ("Niveles de seguridad", "cf_niveles"),
            ("Volver al menú Clave Fiscal", "menu_clavefiscal"),
        ],
    },
    "cf_obtener": {
        "texto": (
            "Cómo obtener Clave Fiscal:\n\n"
            "Opción 1: Por la app ARCA (la más rápida, te da nivel 3)\n"
            "  1. Descargá la app ARCA desde Play Store o App Store\n"
            "  2. Andá a Herramientas > Solicitud de Clave Fiscal\n"
            "  3. Escaneá tu DNI tarjeta (frente y dorso)\n"
            "  4. Sacate una selfie para validación biométrica\n"
            "  5. Elegí tu contraseña\n"
            "  Listo, ya tenés nivel 3.\n\n"
            "Opción 2: Por homebanking (te da nivel 2)\n"
            "  1. Ingresá a tu homebanking\n"
            "  2. Buscá la opción AFIP/ARCA > Clave Fiscal\n"
            "  3. Seguí los pasos de tu banco\n"
            "  Te llega nivel 2 (suficiente para muchos trámites).\n\n"
            "Opción 3: Presencial en ARCA (te da nivel 3)\n"
            "  1. Sacá turno en turnos.arca.gob.ar\n"
            "  2. Andá a la dependencia con DNI tarjeta\n"
            "  3. Te registran datos biométricos (foto, firma, huella)\n"
            "  4. Te dan nivel 3 en el momento.\n\n"
            "Requisitos: DNI argentino en formato tarjeta + ser mayor de edad."
        ),
        "link": "https://www.argentina.gob.ar/servicio/obtener-la-clave-fiscal",
        "botones": [
            ("Qué nivel necesito", "cf_niveles"),
            ("Recuperar clave olvidada", "cf_recuperar"),
            ("Volver al menú Clave Fiscal", "menu_clavefiscal"),
        ],
    },
    "cf_niveles": {
        "texto": (
            "Niveles de seguridad de Clave Fiscal:\n\n"
            "Nivel 2 (básico)\n"
            "  Cómo se obtiene: por homebanking\n"
            "  Qué podés hacer: adherir servicios para vos mismo, consultas básicas, "
            "facturar, acceder al INPI.\n\n"
            "Nivel 3 (el más usado)\n"
            "  Cómo se obtiene: app ARCA o presencial\n"
            "  Qué podés hacer: todo lo de nivel 2 + delegar accesos a terceros, "
            "administrar apoderados, trámites societarios.\n\n"
            "Nivel 4 (máxima seguridad)\n"
            "  Cómo se obtiene: presencial con turno, requiere nivel 3 previo\n"
            "  Qué podés hacer: todo lo anterior + doble autenticación con token, "
            "operaciones de alta seguridad.\n\n"
            "Recomendación: nivel 3 por la app es lo más práctico para la mayoría."
        ),
        "link": "https://www.afip.gob.ar/clavefiscal/ayuda/obtener-clave-fiscal.asp",
        "botones": [
            ("Cómo obtener clave fiscal", "cf_obtener"),
            ("Subir de nivel", "cf_subir_nivel"),
            ("Volver al menú Clave Fiscal", "menu_clavefiscal"),
        ],
    },
    "cf_recuperar": {
        "texto": (
            "Recuperar Clave Fiscal olvidada o bloqueada:\n\n"
            "Opción 1: Desde la app ARCA\n"
            "  1. Abrí la app ARCA\n"
            "  2. Andá a Herramientas > Recupero de Clave Fiscal\n"
            "  3. Escaneá tu DNI tarjeta\n"
            "  4. Sacate una selfie\n"
            "  5. Elegí nueva contraseña\n\n"
            "Opción 2: Por homebanking\n"
            "  Desde tu banco, en la sección AFIP/ARCA, regenerá la clave.\n\n"
            "Opción 3: Presencial\n"
            "  1. Sacá turno en turnos.arca.gob.ar\n"
            "  2. Andá con DNI a una dependencia de ARCA\n"
            "  3. Te blanquean la clave en el momento\n\n"
            "Si te bloquearon por intentos fallidos, esperá 30 minutos "
            "o hacé el recupero por cualquiera de estos medios."
        ),
        "link": "https://www.afip.gob.ar/clavefiscal/ayuda/recupera-clave-fiscal.asp",
        "botones": [
            ("Niveles de seguridad", "cf_niveles"),
            ("Volver al menú Clave Fiscal", "menu_clavefiscal"),
        ],
    },
    "cf_subir_nivel": {
        "texto": (
            "Cómo subir el nivel de tu Clave Fiscal:\n\n"
            "De nivel 2 a nivel 3:\n"
            "  Opción A: Por la app ARCA\n"
            "    Herramientas > Solicitud de Clave Fiscal > Aumentar nivel\n"
            "    Escaneá DNI + selfie = nivel 3 inmediato.\n"
            "  Opción B: Presencial\n"
            "    Turno web + DNI en dependencia ARCA.\n\n"
            "De nivel 3 a nivel 4:\n"
            "  Solo presencial con turno previo.\n"
            "  Te habilitan doble autenticación con token.\n"
            "  Necesitás tener nivel 3 activo.\n\n"
            "Nota: para la mayoría de los trámites (incluyendo INPI), "
            "nivel 2 o 3 es suficiente."
        ),
        "link": "https://www.afip.gob.ar/clavefiscal/ayuda/obtener-clave-fiscal.asp",
        "botones": [
            ("Niveles explicados", "cf_niveles"),
            ("Volver al menú Clave Fiscal", "menu_clavefiscal"),
        ],
    },
    "cf_adherir": {
        "texto": (
            "Adherir un servicio con Clave Fiscal:\n\n"
            "Adherir un servicio significa habilitarlo para usarlo online "
            "(ej: INPI, Monotributo, Comprobantes en Línea, etc.)\n\n"
            "Paso a paso:\n"
            "1. Ingresá a www.arca.gob.ar con tu CUIT y clave fiscal\n"
            "2. Andá a \"Administrador de Relaciones de Clave Fiscal\" "
            "(está en Servicios Administrativos)\n"
            "3. Hacé click en \"Adherir Servicio\"\n"
            "4. Buscá el organismo por nombre:\n"
            "   - INPI: \"Instituto Nacional de la Propiedad Industrial\"\n"
            "   - Facturación: \"Comprobantes en Línea\"\n"
            "   - Monotributo: \"Monotributo\"\n"
            "5. Seleccioná y confirmá\n\n"
            "Con nivel 2 podés adherir servicios para vos mismo.\n"
            "Para adherir en nombre de un tercero, necesitás nivel 3."
        ),
        "link": "https://servicioscf.afip.gob.ar/publico/abc/ABCpaso2.aspx?cat=2949",
        "botones": [
            ("Delegar acceso a otro", "cf_delegar"),
            ("Cómo acceder al INPI", "inpi_acceder"),
            ("Volver al menú Clave Fiscal", "menu_clavefiscal"),
        ],
    },
    "cf_delegar": {
        "texto": (
            "Delegar acceso a otra persona (ej: tu contador):\n\n"
            "Esto le permite a otra persona operar servicios en tu nombre.\n\n"
            "Paso a paso:\n"
            "1. Ingresá a ARCA con tu clave fiscal (necesitás nivel 3)\n"
            "2. Andá a \"Administrador de Relaciones de Clave Fiscal\"\n"
            "3. Elegí \"Nueva Relación\" (NO \"Adherir Servicio\")\n"
            "4. En \"Representado\" elegí tu CUIT\n"
            "5. Elegí el servicio que querés delegar\n"
            "6. En \"Representante\" poné el CUIT de la persona (ej: tu contador)\n"
            "7. Confirmá\n\n"
            "La persona delegada tiene que aceptar:\n"
            "  Entra a ARCA > \"Aceptación de Designación\" > Acepta con su clave fiscal.\n\n"
            "Podés revocar la delegación en cualquier momento desde el mismo lugar."
        ),
        "link": "https://servicioscf.afip.gob.ar/publico/abc/ABCpaso2.aspx?cat=2949",
        "botones": [
            ("Adherir un servicio", "cf_adherir"),
            ("Niveles de clave fiscal", "cf_niveles"),
            ("Volver al menú Clave Fiscal", "menu_clavefiscal"),
        ],
    },

    # ===== ARCA / GENERAL SUB-TOPICS =====
    "arca_que_es": {
        "texto": (
            "ARCA (Agencia de Recaudación y Control Aduanero) es el nuevo nombre "
            "de la AFIP. Es el organismo nacional que administra impuestos y aduanas.\n\n"
            "Desde ARCA podés:\n"
            "  - Inscribirte en monotributo o régimen general\n"
            "  - Facturar electrónicamente\n"
            "  - Pagar impuestos (IVA, Ganancias, Bienes Personales)\n"
            "  - Presentar declaraciones juradas\n"
            "  - Adherir servicios de otros organismos (INPI, ANSES)\n"
            "  - Delegar accesos a contadores o representantes\n"
            "  - Consultar aportes jubilatorios\n"
            "  - Cargar deducciones (SiRADIG)\n"
            "  - Sacar constancia de CUIT\n\n"
            "Para todo necesitás CUIT y Clave Fiscal."
        ),
        "link": "https://www.arca.gob.ar",
        "botones": [
            ("Trámites disponibles online", "arca_tramites"),
            ("Cómo obtener Clave Fiscal", "cf_obtener"),
            ("Volver al menú ARCA", "menu_arca"),
        ],
    },
    "arca_tramites": {
        "texto": (
            "Trámites disponibles online en ARCA:\n\n"
            "Tributarios:\n"
            "  Inscripción en monotributo o régimen general, pago de impuestos, "
            "declaraciones juradas (DDJJ), planes de pago, constancia de CUIT, "
            "certificados de no retención.\n\n"
            "Facturación:\n"
            "  Emitir facturas electrónicas, dar de alta puntos de venta, "
            "anular comprobantes, consultar facturas emitidas/recibidas.\n\n"
            "Laboral:\n"
            "  Consultar aportes jubilatorios, registrar personal doméstico, "
            "Simplificación Registral.\n\n"
            "Deducciones:\n"
            "  Cargar deducciones de Ganancias en SiRADIG (alquileres, "
            "percepciones, donaciones, etc.)\n\n"
            "Otros organismos:\n"
            "  INPI (marcas y patentes), ANSES, Bienes Personales.\n\n"
            "Administrativos:\n"
            "  Adherir/desadherir servicios, delegar accesos, gestionar clave fiscal."
        ),
        "link": "https://servicioscf.afip.gob.ar/publico/abc/ABCPaso1.aspx",
        "botones": [
            ("Monotributo", "arca_monotributo"),
            ("Facturación", "arca_facturacion"),
            ("CUIT / CUIL", "arca_cuit"),
            ("Volver al menú ARCA", "menu_arca"),
        ],
    },
    "arca_monotributo": {
        "texto": (
            "Monotributo - Régimen simplificado:\n\n"
            "Es un régimen para pequeños contribuyentes que unifica en una "
            "cuota mensual: impuesto integrado + aportes jubilatorios + obra social.\n\n"
            "Para quién es: personas que facturen dentro de los límites de cada categoría "
            "y no tengan más de 3 actividades simultáneas.\n\n"
            "Cómo inscribirse:\n"
            "1. Tener CUIT y clave fiscal\n"
            "2. Ingresar a www.arca.gob.ar\n"
            "3. Acceder al servicio \"Monotributo\"\n"
            "4. Elegir categoría según facturación anual estimada\n"
            "5. Completar datos y confirmar\n\n"
            "Categorías: van de la A a la K, según ingresos brutos anuales.\n"
            "Los montos se actualizan semestralmente."
        ),
        "link": "https://www.afip.gob.ar/monotributo/",
        "botones": [
            ("Categorías y montos", "mono_categorias"),
            ("Cómo facturar", "mono_facturar"),
            ("Recategorización", "mono_recategorizacion"),
            ("Volver al menú ARCA", "menu_arca"),
        ],
    },
    "arca_facturacion": {
        "texto": (
            "Facturación electrónica:\n\n"
            "Es obligatoria para todos los contribuyentes inscriptos.\n\n"
            "Requisitos:\n"
            "  CUIT + Clave Fiscal + estar inscripto (monotributo o resp. inscripto) "
            "+ punto de venta habilitado.\n\n"
            "Desde dónde facturar:\n"
            "  1. facturador.afip.gob.ar (web, la más simple)\n"
            "  2. \"Comprobantes en Línea\" en ARCA\n"
            "  3. App ARCA Móvil\n"
            "  4. Sistemas de facturación de terceros (ej: Xubio, Colppy)\n\n"
            "Tipos de factura:\n"
            "  A → De resp. inscripto a resp. inscripto\n"
            "  B → De resp. inscripto a consumidor final\n"
            "  C → De monotributista a cualquiera\n"
            "  E → Factura de exportación"
        ),
        "link": "https://www.afip.gob.ar/facturacion/",
        "botones": [
            ("Paso a paso para facturar", "fact_como"),
            ("Tipos de factura explicados", "fact_tipos"),
            ("Punto de venta", "fact_punto_venta"),
            ("Volver al menú ARCA", "menu_arca"),
        ],
    },
    "arca_cuit": {
        "texto": (
            "CUIT / CUIL:\n\n"
            "CUIL (Clave Única de Identificación Laboral):\n"
            "  Se asigna automáticamente a todo argentino o residente con DNI. "
            "Lo usás para relaciones laborales.\n\n"
            "CUIT (Clave Única de Identificación Tributaria):\n"
            "  Mismo formato que CUIL pero te identifica como contribuyente. "
            "Lo necesitás para: facturar, monotributo, acceder a servicios de ARCA.\n\n"
            "Cómo obtener CUIT:\n"
            "  Si ya tenés CUIL, generalmente ya tenés CUIT (mismo número).\n"
            "  Si necesitás activarlo:\n"
            "  1. Online: desde www.arca.gob.ar > \"Inscripción / Registro\"\n"
            "  2. Presencial: turno en ARCA + DNI\n\n"
            "Consultar tu CUIT:\n"
            "  www.arca.gob.ar > \"Consulta CUIT\" (público, sin clave fiscal)"
        ),
        "link": "https://www.argentina.gob.ar/obtener-cuit",
        "botones": [
            ("Clave Fiscal", "cf_que_es"),
            ("Monotributo", "arca_monotributo"),
            ("Volver al menú ARCA", "menu_arca"),
        ],
    },

    # ===== MONOTRIBUTO SUB-TOPICS =====
    "mono_que_es": {
        "texto": (
            "Monotributo - Qué es y para quién:\n\n"
            "Es un régimen tributario simplificado que unifica en una sola "
            "cuota mensual:\n"
            "  - Impuesto integrado (reemplaza IVA y Ganancias)\n"
            "  - Aportes jubilatorios\n"
            "  - Obra social (podés elegir entre las disponibles)\n\n"
            "Es para vos si:\n"
            "  - Sos trabajador independiente o freelancer\n"
            "  - Tenés un emprendimiento o comercio chico\n"
            "  - Facturás dentro de los límites de las categorías (A a K)\n"
            "  - No tenés más de 3 actividades simultáneas\n"
            "  - No superás los parámetros de superficie, energía o alquileres\n\n"
            "Ventajas: simplicidad, cuota fija mensual, obra social incluida."
        ),
        "link": "https://www.afip.gob.ar/monotributo/",
        "botones": [
            ("Cómo inscribirse", "mono_inscribir"),
            ("Categorías y montos", "mono_categorias"),
            ("Volver al menú Monotributo", "menu_monotributo"),
        ],
    },
    "mono_inscribir": {
        "texto": (
            "Cómo inscribirse en Monotributo:\n\n"
            "1. Tener CUIT y Clave Fiscal (nivel 2 o superior)\n"
            "2. Ingresá a www.arca.gob.ar\n"
            "3. Buscá el servicio \"Monotributo\" (adherilo si no lo tenés)\n"
            "4. Elegí \"Alta Monotributo\"\n"
            "5. Completá:\n"
            "   - Actividad económica\n"
            "   - Categoría (según ingresos estimados)\n"
            "   - Datos de domicilio fiscal\n"
            "   - Obra social (podés elegir)\n"
            "6. Confirmá y listo\n\n"
            "El pago es mensual, vence el día 20 de cada mes.\n"
            "Podés pagar por débito automático, Mercado Pago, transferencia, o VEP."
        ),
        "link": "https://www.afip.gob.ar/monotributo/categorias.asp",
        "botones": [
            ("Categorías y montos", "mono_categorias"),
            ("Cómo facturar", "mono_facturar"),
            ("Volver al menú Monotributo", "menu_monotributo"),
        ],
    },
    "mono_categorias": {
        "texto": (
            "Categorías de Monotributo:\n\n"
            "Van de la A a la K según ingresos brutos anuales.\n"
            "Los montos se actualizan semestralmente (enero y julio).\n\n"
            "Categoría A: la más baja (ingresos más chicos)\n"
            "Categoría K: la más alta (tope del monotributo)\n\n"
            "Cada categoría tiene límites de:\n"
            "  - Ingresos brutos anuales\n"
            "  - Superficie del local\n"
            "  - Energía eléctrica consumida\n"
            "  - Alquileres pagados\n\n"
            "Si superás los límites de la K, tenés que pasar a Responsable Inscripto.\n\n"
            "Para ver los montos vigentes actualizados, consultá el portal de ARCA."
        ),
        "link": "https://www.afip.gob.ar/monotributo/categorias.asp",
        "botones": [
            ("Cómo inscribirse", "mono_inscribir"),
            ("Recategorización", "mono_recategorizacion"),
            ("Volver al menú Monotributo", "menu_monotributo"),
        ],
    },
    "mono_facturar": {
        "texto": (
            "Cómo facturar siendo monotributista:\n\n"
            "Los monotributistas emiten Factura C (a cualquier tipo de cliente).\n\n"
            "Primer paso: dar de alta un punto de venta\n"
            "  En ARCA > \"Registro Único Tributario\" > \"Punto de Venta\" > Alta\n\n"
            "Para emitir facturas:\n"
            "1. Ingresá a facturador.afip.gob.ar (la forma más simple)\n"
            "2. Elegí tipo de comprobante: Factura C\n"
            "3. Completá: datos del cliente, descripción del servicio/producto, monto\n"
            "4. Confirmá y generá el comprobante\n"
            "5. Se genera un PDF para descargar o enviar\n\n"
            "También podés facturar desde la app ARCA Móvil o desde "
            "\"Comprobantes en Línea\" en el portal."
        ),
        "link": "https://www.afip.gob.ar/facturacion/",
        "botones": [
            ("Punto de venta", "fact_punto_venta"),
            ("Nota de crédito / débito", "fact_notas"),
            ("Volver al menú Monotributo", "menu_monotributo"),
        ],
    },
    "mono_recategorizacion": {
        "texto": (
            "Recategorización de Monotributo:\n\n"
            "Se hace 2 veces al año: enero y julio.\n\n"
            "Tenés que evaluar si tus ingresos de los últimos 12 meses "
            "corresponden a tu categoría actual o si tenés que cambiar.\n\n"
            "Cómo hacerlo:\n"
            "1. Ingresá a www.arca.gob.ar\n"
            "2. Accedé al servicio \"Monotributo\"\n"
            "3. Andá a \"Recategorización\"\n"
            "4. El sistema te muestra tu facturación\n"
            "5. Confirmá la nueva categoría si corresponde\n\n"
            "Si no te recategorizás y ARCA detecta que debías, "
            "te recategorizan de oficio y puede haber multas.\n\n"
            "Plazo: hasta el 20 de enero y el 20 de julio."
        ),
        "link": "https://www.afip.gob.ar/monotributo/",
        "botones": [
            ("Categorías y montos", "mono_categorias"),
            ("Volver al menú Monotributo", "menu_monotributo"),
        ],
    },
    "mono_baja": {
        "texto": (
            "Dar de baja el Monotributo:\n\n"
            "Podés darte de baja en cualquier momento.\n\n"
            "Cómo hacerlo:\n"
            "1. Ingresá a www.arca.gob.ar\n"
            "2. Accedé al servicio \"Monotributo\"\n"
            "3. Andá a \"Baja de Monotributo\"\n"
            "4. Confirmá\n\n"
            "La baja es efectiva desde el primer día del mes siguiente.\n\n"
            "Tené en cuenta que si te das de baja perdés la obra social "
            "y los aportes jubilatorios del monotributo. Si seguís trabajando, "
            "tenés que inscribirte en el Régimen General."
        ),
        "link": "https://www.afip.gob.ar/monotributo/",
        "botones": [
            ("Volver al menú Monotributo", "menu_monotributo"),
        ],
    },

    # ===== FACTURACIÓN SUB-TOPICS =====
    "fact_como": {
        "texto": (
            "Cómo facturar electrónicamente - Paso a paso:\n\n"
            "Requisitos previos:\n"
            "  - CUIT + Clave Fiscal\n"
            "  - Estar inscripto (monotributo o resp. inscripto)\n"
            "  - Punto de venta dado de alta\n\n"
            "Paso a paso:\n"
            "1. Ingresá a facturador.afip.gob.ar\n"
            "2. Logueate con CUIT y clave fiscal\n"
            "3. Elegí tu punto de venta\n"
            "4. Seleccioná tipo de comprobante (Factura A, B, C, según tu caso)\n"
            "5. Completá datos del receptor (CUIT/DNI, nombre)\n"
            "6. Agregá los conceptos: descripción, cantidad, precio\n"
            "7. Verificá el total y confirmá\n"
            "8. Se genera el comprobante con CAE (Código de Autorización Electrónico)\n"
            "9. Podés descargarlo como PDF o enviarlo por mail\n\n"
            "El CAE valida que la factura es auténtica ante ARCA."
        ),
        "link": "https://www.afip.gob.ar/facturacion/",
        "botones": [
            ("Tipos de factura", "fact_tipos"),
            ("Punto de venta", "fact_punto_venta"),
            ("Facturar desde el celular", "fact_movil"),
            ("Volver al menú Facturación", "menu_factura"),
        ],
    },
    "fact_tipos": {
        "texto": (
            "Tipos de factura electrónica:\n\n"
            "Factura A:\n"
            "  Emisor: Responsable Inscripto\n"
            "  Receptor: Responsable Inscripto\n"
            "  Discrimina IVA (el receptor se lo puede tomar como crédito fiscal)\n\n"
            "Factura B:\n"
            "  Emisor: Responsable Inscripto\n"
            "  Receptor: Consumidor Final, Monotributista, Exento\n"
            "  No discrimina IVA (va incluido en el total)\n\n"
            "Factura C:\n"
            "  Emisor: Monotributista\n"
            "  Receptor: Cualquiera\n"
            "  No discrimina IVA (monotributo no tiene IVA)\n\n"
            "Factura E:\n"
            "  Para exportación de bienes o servicios.\n"
            "  Cualquier contribuyente que exporte.\n\n"
            "Si sos monotributista, siempre emitís Factura C."
        ),
        "link": "https://www.afip.gob.ar/facturacion/",
        "botones": [
            ("Cómo facturar paso a paso", "fact_como"),
            ("Volver al menú Facturación", "menu_factura"),
        ],
    },
    "fact_punto_venta": {
        "texto": (
            "Dar de alta un Punto de Venta:\n\n"
            "Necesitás al menos un punto de venta habilitado para facturar.\n\n"
            "Paso a paso:\n"
            "1. Ingresá a www.arca.gob.ar con tu clave fiscal\n"
            "2. Buscá \"Registro Único Tributario\" (o A/B/M de Puntos de Venta)\n"
            "3. Elegí \"Alta de Punto de Venta\"\n"
            "4. Completá:\n"
            "   - Número (podés elegir, ej: 1)\n"
            "   - Nombre (ej: \"Mi local\", \"Online\")\n"
            "   - Tipo: \"Factura electrónica\" (RCEL - Régimen de Comprobantes Electrónicos en Línea)\n"
            "   - Domicilio asociado\n"
            "5. Confirmá\n\n"
            "Podés tener varios puntos de venta (ej: uno por sucursal)."
        ),
        "link": "https://www.afip.gob.ar/facturacion/",
        "botones": [
            ("Cómo facturar", "fact_como"),
            ("Tipos de factura", "fact_tipos"),
            ("Volver al menú Facturación", "menu_factura"),
        ],
    },
    "fact_movil": {
        "texto": (
            "Facturar desde el celular:\n\n"
            "Podés emitir facturas desde la app ARCA Móvil.\n\n"
            "Cómo:\n"
            "1. Descargá ARCA Móvil (Play Store / App Store)\n"
            "2. Logueate con CUIT y clave fiscal\n"
            "3. Andá a \"Facturación\" o \"Comprobantes\"\n"
            "4. Seguí los mismos pasos que en la web\n\n"
            "La app es útil para facturar sobre la marcha, pero para "
            "facturación frecuente es más cómoda la web (facturador.afip.gob.ar).\n\n"
            "Otras opciones:\n"
            "  Apps de facturación de terceros (Xubio, Colppy, Alegra) "
            "se conectan directo con ARCA y generan las facturas automáticamente."
        ),
        "link": "https://www.afip.gob.ar/facturacion/",
        "botones": [
            ("Cómo facturar paso a paso", "fact_como"),
            ("Volver al menú Facturación", "menu_factura"),
        ],
    },
    "fact_notas": {
        "texto": (
            "Notas de crédito y débito:\n\n"
            "Nota de crédito:\n"
            "  Sirve para anular total o parcialmente una factura ya emitida.\n"
            "  Ej: el cliente devolvió un producto, te equivocaste en el monto.\n"
            "  Se emite asociada a la factura original.\n\n"
            "Nota de débito:\n"
            "  Sirve para agregar importes a una factura existente.\n"
            "  Ej: intereses por pago tardío, ajustes de precio.\n\n"
            "Cómo emitirlas:\n"
            "  Mismo proceso que una factura, pero elegís \"Nota de Crédito\" "
            "o \"Nota de Débito\" como tipo de comprobante.\n"
            "  Te pide referenciar la factura original.\n\n"
            "Nota: el tipo (A, B, C) de la nota debe coincidir con la factura."
        ),
        "link": "https://www.afip.gob.ar/facturacion/",
        "botones": [
            ("Cómo facturar", "fact_como"),
            ("Tipos de factura", "fact_tipos"),
            ("Volver al menú Facturación", "menu_factura"),
        ],
    },
}

# =====================================================================
# KEYWORD MATCHING (para texto libre)
# Mapea keywords a callback_data o menu_id para responder texto libre
# =====================================================================

KEYWORD_MAP = [
    # Clave fiscal
    {
        "keywords": ["clave fiscal", "que es clave fiscal", "clave fiscal que es", "contraseña arca", "password arca"],
        "target": "cf_que_es",
    },
    {
        "keywords": ["obtener clave fiscal", "sacar clave fiscal", "como saco la clave", "crear clave fiscal",
                     "clave fiscal nueva", "registrarme en arca", "como me registro", "no tengo clave fiscal",
                     "necesito clave fiscal", "quiero clave fiscal"],
        "target": "cf_obtener",
    },
    {
        "keywords": ["nivel clave fiscal", "niveles de seguridad", "nivel 2", "nivel 3", "nivel 4",
                     "que nivel necesito", "diferencia niveles", "subir nivel"],
        "target": "cf_niveles",
    },
    {
        "keywords": ["recuperar clave fiscal", "olvide clave fiscal", "no me acuerdo la clave",
                     "blanquear clave", "resetear clave", "clave bloqueada", "me bloquee"],
        "target": "cf_recuperar",
    },
    {
        "keywords": ["adherir servicio", "agregar servicio", "habilitar servicio", "activar servicio",
                     "como adhiero", "adherir inpi", "agregar inpi", "sumar servicio"],
        "target": "cf_adherir",
    },
    {
        "keywords": ["delegar servicio", "delegar clave fiscal", "dar acceso a otro", "compartir acceso",
                     "contador acceso", "que otro opere", "usuario externo"],
        "target": "cf_delegar",
    },
    # INPI / Marcas
    {
        "keywords": ["que es inpi", "inpi que es", "registro de marcas", "propiedad industrial",
                     "para que sirve inpi", "marcas argentina"],
        "target": "menu_inpi",
    },
    {
        "keywords": ["registrar marca", "como registro marca", "registro de marca", "quiero registrar",
                     "sacar marca", "patentar marca", "patentar nombre", "proteger marca",
                     "inscribir marca", "marca comercial"],
        "target": "inpi_registrar",
    },
    {
        "keywords": ["adherir inpi", "activar inpi", "habilitar inpi", "inpi arca", "inpi clave fiscal",
                     "como entro al inpi", "acceder inpi", "registrarme inpi"],
        "target": "inpi_acceder",
    },
    {
        "keywords": ["cuanto cuesta marca", "costo marca", "precio marca", "arancel marca",
                     "cuanto sale registrar", "tasa inpi", "cuanto cobran"],
        "target": "inpi_costos",
    },
    {
        "keywords": ["seguir tramite", "estado tramite", "como va mi tramite", "seguimiento",
                     "numero de acta", "consultar tramite", "ver tramite"],
        "target": "inpi_seguir",
    },
    {
        "keywords": ["renovar marca", "vencimiento marca", "marca vence", "renovacion marca",
                     "cuanto dura marca", "vencida marca"],
        "target": "inpi_renovar",
    },
    {
        "keywords": ["patente", "patentes", "patentar invencion", "patente de invencion"],
        "target": "inpi_patentes",
    },
    {
        "keywords": ["modelo de utilidad", "modelos de utilidad"],
        "target": "inpi_modelos",
    },
    {
        "keywords": ["diseño industrial", "diseños industriales"],
        "target": "inpi_disenos",
    },
    {
        "keywords": ["clase niza", "clases niza", "clasificacion niza", "clasificacion de marcas"],
        "target": "inpi_clases_niza",
    },
    # Monotributo
    {
        "keywords": ["monotributo", "como me hago monotributista", "inscribir monotributo",
                     "alta monotributo", "categorias monotributo", "ser monotributista",
                     "que es monotributo", "que es el monotributo", "monotributista"],
        "target": "menu_monotributo",
    },
    {
        "keywords": ["recategorizacion", "recategorizarme", "cambiar categoria monotributo"],
        "target": "mono_recategorizacion",
    },
    {
        "keywords": ["baja monotributo", "dar de baja monotributo", "dejar monotributo"],
        "target": "mono_baja",
    },
    # Facturación
    {
        "keywords": ["factura", "facturar", "como facturo", "factura electronica", "emitir factura",
                     "hacer factura", "comprobante", "factura a", "factura b", "factura c"],
        "target": "menu_factura",
    },
    {
        "keywords": ["nota de credito", "nota de debito", "anular factura"],
        "target": "fact_notas",
    },
    {
        "keywords": ["punto de venta", "alta punto de venta", "habilitar punto de venta"],
        "target": "fact_punto_venta",
    },
    # CUIT
    {
        "keywords": ["cuit", "obtener cuit", "sacar cuit", "que es cuit", "cuil",
                     "diferencia cuit cuil", "necesito cuit"],
        "target": "arca_cuit",
    },
    # ARCA general
    {
        "keywords": ["que es arca", "arca que es", "afip", "que es afip", "arca ex afip"],
        "target": "arca_que_es",
    },
    {
        "keywords": ["tramites online", "tramites web", "que puedo hacer online", "que tramites",
                     "servicios arca", "servicios disponibles", "que servicios hay"],
        "target": "arca_tramites",
    },
    # Consulta CUIT
    {
        "keywords": ["consultar cuit", "buscar cuit", "datos cuit", "quien es cuit",
                     "averiguar cuit", "ver cuit", "informacion cuit"],
        "target": "arca_cuit",
    },
    # Vencimientos
    {
        "keywords": ["vencimiento", "vencimientos", "cuando vence", "fecha vencimiento",
                     "calendario fiscal", "cuando pago", "fecha pago"],
        "target": "arca_tramites",
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
    Busca el mejor match en KEYWORD_MAP para texto libre.
    Devuelve {"target": "callback_data"} o None.
    """
    texto_lower = texto.lower().strip()
    mejor_score = 0
    mejor_entry = None

    for entry in KEYWORD_MAP:
        score = 0
        for kw in entry["keywords"]:
            kw_lower = kw.lower()
            if kw_lower in texto_lower:
                score += len(kw_lower.split())
            else:
                palabras_kw = kw_lower.split()
                matches = sum(1 for p in palabras_kw if p in texto_lower)
                if matches > 0:
                    score += matches * 0.5

        if score > mejor_score:
            mejor_score = score
            mejor_entry = entry

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


def get_topic(topic_id: str) -> dict | None:
    """Devuelve un topic por su ID."""
    return TOPICS.get(topic_id)


def get_menu(menu_id: str) -> dict | None:
    """Devuelve un menú por su ID."""
    return MENUS.get(menu_id)
