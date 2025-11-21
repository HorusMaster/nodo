import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from pypdf import PdfReader, PdfWriter

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

def create_overlay(data_item, coords):
    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=letter)
    can.setFont("Helvetica", 10)
    can.setFillColorRGB(0, 0, 0) 

    # Helper to draw text relative to found coordinates
    def draw_relative(label_key, value, offset_x=0, offset_y=0):
        if label_key in coords:
            x, y = coords[label_key]
            # Default: Place text to the right of the label
            can.drawString(x + offset_x, y + offset_y, str(value))
        else:
            print(f"WARNING: Label '{label_key}' not found in PDF. Skipping '{value}'")

    # --- MAPPING CONFIGURATION ---
    
    # Header Info
    draw_relative("Folio", data_item.get('folio', ''), offset_x=35) 
    draw_relative("Fecha", data_item.get('fecha/hora_emision', ''), offset_x=35)
    
    # Emisor: Search for "expedición" to avoid newline issues
    draw_relative("expedición", data_item.get('emisor', ''), offset_x=0, offset_y=20)

    # Receptor -> "Cliente"
    draw_relative("Cliente", data_item.get('receptor', ''), offset_x=40, offset_y=0) 

    # Table Columns
    row_y_offset = -20 
    
    draw_relative("Cantidad", data_item.get('cantidad', ''), offset_x=0, offset_y=row_y_offset)
    
    draw_relative("Descripción", data_item.get('producto', ''), offset_x=0, offset_y=row_y_offset) 
    draw_relative("Precio Unitario", f"${data_item.get('precio_unitario', '')}", offset_x=0, offset_y=row_y_offset)
    
    # Importe fallback: if not found or 0, place relative to Precio
    if "Importe" in coords and coords["Importe"][0] > 10:
        draw_relative("Importe", f"${data_item.get('importe', '')}", offset_x=0, offset_y=row_y_offset)
    elif "Precio Unitario" in coords:
        # Estimate Importe is ~100 units to the right of Precio
        precio_x, precio_y = coords["Precio Unitario"]
        can.drawString(precio_x + 100, precio_y + row_y_offset, f"${data_item.get('importe', '')}")

    # Totals
    draw_relative("Subtotal", f"${data_item.get('subtotal', '')}", offset_x=60)
    draw_relative("Iva", f"${data_item.get('IVA', '')}", offset_x=60) # Note 'Iva' in PDF vs 'IVA' in JSON key
    draw_relative("Total", f"${data_item.get('total_factura', '')}", offset_x=60)

    can.save()
    packet.seek(0)
    return packet

def generate_pdf_bytes(data_item, template_path):
    """
    Generates a filled PDF and returns the bytes.
    """
    # Keywords to search for in the PDF
    search_keywords = [
        "Folio", "Fecha", "expedición",
        "Cliente", 
        "Cantidad", "Descripción", "Precio Unitario", "Importe",
        "Subtotal", "Iva", "Total"
    ]
    
    found_coords = find_coordinates(template_path, search_keywords)
    overlay_packet = create_overlay(data_item, found_coords)
    
    existing_pdf = PdfReader(open(template_path, "rb"))
    output = PdfWriter()
    new_pdf = PdfReader(overlay_packet)
    page = existing_pdf.pages[0]
    page.merge_page(new_pdf.pages[0])
    output.add_page(page)
    
    output_stream = io.BytesIO()
    output.write(output_stream)
    output_stream.seek(0)
    return output_stream
