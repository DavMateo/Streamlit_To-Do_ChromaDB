import json
from config.db import config_inicial
from fastapi import APIRouter
from models.tareas import nueva_tarea
from schemas.tareas import Tarea
from utils.autoincrement import contador
from datetime import datetime


# Configurando conjunto de APIs e Inicializando lo necesario para los endpoints
tareas_api = APIRouter()
client, coleccion = config_inicial("tareas", "Base de datos principal para almacenar la información relacionada con las tareas del usuario.")


@tareas_api.get('/tareas', tags=["tareas"])
def obtener_tareas():
    return coleccion.get()

@tareas_api.get('/tareas/{id}', tags=["tareas"])
def obtener_tareas_por_id(id: str):
    return coleccion.get(ids=[id])


@tareas_api.post('/tareas', tags=["tareas"])
def crear_tarea(tarea: Tarea):
    try:
        data = dict(tarea)
        print(data["titulo"])
        # Agregando el ID al objeto recibido
        tarea_obj = {
            "id": f"id{str(contador(coleccion))}",
            "titulo": data["titulo"],
            "descripcion": data["descripcion"],
            "estado": data["estado"]
        }
        # Realizando la petición a base de datos. Se espera un raise Exception o un True
        resultado = nueva_tarea(tarea_obj, coleccion)
        print(resultado)
        
        return tarea_obj

    except Exception as e:
        print(str(e))
        raise Exception(str(e))


@tareas_api.put('/tareas/{id}', tags=["tareas"])
def editar_tarea(id: str, tarea: Tarea):
    try:
        data = dict(tarea)
        tarea_obj = {
            "titulo": data["titulo"],
            "descripcion": data["descripcion"],
            "estado": data["estado"]
        }
        
        resultado = coleccion.upsert(
            ids=[id],
            documents=[
                str({
                    "titulo": data["titulo"],
                    "descripcion": data["descripcion"]
                })
            ],
            metadatas=[
                {
                    "fecha_actualizacion": str(datetime.now()),
                    "estado": data["estado"]
                }
            ],
        )
        print(resultado)    
        return tarea_obj
    
    except Exception as e:
        print(str(e))
        raise Exception(str(e))


@tareas_api.delete('/tareas/{id}', tags=["tareas"])
def eliminar_tarea(id: str):
    res = coleccion.delete(ids=[id])
    print(res)
    
    return f"La tarea '{id}' ha sido eliminada!!"