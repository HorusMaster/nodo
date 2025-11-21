Nodo para en  base a una plantilla generar  informacion y cotizaciones

Crear Venv
python3.10 -m venv nodo_env
Activar
source nodo_env/bin/activate

pip3 install --upgrade pip
pip3 install pypdf reportlab    

bash -c "source /home/horus/nodo_env/bin/activate && python3 generate_quote.py"