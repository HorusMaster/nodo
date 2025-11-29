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
    draw_relative("Fecha:", data_item.get('fecha/hora_emision', ''), offset_x=35, offset_y=-2)
    draw_relative("Cliente", data_item.get('receptor', ''), offset_x=10, offset_y=-30)
  
    # Receptor -> "Cliente"
    # Fallback to "Nombre / razón social" if "Cliente" is not mapped, or just use "Nombre / razón social" directly
    #if "Nombre / razón social" in coords:
    #    draw_relative("Nombre / razón social: ", data_item.get('receptor', ''), offset_x=380, offset_y=-25)
    #    # Draw RFC relative to Name
    #    name_x, name_y = coords["Nombre / razón social"]
    #    can.drawString(name_x + 380, name_y - 45, data_item.get('rfc_receptor', ''))
    #elif "Cliente" in coords:
    #    draw_relative("Cliente", data_item.get('receptor', ''), offset_x=40, offset_y=-50)
    #    draw_relative("RFC", data_item.get('rfc_receptor', ''), offset_x=350, offset_y=-20)
    #else:
    #    # Absolute fallback if neither found
    #    can.drawString(100, 650, data_item.get('receptor', ''))
    #    can.drawString(100, 635, data_item.get('rfc_receptor', '')) 

    # Table Columns
    products = data_item.get('productos', [])
    if not products and 'producto' in data_item:
        products = [data_item]

    current_y_offset = -20
    line_height = 20

    # Fallback coordinates if keywords are not found (e.g. images in PDF)
    # Cantidad: x=50, Descripción: x=120, Precio Unitario: x=350, Importe: x=480
    # Y start approx 550 (need to adjust based on template)
    
    # We use the first item to establish the Y start if we have to use absolute coordinates
    # But draw_relative relies on a key.
    
    # Strategy: define base coordinates for columns
    col_coords = {
        "Cantidad": coords.get("Cantidad", (72, 550)), # Default approx
        "Descripción": coords.get("Descripción", (140, 550)),
        "Precio Unitario": coords.get("Precio Unitario", (380, 550)),
        "Importe": coords.get("Importe", (480, 550))
    }
    
    # Fix for Price Y alignment: If Importe is found, use its Y for Price default
    if "Importe" in coords:
        col_coords["Precio Unitario"] = (col_coords["Precio Unitario"][0], coords["Importe"][1])

    # Override coords with defaults if missing
    for key, val in col_coords.items():
        if key not in coords:
            coords[key] = val

    for item in products:
        # Now we can safely use draw_relative because we injected the keys into coords
        # We might need to adjust the offsets because draw_relative adds the coord to the offset.
        # If we used absolute defaults, we want offset 0 (or small adjustments).
        
        # Note: draw_relative does: can.drawString(x + offset_x, y + offset_y, ...)
        
        draw_relative("Cantidad", item.get('cantidad', ''), offset_x=0, offset_y=current_y_offset)
        draw_relative("Descripción", item.get('producto', ''), offset_x=0, offset_y=current_y_offset) 
        draw_relative("Precio Unitario", f"${item.get('precio_unitario', '')}", offset_x=0, offset_y=current_y_offset)
        draw_relative("Importe", f"${item.get('importe', '')}", offset_x=0, offset_y=current_y_offset)
            
        current_y_offset -= line_height

    # Totals
    draw_relative("Subtotal", f"${data_item.get('subtotal', '')}", offset_x=80)
    draw_relative("Iva", f"${data_item.get('IVA', '')}", offset_x=60)
    draw_relative("Total", f"${data_item.get('total_factura', '')}", offset_x=80, offset_y=-35)

    can.save()
    packet.seek(0)
    return packet

def generate_pdf_bytes(data_item, template_path):
    """
    Generates a filled PDF and returns the bytes.
    """
    # Keywords to search for in the PDF
    search_keywords = [
        "Folio", "Fecha:",
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

