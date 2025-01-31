import torch
from sentence_transformers import SentenceTransformer


# Inicializando y ejecutando el modelo de embeddings
def conexion_modelo(model):
    # Determinar si se debe ejecutar en CPU o GPU
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Ejecutando modelo en: {device.upper()}")
    return SentenceTransformer(model, device=device)