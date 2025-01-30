import streamlit as st
from chromadb import Collection
from crear_tarjeta import nueva_tarjeta

# Definición de las tabs necesarias
tabs = st.tabs(["Tareas pendientes", "Tareas completadas"])
estados_tabs = {
    True: tabs[0],
    False: tabs[1]
}

# Bucle principal que clasifica las tareas según su estado
def clasificacion_tareas(coleccion: Collection):
    for tab_index, (estado, tab) in enumerate(estados_tabs.items()):
        with tab:
            # La definición de las columnas debe estar dentro del bloque with, esto es debido a que si
            # se pone fuera del bloque with, se va a compartir en toda la interfaz de Streamlit, lo cuál
            # compartirá espacio con las demás tabs, causando duplicidad.
            col1, col2 = st.columns(2, gap="large")
            
            # Preparando el diccionario a analizar para filtrar
            data = coleccion.get()["metadatas"]
            tareas_filtradas = [t for t in data[tab_index]["estado"] if t["estado"] == estado]
            
            # Verificar la existencia de tareas por categoría (Tab)
            if not tareas_filtradas:
                st.info("No hay tareas en esta categoría.")
            
            # Asignar las columnas según la tab elegida, donde las tareas con id impar
            # se mostrarán en la izquierda y las tareas con id par en la derecha
            for i, tarea in enumerate(tareas_filtradas):
                col = col1 if i % 2 == 0 else col2
                nueva_tarjeta(tarea, col, tab_index, coleccion)