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

import random
from datetime import datetime, timedelta

def calculate_display_date(original_date_str):
    """
    Calculates a random date 3-5 days before the original date, excluding Sundays.
    Assumes original_date_str is in YYYY-MM-DD format.
    """
    try:
        # Try parsing YYYY-MM-DD
        original_date = datetime.strptime(original_date_str, "%Y-%m-%d").date()
    except ValueError:
        try:
             # Try parsing DD/MM/YYYY just in case
            original_date = datetime.strptime(original_date_str, "%d/%m/%Y").date()
        except ValueError:
            # Fallback if format is unknown
            return original_date_str

    while True:
        offset = random.randint(3, 5)
        candidate_date = original_date - timedelta(days=offset)
        
        # 6 is Sunday
        if candidate_date.weekday() != 6:
            return candidate_date.strftime("%Y-%m-%d")

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
    
    # Date Logic
    original_date = data_item.get('fecha/hora_emision', '')
    display_date = calculate_display_date(original_date) if original_date else ''
    draw_relative("Fecha", display_date, offset_x=35)
    
    # Cliente
    draw_relative("Cliente", data_item.get('receptor', ''), offset_x=50, offset_y=0) 
    
    # RFC
    draw_relative("RFC", data_item.get('rfc_receptor', ''), offset_x=35, offset_y=0)

    # Table Columns
    # Based on debug: Cantidad (63.225, 424.3), Descripción (201.08, 424.3), Precio (341.1, 424.3), Importe (426.52, 424.3)
    row_y_offset = -20 
    
    # Use 'Precio' instead of 'Precio Unitario' as keyword
    
    draw_relative("Cantidad", data_item.get('cantidad', ''), offset_x=0, offset_y=row_y_offset)
    draw_relative("Descripción", data_item.get('producto', ''), offset_x=0, offset_y=row_y_offset) 
    draw_relative("Precio", f"${data_item.get('precio_unitario', '')}", offset_x=0, offset_y=row_y_offset)
    draw_relative("Importe", f"${data_item.get('importe', '')}", offset_x=0, offset_y=row_y_offset)

    # Totals
    draw_relative("Subtotal", f"${data_item.get('subtotal', '')}", offset_x=60)
    draw_relative("Iva", f"${data_item.get('IVA', '')}", offset_x=60)
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
        "Folio", "Fecha",
        "Cliente", "RFC",
        "Cantidad", "Descripción", "Precio", "Importe",
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
