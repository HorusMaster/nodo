## To execute

uvicorn main:app --reload


Nodo para en  base a una plantilla generar  informacion y cotizaciones


## Para  Instalar
Crear Venv en /home
cd /home/$USER
python3.10 -m venv nodo_env
Activar
source nodo_env/bin/activate

pip3 install --upgrade pip
git clone https://github.com/HorusMaster/nodo.git
cd nodo
pip3 install -r requirements.txt


## Para ejecutar

Para GEMINI:
bash -c "source /home/horus/nodo_env/bin/activate && python3.10 generate_quote.py"

Para ejecutar humanos:
source nodo_env/bin/activate
python3.10 generate_quote.py
