from bs4 import BeautifulSoup
import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time

# Función para hacer scroll hasta el final de la página
def scroll_to_bottom(driver):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)  # Ajusta este retraso según sea necesario

# Función para obtener datos de la primera tienda (BlackDog)
def get_blackdog_data():
    # URL de la primera tienda (BlackDog)
    url_blackdog = "https://www.blackdog.cl"
    driver_path = r'E:\chromedriver_win32\chromedriver-win64\chromedriver.exe'

    # Crea una nueva instancia del controlador de Chrome para la primera tienda
    service = Service(driver_path)
    driver = webdriver.Chrome(service=service)
    driver.maximize_window()

    # Navega a la URL de la primera tienda
    driver.get(url_blackdog)

    # Encuentra y haz clic en el enlace "Shop"
    shop = driver.find_element(By.XPATH, '//ul/li/a/span[contains(text(), "Shop")]')
    shop.click()

    # Encuentra y haz clic en el enlace "PATINES"
    patines = driver.find_element(By.XPATH, '//ul/li/a/span/span[contains(text(), "PATINES")]')
    patines.click()

    # Encuentra y haz clic en el enlace "Agresivos"
    agresivos = driver.find_element(By.XPATH, '//ul/li/a/span[contains(text(), "Agresivos")]')
    agresivos.click()

    # Hace scroll hasta el final de la página
    scroll_to_bottom(driver)

    # Inicializa la variable para el contador de elementos
    last_count = 0

    # Lista para almacenar los datos de la primera tienda
    patines_agresivos_data = []

    # Loop hasta que ya no se carguen más elementos
    while True:
        scroll_to_bottom(driver)
        patines_agresivos = driver.find_elements(By.XPATH, '//div[@class="product-wrapper"]')
        if len(patines_agresivos) == last_count:
            break
        else:
            last_count = len(patines_agresivos)

    # Extrae la información relevante de cada elemento y almacénala en un diccionario
    for patin in patines_agresivos:
        soup = BeautifulSoup(patin.get_attribute("outerHTML"), "html.parser")
        name = soup.find("h3", class_="wd-entities-title").text.strip()
        prices = soup.find("span", class_="price").find_all("bdi")
        offer_price = prices[1].text.strip() if len(prices) > 1 else None
        regular_price = prices[0].text.strip()
        link = soup.find("a", class_="product-image-link")["href"]
        image = soup.find("img", class_="attachment-woocommerce_thumbnail")["src"]
        categories = [cat.text.strip() for cat in soup.find("div", class_="wd-product-cats").find_all("a", rel="tag")]
        brands = [brand.text.strip() for brand in soup.find("div", class_="wd-product-brands-links").find_all("a")]
        patin_data = {
            "name": name,
            "regular_price": regular_price,
            "offer_price": offer_price,
            "link": link,
            "image": image,
            "categories": categories,
            "brands": brands
        }
        patines_agresivos_data.append(patin_data)

    # Cierra el navegador
    driver.quit()

    # Retorna los datos obtenidos de BlackDog
    return patines_agresivos_data

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import time

def get_openboxstore_data():
    # URL de la segunda tienda
    url_openboxstore = "https://www.openboxstore.cl/patines/agresivos"
    driver_path = r'E:\chromedriver_win32\chromedriver-win64\chromedriver.exe'

    # Crea una nueva instancia del controlador de Chrome para la segunda tienda
    service = Service(driver_path)
    driver = webdriver.Chrome(service=service)
    driver.maximize_window()

    # Navega a la URL de la segunda tienda
    driver.get(url_openboxstore)

    # Lista para almacenar los datos
    openboxstore_data = []

    # Loop para recorrer todas las páginas (si hay paginación)
    while True:
        # Encuentra todos los elementos de productos
        products = driver.find_elements(By.XPATH, '//div[@class="col-xl-3 col-md-4 col-6 px-md-2 px-1 mb-md-3 mb-2"]')
        
        # Extrae información de cada producto
        
        for product in products:
            soup = BeautifulSoup(product.get_attribute("outerHTML"), "html.parser")
            name = soup.find("h3").text.strip()
            price_container = soup.find("div", class_="prices")

            # Comprueba si hay dos elementos dentro del contenedor de precios
            if len(price_container.find_all("span")) == 2:
                # Busca el precio regular y el precio de oferta
                regular_price_element = price_container.find("span", class_="product-price-before")
                offer_price_element = price_container.find("span", class_="product-price-discount")
                regular_price = regular_price_element.text.strip() if regular_price_element else None
                offer_price = offer_price_element.text.strip() if offer_price_element else None
            else:
                # Si solo hay un elemento, asume que es el precio regular y no hay oferta
                regular_price_element = price_container.find("span", class_="product-price")
                regular_price = regular_price_element.text.strip() if regular_price_element else None
                offer_price = None

            link = "https://www.openboxstore.cl" + soup.find("a")["href"]
            image = soup.find("img")["src"]
            brand = soup.find("small", class_="brand").text.strip() if soup.find("small", class_="brand") else ""
            category = "Agresivo"  # No hay información sobre la categoría específica, la dejamos como "Agresivo"

            # Almacena los datos en un diccionario
            product_data = {
                "name": name,
                "regular_price": regular_price,
                "offer_price": offer_price,
                "link": link,
                "image": image,
                "categories": [category],
                "brands": [brand] if brand else []  # Si no hay marca, dejar la lista vacía
            }

            # Agrega los datos del producto a la lista
            openboxstore_data.append(product_data)




        # Busca si hay botones para la siguiente página
        next_buttons = driver.find_elements(By.XPATH, '//div[@class="custom-pager border rounded-pill overflow-hidden"]/a')
        if len(next_buttons) < 2 or "disabled" in next_buttons[1].get_attribute("class"):
            break  # Si no se encuentran suficientes botones de siguiente página o el segundo está desactivado, sal del bucle

        # Si hay una página siguiente, haz clic en el segundo botón para cargarla
        next_buttons[1].click()
        time.sleep(5)  # Espera un poco para que los nuevos productos carguen completamente

    # Cierra el navegador
    driver.quit()

    # Retorna los datos obtenidos de OpenBoxStore
    return openboxstore_data

# Función para asignar ID único a cada elemento en el archivo JSON
def assign_ids_to_items(data):
    for i, item in enumerate(data, start=1):
        item["id"] = i
    return data

# Llama a la función para obtener los datos de BlackDog
blackdog_data = get_blackdog_data()

# Convertir los datos a JSON y escribirlos en un archivo
with open("patines_agresivos_data.json", "w") as file:
    json.dump(blackdog_data, file, indent=4)

# Llama a la función para obtener los datos de OpenBoxStore
openboxstore_data = get_openboxstore_data()

# Lee los datos existentes del archivo JSON
with open("patines_agresivos_data.json", "r") as file:
    existing_data = json.load(file)

# Agrega los datos de OpenBoxStore a los datos existentes
existing_data.extend(openboxstore_data)

# Asigna ID único a cada elemento en el archivo JSON
existing_data_with_ids = assign_ids_to_items(existing_data)

# Sobrescribe el archivo JSON con los datos combinados que ahora tienen IDs únicos
with open("patines_agresivos_data.json", "w") as file:
    json.dump(existing_data_with_ids, file, indent=4)
