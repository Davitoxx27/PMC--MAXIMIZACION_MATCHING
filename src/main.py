import os
from tkinter import Tk
from tkinter import filedialog
import pandas as pd
import numpy as np
from scipy.optimize import linear_sum_assignment
from include.constantes import *

# @author: David Calzado Olmo

def main() -> None:
    """
    
    La función de este programa:
    1. Lee dos archivos Excel con respuestas de un formulario.
    2. Calcula una puntuación de compatibilidad entre cada mentor y mentorizado.
    3. Genera una matriz de puntuaciones.
    4. Aplica el algoritmo Húngaro para obtener el emparejamiento óptimo.

    """
    read()


def read() -> None:
    """Lee los excels de mentores y mentorizados, comprueba que son válidos y 
    llama a la función para guardar los excels con las puntuaciones"""
    
    # Guarda las rutas enteras, cogiendo la ruta del script y añadiendo el
    # nombre del archivo(que debe ser mentores.xlsx y mentorizados.xlsx):
    root = Tk()
    root.withdraw()

    ruta_excel_mentores: str = filedialog.askopenfilename(
    title="Selecciona un archivo de Excel para mentores",
    filetypes=[
        ("Archivos de Excel", "*.xlsx *.xls *.xlsm"),
        ("Todos los archivos", "*.*")
    ]
)
    ruta_excel_mentorizados: str = filedialog.askopenfilename(
    title="Selecciona un archivo de Excel para mentorizados",
    filetypes=[
        ("Archivos de Excel", "*.xlsx *.xls *.xlsm"),
        ("Todos los archivos", "*.*")
    ]
)

    valid: bool = True
    try:
        # El lector de excel de pandas devuelve un DataFrame, es decir, las tablas
        mentores: pd.DataFrame = pd.read_excel(ruta_excel_mentores)
    except FileNotFoundError:
        print("El archivo no es correcto\n")
        valid = False
    try:
        mentorizados: pd.DataFrame = pd.read_excel(ruta_excel_mentorizados)
    except FileNotFoundError:
        print("El archivo no es correcto\n")
        valid = False

        # Si las columnas de nombre estan vacias, no se puede hacer nada
    if "Nombre" not in mentores.columns or mentores["Nombre"].empty:
        valid = False
    if "Nombre" not in mentorizados.columns or mentorizados["Nombre"].empty:
        valid = False
    if valid:
        crear_dataframes(mentores, mentorizados)
        valid = True
    else:
        print("Saliendo del programa...\n")


def crear_dataframes(mentores: pd.DataFrame, mentorizados: pd.DataFrame) -> None:
    """Crea los dataframes con los resultados finales, llamando a las funciones para comparar los vectores"""
    
    dataframe_final: list[dict] = []
    lista_mentores: list[list[str]] = []
    lista_mentorizados: list[list[str]] = []
    nombres_mentores: list[str] = []
    nombres_mentorizados: list[str] = []

    # Guardar cada fila como lista, desde columna 3 en adelante y la añade al final de la lista
    for i in range(len(mentores)):
        # Localiza por nombre y luego lo convierte a fila con indices
        vector_mentor = mentores.loc[i, COLUMNAS_MENTORES].tolist()
        vector_mentor = mentores[COLUMNAS_MENTORES].iloc[i].tolist()
        
        # Comprobar que tiene 9 columnas (plantilla forms)
        if len(vector_mentor) == NUM_COLUMNAS_RESPUESTAS:
            lista_mentores.append(vector_mentor[0:NUM_COLUMNAS_RESPUESTAS])
            nombres_mentores.append(mentores.at[i, "Nombre"])
        else:
            print(f"ERROR: Fila {i} de mentores no tiene {NUM_COLUMNAS_RESPUESTAS} columnas de respuestas como la plantilla")
            
    for i in range(len(mentorizados)):
        vector_mentorizados = mentorizados.loc[i, COLUMNAS_MENTORIZADOS].tolist()
        vector_mentorizados = mentorizados[COLUMNAS_MENTORIZADOS].iloc[i].tolist()
        if len(vector_mentorizados) == NUM_COLUMNAS_RESPUESTAS:
            lista_mentorizados.append(vector_mentorizados[0:NUM_COLUMNAS_RESPUESTAS])
            nombres_mentorizados.append(mentorizados.at[i, "Nombre"])
    # Si las listas estan vacias, se devuelve falso
    if lista_mentores and lista_mentorizados:
        puntuaciones: np.ndarray = comparar_vectores(lista_mentores, lista_mentorizados)
        mostrar_tabla(puntuaciones, nombres_mentores, nombres_mentorizados)
        parejas: list[tuple[int, int]] = maximizar_matching_hungaro(puntuaciones)
        print("\n--- MEJOR EMPAREJAMIENTO ---\n")

    # Creamos el dataframe de los resultados finales
        for mentor_idx, mentorizado_idx in parejas:
            puntuacion = puntuaciones[mentor_idx, mentorizado_idx]
            dataframe_final.append({"Mentor": nombres_mentores[mentor_idx], "Mentorizado": nombres_mentorizados[mentorizado_idx], "Puntuación": puntuacion})    

        tabla_final = pd.DataFrame(dataframe_final)
        print(tabla_final)
    else:
        print("No hay filas válidas con al menos 9 columnas de respuestas.\n")


def comparar_vectores(lista_mentores: list[list[str]], lista_mentorizados: list[list[str]]) -> np.ndarray:
    """Construye una matriz 2d (n_mentores x n_mentorizados)
       donde cada [i][j] representa la puntuación entre el mentor i y el mentorizado j."""
    
    num_mentores: int = len(lista_mentores)
    num_mentorizados: int = len(lista_mentorizados)

    puntuaciones: np.ndarray = np.zeros((num_mentores, num_mentorizados))

    for i in range(num_mentores):
        mentores: list[str] = lista_mentores[i]
        for j in range(num_mentorizados):
            mentorizados: list[str] = lista_mentorizados[j]
            c_puntuacion: int = 0

            if mentores[0] == mentorizados[0]: 
                c_puntuacion += PUNTUACION_CIUDAD
            if mentores[1] == mentorizados[1]:
                c_puntuacion += PUNTUACION_PUEBLO_CIUDAD
            if mentores[2] == mentorizados[2]:
                c_puntuacion += PUNTUACION_ESTUDIOS
            if mentores[3] == mentorizados[3]:
                c_puntuacion += PUNTUACION_MODALIDAD
            if mentores[4] == mentorizados[4]:
                c_puntuacion += PUNTUACION_DEPORTES
            if mentores[5] == mentorizados[5]:
                c_puntuacion += PUNTUACION_FUTBOL
            if mentores[6] == mentorizados[6]:
                c_puntuacion += PUNTUACION_ANIME
            if mentores[7] == mentorizados[7]:
                c_puntuacion += PUNTUACION_VIDEOJUEGOS


            # Convierte los gustos musicales en una lista separada por ; luego en un set que son más fáciles de comparar
            gustos_mentores: set[str] = set(str(mentores[8]).split(";"))
            gustos_mentorizados: set[str] = set(str(mentorizados[8]).split(";"))
            # La función & de sets devuelve la intersec entre ambos sets
            coincidencias: set[str] = gustos_mentores & gustos_mentorizados
            # Por cada gusto de musica igual, se suma 2
            c_puntuacion += PUNTUACION_GUSTOS_MUSICALES * len(coincidencias)

            puntuaciones[i][j] = c_puntuacion
    return puntuaciones


def mostrar_tabla(puntuaciones: np.ndarray, nombres_mentores: list[str], nombres_mentorizados: list[str]) -> None:
    """Imprime la tabla de puntuaciones, con los nombres de los mentores y mentorizados, 
    y la puntuación de cada pareja"""
    
    filas = []
    # Guardamos el resultado final:
    for i in range(len(nombres_mentores)):
        for j in range(len(nombres_mentorizados)):
            # Diccionario con Mentor, Mentorizado y Puntuación
            filas.append(
                {"Mentor": nombres_mentores[i], "Mentorizado": nombres_mentorizados[j], "Puntuación": puntuaciones[i][j]})
    # Se crea el dataframe con pandas 
    tabla_final: pd.DataFrame = pd.DataFrame(filas)

    print("\n--- TABLA DE PUNTUACIONES ---\n")
    print(tabla_final)
    # Crea un excel con la tabla final(cambiar tu ruta)
    # tabla_final.to_excel(r"RUTA_SALIDA", index=False)


def maximizar_matching_hungaro(puntuaciones: np.ndarray) -> tuple[list[tuple[int, int]], int]:
    """Devuelve una lista de tuplas con los indices de los mentores y mentorizados emparejados, 
    calculandolo con el algoritmo de asignación lineal (Hungaro) """
    
    parejas: list[tuple[int, int]] = []

    # El algoritmo de asignación lineal (Hungaro) minimiza el coste total,
    # por lo que convertimos las puntuaciones en costes restándolas al valor máximo
    max_val: int = np.max(puntuaciones)
    costes: np.ndarray = max_val - puntuaciones
    # Tanto fila como columna representan los indices de los mentores y mentorizados respectivamente
    # En arrays 2d numpy cada uno
    filas, columnas = linear_sum_assignment(costes)

    for i in range(len(filas)):
        parejas.append((filas[i], columnas[i]))

    return parejas


if __name__ == "__main__":
    main()