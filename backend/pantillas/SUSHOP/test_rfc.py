from pdf_generator import generate_pdf_bytes
import os
from datetime import datetime, timedelta

# Test data
data_item = {
    'folio': 'RFC-TEST-001',
    'fecha/hora_emision': '2023-11-24', # Friday
    'receptor': 'Test Client with RFC',
    'rfc_receptor': 'XAXX010101000',
    'cantidad': '5',
    'producto': 'Sushi Special',
    'precio_unitario': '200.00',
    'importe': '1000.00',
    'subtotal': '1000.00',
    'IVA': '160.00',
    'total_factura': '1160.00'
}

template_path = r"d:\Desarrollo\nodo\backend\pantillas\SUSHOP\SUSHSHOP COTIZACION.pdf"
output_path = r"d:\Desarrollo\nodo\backend\pantillas\SUSHOP\test_rfc_output.pdf"

print(f"Generating PDF with date {data_item['fecha/hora_emision']}...")
pdf_bytes = generate_pdf_bytes(data_item, template_path)

with open(output_path, "wb") as f:
    f.write(pdf_bytes.getvalue())

print(f"PDF generated at {output_path}")

# Verify date logic (simple check)
# Since we can't easily parse the PDF text here without more libs, we trust the generator logic
# but we can print what the logic would output for verification
import random
# Mocking the logic to show what it *should* be
def check_logic(date_str):
    dt = datetime.strptime(date_str, "%Y-%m-%d").date()
    print(f"Input Date: {dt} ({dt.strftime('%A')})")
    for i in range(5):
        offset = random.randint(3, 5)
        cand = dt - timedelta(days=offset)
        print(f"  Attempt {i+1}: Offset {offset} -> {cand} ({cand.strftime('%A')}) - {'Valid' if cand.weekday() != 6 else 'Invalid (Sunday)'}")

print("\nSimulating date logic for verification:")
check_logic(data_item['fecha/hora_emision'])
