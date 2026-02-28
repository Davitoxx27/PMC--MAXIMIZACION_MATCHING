## 1. Archivos de entrada

- `mentores.xlsx` 
- `mentorizados.xlsx` 

Deben seguir el formato del forms dado, y ambos archivos deben estar en la carpeta src.

## 2. Función
        1. Lee los Excel de mentores y mentorizados.
        2. Calcula puntuaciones de compatibilidad entre cada mentor y cada mentorizado:
            - Coincidencias en ciudad, estudios, modalidad, deportes, hobbies, gustos musicales, etc.
        3. Genera una matriz de puntuaciones (mentores-mentorizados).
        4. Aplica el **algoritmo Húngaro** (`scipy.optimize.linear_sum_assignment`) para obtener el mejor emparejamiento posible.

## 3. Output

    - Tabla completa de puntuaciones
    - Mejor emparejamiento con puntuación individual por pareja



## 4. Explicación del algoritmo 

Para la maximización en la elección entre mentores y mentorizados pensé en usar
backtracking, probando todos los posibles casos hasta encontrar el mejor.

Sin embargo, me topé con el método Húngaro, que a base de cálculo de matrices
hace lo mismo y mucho más limpio siendo la complejidad:

- Backtracking O(n!)
- Método Húngaro O(n^3)

Para ello es necesario instalar con el comando: pip install scipy