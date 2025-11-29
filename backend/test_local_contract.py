import sys
import os
from pathlib import Path

# Add backend to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from pantillas.SUSHOP.contrato_generator import generate_contract_docx

def test_local_generation():
    # Define paths
    base_dir = Path(__file__).parent
    template_path = base_dir / "pantillas" / "SUSHOP" / "SUSHSHOP_CONTRATO.docx"
    output_path = base_dir / "test_contrato_output.docx"
    
    print(f"Using template: {template_path}")
    
    if not template_path.exists():
        print("Error: Template not found!")
        return

    # Test data with some fields present and others missing
    data = {
        "receptor": "Empresa de Prueba S.A. de C.V.",
        "representante_receptor": "Juan Pérez",
        "fecha": "2023-11-29",
        # "banco_receptor" is missing, should be XXXXXXXXXX
        # "cuenta_receptor" is missing, should be XXXXXXXXXX
        "clave_receptor": "0123456789"
    }
    
    print("Generating contract with data:", data)
    
    try:
        # Run generator
        docx_stream = generate_contract_docx(data, str(template_path))
        
        # Save to file
        with open(output_path, "wb") as f:
            f.write(docx_stream.getvalue())
            
        print(f"Success! Contract saved to: {output_path}")
        print("Please open this file to verify the replacements.")
        
    except Exception as e:
        print(f"Error generating contract: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_local_generation()
