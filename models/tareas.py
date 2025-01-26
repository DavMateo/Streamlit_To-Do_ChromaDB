from chromadb import Collection
from datetime import datetime


# Obtener todo ("GET")

# Obtener por algún dato ("GET")

# Insertar ("POST")
def nueva_tarea(
    lst_info_tarea: list,
    coleccion: Collection
) -> bool:
    try:
        """Strategy
            Con el fin de simular el funcionammiento de una base de datos relacional SQL en ChromaDB, se
            creó la siguiente estructura: en el campo de documents, se almacena un diccionario transformado
            a una cadena de texto con el título y la descripción de la nueva tarea. La metadata contiene la 
            otra información restante en forma de diccionario y por último, se define el 'id'.
            El objetivo de esto es que por cada entrada, se almacene toda una tarea completa sin necesidad
            de fragmentarla o dedicar recursos para su almacenamiento individual, una misma colección tendrá
            toda la información correspondiente para lo que fue creada.
        """
        
        coleccion.add(
            documents=[
                str({
                    "titulo": lst_info_tarea["titulo"],
                    "descripcion": lst_info_tarea["descripcion"]
                })
            ],
            metadatas=[
                {
                    "id": lst_info_tarea["id"],
                    "fecha_creacion": str(datetime.now()),
                    "estado": lst_info_tarea["estado"]
                }
            ],
            ids=[lst_info_tarea["id"]]
        )
        
        # Retorna "True" para indicar que se realizó la insercción correctamente.
        return True
    
    except Exception as e:
        print(f"Algo ha ido mal durante la insercción de información: {str(e)}")
        raise Exception(str(e))