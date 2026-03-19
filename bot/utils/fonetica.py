"""
Similitud fonética para marcas en español.
Adaptación de Soundex/Metaphone para el castellano rioplatense.
"""

import re


def codigo_fonetico(texto: str) -> str:
    """
    Genera un código fonético para un texto en español.
    Normaliza para detectar similitudes como KAVANA/CABANA, XENON/SENON, etc.
    """
    texto = texto.upper().strip()
    texto = re.sub(r"[^A-ZÑ]", "", texto)

    if not texto:
        return ""

    # Reemplazos fonéticos del español
    reemplazos = [
        # Letras que suenan igual
        ("V", "B"),
        ("W", "B"),
        ("X", "S"),
        ("Z", "S"),
        ("CE", "SE"),
        ("CI", "SI"),
        ("GE", "JE"),
        ("GI", "JI"),
        ("QU", "K"),
        ("CU", "KU"),
        ("CA", "KA"),
        ("CO", "KO"),
        ("CK", "K"),
        ("C", "K"),
        ("PH", "F"),
        ("SH", "S"),
        ("Y", "I"),
        ("LL", "I"),
        ("Ñ", "NI"),
        # H muda
        ("H", ""),
    ]

    resultado = texto
    for viejo, nuevo in reemplazos:
        resultado = resultado.replace(viejo, nuevo)

    # Eliminar letras dobles consecutivas
    limpio = ""
    for char in resultado:
        if not limpio or char != limpio[-1]:
            limpio += char

    return limpio


def similitud_fonetica(nombre1: str, nombre2: str) -> float:
    """
    Calcula similitud fonética entre dos nombres (0.0 a 1.0).
    1.0 = idénticos fonéticamente.
    """
    cod1 = codigo_fonetico(nombre1)
    cod2 = codigo_fonetico(nombre2)

    if not cod1 or not cod2:
        return 0.0

    if cod1 == cod2:
        return 1.0

    # Distancia de Levenshtein normalizada
    distancia = _levenshtein(cod1, cod2)
    max_len = max(len(cod1), len(cod2))
    return 1.0 - (distancia / max_len)


def encontrar_similares_foneticos(
    nombre: str,
    resultados: list,
    umbral: float = 0.7,
) -> list:
    """
    Filtra resultados que son fonéticamente similares al nombre buscado.
    resultados: lista de MarcaResult.
    umbral: mínimo de similitud (0.0 a 1.0).
    """
    similares = []
    for marca in resultados:
        sim = similitud_fonetica(nombre, marca.denominacion)
        if sim >= umbral and marca.denominacion.upper().strip() != nombre.upper().strip():
            similares.append((marca, sim))

    # Ordenar por similitud descendente
    similares.sort(key=lambda x: x[1], reverse=True)
    return similares


def _levenshtein(s1: str, s2: str) -> int:
    """Distancia de Levenshtein entre dos strings."""
    if len(s1) < len(s2):
        return _levenshtein(s2, s1)

    if len(s2) == 0:
        return len(s1)

    prev_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        curr_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = prev_row[j + 1] + 1
            deletions = curr_row[j] + 1
            substitutions = prev_row[j] + (c1 != c2)
            curr_row.append(min(insertions, deletions, substitutions))
        prev_row = curr_row

    return prev_row[-1]
