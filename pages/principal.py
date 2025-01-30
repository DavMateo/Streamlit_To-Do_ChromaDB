import streamlit as st
from chromadb import Collection
from components.info_proyecto import info_proyecto
from components.clasificacion_tareas import clasificacion_tareas

st.title("To-Do List web app 📝")

def render(coleccion: Collection):
    info_proyecto(
        "Información sobre el proyecto",
        "Aplicación web con el objetivo de servir como un gestor de tareas básico basado en la nube. Está aplicación está construída 100% sobre Python, desde su backend hasta su frontend mediante el uso de Streamlit y ChromaDB para base de datos vectorial en conjunto con el modelo de IA de embeddings 'sentence-transformers/all-MiniLM-L6-v2' para vectorizar y optimizar las búsquedas por vectores."
        "Este es un proyecto escolar, enfocado al aprendizaje de la Inteligencia Artificial mediante Python."
    )
    clasificacion_tareas(coleccion)