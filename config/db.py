import os
import chromadb
from chromadb import Settings, Client, Collection


# Definiendo la configuración inicial para el arranque de la base de datos
def config_inicial(
    path: str,
    nombre: str,
    descripcion: str,
    fecha: str,
    space: str="cosine",
    search_ef: int=400,
    construction_ef: int=4,
    num_threads: int=4
) -> list:
    # Verificando la existencia de la carpeta "data"
    if os.path.exists(path):
        print("El directorio ya existe, continuando...")
        
    else:
        print("El directorio no existe, creando...")
        os.makedirs(path, exist_ok=True)
    
    # Creando el cliente de ChromaDB con persistencia de datos
    client = chromadb.PersistentClient(path, settings=Settings(anonymized_telemetry=False))
    
    # Creando la colección principal que tendrá el programa
    coleccion = crear_coleccion(
        client, nombre, descripcion, fecha,
        space, search_ef, construction_ef, num_threads
    )
    
    #Retorna los elementos de conexión y almacenamiento de información
    return [client, coleccion]
    
    
# Definiendo la creación de la colección del programa
def crear_coleccion(
    client: Client,
    nombre: str,
    descripcion: str,
    fecha: str,
    space: str="cosine",
    search_ef: int=400,
    construction_ef: int=400,
    num_threads: int=4,
) -> Collection:
    # Retorna el objeto "Collection" creado.
    return client.get_or_create_collection(
        name=nombre,
        metadata={
            "descripcion": descripcion,
            "creado": fecha,
            "hnsw:space": space,
            "hnsw:search_ef": search_ef,
            "hnsw:construction_ef": construction_ef,
            "hnsw:num_threads": num_threads
        }
    )