"""
Parser de resultados del INPI.
Separado del HTTP client para poder testear sin dependencias externas.
"""

from bs4 import BeautifulSoup
from dataclasses import dataclass


@dataclass
class MarcaResult:
    nro_acta: str
    titulares: str
    fecha_ingreso: str
    clase: str
    denominacion: str
    tipo_marca: str
    nro_resolucion: str
    estado: str
    vencimiento: str

    @property
    def estado_legible(self) -> str:
        estados = {
            "C": "Concedida",
            "E": "En Trámite",
            "N": "Denegada",
            "A": "Abandonada",
            "CA": "Caduca",
            "D": "Desistida",
            "NU": "Nula",
        }
        return estados.get(self.estado, self.estado)

    @property
    def esta_vigente(self) -> bool:
        return self.estado == "C"


def parsear_resultados(html: str) -> list[MarcaResult]:
    """Parsea el HTML de resultados del INPI y extrae las marcas."""
    soup = BeautifulSoup(html, "lxml")

    # La tabla de datos es #tblGrillaMarcas (hay varias tablas en la página)
    tabla = soup.find("table", id="tblGrillaMarcas")
    if not tabla:
        # Fallback: buscar cualquier tabla con las columnas esperadas
        for t in soup.find_all("table"):
            header = t.find("th")
            if header and "NRO ACTA" in header.get_text():
                rows = t.find_all("tr")
                if len(rows) > 1:
                    tabla = t
                    break

    if not tabla:
        return []

    filas = tabla.find_all("tr")
    resultados = []

    for fila in filas[1:]:  # skip header row
        celdas = fila.find_all("td")
        if len(celdas) < 9:
            continue

        resultado = MarcaResult(
            nro_acta=celdas[0].get_text(strip=True),
            titulares=celdas[1].get_text(strip=True),
            fecha_ingreso=celdas[2].get_text(strip=True),
            clase=celdas[3].get_text(strip=True),
            denominacion=celdas[4].get_text(strip=True),
            tipo_marca=celdas[5].get_text(strip=True),
            nro_resolucion=celdas[6].get_text(strip=True),
            estado=celdas[7].get_text(strip=True),
            vencimiento=celdas[8].get_text(strip=True),
        )
        resultados.append(resultado)

    return resultados
