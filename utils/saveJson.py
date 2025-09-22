import json
import os

def guardar_datos(datos, nombre_archivo):
    """Guarda una lista o diccionario en un archivo JSON."""
    try:
        with open(nombre_archivo, 'w', encoding='utf-8') as archivo:
            json.dump(datos, archivo, ensure_ascii=False, indent=4)
        print(f"Datos guardados exitosamente en {nombre_archivo}")
        return True
    except Exception as e:
        print(f"Error al guardar: {e}")
        return False

def cargar_datos(nombre_archivo):
    """Carga datos (lista o diccionario) desde un archivo JSON."""
    try:
        if not os.path.exists(nombre_archivo) or os.path.getsize(nombre_archivo) == 0:
            print(f"El archivo {nombre_archivo} no existe o está vacío. Se creará uno nuevo al guardar.")
            return []  # ### CAMBIO CLAVE: Devuelve una lista vacía
            
        with open(nombre_archivo, 'r', encoding='utf-8') as archivo:
            datos = json.load(archivo)
        print(f"Datos cargados exitosamente desde {nombre_archivo}")
        return datos
    except json.JSONDecodeError:
        print(f"Error: El archivo {nombre_archivo} está malformado. Se creará uno nuevo.")
        return []
    except Exception as e:
        print(f"Error al cargar: {e}")
        return [] 