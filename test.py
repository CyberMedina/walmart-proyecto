import json
import requests
from bs4 import BeautifulSoup
import time
from flask import Flask, render_template
from dotenv import load_dotenv
from flask import request, jsonify
app = Flask(__name__)



def extract_product_info_by_id():
    # Abre el archivo HTML y lee su contenido
    with open("walmart_product.html", "r", encoding='utf-8') as file:
        html_content = file.read()
    
    # Analiza el contenido HTML usando BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Guarda el HTML analizado en un archivo para revisión
    with open("walmart_product_pretty.html", "w", encoding='utf-8') as file:
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

    for key in data:
    # Verifica si la clave contiene 'imageUrl'
        if 'imageUrl' in data[key]:
            print(data[key]['imageUrl'])
            image_url = data[key]['imageUrl']

    # Acceder a la URL de la imagen
    # image_url = data.get("Image:272220", {}).get("imageUrl", "N/A")
    
    # Extrae la información del producto
    product_info = {
        'Codigo_barra': '1',
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

print(extract_product_info_by_id())