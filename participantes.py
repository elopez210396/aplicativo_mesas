import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode, ColumnsAutoSizeMode, AgGridTheme

@st.cache_data(ttl=3600, show_spinner=False)
def get_clientes_cache():
    return pd.DataFrame(columns=['Nombre'])

def save_clientes_cache(clientes_df):
    st.session_state.clientes_cache = clientes_df

def pagina_participantes():
    # Recuperar los clientes del cache o crear un DataFrame vacío
    if 'clientes' not in st.session_state:
        st.session_state.clientes = get_clientes_cache()

    # Input para el nombre del cliente
    cliente = st.text_input('Nombre cliente')

    # Botón para agregar el cliente al DataFrame
    if st.button('Agregar'):
        if cliente:
            # Crear un nuevo DataFrame con el cliente nuevo
            nuevo_cliente = pd.DataFrame({'Nombre': [cliente]})

            # Concatenar el nuevo DataFrame al existente en el estado de sesión
            st.session_state.clientes = pd.concat([st.session_state.clientes, nuevo_cliente], ignore_index=True)

            # Guardar en el cache
            save_clientes_cache(st.session_state.clientes)

            # Re-renderizar la aplicación para actualizar la tabla
            st.rerun()
        else:
            st.error('Por favor ingresa un nombre de cliente.')

    # Mostrar el DataFrame de clientes solo si no está vacío
    if not st.session_state.clientes.empty:
        gb = GridOptionsBuilder.from_dataframe(st.session_state.clientes, editable=True)
        gb.configure_selection(selection_mode="multiple", use_checkbox=True)
        return_value = AgGrid(st.session_state.clientes,
                              gridOptions=gb.build(),
                              columns_auto_size_mode=ColumnsAutoSizeMode.FIT_CONTENTS,
                              theme=AgGridTheme.STREAMLIT,
                              updateMode=GridUpdateMode.VALUE_CHANGED,
                              allow_unsafe_jscode=True)
        clientes_seleccionados = return_value['selected_rows']
        if clientes_seleccionados:
            if st.button('Eliminar'):
                indices_seleccionados = [row['_selectedRowNodeInfo']['nodeRowIndex'] for row in clientes_seleccionados]

                st.session_state.clientes.drop(indices_seleccionados, inplace=True)

                st.session_state.clientes.reset_index(drop=True, inplace=True)

                # Guardar en el cache
                save_clientes_cache(st.session_state.clientes)

                st.rerun()