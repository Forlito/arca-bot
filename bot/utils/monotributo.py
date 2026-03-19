"""
Calculadora de categorías de Monotributo.
Datos vigentes desde enero 2026 (se actualizan semestralmente).
Fuente: https://www.afip.gob.ar/monotributo/categorias.asp
"""

# Categorías vigentes enero 2026
# Formato: (categoria, ingreso_bruto_anual, cuota_mensual_servicios, cuota_mensual_productos)
CATEGORIAS = [
    {
        "id": "A",
        "ingreso_anual": 10_277_988.13,
        "cuota_servicios": 42_386.74,
        "cuota_productos": 42_386.74,
        "superficie": 30,
        "energia": 3330,
        "alquiler": 564_814.69,
    },
    {
        "id": "B",
        "ingreso_anual": 15_416_982.19,
        "cuota_servicios": 48_250.78,
        "cuota_productos": 48_250.78,
        "superficie": 45,
        "energia": 5000,
        "alquiler": 564_814.69,
    },
    {
        "id": "C",
        "ingreso_anual": 21_583_775.07,
        "cuota_servicios": 56_501.85,
        "cuota_productos": 55_671.85,
        "superficie": 60,
        "energia": 6700,
        "alquiler": 564_814.69,
    },
    {
        "id": "D",
        "ingreso_anual": 26_795_236.63,
        "cuota_servicios": 66_781.25,
        "cuota_productos": 64_463.25,
        "superficie": 85,
        "energia": 10_000,
        "alquiler": 564_814.69,
    },
    {
        "id": "E",
        "ingreso_anual": 31_596_247.41,
        "cuota_servicios": 94_941.77,
        "cuota_productos": 78_350.77,
        "superficie": 110,
        "energia": 13_000,
        "alquiler": 846_710.77,
    },
    {
        "id": "F",
        "ingreso_anual": 39_495_309.26,
        "cuota_servicios": 117_640.72,
        "cuota_productos": 94_833.72,
        "superficie": 150,
        "energia": 16_500,
        "alquiler": 846_710.77,
    },
    {
        "id": "G",
        "ingreso_anual": 47_394_371.11,
        "cuota_servicios": 140_122.10,
        "cuota_productos": 110_581.10,
        "superficie": 200,
        "energia": 20_000,
        "alquiler": 846_710.77,
    },
    {
        "id": "H",
        "ingreso_anual": 67_706_244.44,
        "cuota_servicios": 245_388.93,
        "cuota_productos": 214_399.93,
        "superficie": 200,
        "energia": 20_000,
        "alquiler": 1_128_947.69,
    },
    {
        "id": "I",
        "ingreso_anual": 81_247_493.33,
        "cuota_servicios": 330_710.10,
        "cuota_productos": 275_591.10,
        "superficie": 200,
        "energia": 20_000,
        "alquiler": 1_128_947.69,
    },
    {
        "id": "J",
        "ingreso_anual": 94_788_742.22,
        "cuota_servicios": 383_872.50,
        "cuota_productos": 319_893.50,
        "superficie": 200,
        "energia": 20_000,
        "alquiler": 1_128_947.69,
    },
    {
        "id": "K",
        "ingreso_anual": 108_357_084.05,
        "cuota_servicios": 437_034.91,
        "cuota_productos": 364_195.91,
        "superficie": 200,
        "energia": 20_000,
        "alquiler": 1_128_947.69,
    },
]

# Última actualización de las categorías
ULTIMA_ACTUALIZACION = "Enero 2026"


def calcular_categoria(ingreso_anual: float, tipo: str = "servicios") -> dict | None:
    """
    Determina la categoría de monotributo según ingreso anual y tipo de actividad.
    tipo: "servicios" o "productos"
    Retorna dict con la categoría o None si excede el tope.
    """
    for cat in CATEGORIAS:
        if ingreso_anual <= cat["ingreso_anual"]:
            cuota_key = f"cuota_{tipo}"
            return {
                "categoria": cat["id"],
                "ingreso_tope": cat["ingreso_anual"],
                "cuota_mensual": cat[cuota_key],
                "superficie_max": cat["superficie"],
                "energia_max": cat["energia"],
                "alquiler_max": cat["alquiler"],
            }
    return None


def formatear_resultado_calculo(ingreso_anual: float, tipo: str, resultado: dict | None) -> str:
    """Formatea el resultado del cálculo para Telegram."""
    tipo_texto = "Servicios" if tipo == "servicios" else "Productos"

    if resultado is None:
        tope = CATEGORIAS[-1]["ingreso_anual"]
        return (
            f"Con una facturación anual de ${ingreso_anual:,.2f} superás "
            f"el tope del Monotributo (${tope:,.2f}).\n\n"
            f"Tendrías que inscribirte como Responsable Inscripto.\n\n"
            f"Datos vigentes: {ULTIMA_ACTUALIZACION}"
        )

    return (
        f"Calculadora Monotributo ({tipo_texto}):\n\n"
        f"  Facturación anual estimada: ${ingreso_anual:,.2f}\n"
        f"  Categoría: {resultado['categoria']}\n"
        f"  Cuota mensual: ${resultado['cuota_mensual']:,.2f}\n"
        f"  Tope de ingresos: ${resultado['ingreso_tope']:,.2f}\n\n"
        f"  Límites de la categoría:\n"
        f"    Superficie: hasta {resultado['superficie_max']} m²\n"
        f"    Energía eléctrica: hasta {resultado['energia_max']:,} KW\n"
        f"    Alquiler anual: hasta ${resultado['alquiler_max']:,.2f}\n\n"
        f"Datos vigentes: {ULTIMA_ACTUALIZACION}\n"
        f"Los montos se actualizan en enero y julio."
    )


def formatear_tabla_categorias() -> str:
    """Muestra todas las categorías resumidas."""
    lines = [f"Categorías de Monotributo ({ULTIMA_ACTUALIZACION}):\n"]

    for cat in CATEGORIAS:
        lines.append(
            f"  {cat['id']}: hasta ${cat['ingreso_anual']:,.0f}/año "
            f"→ ${cat['cuota_servicios']:,.0f}/mes (serv) "
            f"| ${cat['cuota_productos']:,.0f}/mes (prod)"
        )

    lines.append(f"\nSi superás la K, tenés que pasar a Responsable Inscripto.")
    return "\n".join(lines)
