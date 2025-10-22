Calculadora de Generadores, Pruebas y Distribuciones

Autor: Linares Limachi Alan Yamil
Versión: 1.0
Lenguaje: Python
Bibliotecas utilizadas:

tkinter (interfaz gráfica)

numpy (cálculos numéricos)

scipy (estadística)

matplotlib (gráficas)

Descripción

Este proyecto es una calculadora interactiva que permite generar números pseudoaleatorios mediante distintos algoritmos clásicos, realizar pruebas estadísticas sobre los números obtenidos, y generar valores según diversas distribuciones de probabilidad.

Su objetivo es facilitar el estudio, visualización y análisis de generadores y distribuciones aleatorias de forma didáctica y visual.

Funcionalidades Principales
1. Generadores de números pseudoaleatorios

Incluye tres métodos clásicos:

Cuadrados Medios

Productos Medios

Multiplicador Constante

Cada método muestra los resultados en una tabla y genera una gráfica con los valores pseudoaleatorios obtenidos.

2. Pruebas estadísticas

Permite verificar la aleatoriedad de los números generados con las siguientes pruebas:

Prueba de Medios (Z-test)

Prueba de Varianza (Chi-cuadrado)

Prueba de Uniformidad (Chi-cuadrado de frecuencias)

Cada prueba muestra los cálculos, estadísticos, valores críticos, p-valor y la decisión sobre la hipótesis nula.

3. Generación de distribuciones de probabilidad

Permite generar y graficar datos a partir de las siguientes distribuciones:

Uniforme

Exponencial

Normal

Weibull

Bernoulli

Poisson

Además, se pueden usar los números pseudoaleatorios generados previamente como base para las distribuciones.

Interfaz Gráfica

El programa está desarrollado con Tkinter, organizado en pestañas:

Generadores → Cuadrados, Productos y Multiplicador.

Pruebas → Medios, Varianza, Chi-cuadrado.

Distribuciones → Selección y visualización de distribuciones estadísticas.

Los resultados se presentan en paneles de texto y gráficos interactivos con matplotlib.

Ejecución
Requisitos

Asegúrate de tener instaladas las siguientes librerías:

pip install numpy scipy matplotlib

Ejecución del programa

Ejecuta el archivo principal:

python calculadora_distribuciones.py



Segunda Calculadora - Simulaciones

Autor: Linares Limachi Alan Yamil

Descripción

Este proyecto combina tres simulaciones interactivas desarrolladas con Python, Tkinter y Matplotlib.
Su objetivo es mostrar el comportamiento de sistemas complejos a través de autómatas celulares y modelos probabilísticos.

La interfaz permite ejecutar cada simulación de forma visual e intuitiva, con parámetros configurables por el usuario.

Simulaciones incluidas
1. Juego de la Vida 2D (Variable)

Basado en el autómata celular de Conway, simula la evolución de células vivas y muertas según reglas simples.

Parámetros ajustables: número de filas, columnas y probabilidad inicial.

Permite crear, limpiar, avanzar paso a paso o ejecutar automáticamente la simulación.

2. Juego de la Vida 1D (Reglas de Conway)

Autómata unidimensional con reglas personalizables (0–255).

Permite explorar patrones emergentes a partir de una celda inicial activa.

Visualiza la evolución de cada generación.

3. Simulación de COVID-19

Modelo simplificado de propagación epidemiológica.

Estados: Susceptible, Infectado, Recuperado, Muerto.

Parámetros ajustables:

Número de filas y columnas

Cantidad de infectados iniciales

Probabilidad de infección, recuperación y muerte

Se muestra el avance en tiempo real y una gráfica de evolución poblacional.

Tecnologías utilizadas

Python 3.10+

Tkinter (interfaz gráfica)

Matplotlib (visualización de datos)

NumPy (cálculos numéricos)

Threading (ejecución en paralelo para animaciones)

Ejecución

Clona o descarga el repositorio.

Asegúrate de tener instaladas las librerías necesarias:

pip install numpy matplotlib


Ejecuta el archivo principal:

python simulaciones.py


Usa las pestañas para explorar las distintas simulaciones.

Créditos

Todo el código fue desarrollado por Linares Limachi Alan Yamil.
Basado en documentación oficial de Matplotlib, NumPy y Tkinter.
