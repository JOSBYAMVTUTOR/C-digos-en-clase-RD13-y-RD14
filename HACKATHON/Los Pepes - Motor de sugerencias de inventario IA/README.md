**Motor de Sugerencias de Inventario IA** 



Este proyecto consiste en una aplicación ejecutable desarrollada con Streamlit cuyo objetivo es predecir la demanda futura de productos a partir de datos históricos contenidos en un archivo .csv que contenga información sobre los productos y sus ventas. A partir de esta predicción, el sistema estima la banda inferior de stock y envía señales al departamento de compras para evitar déficits de inventario. 

&nbsp;  



**Pre-requisitos**  



Python. 



Anaconda. 



Anaconda prompt. 



Un entorno en Anaconda de Python. 



Librerías streamlit, pandas, prophet y plotly dentro del entorno. 



&nbsp; 



**Ejecución** 

&nbsp;



1. Abrir Anaconda Prompt. 



2\. Digitar “conda activate \[nombre del entorno con Python]” 



3\. Entrar en la carpeta o ruta donde está el archivo app.py descargado. 



4\. Copiar la ruta de la carpeta que contiene el app.py (ejemplo: “C:\\Users\\user\\Desktop\\Proyecto”). 



5\. Digitar en el Anaconda Prompt: “cd \[insertar la ruta copiada en el paso anterior”] (ejemplo: cd C:\\Users\\user\\Desktop\\Proyecto). Esto abrirá la carpeta donde está contenido el documento app.py. 



6\. Una vez dentro de la misma, digitar “streamlit run app.py”. Esto debería abrir el programa en una pestaña del navegador predeterminado. 



&nbsp; 



**Una vez dentro** 

&nbsp;



El programa muestra un entorno bastante amigable. 



Lo primero que debe hacerse es seleccionar el botón para cargar un archivo en el centro de la pantalla. Esto abrirá un buscador de archivos donde debe seleccionarse el documento .csv a cargar. De no tener ninguno, el programa da la opción de descargar un ejemplo utilizable a modo de demo. 



Una vez cargado el .csv, pedirá que especifiquemos tres menús desplegables las columnas correspondientes a las fechas, el id o nombre de los productos, y la cantidad vendida. Deben seleccionarse con el nombre con el que están disponibles en el archivo .csv. Posteriormente, se especifica el ID o nombre del producto a analizar y damos click en “analizar”. 



Aparecerán ilustradas las bandas de restock mencionadas más arriba, junto con una evolución histórica de la cantidad demanda y las bandas mismas. 



Más abajo aparecen las unidades a ordenar para cubrir el tiempo de entrega, cuánto debe ordenarse, cuál es el intervalo de confianza y los días en que llegaría el restock. Se pueden descargar estos resultados en formato .csv. 



En la parte izquierda se pueden modificar tanto el intervalo de confianza de la predicción, así como el tiempo de entrega que tarda el restock en llegar. 

