import requests

# Test directo a n8n
n8n_url = "https://n8n.redinmex.com/webhook/86ce68b9-267c-4d46-b4c7-6651bffc116e"

# Crear un archivo de prueba
test_file_content = b"Test file content"
files = [('files', ('test.txt', test_file_content, 'text/plain'))]

print(f"Enviando archivo de prueba a: {n8n_url}")
print(f"Archivo: test.txt")

try:
    response = requests.post(n8n_url, files=files)
    print(f"\nStatus Code: {response.status_code}")
    print(f"Response Headers: {dict(response.headers)}")
    print(f"Response Body: {response.text}")
    
    if response.status_code == 200:
        print("\n✓ Éxito! El archivo llegó a n8n")
    else:
        print(f"\n✗ Error: n8n respondió con status {response.status_code}")
        
except Exception as e:
    print(f"\n✗ Error al conectar con n8n: {e}")
