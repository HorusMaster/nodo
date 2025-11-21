import io
import json
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from pypdf import PdfReader, PdfWriter

# Data to populate
data = [
    {
        "folio": "A-355",
        "emisor": "LEARN&WELL22",
        "receptor": "MANTENIMIENTO INDUSTRIAL Y COMERCIAL XICO",
        "fecha/hora_emision": "2025-10-07T11:57:01",
        "producto": "LOTE DE TELAS VARIAS",
        "cantidad": 1.5,
        "unidad": "E48",
        "precio_unitario": 9450,
        "importe": 14175,
        "subtotal": 14175,
        "IVA": 2268,
        "total_factura": 16443
    }
]

def find_coordinates(pdf_path, keywords):
    """
    Scans the first page of the PDF for keywords and returns their coordinates.
    Returns a dict: {keyword: (x, y)}
    """
    reader = PdfReader(pdf_path)
    page = reader.pages[0]
    
    found_coords = {}
    
    def visitor_body(text, cm, tm, fontDict, fontSize):
        x = tm[4]
        y = tm[5]
        # Check if any keyword is in the current text chunk
        for key in keywords:
            if key.lower() in text.lower():
                # Store the coordinate. We might find multiple, take the last one or first?
                # Usually labels are unique.
                found_coords[key] = (x, y)
    
    page.extract_text(visitor_text=visitor_body)
    return found_coords

def create_overlay(data_dict, coords, output_filename="overlay.pdf"):
    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=letter)
    can.setFont("Helvetica", 10)
    can.setFillColorRGB(0, 0, 0) 

    item = data_dict[0]

    # Helper to draw text relative to found coordinates
    def draw_relative(label_key, value, offset_x=0, offset_y=0):
        if label_key in coords:
            x, y = coords[label_key]
            # Default: Place text to the right of the label
            can.drawString(x + offset_x, y + offset_y, str(value))
            print(f"Placed '{value}' relative to '{label_key}' at ({x+offset_x}, {y+offset_y})")
        else:
            print(f"WARNING: Label '{label_key}' not found in PDF. Skipping '{value}'")

    # --- MAPPING CONFIGURATION ---
    
    # Header Info
    draw_relative("Folio", item['folio'], offset_x=35) 
    draw_relative("Fecha", item['fecha/hora_emision'], offset_x=35)
    
    # Emisor: Search for "expedición" to avoid newline issues
    draw_relative("expedición", item['emisor'], offset_x=0, offset_y=20)

    # Receptor -> "Cliente"
    draw_relative("Cliente", item['receptor'], offset_x=40, offset_y=0) 

    # Table Columns
    row_y_offset = -20 
    
    draw_relative("Cantidad", item['cantidad'], offset_x=0, offset_y=row_y_offset)
    
    draw_relative("Descripción", item['producto'], offset_x=0, offset_y=row_y_offset) 
    draw_relative("Precio Unitario", f"${item['precio_unitario']}", offset_x=0, offset_y=row_y_offset)
    
    # Importe fallback: if not found or 0, place relative to Precio
    if "Importe" in coords and coords["Importe"][0] > 10:
        draw_relative("Importe", f"${item['importe']}", offset_x=0, offset_y=row_y_offset)
    elif "Precio Unitario" in coords:
        # Estimate Importe is ~100 units to the right of Precio
        precio_x, precio_y = coords["Precio Unitario"]
        can.drawString(precio_x + 100, precio_y + row_y_offset, f"${item['importe']}")
        print(f"Placed '${item['importe']}' relative to 'Precio Unitario' (fallback for Importe)")

    # Totals
    draw_relative("Subtotal", f"${item['subtotal']}", offset_x=60)
    draw_relative("Iva", f"${item['IVA']}", offset_x=60) # Note 'Iva' in PDF vs 'IVA' in JSON key
    draw_relative("Total", f"${item['total_factura']}", offset_x=60)

    can.save()
    packet.seek(0)
    return packet

def merge_pdfs(template_path, overlay_packet, output_path):
    existing_pdf = PdfReader(open(template_path, "rb"))
    output = PdfWriter()
    new_pdf = PdfReader(overlay_packet)
    page = existing_pdf.pages[0]
    page.merge_page(new_pdf.pages[0])
    output.add_page(page)
    with open(output_path, "wb") as outputStream:
        output.write(outputStream)
    print(f"Generated {output_path}")

if __name__ == "__main__":
    template = "pantillas/L&W COTIZACION.pdf"
    output = "cotizacion_generada.pdf"
    
    # Keywords to search for in the PDF
    search_keywords = [
        "Folio", "Fecha", "expedición",
        "Cliente", 
        "Cantidad", "Descripción", "Precio Unitario", "Importe",
        "Subtotal", "Iva", "Total"
    ]
    
    print("Scanning PDF for coordinates...")
    found_coords = find_coordinates(template, search_keywords)
    print("Found coordinates:", found_coords)
    
    print("Generating overlay...")
    overlay = create_overlay(data, found_coords)
    
    print("Merging PDFs...")
    merge_pdfs(template, overlay, output)

