import requests
import json

url = "http://127.0.0.1:8000/generate-pdf"

payload = {
    "folio": "API-TEST-002",
    "emisor": "SUSHOP",
    "receptor": "API Client Fixed",
    "fecha/hora_emision": "2023-11-24",
    "subtotal": 500.0,
    "IVA": 80.0,
    "total_factura": 580.0,
    "productos": [
        {
            "producto": "Sushi Roll Deluxe",
            "cantidad": 2,
            "unidad": "pz",
            "precio_unitario": 250.0,
            "importe": 500.0
        }
    ]
}

print(f"Sending request to {url}...")
try:
    response = requests.post(url, json=payload)
    
    if response.status_code == 200:
        output_path = "api_test_output_fixed.pdf"
        with open(output_path, "wb") as f:
            f.write(response.content)
        print(f"Success! PDF saved to {output_path}")
    else:
        print(f"Failed with status {response.status_code}")
        print(response.text)
except Exception as e:
    print(f"Error: {e}")
    print("Make sure the server is running (uvicorn main:app --reload)")
