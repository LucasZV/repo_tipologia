import requests
from bs4 import BeautifulSoup
import pandas as pd

##------------------------------------------------------------------------------------------------------------##
# Scraping de datos de buques de España desde el censo de buques del Ministerio de Agricultura, Pesca y Alimentación
# Este script permite buscar buques por su CFR (Código de Flota de Registro) y extraer información relevante.
# El script utiliza la librería requests para realizar solicitudes HTTP y BeautifulSoup para analizar el HTML.

# Autor: Julio Úbeda Quesada y Lucas Zamora Vera
# Fecha: 2023-10-23

# Cargar el dataset
file_path = r"/Users/macbookairjulio/Documents/GitHub/repo_tipologia/data/resultados_fleet.csv"
df = pd.read_csv(file_path, dtype=str)  # Leer como string para evitar problemas de formato
# Filtrar solo los buques de España
df_esp = df[df["Flag"] == "ESP"].copy()
# Obtener la lista de identificadores únicos CFR
cfr_list = df_esp["CFR"].dropna().unique().tolist()
##------------------------------------------------------------------------------------------------------------##

# URL base de búsqueda
base_url = "https://servicio.pesca.mapama.es/censo/ConsultaBuqueRegistro/Buques/Search"

# Crear sesión para mantener cookies
session = requests.Session()

# Lista para almacenar los datos de los buques
data = []
# Lista para almacenar los CFRs sin buque asociado
cfrs_sin_buque = []

# Iterar sobre la lista de CFRs
total_cfrs = len(cfr_list)

# Mostrar el progreso
for index, cfr in enumerate(cfr_list, start=1):
    print(f"Procesando {index}/{total_cfrs}: CFR {cfr}")
    # Realizar la búsqueda del CFR
    params = {"text": cfr}
    # Realizar la solicitud GET con el CFR
    response = session.get(base_url, params=params)
    
    # Verificar si la solicitud fue exitosa
    if response.status_code == 200:
        # Analizar la respuesta HTML con BeautifulSoup
        soup = BeautifulSoup(response.text, "html.parser")
        # Buscar el pagina de detalles del buque
        buque_link = soup.find("a", class_="apply--emphasize")
        
        # Si se encuentra el enlace del buque, acceder a la página de detalles
        if buque_link:
            # Construir la URL completa del buque
            buque_url = "https://servicio.pesca.mapama.es" + buque_link["href"]
            # Realizar la solicitud a la página del buque
            buque_response = session.get(buque_url)
            
            # Verificar si la solicitud fue exitosa antes de extraer los datos
            if buque_response.status_code == 200:
                # Analizar la respuesta HTML de la página del buque
                buque_soup = BeautifulSoup(buque_response.text, "html.parser")
                # Extraer el nombre del buque
                nombre_buque = buque_soup.find("h2", class_="title--vessel-details").text.split("Nombre: ")[-1]
                
                # Crear un diccionario con CFR y nombre del buque
                datos_buque = {"CFR": cfr, "Nombre": nombre_buque}
                
                # Recorrer la pagina buscando etiquetas <div> para extraer los datos
                for div in buque_soup.find_all("div"):
                    label = div.find("dt", class_="info-field--label")
                    value = div.find("dd", class_="info-field--value")
                    if label and value:
                        datos_buque[label.text.strip()] = value.text.strip()
                
                # Agregar los datos del buque a la lista
                data.append(datos_buque)
                print(f"✔️ Datos extraídos para {cfr} ({nombre_buque})")
            # Si no se pudo acceder a la página del buque, registrar el CFR    
            else:
                print(f"❌ Error {buque_response.status_code}: No se pudo acceder a la página del buque {cfr}")
                cfrs_sin_buque.append(cfr)
        # Si no se encontró el enlace del buque, registrar el CFR
        else:
            print(f"⚠️ No se encontró un buque asociado para CFR {cfr}")
            cfrs_sin_buque.append(cfr)
    # Si no se pudo acceder a la página de búsqueda, registrar el CFR
    else:
        print(f"❌ Error {response.status_code}: No se pudo acceder a la página de búsqueda para CFR {cfr}")
        cfrs_sin_buque.append(cfr)

# Crear DataFrame con los datos obtenidos
df = pd.DataFrame(data)
print("\nExtracción finalizada.")
print(df)

# Mostrar CFRs sin buque asociado
if cfrs_sin_buque:
    print("\nCFRs sin buque asociado:")
    print(cfrs_sin_buque)

# Guardar los datos en un archivo CSV
output_file = r"./data/datos_buques_ESP.csv"
df.to_csv(output_file, encoding="utf-8", index=False)
print(f"\nDatos guardados en {output_file}")