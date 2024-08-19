import json
import requests
from bs4 import BeautifulSoup
import time
from flask import Flask, render_template
from dotenv import load_dotenv
from flask import request, jsonify
import re
app = Flask(__name__)

# Cargar las variables de entorno desde el archivo .env
load_dotenv()


@app.route('/')
def index():
    return render_template('/index.html')




@app.route('/api/busqueda_producto_codigo_barra', methods=['POST'])
def api_busqueda_producto_codigo_barra():




    data = request.get_json()

    product_id = data['codigo_barra']

    # return jsonify({'Codigo_barra': '1', 'Nombre': 'Protec Nivea Sun Sensac Ligera F50 - 200ml', 'Descripción': 'Protec Nivea Sun Sensac Ligera F50 - 200ml', 'Imagen': 'https://walmartni.vtexassets.com/arquivos/ids/371972/Protec-Nivea-Sun-Sensac-Ligera-F50-200ml-2-4784.jpg?v=638454009729930000', 'Precio': 505})

    
    base_url = "https://www.walmart.com.ni/"
    search_url = f"{base_url}{product_id}"
    product = extract_product_info_by_id(search_url, product_id)
    # product = 0
    if product:
        print(product)
        return jsonify(product)
    else:
        print("No se pudo recuperar la información del producto.")
        return 'No se pudo recuperar la información del producto.'
    

    return 'Hello, World!'


# Función para extraer datos de un producto específico utilizando su ID
def extract_product_info_by_id(search_url, product_id):
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
            template_tag = soup.find('template', {'data-varname': '__STATE__'})
            if template_tag is None:
                print("No se encontró el elemento 'template' con 'data-varname' '__STATE__'.")
                return None

            script_tag = template_tag.find('script')
            if script_tag is None:
                print("No se encontró un elemento 'script' dentro del 'template'.")
                return None
            
            # Extrae el contenido del script
            json_data = script_tag.string

            
            # Carga el contenido como un diccionario de Python
            try:
                data = json.loads(json_data)
            except json.JSONDecodeError:
                print("Error al decodificar el JSON del script.")
                return None

            # Busca la clave que contiene el ID del producto
            product_key = next((key for key in data.keys() if key.startswith('Product:sp-')), None)
            if not product_key:
                print("No se encontró la clave del producto en el JSON.")
                return None
            
            product = data[product_key]

            # Define la expresión regular para encontrar '-1-' en el medio de la URL
            pattern = re.compile(r'(-1-|_01)')

            for key in data:
                if 'imageUrl' in data[key]:
                    image_url = data[key]['imageUrl']
                    # Verifica si '-1-' está en el medio de la URL usando la expresión regular
                    if pattern.search(image_url):
                        selected_url = image_url
                    else:
                        # Siempre actualiza selected_url con la última URL encontrada
                        selected_url = image_url

            print(selected_url)


            # Acceder a la URL de la imagen
            # image_url = data.get("Image:272220", {}).get("imageUrl", "N/A")
            
            # Extrae la información del producto
            product_info = {
                'Codigo_barra': product_id,
                'Nombre': product.get('productName', 'N/A'),
                'Descripción': product.get('description', 'N/A'),
                'Imagen': image_url
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


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000, debug=True)
 
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