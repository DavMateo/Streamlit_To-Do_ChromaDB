import streamlit as st
from datetime import datetime
from utils.cant_cpu import cant_cpus_disp
from config.db import config_inicial
from utils.ai_modelo_embeddings import conexion_modelo
from pages.principal import render

##########################
### INICIANDO PROGRAMA ###
##########################
#
# Configurando la conexión a la base de datos ChromaDB
dict_config_coleccion = cant_cpus_disp()
client, coleccion = config_inicial(
    "./data", "tareas", 
    "Esta colección almacenará toda la información de las tareas del usuario ordenados por índice.",
    str(datetime.now()), "cosine", dict_config_coleccion["search_ef"],
    dict_config_coleccion["construction_ef"], dict_config_coleccion["cant_cpu"]
)
# Inicializando modelo de embedding
model = conexion_modelo("sentence-transformers/all-MiniLM-L6-v2")


##########################################
### RENDERIZADO FRONTEND CON STREAMLIT ###
##########################################
#
# Configurando página Streamlit
st.set_page_config(page_title="To-Do List", layout="wide")
render(coleccion)