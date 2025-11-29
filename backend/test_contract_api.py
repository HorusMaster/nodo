"""
Script de prueba para el endpoint /generate-contract
"""

import requests
import json

# URL del endpoint
url = "http://localhost:8000/generate-contract"

# Datos de prueba completos
test_data_complete = {
    'receptor': 'EMPRESA EJEMPLO S.A. DE C.V.',
    'representante_receptor': 'Juan Pérez García',
    'banco_receptor': 'BBVA Bancomer',
    'cuenta_receptor': '0123456789',
    'clave_receptor': 'ABC123XYZ',
    'fecha': '2025-11-28',
    'hora_emision': '21:35:00'
}

# Datos de prueba incompletos
test_data_incomplete = {
    'receptor': 'OTRA EMPRESA S.A.',
    'fecha_hora_emision': '2025-11-28 15:30:00'
}

print("Probando endpoint /generate-contract...")
print("=" * 60)

# Test 1: Datos completos
print("\n1. Test con datos completos:")
try:
    response = requests.post(url, json=test_data_complete)
    if response.status_code == 200:
        with open("api_test_contrato_completo.docx", "wb") as f:
            f.write(response.content)
        print("   ✓ SUCCESS! Contrato generado: api_test_contrato_completo.docx")
    else:
        print(f"   ✗ Error: {response.status_code} - {response.text}")
except Exception as e:
    print(f"   ✗ Exception: {e}")

# Test 2: Datos incompletos
print("\n2. Test con datos incompletos (debería usar XXXXXXXXXX):")
try:
    response = requests.post(url, json=test_data_incomplete)
    if response.status_code == 200:
        with open("api_test_contrato_incompleto.docx", "wb") as f:
            f.write(response.content)
        print("   ✓ SUCCESS! Contrato generado: api_test_contrato_incompleto.docx")
    else:
        print(f"   ✗ Error: {response.status_code} - {response.text}")
except Exception as e:
    print(f"   ✗ Exception: {e}")

# Test 3: Formato de lista (como n8n)
print("\n3. Test con formato de lista (como n8n):")
try:
    response = requests.post(url, json=[test_data_complete])
    if response.status_code == 200:
        with open("api_test_contrato_lista.docx", "wb") as f:
            f.write(response.content)
        print("   ✓ SUCCESS! Contrato generado: api_test_contrato_lista.docx")
    else:
        print(f"   ✗ Error: {response.status_code} - {response.text}")
except Exception as e:
    print(f"   ✗ Exception: {e}")

print("\n" + "=" * 60)
print("¡Pruebas completadas! Revisa los archivos generados.")
