"""
Clasificación Internacional de Niza (45 clases).
Usada mundialmente para clasificar marcas.
"""

CLASES_NIZA = {
    1: "Productos químicos para la industria, ciencia, fotografía, agricultura",
    2: "Pinturas, barnices, lacas; protección contra la corrosión",
    3: "Cosméticos, productos de limpieza, perfumería",
    4: "Aceites y grasas industriales, lubricantes, combustibles",
    5: "Productos farmacéuticos, veterinarios, desinfectantes",
    6: "Metales comunes y sus aleaciones, materiales de construcción metálicos",
    7: "Máquinas y máquinas herramientas, motores",
    8: "Herramientas e instrumentos de mano",
    9: "Aparatos e instrumentos científicos, electrónicos, informáticos, software",
    10: "Aparatos e instrumentos médicos, quirúrgicos, dentales",
    11: "Aparatos de alumbrado, calefacción, refrigeración",
    12: "Vehículos, aparatos de locomoción terrestre, aérea o acuática",
    13: "Armas de fuego, municiones, explosivos, fuegos artificiales",
    14: "Metales preciosos, joyería, relojería",
    15: "Instrumentos musicales",
    16: "Papel, cartón, artículos de oficina, imprenta",
    17: "Caucho, goma, plásticos en bruto, materiales de aislamiento",
    18: "Cuero, equipaje, bolsos, paraguas",
    19: "Materiales de construcción no metálicos (cemento, madera, asfalto)",
    20: "Muebles, espejos, marcos, productos de madera/plástico/corcho",
    21: "Utensilios de cocina, cristalería, porcelana, cerámica",
    22: "Cuerdas, redes, tiendas de campaña, toldos, lonas",
    23: "Hilos para uso textil",
    24: "Tejidos y productos textiles (ropa de cama, mesa)",
    25: "Vestimenta, calzado, sombrerería",
    26: "Puntillas, bordados, cintas, botones, alfileres",
    27: "Alfombras, felpudos, revestimientos de suelos",
    28: "Juegos, juguetes, artículos de gimnasia y deporte",
    29: "Carne, pescado, frutas y legumbres en conserva, lácteos, aceites",
    30: "Café, té, azúcar, arroz, harinas, pan, pastelería, chocolate",
    31: "Productos agrícolas, granos, frutas y verduras frescas, plantas",
    32: "Cervezas, aguas minerales, jugos de frutas, bebidas sin alcohol",
    33: "Bebidas alcohólicas (excepto cervezas)",
    34: "Tabaco, artículos para fumadores",
    35: "Publicidad, gestión comercial, administración de empresas, retail",
    36: "Seguros, negocios financieros, negocios inmobiliarios, criptomonedas",
    37: "Construcción, reparación, servicios de instalación",
    38: "Telecomunicaciones",
    39: "Transporte, almacenamiento, organización de viajes",
    40: "Tratamiento de materiales, reciclaje, impresión",
    41: "Educación, formación, entretenimiento, actividades deportivas/culturales",
    42: "Servicios científicos/tecnológicos, diseño industrial, software, SaaS",
    43: "Servicios de restauración, hospedaje (hoteles, bares, restaurantes)",
    44: "Servicios médicos, veterinarios, agricultura, jardinería",
    45: "Servicios jurídicos, seguridad, servicios personales y sociales",
}


def obtener_clase(numero: int) -> str | None:
    """Devuelve la descripción de una clase Niza, o None si no existe."""
    return CLASES_NIZA.get(numero)


def buscar_clases_por_keyword(keyword: str) -> list[tuple[int, str]]:
    """Busca clases que contengan una palabra clave en su descripción."""
    keyword = keyword.lower()
    return [
        (num, desc)
        for num, desc in CLASES_NIZA.items()
        if keyword in desc.lower()
    ]


def sugerir_clases(actividad: str) -> list[tuple[int, str]]:
    """
    Sugiere clases Niza basadas en una descripción de actividad.
    Busca por palabras clave en la descripción.
    """
    palabras = actividad.lower().split()
    resultados = set()
    for palabra in palabras:
        if len(palabra) < 3:
            continue
        for num, desc in CLASES_NIZA.items():
            if palabra in desc.lower():
                resultados.add((num, desc))
    return sorted(resultados, key=lambda x: x[0])
