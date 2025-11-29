"""
Script de prueba para el generador de contratos DOCX.
"""

import sys
sys.path.insert(0, 'pantillas/LW')
from contrato_generator import generate_contract_docx

# Datos de prueba simulando lo que vendría de n8n
test_data = {
    'receptor': 'EMPRESA EJEMPLO S.A. DE C.V.',
    'representante_receptor': 'Juan Pérez García',
    'banco_receptor': 'BBVA Bancomer',
    'cuenta_receptor': '0123456789',
    'clave_receptor': 'ABC123XYZ',
    'fecha': '2025-11-28',
    'hora_emision': '21:35:00'
}

# Datos de prueba con campos faltantes
test_data_incomplete = {
    'receptor': 'OTRA EMPRESA S.A.',
    'fecha_hora_emision': '2025-11-28 15:30:00'
    # Faltan: representante_receptor, banco_receptor, cuenta_receptor, clave_receptor
}

template_path = "pantillas/LW/LW CONTRATO.docx"

print("Generando contrato con datos completos...")
try:
    output1 = generate_contract_docx(test_data, template_path)
    with open("test_contrato_completo.docx", "wb") as f:
        f.write(output1.read())
    print("✓ Contrato completo generado: test_contrato_completo.docx")
except Exception as e:
    print(f"✗ Error: {e}")
    import traceback
    traceback.print_exc()

print("\nGenerando contrato con datos incompletos (debería usar XXXXXXXXXX)...")
try:
    output2 = generate_contract_docx(test_data_incomplete, template_path)
    with open("test_contrato_incompleto.docx", "wb") as f:
        f.write(output2.read())
    print("✓ Contrato incompleto generado: test_contrato_incompleto.docx")
except Exception as e:
    print(f"✗ Error: {e}")
    import traceback
    traceback.print_exc()

print("\n¡Pruebas completadas! Revisa los archivos generados.")
