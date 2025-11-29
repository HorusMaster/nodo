import sys
import traceback
sys.path.insert(0, 'pantillas/L&W')

print("Step 1: Importing...")
try:
    from contrato_generator import generate_contract_docx
    print("✓ Import successful")
except Exception as e:
    print(f"✗ Import failed: {e}")
    traceback.print_exc()
    sys.exit(1)

print("\nStep 2: Preparing data...")
test_data = {'receptor': 'TEST EMPRESA'}
template_path = "pantillas/L&W/L&W CONTRATO.docx"
print(f"✓ Data prepared")
print(f"  Template path: {template_path}")

print("\nStep 3: Calling generator...")
try:
    output = generate_contract_docx(test_data, template_path)
    print("✓ SUCCESS! Contract generated")
    with open("test_output.docx", "wb") as f:
        f.write(output.read())
    print("✓ Saved to test_output.docx")
except Exception as e:
    print(f"✗ Generation failed")
    print(f"Error type: {type(e).__name__}")
    print(f"Error message: {e}")
    print("\nFull traceback:")
    traceback.print_exc()
