"""
Calendario de vencimientos fiscales de ARCA.
Fuente: https://www.afip.gob.ar/vencimientos/

Los vencimientos de IVA y DDJJ se escalonan por terminación de CUIT.
Monotributo vence el 20 de cada mes (o siguiente hábil).
"""

from datetime import date, timedelta

# Vencimientos de IVA mensual por terminación de CUIT
# Día del mes siguiente al período fiscal
IVA_VENCIMIENTOS = {
    "0": 18, "1": 18,
    "2": 19, "3": 19,
    "4": 20, "5": 20,
    "6": 21, "7": 21,
    "8": 22, "9": 22,
}

# Vencimientos de DDJJ Ganancias/Bienes Personales (anuales, en junio)
GANANCIAS_VENCIMIENTOS = {
    "0": 13, "1": 13,
    "2": 14, "3": 14,
    "4": 15, "5": 15,
    "6": 16, "7": 16,
    "8": 17, "9": 17,
}

# Monotributo: siempre día 20
MONOTRIBUTO_DIA = 20

# Empleadores (F.931) por terminación de CUIT
F931_VENCIMIENTOS = {
    "0": 9, "1": 9,
    "2": 10, "3": 10,
    "4": 11, "5": 11,
    "6": 12, "7": 12,
    "8": 13, "9": 13,
}


def obtener_proximo_vencimiento(dia: int, hoy: date | None = None) -> date:
    """Calcula la próxima fecha de vencimiento a partir de hoy."""
    if hoy is None:
        hoy = date.today()

    # Si el día ya pasó este mes, va al mes siguiente
    try:
        fecha = hoy.replace(day=dia)
    except ValueError:
        # Mes con menos días (ej: feb 30 → mar)
        if hoy.month == 12:
            fecha = date(hoy.year + 1, 1, dia)
        else:
            fecha = date(hoy.year, hoy.month + 1, dia)

    if fecha < hoy:
        if fecha.month == 12:
            fecha = date(fecha.year + 1, 1, dia)
        else:
            try:
                fecha = date(fecha.year, fecha.month + 1, dia)
            except ValueError:
                fecha = date(fecha.year, fecha.month + 2, 1)

    return fecha


def obtener_vencimientos_generales(hoy: date | None = None) -> str:
    """Muestra los próximos vencimientos generales del mes."""
    if hoy is None:
        hoy = date.today()

    mes_nombre = _nombre_mes(hoy.month)

    lines = [
        f"Próximos vencimientos fiscales ({mes_nombre} {hoy.year}):\n",
        f"MONOTRIBUTO:",
        f"  Día {MONOTRIBUTO_DIA} de cada mes (todos los CUIT)\n",
        f"IVA (DDJJ mensual):",
    ]

    for term in ["0-1", "2-3", "4-5", "6-7", "8-9"]:
        first = term[0]
        dia = IVA_VENCIMIENTOS[first]
        lines.append(f"  CUIT terminado en {term}: día {dia}")

    lines.append(f"\nEMPLEADORES (F.931):")
    for term in ["0-1", "2-3", "4-5", "6-7", "8-9"]:
        first = term[0]
        dia = F931_VENCIMIENTOS[first]
        lines.append(f"  CUIT terminado en {term}: día {dia}")

    lines.append(
        f"\nPara ver tus vencimientos específicos usá:\n"
        f"  /vencimientos <terminación de CUIT>\n"
        f"  Ejemplo: /vencimientos 3"
    )

    return "\n".join(lines)


def obtener_vencimientos_por_terminacion(terminacion: str, hoy: date | None = None) -> str:
    """Muestra los próximos vencimientos para una terminación de CUIT."""
    if hoy is None:
        hoy = date.today()

    if terminacion not in "0123456789":
        return "La terminación de CUIT debe ser un número del 0 al 9."

    mono_fecha = obtener_proximo_vencimiento(MONOTRIBUTO_DIA, hoy)
    iva_dia = IVA_VENCIMIENTOS[terminacion]
    iva_fecha = obtener_proximo_vencimiento(iva_dia, hoy)
    f931_dia = F931_VENCIMIENTOS[terminacion]
    f931_fecha = obtener_proximo_vencimiento(f931_dia, hoy)

    lines = [
        f"Próximos vencimientos para CUIT terminado en {terminacion}:\n",
        f"  Monotributo: {_formato_fecha(mono_fecha)}",
        f"  IVA (DDJJ mensual): {_formato_fecha(iva_fecha)}",
        f"  Empleadores (F.931): {_formato_fecha(f931_fecha)}",
        f"\nRecordá que si el vencimiento cae en feriado o fin de semana,",
        f"se traslada al siguiente día hábil.",
        f"\nFuente: afip.gob.ar/vencimientos",
    ]

    return "\n".join(lines)


def _formato_fecha(fecha: date) -> str:
    """Formatea una fecha como 'lunes 20 de marzo'."""
    dias = ["lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"]
    dia_semana = dias[fecha.weekday()]
    mes = _nombre_mes(fecha.month)
    return f"{dia_semana} {fecha.day} de {mes}"


def _nombre_mes(mes: int) -> str:
    meses = [
        "", "enero", "febrero", "marzo", "abril", "mayo", "junio",
        "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"
    ]
    return meses[mes]
