import streamlit as st
import pandas as pd
import funciones as fc

def convertir_a_imagen(data):
    from PIL import Image
    import io
    if data is not None:
        return Image.open(io.BytesIO(data))
    return None

def pagina_menu():
    @st.cache_data(show_spinner=False)
    def leer_menu():
        productos = fc.obtener_articulos()
        productos = pd.DataFrame(productos, columns=['nombre', 'precio', 'imagen','categoria'])
        return productos
    productos =leer_menu()
    st.header("Menú")

    if 'articulos_seleccionados' not in st.session_state:
        st.session_state.articulos_seleccionados = pd.DataFrame()
    articulos_seleccionados_temporal = pd.DataFrame()

    def mostrar_productos(productos_filtrados, categoria):
        nonlocal articulos_seleccionados_temporal
        with st.expander(categoria):
            cols = st.columns(3)  # Crear 3 columnas

            for i, (index, row) in enumerate(productos_filtrados.iterrows()):
                nombre = row['nombre']
                precio = row['precio']
                imagen = row['imagen']
                imagen_pil = convertir_a_imagen(imagen)

                col = cols[i % 3]  
                with col:
                    if imagen_pil is not None:
                        st.image(imagen_pil, width=150)
                    st.write(f"**{nombre}**")
                    st.write(f"Precio: ${precio}")
                    cantidad_nombre = st.number_input(f'Cantidad para {nombre}', min_value=0, step=1, value=0, key=f'{categoria}_{nombre}')
                    if cantidad_nombre > 0:
                        nuevo_articulo = {'nombre': nombre, 'cantidad': cantidad_nombre, 'precio unitario': precio, 'precio total': precio*cantidad_nombre}
                        articulos_seleccionados_temporal = pd.concat([articulos_seleccionados_temporal, pd.DataFrame([nuevo_articulo])], ignore_index=True)
                    st.write('---')

    categorias = productos['categoria'].unique()
    for categoria in categorias:
        productos_filtrados = productos[productos['categoria'] == categoria]
        mostrar_productos(productos_filtrados, categoria)

    if not articulos_seleccionados_temporal.empty:
        st.header("Pedido")
        st.write(articulos_seleccionados_temporal)
        if st.button('Pedir'):
            if 'cuenta' in st.session_state:
                st.session_state.cuenta = pd.concat([st.session_state.cuenta, articulos_seleccionados_temporal], ignore_index=True)
            else:
                st.session_state['cuenta'] = articulos_seleccionados_temporal
            
            st.success('Tu pedido ha sido creado, pronto llegará a tu mesa')
            #st.rerun()