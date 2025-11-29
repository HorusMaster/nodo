from docxtpl import DocxTemplate
import os

# Probar con ruta absoluta
template_path = r"D:\Desarrollo\nodo\backend\pantillas\L&W\L&W CONTRATO.docx"

print(f"Template path: {template_path}")
print(f"Exists: {os.path.exists(template_path)}")

try:
    print("\nLoading template...")
    doc = DocxTemplate(template_path)
    print("✓ Template loaded successfully!")
    
    # Try rendering with simple data
    context = {'receptor': 'TEST'}
    doc.render(context)
    print("✓ Template rendered!")
    
    # Save
    doc.save("test_simple_output.docx")
    print("✓ Saved to test_simple_output.docx")
    
except Exception as e:
    print(f"✗ Error: {e}")
    import traceback
    traceback.print_exc()
