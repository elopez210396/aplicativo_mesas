import streamlit as st


def pagina_sugerencias():
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