import sys
import traceback
sys.path.insert(0, 'pantillas/L&W')
from contrato_generator import generate_contract_docx

test_data = {'receptor': 'TEST EMPRESA'}
template_path = "pantillas/L&W/L&W CONTRATO.docx"

try:
    output = generate_contract_docx(test_data, template_path)
    print("SUCCESS!")
except Exception as e:
    print("ERROR:")
    traceback.print_exc()
