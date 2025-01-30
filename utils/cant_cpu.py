import os

# Función para obtener los núcleos del sistema
def cant_cpus_disp() -> dict:
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