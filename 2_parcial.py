import tkinter as tk
from itertools import product

# Variable global para almacenar las ventanas
tabla_ventana = None
arbol_ventana = None

# Función que se ejecuta al presionar el botón
def mostrar_texto():
    # Obtener el texto ingresado en el campo de entrada y convertirlo a minúsculas
    texto = entrada_texto.get().lower()
    
    # Inicializar listas para almacenar partes y operadores
    partes_y = texto.split(" y ")
    partes = []
    operadores = []
    contador = 1  # Contador para nombrar variables secuencialmente

    # Fraccionar el texto utilizando "y" y "o"
    for i, parte in enumerate(partes_y):
        subpartes = parte.split(" o ")
        for j, subparte in enumerate(subpartes):
            partes.append(f"A{contador}")
            contador += 1
            if j < len(subpartes) - 1:
                operadores.append("v")  # Reemplazar "o" por "v"
        if i < len(partes_y) - 1:
            operadores.append("^")  # Reemplazar "y" por "^"

    # Construir la fórmula
    formula = partes[0]
    for k in range(len(operadores)):
        formula += f" {operadores[k]} {partes[k + 1]}"

    etiqueta_resultado.config(text=f"Fórmula resultante:\n{formula}")
    
    # Obtener coordenadas para la tabla y el árbol
    x_tabla = int(entrada_x_tabla.get() or 0)
    y_tabla = int(entrada_y_tabla.get() or 0)
    x_arbol = int(entrada_x_arbol.get() or 0)
    y_arbol = int(entrada_y_arbol.get() or 0)

    mostrar_tabla_verdad(partes, x_tabla, y_tabla)
    mostrar_arbol_logico(partes, x_arbol, y_arbol)

# Función para mostrar la tabla de verdad
def mostrar_tabla_verdad(variables, x, y):
    global tabla_ventana
    if tabla_ventana is not None:
        tabla_ventana.destroy()

    tabla_ventana = tk.Toplevel()
    tabla_ventana.title("Tabla de Verdad")
    tabla_ventana.geometry("600x400")
    tabla_ventana.geometry(f"+{x}+{y}")  # Posicionar en coordenadas (x, y)

    combinaciones = list(product([0, 1], repeat=len(variables)))

    for col, var in enumerate(variables):
        encabezado = tk.Label(tabla_ventana, text=var, width=10, height=2, font=("Arial", 14, "bold"), borderwidth=2, relief="solid")
        encabezado.grid(row=0, column=col)

    for row, combinacion in enumerate(combinaciones, start=1):
        for col, valor in enumerate(combinacion):
            celda = tk.Label(tabla_ventana, text=str(valor), width=10, height=2, font=("Arial", 14), borderwidth=2, relief="solid")
            celda.grid(row=row, column=col)

# Función para mostrar el árbol de valores lógicos
def mostrar_arbol_logico(variables, x, y):
    global arbol_ventana
    if arbol_ventana is not None:
        arbol_ventana.destroy()

    arbol_ventana = tk.Toplevel()
    arbol_ventana.title("Árbol de Valores Lógicos")
    arbol_ventana.geometry("600x600")
    arbol_ventana.geometry(f"+{x}+{y}")  # Posicionar en coordenadas (x, y)

    # Crear una etiqueta de título
    titulo = tk.Label(arbol_ventana, text="Árbol de Valores Lógicos", font=("Arial", 16, "bold"))
    titulo.pack(pady=10)

    # Llamar a la función recursiva para crear el árbol
    crear_arbol(variables, 0, "")

# Función recursiva para crear el árbol de decisiones
def crear_arbol(variables, nivel, prefijo):
    if nivel < len(variables):
        # Añadir rama para True
        crear_arbol(variables, nivel + 1, prefijo + f"{variables[nivel]}=True\n")
        # Añadir rama para False
        crear_arbol(variables, nivel + 1, prefijo + f"{variables[nivel]}=False\n")
    else:
        # Cuando se llega a la profundidad de las variables, mostrar el resultado
        etiqueta_nodo = tk.Label(arbol_ventana, text=prefijo.strip(), font=("Arial", 12))
        etiqueta_nodo.pack(anchor="w", padx=20)

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Fraccionador de Texto")
ventana.geometry("400x400")

# Etiqueta de instrucciones
etiqueta_instrucciones = tk.Label(ventana, text="Ingresa tu proposición compuesta:")
etiqueta_instrucciones.pack(pady=10)

# Campo de entrada para el texto
entrada_texto = tk.Entry(ventana, width=50)
entrada_texto.pack(pady=5)

# Campos para coordenadas de la tabla de verdad
tk.Label(ventana, text="Coordenadas Tabla (x, y):").pack(pady=5)
entrada_x_tabla = tk.Entry(ventana, width=10)
entrada_x_tabla.pack(side=tk.LEFT, padx=5)
entrada_y_tabla = tk.Entry(ventana, width=10)
entrada_y_tabla.pack(side=tk.LEFT, padx=5)

# Campos para coordenadas del árbol lógico
tk.Label(ventana, text="Coordenadas Árbol (x, y):").pack(pady=5)
entrada_x_arbol = tk.Entry(ventana, width=10)
entrada_x_arbol.pack(side=tk.LEFT, padx=5)
entrada_y_arbol = tk.Entry(ventana, width=10)
entrada_y_arbol.pack(side=tk.LEFT, padx=5)

# Botón para mostrar el texto ingresado
boton_mostrar = tk.Button(ventana, text="Fraccionar Texto", command=mostrar_texto)
boton_mostrar.pack(pady=10)

# Etiqueta para mostrar el resultado
etiqueta_resultado = tk.Label(ventana, text="", justify="left")
etiqueta_resultado.pack(pady=10)

# Iniciar el bucle principal de la interfaz
ventana.mainloop()
