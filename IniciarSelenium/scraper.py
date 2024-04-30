import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from concurrent.futures import ThreadPoolExecutor

# Función para hacer scroll hasta el final de la página
def scroll_to_bottom(driver):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(1)  # Ajusta este retraso según sea necesario

# Función para obtener datos de la primera tienda (BlackDog)
def get_blackdog_data():
    # URL de la primera tienda (BlackDog)
    url_blackdog = "https://www.blackdog.cl"
    driver_path = r'E:\chromedriver_win32\chromedriver-win64\chromedriver.exe'

    # Configurar opciones para el navegador Chrome
    chrome_options = webdriver.ChromeOptions()
    #headless
    chrome_options.add_argument("--headless")
    #other options
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--allow-insecure-localhost")
    chrome_options.add_argument("--window-size=1920,1200")
    # Configurar el nivel de registro para ocultar mensajes de JavaScript
    chrome_options.add_argument("--log-level=3")
    # Crea una nueva instancia del controlador de Chrome para la primera tienda
    service = Service(driver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)
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

# Función para obtener datos de la segunda tienda (OpenBox)
def get_openboxstore_data():
    # URL de la segunda tienda
    url_openboxstore = "https://www.openboxstore.cl/patines/agresivos"
    driver_path = r'E:\chromedriver_win32\chromedriver-win64\chromedriver.exe'

    # Configurar opciones para el navegador Chrome
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")  # Ejecutar en modo headless
    chrome_options.add_argument("log-level=3")  # Configurar el nivel de registro

    # Crea una nueva instancia del controlador de Chrome para la primera tienda
    service = Service(driver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)
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
            brand = brand if brand else name.split()[0]

            # Almacena los datos en un diccionario
            product_data = {
                "name": name,
                "regular_price": regular_price,
                "offer_price": offer_price,
                "link": link,
                "image": image,
                "categories": [category],
                "brands": [brand] 
                
            }

            # Agrega los datos del producto a la lista
            openboxstore_data.append(product_data)




        # Busca si hay botones para la siguiente página
        next_buttons = driver.find_elements(By.XPATH, '//div[@class="custom-pager border rounded-pill overflow-hidden"]/a')
        if len(next_buttons) < 2 or "disabled" in next_buttons[1].get_attribute("class"):
            break  # Si no se encuentran suficientes botones de siguiente página o el segundo está desactivado, sal del bucle

        # Si hay una página siguiente, haz clic en el segundo botón para cargarla
        next_buttons[1].click()
        # time.sleep(1)  # Espera un poco para que los nuevos productos carguen completamente

    # Cierra el navegador
    driver.quit()

    # Retorna los datos obtenidos de OpenBoxStore
    return openboxstore_data

# Función para obtener datos de la tercera tienda (Unity)
def get_unity_data():
    # URL de la tercera tienda
    url_unity = 'https://www.unity-skateshop.cl/index.php/categoria-producto/patines/agresivos/?products-per-page=all'
    driver_path = r'E:\chromedriver_win32\chromedriver-win64\chromedriver.exe'
    
    # Configurar opciones para el navegador Chrome
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")  # Ejecutar en modo headless
    chrome_options.add_argument("log-level=3")  # Configurar el nivel de registro

    # Crea una nueva instancia del controlador de Chrome para la primera tienda
    service = Service(driver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.maximize_window()

    # Navega a la URL de la tercera tienda
    driver.get(url_unity)

    # Espera un momento para que se carguen completamente los elementos en la página
    time.sleep(2)

    # Lista para almacenar los datos de la tercera tienda
    unity_data = []

    # Encontrar todos los elementos de productos en la página
    products = driver.find_elements(By.CLASS_NAME, 'product-inner')

    # Iterar sobre los elementos de productos y extraer la información relevante
    for product in products:
        # Extraer el nombre del producto
        name = product.find_element(By.CLASS_NAME, 'title').text.strip()

        # Extraer el precio del producto utilizando XPath
        price_elements = product.find_elements(By.XPATH, '//span/span/bdi')
        price = price_elements[1].text.strip() if price_elements else None

        # Extraer el enlace del producto
        link = product.find_element(By.TAG_NAME, 'a').get_attribute('href')

        # Extraer la imagen del producto
        image = product.find_element(By.TAG_NAME, 'img').get_attribute('src')

        # Extraer las categorías del producto
        categories_element = product.find_element(By.CLASS_NAME, 'category')
        categories = [a.text.strip() for a in categories_element.find_elements(By.TAG_NAME, 'a')]

        # Dejar el campo de la marca vacío
        brand = ""

        # Crear el diccionario de datos del producto
        product_data = {
            "name": name,
            "price": price,
            "link": link,
            "image": image,
            "categories": categories,
            "brand": brand
        }

        # Agregar el diccionario de datos del producto a la lista
        unity_data.append(product_data)

    # Cerrar el navegador
    driver.quit()

    # Retornar los datos obtenidos de Unity Skate Shop
    return unity_data


    



# Función para asignar ID único a cada elemento en el archivo JSON
def assign_ids_to_items(data):
    for i, item in enumerate(data, start=1):
        item["id"] = i
    return data



# # Mide el tiempo de ejecución
# start_time = time.time()

# # Ejecutar las funciones en paralelo usando ThreadPoolExecutor
# with ThreadPoolExecutor(max_workers=2) as executor:
#     blackdog_future = executor.submit(get_blackdog_data)
#     openboxstore_future = executor.submit(get_openboxstore_data)

#     # Obtener los resultados de las funciones
#     blackdog_data = blackdog_future.result()
#     openboxstore_data = openboxstore_future.result()

# # Lee los datos existentes del archivo JSON
# with open("patines_agresivos_data.json", "r") as file:
#     existing_data = json.load(file)

# # Agrega los datos de OpenBoxStore a los datos existentes
# existing_data.extend(openboxstore_data)

# # Asigna ID único a cada elemento en el archivo JSON
# existing_data_with_ids = assign_ids_to_items(existing_data)

# # Sobrescribe el archivo JSON con los datos combinados que ahora tienen IDs únicos
# with open("patines_agresivos_data.json", "w") as file:
#     json.dump(existing_data_with_ids, file, indent=4)

# # Calcula el tiempo de ejecución
# end_time = time.time()
# execution_time = end_time - start_time

# # Imprime el tiempo total de ejecución
# print("Tiempo de ejecución:", execution_time, "segundos")
