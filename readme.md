Aplicación de Encuestas de Consumo de Bebidas

Esta aplicación permite gestionar encuestas sobre el consumo de bebidas, con una interfaz gráfica moderna desarrollada en Python usando Tkinter y MySQL como base de datos.

📋 Requisitos Previos

Python 3.x

Puedes descargarlo desde python.org


MySQL Server

Descarga e instala MySQL Server desde mysql.com


Dependencias de Python ( Poner los siguientes comandos en el CMD para la instalacion )

bashCopypip install mysql-connector-python
pip install pandas
pip install matplotlib


🛠️ Configuración de la Base de Datos

1. Abre MySQL Command Line Client o MySQL Workbench

2. Ejecuta el script SQL proporcionado en encuestas.sql:

3. Configura la conexión a la base de datos en db.py:

pythonCopyconn = mysql.connector.connect(
    host='localhost',
    database='encuestas',
    user='root',
    password='tu_contraseña'  # Cambia esto por tu contraseña
)


🚀 Ejecución del Programa

1. Descarga todos los archivos del proyecto en una carpeta
Asegúrate de tener todos los archivos necesarios:

- main.py
- app.py
- db.py
- styles.py
- encuestas.sql


2. Ejecuta el programa:
bashCopypython main.py


💻 Uso de la Aplicación
Operaciones CRUD

1. Crear (Create)

Rellena todos los campos en el formulario
Haz clic en "Agregar Encuesta"


2. Leer (Read)

Introduce el ID de la encuesta
Haz clic en "Leer Encuesta"


3. Actualizar (Update)

Introduce el ID de la encuesta a modificar
Actualiza los campos deseados
Haz clic en "Editar Encuesta"


4. Eliminar (Delete)

Introduce el ID de la encuesta
Haz clic en "Eliminar Encuesta"



Filtros y Ordenación

Filtrar datos

Usa los controles de filtro en la parte superior de la tabla
Puedes filtrar por:

- Rango de edad
- Sexo
- Consumo de bebidas




Ordenar datos

Haz clic en los encabezados de las columnas para ordenar
Cada clic alterna entre orden ascendente y descendente



Visualización de Datos

Exportar a Excel

Haz clic en "Exportar a Excel"
Selecciona la ubicación para guardar el archivo


Gráficos

"Gráfico Consumo por Edad": Muestra el consumo promedio por grupos de edad
"Gráfico Alcohol vs Salud": Visualiza la relación entre consumo total y pérdidas de control



🎨 Características de la Interfaz

Diseño moderno y limpio
Botones con efectos hover
Tabla con scroll y ordenamiento
Filtros intuitivos

⚠️ Solución de Problemas Comunes

Error de conexión a MySQL

Verifica que MySQL Server esté en ejecución
Asegúrate de que la base de datos 'encuestas' existe

- El error mas habitual puede ser la conexion con la base de datos, pero para ello lo mas importante es tener claro todos los datos para conseguir enlazarlo con ella. 


Error en la tabla

Ejecuta nuevamente el script SQL
Verifica que todos los campos coincidan con la estructura especificada


Problemas con los gráficos

Asegúrate de tener matplotlib instalado correctamente
Verifica que haya datos en la base de datos

