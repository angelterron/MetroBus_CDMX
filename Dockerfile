# Se utiliza una imagen de python como base
FROM python:3.8.15-alpine3.16

# Se habilita la opción para permitir a Python mostrar mensajes en consola
ENV PYTHONUNBUFFERED=1

# Directorio de trabajo
WORKDIR /app

# Instalar paquetes necesarios
RUN apk update \
    && apk add --no-cache gcc g++ libxml2-dev libxslt-dev python3-dev \
    && pip install --upgrade pip

# Agregar archivo requriments.txt a la virtualización
COPY ./requirements.txt ./

# Instalar las librerias del archivo requirements.txt
RUN pip install -r requirements.txt

# Copiar el contenido del proyecto
COPY ./ ./

# Ejecutar los comandos para realizar las migraciones de Django.
# La aplicación es llamada estaciones
# Se ejecuta el archivo data.py para realizar el proceso ETL de las estaciones
# Al finalizar se inicia el servidor con la ip 0.0.0.0 para que sea visible fuera del contenedor
CMD python metrobus/manage.py makemigrations estaciones;python metrobus/manage.py migrate estaciones;python metrobus/data.py metrobus/mb_kmz;python metrobus/manage.py runserver 0.0.0.0:8000

