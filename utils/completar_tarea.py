import streamlit as st
from chromadb import Collection
from example import tareas

# Definiendo la lógica de finalizar una tarea
def completar_tarea(id_tarea: list, coleccion: Collection):
    for tarea in tareas:
        # Encontrar la tarea a editar
        if tarea["id"] == id_tarea:
            coleccion.update(
                ids=[tarea["id"]],  #Buscar referencia por ID
                metadatas=[{"estado": not tarea["estado"]}]  #Actualiza únicamente el campo "estado" de la metadata
            )
            st.rerun()