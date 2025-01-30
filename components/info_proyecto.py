import streamlit as st

# Componente contenedor que expande la información mediante click.
def info_proyecto(titulo: str, contenido: str, aviso: str=""):
    with st.expander(titulo):
        st.write(contenido)
        
        if len(aviso) != 0:
            st.info(aviso)