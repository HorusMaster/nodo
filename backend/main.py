from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.responses import StreamingResponse
import os
from pdf_generator import generate_pdf_bytes

app = FastAPI()

class InvoiceItem(BaseModel):
    folio: str
    emisor: str
    receptor: str
    fecha_hora_emision: str
    producto: str
    cantidad: float
    unidad: str
    precio_unitario: float
    importe: float
    subtotal: float
    IVA: float
    total_factura: float

    class Config:
        # Allow both snake_case and the keys from the example (some have special chars like '/')
        # But for simplicity in Pydantic, we map them manually or use alias.
        # Let's use a dict for the input payload to be flexible with keys like "fecha/hora_emision"
        extra = "allow" 

@app.post("/generate-pdf")
async def generate_pdf(payload: dict):
    """
    Receives a JSON payload, selects a template based on 'emisor',
    and returns a generated PDF.
    """
    # Extract the first item if it's a list, or use the dict directly
    # The user example showed a list "data = [{...}]" but the request says "payload"
    # We'll handle both single dict or list of dicts (taking the first one)
    data_item = payload
    if isinstance(payload, list):
        if not payload:
            raise HTTPException(status_code=400, detail="Empty list provided")
        data_item = payload[0]
    
    emisor = data_item.get("emisor")
    if not emisor:
        raise HTTPException(status_code=400, detail="Missing 'emisor' field")

    # Template selection logic
    template_map = {
        "LEARN&WELL22": "pantillas/L&W COTIZACION.pdf"
    }
    
    template_path = template_map.get(emisor)
    
    if not template_path:
        # Fallback or error? For now, error if not found, or maybe a default?
        # Let's try to find a default or error.
        raise HTTPException(status_code=404, detail=f"No template found for emisor: {emisor}")
    
    if not os.path.exists(template_path):
         raise HTTPException(status_code=500, detail=f"Template file not found on server: {template_path}")

    try:
        pdf_stream = generate_pdf_bytes(data_item, template_path)
        
        # Return as a streaming response
        return StreamingResponse(
            pdf_stream, 
            media_type="application/pdf",
            headers={"Content-Disposition": f"attachment; filename=cotizacion_{data_item.get('folio', 'generated')}.pdf"}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
def health_check():
    return {"status": "ok"}
