# Metrobus_CDMX

Proyecto realizado con la finalidad de conocer las ubicaciones de las estaciones del Metrobús de la Ciudad de México. 

Para el desarrollo backend se utiliza el framework **Django** el cual se encuentra escrito en el lenguaje de programación **Python**. La base de datos utilizada es **SQLite** la cual es proporcionada por el framework **Django**. Para realizar las consultas a la API desarrollada, se utiliza el lenguaje de consulta **GraphQL**. Para facilitar despliegue del proyecto, se utiliza **Docker**.

El archivo *Diagrama_Solucion.pdf* contiene el diagrama de la solución, se encuentra divido en las tecnologías utilizadas y los procesos para las que fueron utilizadas.

## Ejecución del proyecto

Para poder ejecutar el proyecto es necesario crear el contenedor de Docker con las siguientes instrucciones:

- Se construye la imagen de docker:

    `docker build -t dev/metrobus . `

- Se crea el contenedor para iniciar la API:

    `docker build -t dev/metrobus_cdmx/metrobus . `

## Prueba del proyecto

El endpoint desarrollado para realizar las consultas den GraphQL es */consultas/*. A continuación se enlistan algunas pruebas que pueden realizarce:

- Obtener una lista de unidades disponibles:
    ```
    {
        estaciones {
            id
            nombre
        } 
    }
    ```
- Consultar la ubicación de una unidad dado su ID:
    ```
    {
        estaciones(id:5) {
            ubicacion
        } 
    }
    ````
- Obtener una lista de alcaldías disponibles
    ```
    {
        alcaldias{
            id
            nombre
        } 
    }
    ```
- Obtener la lista de unidades que se encuentren dentro de una alcaldía
    ```
    {
        estaciones(alcaldiaId: 5){
            id
            nombre
            alcaldia {
            nombre
            }
        } 
    }
    ```