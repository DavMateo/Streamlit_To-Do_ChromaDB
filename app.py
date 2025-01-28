import os
import chromadb
import streamlit as st
from sentence_transformers import SentenceTransformer
from chromadb import Settings
from datetime import datetime

# Definiendo las variables necesarias
PATH = "./data"
MODEL = "sentence-transformers/all-MiniLM-L6-v2"
COLLECTION_NAME = "tareas"


# Creando el directorio de permanencia de información de la base de datos
if os.path.exists(PATH):
    print("El directorio ya existe, continuando...")

else:
    print("El directorio no existe, creando...")
    os.makedirs(PATH, exist_ok=True)


# Función para obtener los núcleos del sistema
def cant_cpus_disp():
    cant_cpu = os.cpu_count()
    
    # Condicional para determinar la cantidad de CPUs disponibles a asignar a ChromaDB
    if cant_cpu == 0:
        return {
            "cant_cpu": 4,
            "search_ef": 200,
            "construction_ef": 200
        }
    
    else:
        # Si cantidad CPUs disponibles es igual o menor a 4, se usará toda la capacidad del CPU.
        # Otros parámetros serán ajustados a la medida según los CPUs disponibles.
        # Calidad estándar por default de los embeddings por ChromaDB.
        if cant_cpu <= 4:
            return {
                "cant_cpu": cant_cpu,
                "search_ef": 200,
                "construction_ef": 200
            }
        
        # Si cantidad CPUs es mayor a 4, se usará toda la capacidad del CPU menos 2.
        # Otros parámetros serán ajustados a la medida según los CPUs disponibles.
        # Mediana calidad de los embeddings por ChromaDB.
        elif cant_cpu > 4 and cant_cpu <= 8:
            return {
                "cant_cpu": cant_cpu - 2,
                "search_ef": 400,
                "construction_ef": 400
            }
        
        # Otros parámetros serán ajustados a la medida según los CPUs disponibles.
        # Máxima calidad de los embeddings por ChromaDB.
        else:
            return {
                "cant_cpu": cant_cpu - 2,
                "search_ef": 800,
                "construction_ef": 800
            }


# Inicializando y configurando la base de datos ChromaDB
def init_chroma(dict_config: dict) -> list:
    client = chromadb.PersistentClient(PATH, settings=Settings(anonymized_telemetry=False))
    coleccion = client.get_or_create_collection(
        name=COLLECTION_NAME,
        metadata={
            "descripcion": "Esta colección almacenará toda la información de las tareas del usuario ordenados por índice.",
            "creado": str(datetime.now()),
            "hnsw:space": "cosine",
            "hnsw:search_ef": dict_config["cant_cpu"],
            "hnsw:construction_ef": dict_config["search_ef"],
            "hnsw:num_threads": dict_config["cant_cpu"]
        }
    )
    return [client, coleccion]


# Inicializando y ejecución del modelo de embeddings
ai_model = SentenceTransformer(MODEL)

def generar_embedding(texto: str):
    return ai_model.encode(texto).tolist()


# Definiendo la interfaz gráfica con Streamlit
st.set_page_config(page_title="To-Do List", layout="wide")
st.title("To-Do List web app 📝")

# Componente contenedor que expande la información mediante click.
with st.expander("Información sobre el proyecto"):
    st.write("Aplicación web con el objetivo de servir como un gestor de tareas básico basado en la nube. Está aplicación está construída 100% sobre Python, desde su backend hasta su frontend mediante el uso de Streamlit y ChromaDB para base de datos vectorial en conjunto con el modelo de IA de embeddings 'sentence-transformers/all-MiniLM-L6-v2' para vectorizar y optimizar las búsquedas por vectores.")
    st.write("\nEste es un proyecto escolar, enfocado al aprendizaje de la Inteligencia Artificial mediante Python.")


# Diccionario de ejemplo
if "tareas" not in st.session_state:
    st.session_state.tareas = [
        {
            "id": "id1",
            "titulo": "Probando app Streamlit",
            "descripcion": "Esta es una tarea de prueba.",
            "fecha": "26/01/2025",
            "estado": True
        },
        {
            "id": "id2",
            "titulo": "Corrigiendo problemas del código",
            "descripcion": "Descripción de la **tarea n°2** del test.",
            "fecha": "14/01/2025",
            "estado": True
        }
    ]


# Definiendo la lógica de actualizar una tarea
def completar_tarea(id_tarea):
    for tarea in st.session_state.tareas:
        if tarea["id"] == id_tarea:
            tarea["estado"] = not tarea["estado"]
            st.rerun()


def crear_tarjeta(tarea, col, tab_index):
    with col:
        # Container: tarea
        with st.container(border=True):
            # Container: tarea__contenido
            with st.container():
                st.subheader(tarea["titulo"])
                st.markdown(tarea["descripcion"])
                
                # Container: contenido__btns
                with st.container():
                    btn1, btn2 = st.columns(2, vertical_alignment="center")
                    
                    with btn1:
                        if st.button(
                            "Completar" if tarea["estado"] else "Re-activar",
                            use_container_width=True, 
                            type="primary",
                            key=f"btn_toggle{tarea['id']}_{tab_index}"
                        ):
                            completar_tarea(tarea["id"])
                    
                    with btn2:
                        if st.button(
                            "Eliminar",
                            use_container_width=True,
                            type="secondary",
                            key=f"btn_delete{tarea['id']}_{tab_index}"
                        ):
                            st.session_state.tareas = [t for t in st.session_state.tareas if t["id"] != tarea["id"]]
                            st.rerun()
            
            # Container: tarea__footer
            with st.container():
                info_id, info_fecha = st.columns(2, vertical_alignment="center")
                
                with info_id:
                    st.markdown(f"""
                        <div style='
                            text-align: left; 
                            color: #5F6A6A; 
                            margin: .75rem 0;'>
                            ID: {tarea["id"]}
                        </div>
                    """, unsafe_allow_html=True)
                
                with info_fecha:
                    st.markdown(f"""
                        <div style='
                            text-align: right;
                            color: #5F6A6A;
                            margin: .75rem 0;'>
                            Fecha: {tarea["fecha"]}
                        </div>
                    """, unsafe_allow_html=True)



# Definición de las tabs necesarias
tabs = st.tabs(["Tareas pendientes", "Tareas completadas"])
estados_tabs = {
    True: tabs[0],
    False: tabs[1]
}

# Bucle principal que clasifica las tareas según su estado
for tab_index, (estado, tab) in enumerate(estados_tabs.items()):
    with tab:
        # La definición de las columnas debe estar dentro del bloque with, esto es debido a que si
        # se pone fuera del bloque with, se va a compartir en toda la interfaz de Streamlit, lo cuál
        # compartirá espacio con las demás tabs, causando duplicidad.
        col1, col2 = st.columns(2, gap="large")
        tareas_filtradas = [t for t in st.session_state.tareas if t["estado"] == estado]
        
        # Verificar la existencia de tareas por categoría (Tab)
        if not tareas_filtradas:
            st.info("No hay tareas en esta categoría.")
        
        # Asignar las columnas según la tab elegida, donde las tareas con id impar
        # se mostrarán en la izquierda y las tareas con id par en la derecha
        for i, tarea in enumerate(tareas_filtradas):
            col = col1 if i % 2 == 0 else col2
            crear_tarjeta(tarea, col, tab_index)


