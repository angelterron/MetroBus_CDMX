import os
import django
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'metrobus.settings')

django.setup()

from zipfile import ZipFile
import pandas as pd
from bs4 import BeautifulSoup
import numpy as np
from geopy.geocoders import Nominatim

from estaciones.Alcaldias.models import Alcaldia
from estaciones.Tipos_Estacion.models import Tipo_Estacion
from estaciones.Estaciones.models import Estacion

def crear_diccionario(lista_objetos):
    """
    Recibe como parametros una lista de objetos que contienen
    los atributos id y nombre para generar un diccionario.
    """
    diccionario = {}
    for objeto in lista_objetos:
        diccionario[objeto.nombre] = objeto.id

    return diccionario

def import_data(arg):
    """
    Proceso ETL de las estaciones de la Ciudad de México
    """

    # Se verifica que se hayan recibido argumentos
    if len(arg) < 1:
        print('Es necesario el nombre del directorio donde se encuentra el archivo a cargar.')
        return

    # Se obtiene el primer argumento con el directorio donde se
    # encuentra el archivo a extraer
    dir = arg[0]
    
    # Se verifica que el directorio exista
    if os.path.exists(dir) == False:
        print('El directorio no existe')
        return
    
    file = 'Metrobus_estaciones.kmz' # Nombre del archivo que contiene la información
    path = os.path.join(dir, file) # Ruta donde se encuentra el archivo

    # Se descomprime el archivo kmz
    kmz = ZipFile(path)

    # Se iteran los archivos y se obtiene el que tenga una extensión kml
    for file_kmz in kmz.filelist:                                
        if str(file_kmz.filename).endswith('.kml'):                
            kml_string = kmz.open(file_kmz, 'r').read()

    # Se le da formato de xml al texto dentro del archivo kml
    soup = BeautifulSoup(kml_string, 'xml')
    
    rows = [] # Lista para almacenar todas las estaciones

    # Se buscan todas las etiquetas Placemark y se iteran para extraer la información de las estaciones
    for element in soup.find_all('Placemark'):
        row = {} # Diccionario para almacenar los datos de las estaciones
        # Se buscan todas las etiquetas Data y se iteran para extraer los atributos de las estaciones
        for val in element.find_all('Data'):        
            row[val.find('displayName').text] = val.find('value').text.strip() # Se agrega el nombre del atributo y su valor al diccionario
        
        # Se obtienen las coordenadas de las estaciones buscando la etiqueta 'coordinates'
        row['coordinates'] = element.find('coordinates').text.strip()
        # Se agrega el diccionario a la lista de estaciones
        rows.append(row) 

    df = pd.DataFrame(rows) # Se convierte la lista de diccionarios en un dataframe

    geolocator = Nominatim(user_agent="estaciones")  # Se inicializa el objeto para obtener las direcciones con las coordenadas

    df['Ubicacion'] = df['coordinates'].apply(lambda x: geolocator.geocode(x.split(',')[1]+','+x.split(',')[0]).address) # Se obtienen las direcciones con las coordenadas

    alcaldias = np.unique(df['ALCALDIAS']) # Se obtienen los nombres de las diferentes alcaldias
    tipos_estacion = np.unique(np.unique(df[df['TIPO'] != '']['TIPO'])) # Se obtienen los nombres de los diferentes tipos de estaciones

    # Se agregan las alcaldias a la base de datos
    for alcaldia in alcaldias:
        Alcaldia.objects.update_or_create(
            nombre = alcaldia
        )

    # Se agregan los tipos de estación a la base de datos
    for tipo in tipos_estacion:
        Tipo_Estacion.objects.update_or_create(
            nombre = tipo
        )        
    
    # Se transforma en diccionario la lista de alcaldias
    diccionario_alcaldias = crear_diccionario(
        Alcaldia.objects.all()
    )

    # Se transforma en diccionario la lista de tipos de estacion
    diccionario_tipo = crear_diccionario(
        Tipo_Estacion.objects.all()
    )

    df['ALCALDIAS'] = df['ALCALDIAS'].apply(lambda x: diccionario_alcaldias[x]) # Se cambia el nombre de la alcaldia por el identificador del catálogo recien creado en la base de datos
    df['TIPO'] = df['TIPO'].apply(lambda x: int(diccionario_tipo[x]) if x != '' else None) # Se cambia el nombre del tipo de estación por el identificador del catálogo recien creado en la base de datos

    # Se itera el dataframe de estaciones para almacenar la información en la base de datos
    for index, row in df.iterrows():        
        tipo = np.nan_to_num((row['TIPO'])) # Al existir valores NaN se convierten a tipo flotante 
        
        # Se verifica si no cuenta con tipo de estación
        if tipo == 0.0:
            tipo = None # Se le asigna un valor de None para se almacene como NULL dentro de la base de datos
        
        # se realiza el guardado de la estación
        Estacion.objects.update_or_create(
            nombre = row['NOMBRE'],
            linea = row['LINEA'],
            est = row['EST'],
            cve_est = row['CVE_EST'],
            cve_eod17 = row['CVE_EOD17'],
            tipo_id = tipo,
            alcaldia_id = row['ALCALDIAS'],
            anio = row['AÑO'],
            ubicacion = row['Ubicacion'],
        )
    
    
    
if __name__ == "__main__":
    import_data(sys.argv[1:])