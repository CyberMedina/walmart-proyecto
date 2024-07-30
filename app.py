import requests
from bs4 import BeautifulSoup
import time

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

        


        # Encuentra el primer contenedor del producto
        first_product_container = soup.find('section', class_='vtex-product-summary-2-x-container')

        if first_product_container:
            # Extrae el nombre del producto
            name_tag = first_product_container.find('span', class_='vtex-product-summary-2-x-productBrand')
            # Extrae el precio del producto
            price_tag = first_product_container.find('span', class_='vtex-store-components-3-x-currencyContainer')

            if name_tag and price_tag:
                name = name_tag.get_text(strip=True)
                price = price_tag.get_text(strip=True)
                return {'name': name, 'price': price}
            else:
                print("No se encontraron las etiquetas de nombre o precio.")
        else:
            print("No se encontró el contenedor del producto.")
    
    else:
        print(f"Error: {response.status_code}")
    
    return None

# Ejemplo de uso
product_id = "4005808944767"  # ID del producto específico
base_url = "https://www.walmart.com.ni/"

search_url = f"{base_url}{product_id}"
print(search_url)
product = extract_product_info_by_id(search_url)

if product:
    print(f"Nombre: {product['name']}, Precio: {product['price']}")
else:
    print("No se pudo recuperar la información del producto.")

# Espera de 5 segundos entre solicitudes
time.sleep(5)