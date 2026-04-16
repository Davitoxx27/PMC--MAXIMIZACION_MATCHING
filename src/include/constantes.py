
#Constantes puntuación
PUNTUACION_CIUDAD = 1
PUNTUACION_PUEBLO_CIUDAD = 2
PUNTUACION_ESTUDIOS = 2
PUNTUACION_MODALIDAD = 5
PUNTUACION_DEPORTES = 2
PUNTUACION_FUTBOL = 3
PUNTUACION_ANIME = 3
PUNTUACION_VIDEOJUEGOS = 3
PUNTUACION_GUSTOS_MUSICALES = 2
NUM_COLUMNAS_RESPUESTAS = 9
COLUMNAS_MENTORES = [
    "Ciudad",
    "¿Vives ahora en Ciudad Real?",
    "¿De qué pueblo/ciudad vienes?",
    "¿Qué has estudiado hasta ahora?",
    "¿Qué modalidad has escogido?",
    "¿Te gusta hacer deporte?",
    "¿Te gusta el fútbol?",
    "¿Te gusta ver Anime?",
    "Gustos en música (Puedes elegir varias)"
]

COLUMNAS_MENTORIZADOS = [
    "¿De qué pueblo/ciudad vienes?",  # equivalente a Ciudad
    "¿Vives ahora en Ciudad Real?",
    "¿De qué pueblo/ciudad vienes?",
    "¿Qué has estudiado hasta ahora?",
    "¿Qué modalidad has escogido?",
    "¿Te gusta hacer deporte?",
    "¿Te gusta el fútbol?",
    "¿Te gusta ver Anime?",
    "Gustos en música (Puedes elegir varias)"
]
# Rutas
ARCHIVO_MENTORES = "data/mentores.xlsx"
ARCHIVO_MENTORIZADOS = "data/mentorizados.xlsx"
RUTA_SALIDA = "outputs/mejor_emparejamiento.xlsx"

# Config
MOSTRAR_TABLA_COMPLETA = True
GUARDAR_EXCEL = True