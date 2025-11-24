from pypdf import PdfReader

def find_coordinates(pdf_path, keywords):
    reader = PdfReader(pdf_path)
    page = reader.pages[0]
    
    found_coords = {}
    
    def visitor_body(text, cm, tm, fontDict, fontSize):
        x = tm[4]
        y = tm[5]
        # Check if any keyword is in the current text chunk
        for key in keywords:
            if key.lower() in text.lower():
                print(f"Found '{key}' in text '{text.strip()}' at ({x}, {y})")
                found_coords[key] = (x, y)
    
    page.extract_text(visitor_text=visitor_body)
    return found_coords

pdf_path = r"d:\Desarrollo\nodo\backend\pantillas\SUSHOP\SUSHSHOP COTIZACION.pdf"
keywords = [
    "RFC", "R.F.C.", "Dirección", "Cliente"
]

print(f"Scanning {pdf_path}...")
coords = find_coordinates(pdf_path, keywords)
print("\nFinal Found Coordinates:")
for k, v in coords.items():
    print(f"{k}: {v}")
