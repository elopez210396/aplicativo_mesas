import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode, ColumnsAutoSizeMode, AgGridTheme
import pandas as pd

def pagina_cuenta():
    def actualizar_cuenta(cuenta, pagos):
        for producto, cantidad_pagada in pagos.items():
            cuenta.loc[cuenta['nombre'] == producto, 'cantidad'] -= cantidad_pagada
        cuenta = cuenta[cuenta['cantidad'] > 0]
        return cuenta

    if 'cuenta' not in st.session_state:
        st.session_state.cuenta = pd.DataFrame(columns=['nombre', 'cantidad', 'precio unitario', 'precio total'])

    if 'clientes' not in st.session_state:
        st.session_state.clientes = pd.DataFrame(columns=['Nombre'])

    if 'pagos_por_cliente' not in st.session_state:
        st.session_state.pagos_por_cliente = pd.DataFrame(columns=['Cliente', 'Total a pagar'])

    if 'cuenta' in st.session_state:
        cuenta_parcial = st.session_state.cuenta.groupby(['nombre']).agg({'cantidad':'sum','precio unitario':'mean','precio total':'sum'}).reset_index()
        gb = GridOptionsBuilder.from_dataframe(cuenta_parcial, editable=False)
        gb.configure_selection(selection_mode="multiple", use_checkbox=True)
        return_value = AgGrid(cuenta_parcial, 
                            gridOptions=gb.build(),
                            columns_auto_size_mode=ColumnsAutoSizeMode.FIT_CONTENTS,
                            theme=AgGridTheme.STREAMLIT,
                            updateMode=GridUpdateMode.VALUE_CHANGED,
                            allow_unsafe_jscode=True)
        
        if 'clientes' in st.session_state and not st.session_state.clientes.empty:
            productos_seleccionados = return_value['selected_rows']
            nombres_seleccionados = [producto['nombre'] for producto in productos_seleccionados]
            cantidades_maximas = [producto['cantidad'] for producto in productos_seleccionados]
            precios_unitarios = {producto['nombre']: producto['precio unitario'] for producto in productos_seleccionados}

            for nombre, cantidad_max in zip(nombres_seleccionados, cantidades_maximas):
                col1, col2, col3 = st.columns(3)
                with col1:
                    cantidad_seleccionada = st.selectbox(f'Cantidad de {nombre}', options=list(range(1, cantidad_max + 1)), key=f'cantidad_{nombre}')
                with col3:
                    clientes_seleccionados = st.multiselect(f'Clientes para {nombre}', options=st.session_state.clientes['Nombre'].unique(), key=f'clientes_{nombre}')
                
                if len(clientes_seleccionados) > 0:
                    total_cliente = (cantidad_seleccionada * precios_unitarios[nombre]) / len(clientes_seleccionados)
                    for cliente in clientes_seleccionados:
                        if cliente in st.session_state.pagos_por_cliente['Cliente'].values:
                            st.session_state.pagos_por_cliente.loc[st.session_state.pagos_por_cliente['Cliente'] == cliente, 'Total a pagar'] += total_cliente
                        else:
                            nuevo_registro = pd.DataFrame({'Cliente': [cliente], 'Total a pagar': [total_cliente]})
                            st.session_state.pagos_por_cliente = pd.concat([st.session_state.pagos_por_cliente, nuevo_registro], ignore_index=True)

            st.write("Cuenta por cliente:")
            st.write(st.session_state.pagos_por_cliente)