from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.responses import StreamingResponse
import os
from pdf_generator import generate_pdf_bytes

app = FastAPI()

class ProductItem(BaseModel):
    producto: str
    cantidad: float
    unidad: str
    precio_unitario: float
    importe: float

class InvoiceData(BaseModel):
    folio: str
    emisor: str
    receptor: str
    fecha_hora_emision: str = None # Optional, or alias "fecha/hora_emision"
    subtotal: float
    IVA: float
    total_factura: float
    productos: list[ProductItem]

    class Config:
        extra = "allow"

@app.post("/generate-pdf")
async def generate_pdf(payload: list[dict] | dict):
    """
    Receives a JSON payload (list or dict), selects a template based on 'emisor',
    and returns a generated PDF.
    """
    # Handle list input (n8n often sends a list of items)
    if isinstance(payload, list):
        if not payload:
            raise HTTPException(status_code=400, detail="Empty list provided")
        raw_data = payload[0]
    else:
        raw_data = payload

    # Normalize keys if needed (e.g. "fecha/hora_emision" -> "fecha_hora_emision")
    # For simplicity, we'll just work with the dict directly to pass to the generator
    
    emisor = raw_data.get("emisor")
    if not emisor:
        raise HTTPException(status_code=400, detail="Missing 'emisor' field")

    # Flatten data for the PDF generator
    # The generator expects keys like 'producto', 'cantidad' at the top level.
    # We will take the first product from the list.
    pdf_data = raw_data.copy()
    
    productos = raw_data.get("productos", [])
    if productos and isinstance(productos, list) and len(productos) > 0:
        first_product = productos[0]
        pdf_data.update(first_product) # Merge product fields into top level
    
    # Template selection logic
    template_map = {
        "LEARN&WELL22": "pantillas/L&W COTIZACION.pdf",
        "SUSHSHOP DEL CENTRO": "pantillas/SUSHOP/SUSHSHOP COTIZACION.pdf"
    }
    
    template_path = template_map.get(emisor)
    
    if not template_path:
        raise HTTPException(status_code=404, detail=f"No template found for emisor: {emisor}")
    
    if not os.path.exists(template_path):
         raise HTTPException(status_code=500, detail=f"Template file not found on server: {template_path}")

    try:
        pdf_stream = generate_pdf_bytes(pdf_data, template_path)
        
        # Return as a streaming response
        return StreamingResponse(
            pdf_stream, 
            media_type="application/pdf",
            headers={"Content-Disposition": f"attachment; filename=cotizacion_{pdf_data.get('folio', 'generated')}.pdf"}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
def health_check():
    return {"status": "ok"}
