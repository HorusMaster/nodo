import importlib.util
import os
import sys

def load_module_from_path(module_name, file_path):
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module

def generate_pdf_bytes(data_item, template_path):
    """
    Dispatches the PDF generation to the appropriate module based on the template path.
    """
    # Normalize path separators
    template_path = template_path.replace("/", os.sep).replace("\\", os.sep)
    
    # Determine which generator to use based on the folder structure
    # Expected path: backend/pantillas/FOLDER/template.pdf
    
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    if "SUSHOP" in template_path:
        generator_path = os.path.join(base_dir, "pantillas", "SUSHOP", "pdf_generator.py")
        module_name = "sushop_generator"
    elif "LW" in template_path:
        generator_path = os.path.join(base_dir, "pantillas", "LW", "pdf_generator.py")
        module_name = "lw_generator"
    else:
        raise ValueError(f"Unknown template type for path: {template_path}")

    if not os.path.exists(generator_path):
        raise FileNotFoundError(f"Generator not found at: {generator_path}")

    generator_module = load_module_from_path(module_name, generator_path)
    return generator_module.generate_pdf_bytes(data_item, template_path)
