import pandas as pd

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()
driver.get("https://webgate.ec.europa.eu/fleet-europa/search_en")

wait = WebDriverWait(driver, 1)

# Hacer clic en el botón "EU"
eu_option = wait.until(EC.element_to_be_clickable((By.XPATH, "//label[@for='countryType1']")))
eu_option.click()

# Hacer click en "All Vessels"
all_vessels_option = wait.until(EC.element_to_be_clickable((By.XPATH, "//label[@for='period1']")))
all_vessels_option.click()

# Hacer clic en el botón "Search"
btn_search = wait.until(EC.element_to_be_clickable((By.XPATH, "//button/span[text()='Search']")))
btn_search.click()


#-----------------------------------------------------------------------------------------------------#

# Esperar a que el selector de la página de resultados se muestre
wait.until(EC.presence_of_element_located((By.CLASS_NAME, "select2-selection--single")))

# Esperar hasta que el elemento esté visible y clickeable
page_size_selector = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "select2-selection--single")))
wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "select2-selection--single")))

# Hacer clic en el selector
page_size_selector.click()

# Esperar a que la lista con opciones sea visible
#wait.until(EC.presence_of_element_located((By.XPATH, "//ul[@class='select2-results__options']")))
#
## Intentar hacer clic en la opción que contiene el texto "100"
page_size_100 = wait.until(EC.element_to_be_clickable((By.XPATH, "//li[contains(text(),'100')]")))
#
## Desplazar el elemento a la vista para asegurar que se puede hacer clic
#driver.execute_script("arguments[0].scrollIntoView(true);", page_size_100)
#
## Usar JavaScript para hacer clic en el elemento
driver.execute_script("arguments[0].click();", page_size_100)

#-----------------------------------------------------------------------------------------------------#
# Esperar a que la tabla cargue
wait.until(EC.presence_of_element_located((By.CLASS_NAME, "table-header-container")))

# Nº de resultados por página 100
page_size_selector = driver.find_element(By.CLASS_NAME, "select2-selection--single")
page_size_selector.click()

# Extraer los nombres de las columnas 
column_headers = driver.find_elements(By.XPATH, "//div[@class='table-header-container']/span")
column_names = [header.text.strip() for header in column_headers] 

# Contenido de las filas
rows = driver.find_elements(By.XPATH, "//table/tbody/tr")

data = []

while True:
    # Extraer filas de la tabla
    rows = driver.find_elements(By.XPATH, "//table/tbody/tr")
    
    for row in rows:
        cells = row.find_elements(By.TAG_NAME, "td")
        row_data = [cell.text.strip() for cell in cells]  # Solo tomar los primeros 3 campos
        data.append(row_data)

    # Intentar encontrar el botón "Next"
    try:
        # Buscar el botón "Next" usando el atributo aria-label
        next_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@aria-label='Go to next page']")))

        # Desplazar hasta el botón "Next"
        driver.execute_script("arguments[0].scrollIntoView(true);", next_button)
        
        # Verificar si el botón "Next" está habilitado
        if "disabled" not in next_button.get_attribute("class"):  
            # Hacer clic en el botón "Next"
            next_button.click()
            wait.until(EC.presence_of_element_located((By.TAG_NAME, "table")))  # Esperar a que la nueva página cargue
        else:
            break  # Si el botón está deshabilitado, salir del bucle
    except:
        break  # Si no hay botón "Next" o hubo un error, salir del bucle
   

# Crear DataFrame con todos los datos recopilados
df = pd.DataFrame(data, columns=column_names)

df.to_csv("./data/resultados_scrapping_fleet.csv", index= False, encoding= "uft-8")

# Cerrar el driver
driver.quit()