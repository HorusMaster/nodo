from docxtpl import DocxTemplate
import sys

# Load the template
template_path = "pantillas/L&W/L&W CONTRATO.docx"
doc = DocxTemplate(template_path)

# Get all variables used in the template
variables = doc.get_undeclared_template_variables()

print("Variables found in the DOCX template:")
print("=" * 50)
for var in sorted(variables):
    print(f"  - {var}")
print("=" * 50)
print(f"Total variables: {len(variables)}")

# Also save to file
with open("template_variables.txt", "w", encoding="utf-8") as f:
    f.write("Variables in L&W CONTRATO.docx:\n")
    f.write("=" * 50 + "\n")
    for var in sorted(variables):
        f.write(f"  - {var}\n")
    f.write("=" * 50 + "\n")
    f.write(f"Total: {len(variables)}\n")

print("\nVariables also saved to template_variables.txt")
