"""
Validación de CUIT/CUIL argentino.
Formato: XX-XXXXXXXX-X (11 dígitos, verificación módulo 11).
"""


def validar_cuit(cuit: str) -> tuple[bool, str]:
    """
    Valida un CUIT/CUIL argentino.
    Acepta formatos: 20-12345678-9, 20123456789, 20 12345678 9
    Retorna (es_valido, cuit_limpio_o_error).
    """
    # Limpiar: quitar guiones, espacios, puntos
    limpio = cuit.replace("-", "").replace(" ", "").replace(".", "")

    if not limpio.isdigit():
        return False, "El CUIT debe contener solo números."

    if len(limpio) != 11:
        return False, "El CUIT debe tener 11 dígitos."

    # Verificar prefijo válido
    prefijo = int(limpio[:2])
    prefijos_validos = {20, 23, 24, 27, 30, 33, 34}
    if prefijo not in prefijos_validos:
        return False, f"Prefijo {prefijo} no es válido para CUIT/CUIL."

    # Verificación módulo 11
    multiplicadores = [5, 4, 3, 2, 7, 6, 5, 4, 3, 2]
    suma = sum(int(limpio[i]) * multiplicadores[i] for i in range(10))
    resto = 11 - (suma % 11)

    if resto == 11:
        digito_esperado = 0
    elif resto == 10:
        digito_esperado = 9
    else:
        digito_esperado = resto

    digito_real = int(limpio[10])

    if digito_real != digito_esperado:
        return False, "El dígito verificador no es correcto."

    return True, limpio


def formatear_cuit(cuit: str) -> str:
    """Formatea un CUIT limpio como XX-XXXXXXXX-X."""
    return f"{cuit[:2]}-{cuit[2:10]}-{cuit[10]}"
