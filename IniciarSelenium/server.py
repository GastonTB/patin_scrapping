import http.server
import json
import time
from urllib.parse import urlparse
from http import HTTPStatus
from concurrent.futures import ThreadPoolExecutor
from scraper import get_blackdog_data, get_openboxstore_data, get_unity_data, get_pedacity_data

class MyHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        # Parsea la URL
        parsed_path = urlparse(self.path)

        # Si la ruta coincide con lo que necesitas
        if parsed_path.path == "/patines_agresivos_data":
            # Mide el tiempo de ejecución
            start_time = time.time()

            # Ejecuta las funciones de scraping en hilos separados
            with ThreadPoolExecutor() as executor:
                future_blackdog = executor.submit(get_blackdog_data)
                future_openboxstore = executor.submit(get_openboxstore_data)
                future_unity = executor.submit(get_unity_data)
                future_pedalcity = executor.submit(get_pedacity_data)

                # Espera a que ambas funciones terminen y obtiene los resultados
                blackdog_data = future_blackdog.result()
                openboxstore_data = future_openboxstore.result()
                unity_data = future_unity.result()
                pedalcity_data = future_pedalcity.result()

            # Combina los datos
            combined_data = blackdog_data + openboxstore_data + unity_data + pedalcity_data

            # Asigna ID único a cada elemento en el archivo JSON
            # combined_data_with_ids = assign_ids_to_items(combined_data)

            # Convierte los datos combinados a JSON
            json_data = json.dumps(combined_data, indent=4)

            # Calcula el tiempo de ejecución
            end_time = time.time()
            execution_time = end_time - start_time

            # Establece las cabeceras de la respuesta
            self.send_response(HTTPStatus.OK)
            self.send_header("Content-type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")  # Permitir acceso desde cualquier origen
            self.send_header("Access-Control-Allow-Methods", "GET")  # Permitir método GET
            self.end_headers()

            # Escribir el JSON en el cuerpo de la respuesta
            self.wfile.write(json_data.encode("utf-8"))

            # Imprime el tiempo total de ejecución en el servidor
            print("Tiempo de ejecución:", execution_time, "segundos")
        else:
            # Si la ruta no es válida, devuelve un error 404
            self.send_error(HTTPStatus.NOT_FOUND, "Página no encontrada")

# Configura el servidor para escuchar en el puerto 8000
server_address = ("", 8000)
httpd = http.server.HTTPServer(server_address, MyHandler)

# Inicia el servidor
print("Servidor iniciado en el puerto 8000...")
httpd.serve_forever()
