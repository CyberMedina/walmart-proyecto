import json
import requests
from bs4 import BeautifulSoup
import time
from flask import Flask, render_template
from dotenv import load_dotenv
from flask import request
app = Flask(__name__)

# Cargar las variables de entorno desde el archivo .env
load_dotenv()


@app.route('/')
def index():
    return render_template('/index.html')

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000, debug=True)
 


@app.route('/api/busqueda_producto_codigo_barra', methods=['POST'])
def api_busqueda_producto_codigo_barra():




    data = request.get_json()

    product_id = data['codigo_barra']

    
    base_url = "https://www.walmart.com.ni/"
    search_url = f"{base_url}{product_id}"
    product = extract_product_info_by_id(search_url)
    if product:
        print(product)
        return product
    else:
        return 'No se pudo recuperar la información del producto.'

    return 'Hello, World!'


# Función para extraer datos de un producto específico utilizando su ID
def extract_product_info_by_id(search_url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    response = requests.get(search_url, headers=headers)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        # Guarda el html en un archivo para revisar la estructura
        with open("walmart_product.html", "w", encoding='utf-8') as file:
            file.write(soup.prettify())

        


            # Buscar el <script> dentro del <template>
        script_tag = soup.find('template', {'data-varname': '__STATE__'}).find('script')
        
        # Extrae el contenido del script
        json_data = script_tag.string
        
        # Carga el contenido como un diccionario de Python
        data = json.loads(json_data)
        
        # Busca la clave que contiene el ID del producto
        product_key = next((key for key in data.keys() if key.startswith('Product:sp-')), None)
        if not product_key:
            return None
        
        product = data[product_key]
        
        # Extrae la información del producto
        product_info = {
            'Nombre': product['productName'],
            'Descripción': product['description'],
        }
        
        # Intenta obtener el precio del producto
        try:
            price_range_key = f"${product_key}.priceRange"
            selling_price_key = data[price_range_key]['sellingPrice']['id']
            price_range = data[selling_price_key]
            product_info['Precio'] = price_range['highPrice']
        except KeyError:
            product_info['Precio'] = 'N/A'
        
        return product_info

# Ejemplo de uso
# product_id = "7501032907495"  # ID del producto específico
# base_url = "https://www.walmart.com.ni/"

# search_url = f"{base_url}{product_id}"
# print(search_url)
# product = extract_product_info_by_id(search_url)

# if product:
#     print(product)
# else:
#     print("No se pudo recuperar la información del producto.")

# # Espera de 5 segundos entre solicitudes
# time.sleep(5)