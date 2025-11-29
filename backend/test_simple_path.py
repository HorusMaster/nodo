from docxtpl import DocxTemplate
from pathlib import Path
import shutil

# Copy template to a simple path without special characters
source = Path("pantillas/L&W/L&W CONTRATO.docx")
dest = Path("temp_contrato.docx")

print(f"Copying {source} to {dest}...")
shutil.copy(source, dest)
print("✓ Copied")

print("\nTrying to load from simple path...")
try:
    doc = DocxTemplate(dest)
    print("✓ Template loaded successfully!")
    
    context = {
        'receptor': 'TEST EMPRESA',
        'representante_receptor': 'Juan Pérez',
        'banco_receptor': 'BBVA',
        'cuenta_receptor': '123456',
        'clave_receptor': 'ABC123',
        'fecha': '2025-11-28',
        'hora_emision': '21:00:00'
    }
    
    doc.render(context)
    print("✓ Rendered")
    
    doc.save("output_test.docx")
    print("✓ Saved to output_test.docx")
    print("\n✓✓✓ SUCCESS! The generator works with simple paths!")
    
except Exception as e:
    print(f"✗ Error: {e}")
    import traceback
    traceback.print_exc()
