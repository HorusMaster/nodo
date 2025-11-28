from fastapi import FastAPI, HTTPException, UploadFile, File, Request
from fastapi.middleware.cors import CORSMiddleware
import requests
from pydantic import BaseModel
from fastapi.responses import StreamingResponse
import os
from pdf_generator import generate_pdf_bytes
import logging
import time

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Configure CORS with explicit headers
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especifica los dominios permitidos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

# Add request logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    logger.info(f"Incoming request: {request.method} {request.url.path}")
    
    response = await call_next(request)
    
    process_time = time.time() - start_time
    logger.info(f"Completed {request.method} {request.url.path} - Status: {response.status_code} - Time: {process_time:.2f}s")
    
    return response

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
        "LEARN&WELL22": "pantillas/L&W/L&W COTIZACION.pdf",
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

@app.post("/upload_multiple_files")
async def upload_multiple_files(files: list[UploadFile] = File(...)):
    """
    Receives multiple files and forwards them to the configured n8n webhook.
    Sends one request per file since the webhook doesn't support multiple files.
    """
    n8n_url = "https://n8n.redinmex.com/webhook/86ce68b9-267c-4d46-b4c7-6651bffc116e"
    
    files_to_send = []
    
    try:
        # Collect all files first
        for file in files:
            # Read file content
            content = await file.read()
            
            # Add to the list with field name 'file'
            files_to_send.append(('file', (file.filename, content, file.content_type)))
            
            # Close the file
            await file.close()
        
        # Send all files in a single request to n8n
        response = requests.post(n8n_url, files=files_to_send)
        
        if response.status_code != 200:
            raise HTTPException(status_code=502, detail=f"n8n returned status {response.status_code}: {response.text}")
             
        return {"status": "success", "n8n_response": response.text, "files_sent": len(files_to_send)}
        
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/upload_multiple_files_test")
async def upload_multiple_files_test(files: list[UploadFile] = File(...)):
    """
    TEST MODE: Receives multiple files and forwards them to the n8n TEST webhook.
    Use this endpoint while editing your workflow in n8n.
    """
    n8n_test_url = "https://n8n.redinmex.com/webhook-test/86ce68b9-267c-4d46-b4c7-6651bffc116e"
    
    files_to_send = []
    
    try:
        # Collect all files first
        for file in files:
            # Read file content
            content = await file.read()
            
            # Add to the list with field name 'file'
            files_to_send.append(('file', (file.filename, content, file.content_type)))
            
            # Close the file
            await file.close()
        
        # Send all files in a single request to n8n TEST webhook
        response = requests.post(n8n_test_url, files=files_to_send)
        
        if response.status_code != 200:
            raise HTTPException(status_code=502, detail=f"n8n TEST returned status {response.status_code}: {response.text}")
             
        return {"status": "success", "mode": "TEST", "n8n_response": response.text, "files_sent": len(files_to_send)}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
def health_check():
    return {"status": "ok"}
