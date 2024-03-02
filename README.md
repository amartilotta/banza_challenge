# Challenge-Banza
Repositorio backend para un sistema de control de movimientos monetarios.

### Requerimientos recomendados:

    Python v3.11


### Instalación

Antes que nada se debe preparar en la carpeta donde se descargo el proyecto (afuera de src) el entorno virtual de python con el comando

.\venv\Scripts\activate

Una vez descargado el proyecto y en la carpeta raiz del mismo se debe instalar las dependencias con el comando

pip install -r requirement.txt


### Levantar proyecto


Para ejecutar el proyecto y que se levanta el servidor se deberá correr sobre la carpeta src

uvicorn app:app --reload

Esto creará un servidor donde está corriendo la app, en la siguiente url http://localhost:8000/

### Estructura del proyecto

Para una correcta organización, el proyeco se dividió en varias carpetas dentro de la carpeta src, cada una almacena elementos con responsabilidades separadas y se divide en:
- db: Esta carpeta almacena los archivos relacionados con la base de datos. Esto incluye los modelos de las tablas de la base de datos, así como cualquier configuración necesaria para interactuar con la base de datos, como la configuración de la conexión.
- managers: En esta carpeta se encuentran los servicios o managers, que son responsables de manejar la lógica de negocio de la aplicación. Estos managers pueden interactuar con la base de datos a través de los modelos y también pueden integrarse con servicios externos.
- routers: Aquí es donde se encuentran definidos los endpoints de la API. Cada archivo en esta carpeta puede contener uno o más routers que definen las rutas y manejan las solicitudes HTTP entrantes, delegando la lógica de manejo a los managers correspondientes.
- test: Esta carpeta contiene archivos de prueba para la aplicación. Estos archivos incluyen pruebas unitarias y de integración que verifican el correcto funcionamiento de los endpoints y la lógica de negocio de la aplicación


### Archivo de configuración

Dentro de la carpeta raiz se deberá crear un archivo ENV, donde se debe colocar la ruta donde

"DATABASE_PATH": "RUTA_DONDE_GUARDAR_LA_BASE_DE_DATOS"
