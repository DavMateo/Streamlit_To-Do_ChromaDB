import streamlit as st
from utils.completar_tarea import completar_tarea

# Componente para crear una nueva tarjeta a partir de las tareas existentes y nuevas
def nueva_tarjeta(tarea, col, tab_index, coleccion):
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
                    
                    # Botón "Completar" o "Re-activar" (Dinámico) de tipo primario
                    with btn1:
                        if st.button(
                            "Completar" if tarea["estado"] else "Re-activar",
                            use_container_width=True,
                            type="primary",
                            key=f"btn_toggle{tarea["id"]}_{tab_index}"
                        ):
                            completar_tarea(tarea["id"], coleccion)
                    
                    # Botón "Eliminar" de tipo secundario con acción "delete" por ChromaDB
                    with btn2:
                        if st.button(
                            "Eliminar",
                            use_container_width=True,
                            type="secondary",
                            key=f"btn_delete{tarea["id"]}_{tab_index}"
                        ):
                            # Consulta ChromaDB para eliminar [Insertar aquí]
                            st.rerun()
            
            # Container: tarea__footer
            with st.container():
                info_id, info_fecha = st.columns(2, vertical_alignment="center")
                
                with info_id:
                    st.markdown(f"""
                        <div style='
                            text-align: left;
                            color: #5F6A6A;
                            margin: .75rem 0;'
                        >
                            ID: {tarea["id"]}
                        </div>
                    """, unsafe_allow_html=True)
                
                with info_fecha:
                    st.markdown(f"""
                        <div style='
                            text-align: right;
                            color: #5F6A6A;
                        >
                            Fecha: {tarea["fecha"]}
                        </div>
                    """, unsafe_allow_html=True)