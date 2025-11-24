import sys
import os
import io

# Add the current directory to sys.path to ensure we can import modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Note: The folder is named "L&W" but Python import might struggle with "&".
# If "L&W" is a package, it's invalid identifier.
# I will use dynamic import for L&W to be safe.
import importlib.util

def import_module_from_path(module_name, file_path):
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module

# Paths
base_dir = os.path.dirname(os.path.abspath(__file__))
sushop_template = os.path.join(base_dir, "pantillas", "SUSHOP", "SUSHSHOP COTIZACION.pdf")
lw_template = os.path.join(base_dir, "pantillas", "L&W", "L&W COTIZACION.pdf")

# Import Generators
sushop_gen = import_module_from_path("sushop_gen", os.path.join(base_dir, "pantillas", "SUSHOP", "pdf_generator.py"))
lw_gen = import_module_from_path("lw_gen", os.path.join(base_dir, "pantillas", "L&W", "pdf_generator.py"))

data = [
  {
    "folio": "2318",
    "emisor": "SUSHSHOP DEL CENTRO",
    "receptor": "ALBERTO RAMIREZ TORRES",
    "rfc_receptor": "RATX681027I98",
    "fecha/hora_emision": "2025-10-24T17:23:35",
    "subtotal": 4525.85,
    "IVA": 724.14,
    "total_factura": 5249.99,
    "productos": [
      {
        "producto": "VALVULA DE ESFERA DE 3 PULGADAS",
        "cantidad": 1,
        "unidad": "H87",
        "precio_unitario": 2758.62,
        "importe": 2758.62
      },
      {
        "producto": "CONEXIÓN RAPIDA C200",
        "cantidad": 1,
        "unidad": "H87",
        "precio_unitario": 387.93,
        "importe": 387.93
      },
      {
        "producto": "CONEXIONES RAPIDAS F300",
        "cantidad": 2,
        "unidad": "H87",
        "precio_unitario": 1379.3,
        "importe": 1379.3
      }
    ]
  }
]

def run_test():
    item = data[0]
    
    print("Generating SUSHOP PDF...")
    try:
        pdf_bytes = sushop_gen.generate_pdf_bytes(item, sushop_template)
        with open("test_output_sushop.pdf", "wb") as f:
            f.write(pdf_bytes.getvalue())
        print("Success! Saved to test_output_sushop.pdf")
    except Exception as e:
        print(f"Error generating SUSHOP PDF: {e}")

    print("\nGenerating L&W PDF...")
    try:
        pdf_bytes = lw_gen.generate_pdf_bytes(item, lw_template)
        with open("test_output_lw.pdf", "wb") as f:
            f.write(pdf_bytes.getvalue())
        print("Success! Saved to test_output_lw.pdf")
    except Exception as e:
        print(f"Error generating L&W PDF: {e}")

if __name__ == "__main__":
    run_test()
