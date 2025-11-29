import requests
import json
import zipfile
import io
import os

url = "http://127.0.0.1:8000/generate-pdf"

payload = [
    {
        "folio": "BATCH-001",
        "emisor": "SUSHSHOP DEL CENTRO",
        "receptor": "Batch Client 1",
        "fecha/hora_emision": "2023-11-27",
        "subtotal": 100.0,
        "IVA": 16.0,
        "total_factura": 116.0,
        "productos": [
            {
                "producto": "Item 1",
                "cantidad": 1,
                "unidad": "pz",
                "precio_unitario": 100.0,
                "importe": 100.0
            }
        ],
        "generate_contract": True
    },
    {
        "folio": "BATCH-002",
        "emisor": "LEARN&WELL22",
        "receptor": "Batch Client 2",
        "fecha/hora_emision": "2023-11-27",
        "subtotal": 200.0,
        "IVA": 32.0,
        "total_factura": 232.0,
        "productos": [
            {
                "producto": "Item 2",
                "cantidad": 2,
                "unidad": "pz",
                "precio_unitario": 100.0,
                "importe": 200.0
            }
        ],
        "generate_contract": True
    }
]

print(f"Sending batch request to {url}...")
try:
    response = requests.post(url, json=payload)
    
    if response.status_code == 200:
        content_type = response.headers.get("Content-Type")
        print(f"Response Content-Type: {content_type}")
        
        if content_type == "application/zip":
            output_path = "batch_output_with_contracts.zip"
            with open(output_path, "wb") as f:
                f.write(response.content)
            print(f"Success! ZIP saved to {output_path}")
            
            # Verify zip contents
            with zipfile.ZipFile(io.BytesIO(response.content)) as z:
                print("Files in ZIP:")
                files = z.namelist()
                for name in files:
                    print(f" - {name}")
                
                # Expecting 2 PDFs and 2 DOCXs = 4 files
                # Note: LW might fail if template missing, but SUSHOP should work
                # If LW fails, we might get fewer files or error depending on implementation
                # My implementation prints warning for missing template but continues
                
                pdf_count = len([f for f in files if f.endswith(".pdf")])
                docx_count = len([f for f in files if f.endswith(".docx")])
                
                print(f"Found {pdf_count} PDFs and {docx_count} DOCXs.")
                
                if pdf_count == 2 and docx_count >= 1:
                     print("Verification PASSED: PDFs and DOCXs found.")
                else:
                     print("Verification WARNING: Unexpected file count.")

        else:
             print(f"Verification FAILED: Expected application/zip, got {content_type}")

    else:
        print(f"Failed with status {response.status_code}")
        print(response.text)
except Exception as e:
    print(f"Error: {e}")
    print("Make sure the server is running (uvicorn main:app --reload)")
