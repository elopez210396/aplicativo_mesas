import pandas as pd
import mysql.connector as sql
import streamlit as st
from PIL import Image, UnidentifiedImageError
import io

def obtener_articulos():
    user='root',
    password='',
    host='127.0.0.1',
    database='aplicativo_mesas',
    port=3306
    db_connection = sql.connect(user=user, password=password, host=host, database=database,port=port)
    cursor = db_connection.cursor()
    cursor.execute("SELECT nombre, precio, imagen, categoria FROM productos")
    productos = cursor.fetchall()
    cursor.close()
    db_connection.close()

    return productos

def convertir_a_imagen(binarios, size=(150, 120)):
    try:
        img = Image.open(io.BytesIO(binarios))
        img.verify()  # Verificar si es una imagen válida
        img = Image.open(io.BytesIO(binarios))  # Abrir de nuevo para manipulación
        img = img.resize(size, Image.ANTIALIAS)
        return img
    except UnidentifiedImageError:
        print("Error: Los datos binarios no corresponden a una imagen válida.")
        return None
    
def mostrar_productos(productos_filtrados, categoria):
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