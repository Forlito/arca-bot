"""
Formatea resultados del INPI para mensajes de Telegram.
Usa MarkdownV2 de Telegram.
"""

from bot.scrapers.parser import MarcaResult


def escapar_md(text: str) -> str:
    """Escapa caracteres especiales para MarkdownV2 de Telegram."""
    chars = r"_*[]()~`>#+-=|{}.!"
    for c in chars:
        text = text.replace(c, f"\\{c}")
    return text


def formatear_resultados(
    query: str,
    resultados: list[MarcaResult],
    solo_vigentes: bool = True,
    max_mostrar: int = 10,
) -> str:
    """Formatea una lista de resultados de marcas para Telegram."""
    if not resultados:
        filtro = " \\(solo vigentes\\)" if solo_vigentes else ""
        return (
            f"🔍 No se encontraron marcas para "
            f"*{escapar_md(query)}*{filtro}\\.\n\n"
            f"Esto no garantiza disponibilidad\\. "
            f"El INPI puede denegar por similitud fonética\\."
        )

    total = len(resultados)
    mostrar = resultados[:max_mostrar]
    filtro = " \\(solo vigentes\\)" if solo_vigentes else ""

    lines = [
        f"🔍 *{escapar_md(query)}*{filtro}: {total} resultado{'s' if total != 1 else ''}\n"
    ]

    for i, m in enumerate(mostrar, 1):
        estado = escapar_md(m.estado_legible)
        nombre = escapar_md(m.denominacion)
        titular = escapar_md(_acortar_titular(m.titulares))
        venc = escapar_md(m.vencimiento) if m.vencimiento else "\\-"

        lines.append(
            f"*{i}\\.* {nombre}\n"
            f"   Clase {escapar_md(m.clase)} \\| {estado} \\| Vence: {venc}\n"
            f"   Titular: {titular}\n"
        )

    if total > max_mostrar:
        resto = total - max_mostrar
        lines.append(f"\n_\\.\\.\\.y {resto} resultado{'s' if resto != 1 else ''} más\\._")

    return "\n".join(lines)


def formatear_disponibilidad(nombre: str, resultado: dict) -> str:
    """Formatea el resultado de verificar_disponibilidad para Telegram."""
    nombre_esc = escapar_md(nombre)
    exactas = resultado["exactas"]
    similares = resultado["similares"]
    disponible = resultado["disponible"]

    if disponible and not similares:
        msg = (
            f"✅ *{nombre_esc}* no tiene coincidencias exactas vigentes\\.\n\n"
            f"Podría estar disponible, pero esto es orientativo\\.\n"
        )
    elif disponible and similares:
        msg = (
            f"⚠️ *{nombre_esc}* no tiene coincidencia exacta, "
            f"pero hay {len(similares)} marca{'s' if len(similares) != 1 else ''} similar{'es' if len(similares) != 1 else ''}:\n\n"
        )
        for m in similares[:5]:
            msg += f"  • {escapar_md(m.denominacion)} \\(Clase {escapar_md(m.clase)}\\)\n"
    else:
        msg = (
            f"❌ *{nombre_esc}* ya está registrada:\n\n"
        )
        for m in exactas[:3]:
            msg += (
                f"  • Clase {escapar_md(m.clase)} \\| {escapar_md(m.estado_legible)}\n"
                f"    Titular: {escapar_md(_acortar_titular(m.titulares))}\n"
                f"    Vence: {escapar_md(m.vencimiento)}\n\n"
            )

    msg += f"\n⚖️ _{escapar_md(resultado['disclaimer'])}_"
    return msg


def _acortar_titular(titular: str, max_len: int = 50) -> str:
    """Acorta el texto del titular para que entre en el mensaje."""
    # Sacar el CUIT del principio si existe
    partes = titular.split(" ", 1)
    if len(partes) > 1 and partes[0].replace(".", "").isdigit():
        titular = partes[1]

    # Sacar porcentaje del final
    if "100.00%" in titular:
        titular = titular.replace("100.00%", "").strip()

    if len(titular) > max_len:
        return titular[:max_len] + "..."
    return titular
