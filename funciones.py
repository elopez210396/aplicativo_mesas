import mysql.connector as sql
import pandas as pd
from PIL import Image, UnidentifiedImageError
import io


def obtener_articulos():
    user='root'
    password=''
    host='127.0.0.1'
    database='aplicativo_mesas'
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