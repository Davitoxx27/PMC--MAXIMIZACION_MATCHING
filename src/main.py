import os
import pandas as pd
import numpy as np
from scipy.optimize import linear_sum_assignment


def main() -> None:
    read()


def read() -> None:
    # Guarda las rutas enteras, cogiendo la ruta del script y añadiendo el
    # nombre del archivo(que debe ser mentores.xlsx y mentorizados.xlsx):
    base_dir = os.path.dirname(__file__)
    ruta_excel = os.path.join(base_dir, "mentores.xlsx")
    valid = True
    try:
        # El lector de excel de pandas devuelve un DataFrame, es decir, las tablas
        mentores = pd.read_excel(ruta_excel)
    except FileNotFoundError:
        print("El nombre del archivo no es correcto:mentores.xlsx, o no esta el archivo")
        valid = False
    ruta_excel = os.path.join(base_dir, "mentorizados.xlsx")
    try:
        mentorizados = pd.read_excel(ruta_excel)
    except FileNotFoundError:
        print(
            "El nombre del archivo no es correcto:mentorizados.xlsx, o no esta el archivo\n")
        valid = False
        # Si las columnas de nombre estan vacias, no se puede hacer nada
    if "Nombre" not in mentores.columns or mentores["Nombre"].empty:
        valid = False
    if "Nombre" not in mentorizados.columns or mentorizados["Nombre"].empty:
        valid = False
    if valid:
        guardar_excels(mentores, mentorizados)
    else:
        print("Saliendo del programa...\n")


def guardar_excels(mentores, mentorizados) -> None:

    dataframe_final = []
    lista_mentores = []
    lista_mentorizados = []
    nombres_mentores = []
    nombres_mentorizados = []

    # Guardar cada fila como lista, desde columna 3 en adelante y la añade al final de la lista
    for i in range(len(mentores)):
        vector_mentor = mentores.iloc[i, 3:12].tolist()
        # Comprobar que tiene al menos 9 columnas (plantilla forms)
        if len(vector_mentor) >= 9:
            lista_mentores.append(vector_mentor[0:9])
            nombres_mentores.append(mentores.at[i, "Nombre"])

    for i in range(len(mentorizados)):
        vector_mentorizados = mentorizados.iloc[i, 3:].tolist()
        if len(vector_mentorizados) >= 9:
            lista_mentorizados.append(vector_mentorizados[0:9])
            nombres_mentorizados.append(mentorizados.at[i, "Nombre"])
    # Si las listas estan vacias, se devuelve falso
    if lista_mentores and lista_mentorizados:
        puntuaciones = comparar_vectores(lista_mentores, lista_mentorizados)
        mostrar_tabla(puntuaciones, nombres_mentores, nombres_mentorizados)
        parejas, suma_total = maximizar_matching_hungaro(puntuaciones)
        print("\n--- MEJOR EMPAREJAMIENTO ---\n")

    # Creamos el dataframe de los resultados finales
        for mentor_idx, mentorizado_idx in parejas:
            puntuacion = puntuaciones[mentor_idx, mentorizado_idx]
            dataframe_final.append({"Mentor": nombres_mentores[mentor_idx], "Mentorizado": nombres_mentorizados[mentorizado_idx], "Puntuación": puntuacion})    
            # print(f"{nombres_mentores[mentor_idx]} → {nombres_mentorizados[mentorizado_idx]} (Puntuación: {puntuacion})")
        tabla_final = pd.DataFrame(dataframe_final)
        print(tabla_final)
    else:
        print("No hay filas válidas con al menos 9 columnas de respuestas.\n")


def comparar_vectores(lista_mentores, lista_mentorizados) -> list[list[int]]:

    num_mentores = len(lista_mentores)
    num_mentorizados = len(lista_mentorizados)

    puntuaciones = np.zeros((num_mentores, num_mentorizados))

    for i in range(num_mentores):
        mentores = lista_mentores[i]
        for j in range(num_mentorizados):
            mentorizados = lista_mentorizados[j]
            c_puntuacion = 0

            if mentores[0] == mentorizados[0]:  # ¿Vives en Ciudad Real?
                c_puntuacion += 1
            if mentores[1] == mentorizados[1]:  # Pueblo/Ciudad
                c_puntuacion += 2
            if mentores[2] == mentorizados[2]:  # Qué has estudiado
                c_puntuacion += 2
            if mentores[3] == mentorizados[3]:  # Modalidad
                c_puntuacion += 5
            if mentores[4] == mentorizados[4]:  # Deporte
                c_puntuacion += 2
            if mentores[5] == mentorizados[5]:  # Fútbol
                c_puntuacion += 3
            if mentores[6] == mentorizados[6]:  # Anime
                c_puntuacion += 3
            if mentores[7] == mentorizados[7]:  # Videojuegos / salir
                c_puntuacion += 3

            # Convierte los gustos musicales en una lista separada por ; luego en un set que son más fáciles de comparar
            gustos_mentores = set(str(mentores[8]).split(";"))
            gustos_mentorizados = set(str(mentorizados[8]).split(";"))
            # La función & de sets devuelve la intersección entre ambos sets
            coincidencias = gustos_mentores & gustos_mentorizados
            # Por cada gusto de musica igual, se suma 2
            c_puntuacion += 2 * len(coincidencias)

            puntuaciones[i][j] = c_puntuacion
    return puntuaciones


def mostrar_tabla(puntuaciones, nombres_mentores, nombres_mentorizados) -> None:
    filas = []
    # Guardamos el resultado final:
    for i in range(len(nombres_mentores)):
        for j in range(len(nombres_mentorizados)):
            # Diccionario con Mentor, Mentorizado y Puntuación
            filas.append(
                {"Mentor": nombres_mentores[i], "Mentorizado": nombres_mentorizados[j], "Puntuación": puntuaciones[i][j]})
    # Se crea el dataframe con pandas despues del bucle anidado
    tabla_final = pd.DataFrame(filas)

    print("\n--- TABLA DE PUNTUACIONES ---\n")
    print(tabla_final)
    # Crea un excel con la tabla final(cambiar tu ruta)
    # tabla_final.to_excel(r"C:\Users\USUARIO\Downloads\ej.xlsx", index=False)


def maximizar_matching_hungaro(puntuaciones):
    puntuaciones = np.array(puntuaciones)

    # El algoritmo de asignación lineal (Hungaro) minimiza el coste total,
    # por lo que convertimos las puntuaciones en costes restándolas al valor máximo
    max_val = np.max(puntuaciones)
    costes = max_val - puntuaciones

    filas, columnas = linear_sum_assignment(costes)

    suma_total = puntuaciones[filas, columnas].sum()

    parejas = []

    for i in range(len(filas)):
        parejas.append((filas[i], columnas[i]))

    return parejas, suma_total


main()
