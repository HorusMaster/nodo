"""
Script para generar un contrato específico solicitado por el usuario.
"""

import sys
import os
import json

# Asegurar que podemos importar el generador
sys.path.insert(0, 'pantillas/LW')
from contrato_generator import generate_contract_docx

# Datos proporcionados por el usuario
data = [
  {
    "folio": "355",
    "emisor": "LEARN&WELL22",
    "receptor": "MANTENIMIENTO INDUSTRIAL Y COMERCIAL XICO",
    "rfc_receptor": "MIC191114530",
    "fecha_hora_emision": "2025-10-07T11:57:01",
    "subtotal": 14175,
    "IVA": 2268,
    "total_factura": 16443,
    "productos": [
      {
        "producto": "LOTE DE TELAS VARIAS 73141715 - SERVICIO DE COSTURA INDUSTRIAL 02- Sí Objeto de impuesto. LOTE DE TELAS VARIAS",
        "cantidad": 9450,
        "unidad": "E48",
        "precio_unitario": 14175,
        "importe": 14175
      }
    ]
  }
]

# Usar el primer elemento de la lista
contract_data = data[0]

# Ruta de la plantilla
template_path = "pantillas/LW/LW CONTRATO.docx"

print(f"Generando contrato para: {contract_data['receptor']}")
print(f"Fecha/Hora: {contract_data['fecha_hora_emision']}")

try:
    # Generar contrato
    output_stream = generate_contract_docx(contract_data, template_path)
    
    # Nombre del archivo de salida (con timestamp para evitar bloqueos)
    import time
    timestamp = int(time.time())
    output_filename = f"contrato_MANTENIMIENTO_INDUSTRIAL_XICO_{timestamp}.docx"
    
    # Guardar archivo
    with open(output_filename, "wb") as f:
        f.write(output_stream.read())
        
    print(f"✓ Contrato generado exitosamente: {output_filename}")
    print(f"Ubicación completa: {os.path.abspath(output_filename)}")
    
except Exception as e:
    print(f"✗ Error generando contrato: {e}")
    import traceback
    traceback.print_exc()
