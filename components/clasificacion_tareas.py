import ast
import streamlit as st
from chromadb import Collection
from components.crear_tarjeta import nueva_tarjeta

# Definición de las tabs necesarias
tabs = st.tabs(["Tareas pendientes", "Tareas completadas"])
estados_tabs = {
    True: tabs[0],
    False: tabs[1]
}

# Bucle principal que clasifica las tareas según su estado
def clasificacion_tareas(coleccion: Collection):
    for tab_index, (estado, tab) in enumerate(estados_tabs.items()):
        st.write(estado)
        
        with tab:
            # La definición de las columnas debe estar dentro del bloque with, esto es debido a que si
            # se pone fuera del bloque with, se va a compartir en toda la interfaz de Streamlit, lo cuál
            # compartirá espacio con las demás tabs, causando duplicidad.
            col1, col2 = st.columns(2, gap="large")
            
            # Preparando el diccionario a analizar para filtrar
            data = formateo_data(coleccion)
            tareas_filtradas = [t for t in data if t["estado"] == estado]
            
            # Verificar la existencia de tareas por categoría (Tab)
            if not tareas_filtradas:
                st.info("No hay tareas en esta categoría.")
            
            # Asignar las columnas según la tab elegida, donde las tareas con id impar
            # se mostrarán en la izquierda y las tareas con id par en la derecha
            for i, tarea in enumerate(tareas_filtradas):
                col = col1 if i % 2 == 0 else col2
                nueva_tarjeta(tarea, col, tab_index, coleccion)
                

# Definiendo función para formatear la información pertinente
def formateo_data(coleccion: Collection) -> list:
    # Definiendo las variables necesarias para la función
    data = coleccion.get()
    lst_keys = ["id", "titulo", "descripcion", "fecha", "estado"]
    lst_data_dict = []
    lst_data = []
    
    # Bucle de ordenamiento para estructura de diccionario con los datos de chromadb
    for i in range(len(data["ids"])):
        lst_apoyo = []  #Variable temporal
        
        # Bucle para dar forma a la estructura de la matriz
        #
        # El objetivo es hacer que la data traída de ChromaDB sea legible por el programa actual.
        # Se busca generar una lista de diccionarios con una estructura específica de:
        # "id", "titulo", "descripcion", "fecha" y "estado" que será usado por el programa. En base
        # a esto, se está preparando la información en una lista con tantas listas como "ids" tenga
        # la consulta "get" de ChromaDB para usar la función de crear diccionario con "zip()".
        for key in data:
            # Se filtra los campos que no tengan información
            if data[key] != None:
                if key == "documents":
                    lst_to_dict = ast.literal_eval(data[key][i])
                    # Se convierte el string a diccionario y se obtienen los dos campos solicitados
                    lst_apoyo.append(lst_to_dict["titulo"])
                    lst_apoyo.append(lst_to_dict["descripcion"])
                
                elif key == "metadatas":
                    lst_apoyo.append(data[key][i]["fecha"])
                    lst_apoyo.append(data[key][i]["estado"])
                
                else:
                    # En caso de haber otro tipo de información que pueda ser indexada en un futuro
                    lst_apoyo.append(data[key][i])
        lst_data_dict.append(lst_apoyo)  #Añade la lista formateada al contenedor de listas

    # Crea tantos diccionarios como sublistas hayan en "lst_data_dict"
    #
    # Los diccionarios se almacenarán en una lista, semejante a un formato JSON, donde habrán tantos
    # diccionarios como "ids" en la consulta "get()" de ChromaDB. Esta información es la requerida para
    # que el sistema pueda interpretar los datos que requiera durante su ejecución.
    for i in range(len(lst_data_dict)):
        lst_data.append(dict(zip(lst_keys, lst_data_dict[i])))
    
    # lst_data es la lista de diccionarios
    return lst_data