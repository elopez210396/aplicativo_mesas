import streamlit as st
from streamlit_option_menu import option_menu
#import menu, cuenta, sugerencias, participantes
import pandas as pd

query_params = st.query_params.get_all(key='mesa')
if len (query_params)>0:
    st.header(f'Mesa # {query_params[0]}')
    selected = option_menu(None, ["Menu", "Cuenta", "Participantes",'Sugerencias'], 
        icons=['book', 'check', "list-task", 'info'], 
        orientation="horizontal", key='menu')
    if selected == 'Sugerencias':
        with st.form('sugerencia'):
                nombre = st.text_input('Nombre completo')
                correo = st.text_input('Correo electrónico')
                comentarios = st.text_area('Déjanos tus comentarios')
                enviar = st.form_submit_button('Enviar')
                if enviar:
                    if nombre == '':
                        st.error('Ingresa tu nombre')
                    if correo == '':
                        st.error('Ingresa tu correo electrónico')
                    if comentarios == '':
                        st.error('Ingresa tus comentarios')
                    if (nombre !='')&(correo!='')&(comentarios!=''):    
                        st.success('Gracias por tus comentarios')        
    elif selected == 'Participantes':
        if 'clientes' in st.session_state:
            @st.cache_data()
            def clientes():
                clientes = st.session_state['clientes']
                return clientes

        cliente = st.text_input('Nombre cliente')
        if st.button('Agregar'):
            if cliente:
                # Crear un nuevo DataFrame con el cliente nuevo
                nuevo_cliente = pd.DataFrame({'Nombre': [cliente]})
                st.session_state.clientes = pd.concat([st.session_state.clientes, nuevo_cliente], ignore_index=True)
                clientes = clientes()
        st.write(clientes)
    elif selected == 'Menu':
        st.write('Menu')
        #menu.pagina_menu()        

    elif selected == 'Cuenta':
        st.write('Cuenta')
        #cuenta.pagina_cuenta()
else:   
    st.write("No se ha proporcionado un número de mesa en la URL.")

