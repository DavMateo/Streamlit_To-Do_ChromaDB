import streamlit as st


# Configurando página Streamlitst.set_page_config(page_title="To-Do List", layout="wide")
st.set_page_config(page_title="To-Do List", layout="wide")

# Componente contenedor que expande la información mediante click.
def info_proyecto(titulo: str, contenido: str, aviso: str=""):
    with st.expander(titulo):
        st.write(contenido)
        
        if len(aviso) != 0:
            st.info(aviso)