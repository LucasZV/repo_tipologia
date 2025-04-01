# Tipología y ciclo de vida de los datos: 
# PR1: ¿Cómo podemos capturar los datos de la web?

## Descripción 

Este proyecto utiliza Selenium para automatizar la extracción de datos desde el sitio web de Fleet Europa de la Unión Europea. El script automatiza la búsqueda de todos los barcos registrados, navega a través de las páginas de resultados y guarda los datos en un archivo CSV.

## Estructura del Proyecto

La librería tiene la siguiente jerarquía:

REPO_TIPOLOGIA/  
├── data/                                # Datos generados en la PR1  
│   ├── resultados_fleet.csv             # Archivo CSV con los datos resultado de la página/s.  
├── memoria/                             # Informes de la PR1  
│   ├── PR1_Julio-Lucas.docx             # Memoria docx con las respuestas a los diferentes apartados   
├── src/                                 # Código fuente   
│   ├── scrapping_CFRs_EU_PRUEBAS.ipynb  # Jupyter notebook de pruebas  
│   ├── scrapping_fleet_EU.py            # Código Python para realizar la captura de los datos de la web  
├── README.md                            # Archivo de documentación del proyecto  
├── requirements.txt                     # Lista de dependencias necesarias  
  
### Archivos Principales

- src/: Contiene el código fuente para la captura de los datos de la web.
- memoria/: Contiene el informe solicitado en la PR1, completando cada uno de los apartados requeridos.
- data/: Contiene el dataset en formato csv, capturado, transformado y almacenado para su posterior manipulacion y/o análisis.

## Uso

Para capturar los datos desde la web de [Fleet Europa de la Unión Europea]("https://webgate.ec.europa.eu/fleet-europa/search_en") sigue estos pasos:

### 1.  Abre la terminal en VSCode:
Haz clic en el menú "Terminal" y selecciona "Nueva terminal".
Asegúrate de que estás en el directorio del proyecto donde se encuentran los subdirectorios listados arriba.
Puedes ejecutar: 
```bash
cd Repo_Tipologia
```
### 2. Instala las dependencias:
Asegúrate de haber instalado las dependencias listadas en `requirements.txt` antes de ejecutar el archivo principal:
```bash
pip install -r requirements.txt
```
### 3. Ejecuta el archivo principal:

1. Ejectuta el script de la siguiente manera:

- Si lo ejecutas desde Windows simplemente ejecuta el siguiente comando en la terminal: 
```bash
python scrapping_fleet_EU.py
```
- Si usas macos y quieres evitar mensajes de warnings ejecuta: 
```bash
QT_LOGGING_RULES="*.debug=false" python scrapping_fleet_EU.py
```

2.  El script realizará lo siguiente:

- - Accederá a la página de Fleet Europa.
- - Seleccionará la opción "EU" y "All Vessels".
- - Iniciará la búsqueda de barcos registrados.
- - Ajustará el número de resultados por página a 100.
- - Recorrerá todas las páginas de resultados.
- - Extraerá los datos y los guardará en ./data/resultados_scrapping_fleet.csv.

## Licencia

Este proyecto está bajo la Licencia MIT, lo que te permite usar, modificar y distribuir el software libremente, siempre y cuando mantengas el aviso de copyright. 
Consulta el archivo [`LICENSE`](./LICENSE) o [Licencia MIT](https://opensource.org/licenses/MIT) para más detalles.

