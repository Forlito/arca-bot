"""
Test del parser de resultados del INPI.
Usa HTML de ejemplo capturado del portal real.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from bot.scrapers.parser import parsear_resultados as _parsear_resultados, MarcaResult


# HTML de ejemplo capturado del portal real del INPI
# Búsqueda: "COCA COLA", solo vigentes
SAMPLE_HTML = """
<html><body>
<table id="tblGrillaMarcas" class="table table-hover">
<tr>
  <th>NRO ACTA</th><th>TITULARES ASIGNADOS</th><th>FECHA INGRESO</th>
  <th>CLASE</th><th>DENOMINACION</th><th>TIPO DE MARCA</th>
  <th>NRO RESOLUCION</th><th>ESTADO</th><th>VENCIMIENTO</th><th></th>
</tr>
<tr>
  <td>3526042</td>
  <td>THE COCA-COLA COMPANY 100.00%</td>
  <td>28/07/2016</td>
  <td>42</td>
  <td>COCA COLA FM FOR ME</td>
  <td>Mixta</td>
  <td>2882733</td>
  <td>C</td>
  <td>12/04/2027</td>
  <td></td>
</tr>
<tr>
  <td>4225106</td>
  <td>THE COCA-COLA COMPANY 100.00%</td>
  <td>09/03/2023</td>
  <td>25</td>
  <td>COCA COLA</td>
  <td>Mixta</td>
  <td>3403168</td>
  <td>C</td>
  <td>30/04/2033</td>
  <td></td>
</tr>
<tr>
  <td>4511773</td>
  <td>0 THE COCA-COLA COMPANY 100.00%</td>
  <td>21/05/2025</td>
  <td>32</td>
  <td>COCA COLA</td>
  <td>Mixta</td>
  <td>3696314</td>
  <td>C</td>
  <td>18/08/2035</td>
  <td></td>
</tr>
</table>
</body></html>
"""

# HTML vacío (sin resultados)
EMPTY_HTML = """
<html><body>
<table id="tblGrillaMarcas" class="table table-hover">
<tr>
  <th>NRO ACTA</th><th>TITULARES ASIGNADOS</th><th>FECHA INGRESO</th>
  <th>CLASE</th><th>DENOMINACION</th><th>TIPO DE MARCA</th>
  <th>NRO RESOLUCION</th><th>ESTADO</th><th>VENCIMIENTO</th><th></th>
</tr>
</table>
</body></html>
"""

# HTML sin tabla (INPI caído o error)
NO_TABLE_HTML = "<html><body><h1>Error</h1></body></html>"


def test_parsear_resultados():
    """Verifica que el parser extrae las marcas correctamente."""
    resultados = _parsear_resultados(SAMPLE_HTML)

    assert len(resultados) == 3, f"Esperaba 3 resultados, obtuve {len(resultados)}"

    # Verificar primer resultado
    r0 = resultados[0]
    assert r0.nro_acta == "3526042"
    assert "COCA-COLA COMPANY" in r0.titulares
    assert r0.clase == "42"
    assert r0.denominacion == "COCA COLA FM FOR ME"
    assert r0.tipo_marca == "Mixta"
    assert r0.estado == "C"
    assert r0.estado_legible == "Concedida"
    assert r0.esta_vigente is True
    assert r0.vencimiento == "12/04/2027"

    # Verificar que "COCA COLA" exacto aparece
    r1 = resultados[1]
    assert r1.denominacion == "COCA COLA"
    assert r1.clase == "25"

    print("OK: test_parsear_resultados")


def test_parsear_sin_resultados():
    """Verifica que HTML vacío devuelve lista vacía."""
    resultados = _parsear_resultados(EMPTY_HTML)
    assert len(resultados) == 0, f"Esperaba 0 resultados, obtuve {len(resultados)}"
    print("OK: test_parsear_sin_resultados")


def test_parsear_sin_tabla():
    """Verifica que HTML sin tabla devuelve lista vacía."""
    resultados = _parsear_resultados(NO_TABLE_HTML)
    assert len(resultados) == 0, f"Esperaba 0 resultados, obtuve {len(resultados)}"
    print("OK: test_parsear_sin_tabla")


def test_estado_legible():
    """Verifica la traducción de estados."""
    marca = MarcaResult(
        nro_acta="1", titulares="", fecha_ingreso="", clase="1",
        denominacion="TEST", tipo_marca="", nro_resolucion="",
        estado="E", vencimiento=""
    )
    assert marca.estado_legible == "En Trámite"
    assert marca.esta_vigente is False

    marca.estado = "C"
    assert marca.estado_legible == "Concedida"
    assert marca.esta_vigente is True

    marca.estado = "N"
    assert marca.estado_legible == "Denegada"

    marca.estado = "XYZ"
    assert marca.estado_legible == "XYZ"  # desconocido devuelve original

    print("OK: test_estado_legible")


if __name__ == "__main__":
    test_parsear_resultados()
    test_parsear_sin_resultados()
    test_parsear_sin_tabla()
    test_estado_legible()
    print("\n=== Todos los tests pasaron ===")
