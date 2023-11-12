from flask import Flask, render_template, jsonify
import random
import json
import os
from dotenv import load_dotenv

app = Flask(__name__)

# Carga las variables de entorno desde el archivo .env
load_dotenv()

# Obtiene el nombre del proyecto y del bucket desde las variables de entorno
project_id = os.getenv("GCP_PROJECT_ID")
bucket_name = os.getenv("GCP_BUCKET_NAME")

# Lee el archivo JSON
with open('pokeneas.json', 'r') as file:
    pokeneas_data = file.read()

# Convierte el JSON a un diccionario de Python
pokeneas_dict = json.loads(pokeneas_data)

# Obtén las URL de las imágenes
pokeneas_with_image_urls = [
    {**pokenea, 'imagen_url': f"https://storage.googleapis.com/{bucket_name}/images/{pokenea['imagen']}"}
    for pokenea in pokeneas_dict['pokeneas']
]

@app.route('/start')
def index():
    return render_template('index.html')

@app.route('/random_pokenea')
def random_pokenea():
    # Obtiene un Pokenea aleatorio
    random_pokenea = random.choice(pokeneas_with_image_urls)
    return jsonify(random_pokenea)

# Nueva ruta para listar todos los Pokeneas
@app.route('/pokeneas')
def list_pokeneas():
    # No necesitas obtener las URL aquí, ya las tienes precalculadas
    return render_template('pokeneas.html', pokeneas=pokeneas_with_image_urls)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
