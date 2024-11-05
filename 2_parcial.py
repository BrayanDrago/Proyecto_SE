import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from itertools import product
import os

# Obtener la ruta del escritorio del usuario
carpeta_escritorio = os.path.join(os.path.expanduser("~"), "Desktop")
carpeta_textos = os.path.join(carpeta_escritorio, "textos_guardados")

# Crear una carpeta en el escritorio para guardar los archivos de texto si no existe
if not os.path.exists(carpeta_textos):
    os.makedirs(carpeta_textos)

# Variables globales para almacenar las ventanas y el índice de la variable actual
tabla_ventana = None
arbol_ventana = None
tabla_atomos_ventana = None
indice_variable_actual = 0
selecciones = []  # Almacena las selecciones de los comboboxes

# Función que se ejecuta al presionar el botón de fraccionar texto
def mostrar_texto():
    texto = entrada_texto.get().lower()
    partes_y = texto.split(" y ")
    partes = []
    operadores = []
    contador = 1
    subparte_to_variable = {}  # Diccionario para mapear subpartes a variables

    for i, parte in enumerate(partes_y):
        subpartes = parte.split(" o ")
        for j, subparte in enumerate(subpartes):
            if subparte not in subparte_to_variable:  # Verificar si la subparte ya fue añadida
                variable = f"A{contador}"
                subparte_to_variable[subparte] = variable
                partes.append(variable)
                contador += 1
            else:
                variable = subparte_to_variable[subparte]
                partes.append(variable)

            if j < len(subpartes) - 1:
                operadores.append("v")  # "o" por "v"
        if i < len(partes_y) - 1:
            operadores.append("^")  # "y" por "^"

    formula = partes[0]
    for k in range(len(operadores)):
        formula += f" {operadores[k]} {partes[k + 1]}"

    etiqueta_resultado.config(text=f"Fórmula resultante:\n{formula}")
    mostrar_tabla_verdad(partes, operadores)  # Pasa las partes y los operadores a la tabla de verdad
    mostrar_tabla_atomos(subparte_to_variable)  # Muestra la tabla de átomos
    mostrar_arbol_logico(partes)  # Llama a la función para mostrar el árbol de átomos

# Función para guardar el texto en un archivo en la carpeta del escritorio especificada
def guardar_texto():
    texto = entrada_texto.get()
    if texto.strip() == "":
        messagebox.showwarning("Advertencia", "No hay texto para guardar.")
        return
    
    # Crear un archivo con nombre único
    nombre_archivo = f"texto_{len(os.listdir(carpeta_textos)) + 1}.txt"
    ruta_archivo = os.path.join(carpeta_textos, nombre_archivo)

    with open(ruta_archivo, "w") as archivo:
        archivo.write(texto)

    messagebox.showinfo("Guardar Texto", f"Texto guardado en {nombre_archivo} en el escritorio.")

# Función para cargar el texto desde un archivo
def cargar_texto():
    archivo_seleccionado = filedialog.askopenfilename(initialdir=carpeta_textos, title="Selecciona un archivo de texto",
                                                      filetypes=(("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*")))
    if archivo_seleccionado:
        with open(archivo_seleccionado, "r") as archivo:
            texto = archivo.read()
            entrada_texto.delete(0, tk.END)  # Limpiar el campo de entrada
            entrada_texto.insert(0, texto)   # Insertar el texto cargado

# Función para mostrar la tabla de verdad
def mostrar_tabla_verdad(variables, operadores):
    global tabla_ventana
    if tabla_ventana is not None:
        tabla_ventana.destroy()

    tabla_ventana = tk.Toplevel()
    tabla_ventana.title("Tabla de Verdad")
    tabla_ventana.geometry("800x400")

    combinaciones = list(product([0, 1], repeat=len(variables)))

    # Crear encabezados de la tabla
    for col, var in enumerate(variables):
        encabezado = tk.Label(tabla_ventana, text=var, width=10, height=2, font=("Arial", 14, "bold"), borderwidth=2, relief="solid")
        encabezado.grid(row=0, column=col)

    # Encabezado de la columna de resultados
    encabezado_resultado = tk.Label(tabla_ventana, text="Resultado", width=10, height=2, font=("Arial", 14, "bold"), borderwidth=2, relief="solid")
    encabezado_resultado.grid(row=0, column=len(variables))

    # Evaluar resultados
    for row, combinacion in enumerate(combinaciones, start=1):
        for col, valor in enumerate(combinacion):
            celda = tk.Label(tabla_ventana, text=str(valor), width=10, height=2, font=("Arial", 14), borderwidth=2, relief="solid")
            celda.grid(row=row, column=col)

        # Evaluar el resultado de la fila actual según los operadores
        resultado = combinacion[0]  # Comenzamos con el primer valor
        for i, operador in enumerate(operadores):
            if operador == "^":  # AND
                resultado = resultado and combinacion[i + 1]
            elif operador == "v":  # OR
                resultado = resultado or combinacion[i + 1]

        # Mostrar el resultado en la columna correspondiente
        celda_resultado = tk.Label(tabla_ventana, text=str(resultado), width=10, height=2, font=("Arial", 14), borderwidth=2, relief="solid")
        celda_resultado.grid(row=row, column=len(variables))

# Función para mostrar la tabla de átomos
def mostrar_tabla_atomos(subparte_to_variable):
    global tabla_atomos_ventana
    if tabla_atomos_ventana is not None:
        tabla_atomos_ventana.destroy()

    tabla_atomos_ventana = tk.Toplevel()
    tabla_atomos_ventana.title("Tabla de Átomos")
    tabla_atomos_ventana.geometry("400x400")

    tree = ttk.Treeview(tabla_atomos_ventana, columns=("Variable", "Valor"), show='headings')
    tree.pack(fill=tk.BOTH, expand=True)

    tree.heading("Variable", text="Variable")
    tree.heading("Valor", text="Valor")

    for subparte, variable in subparte_to_variable.items():
        tree.insert("", tk.END, values=(variable, subparte))

# Función para mostrar el árbol de átomos con listas desplegables secuenciales
def mostrar_arbol_logico(variables):
    global arbol_ventana, indice_variable_actual, selecciones
    if arbol_ventana is not None:
        arbol_ventana.destroy()
        
    indice_variable_actual = 0
    selecciones = []  # Reiniciar las selecciones al mostrar el árbol

    arbol_ventana = tk.Toplevel()
    arbol_ventana.title("Árbol de Átomos")
    arbol_ventana.geometry("300x300")

    # Función para manejar la selección y mostrar el siguiente `Combobox`
    def mostrar_siguiente_combobox(event=None):
        global indice_variable_actual, selecciones
        seleccion = valores_combo.get()
        selecciones.append(seleccion)  # Guardar la selección actual
        if indice_variable_actual < len(variables) - 1:
            indice_variable_actual += 1
            crear_combobox(indice_variable_actual)
        else:
            # Mostrar el camino seleccionado al finalizar
            mostrar_camino(selecciones)

    # Crear el primer `Combobox` y mostrar las variables secuencialmente
    def crear_combobox(indice):
        variable = variables[indice]
        etiqueta_variable = tk.Label(arbol_ventana, text=variable, font=("Arial", 12, "bold"))
        etiqueta_variable.pack(pady=5)

        # Crear `Combobox` para seleccionar True o False
        global valores_combo
        valores_combo = ttk.Combobox(arbol_ventana, values=["True", "False"], font=("Arial", 12))
        valores_combo.set("Seleccionar")
        valores_combo.pack(pady=5)
        valores_combo.bind("<<ComboboxSelected>>", mostrar_siguiente_combobox)

    crear_combobox(indice_variable_actual)

    # Función para mostrar el camino seleccionado
    def mostrar_camino(selecciones):
        camino_seleccionado = "Camino seleccionado: " + " -> ".join(selecciones)
        etiqueta_camino = tk.Label(arbol_ventana, text=camino_seleccionado, font=("Arial", 10), fg="green")
        etiqueta_camino.pack(pady=10)

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Fraccionador de Texto")
ventana.geometry("400x300")

# Etiqueta de instrucciones
etiqueta_instrucciones = tk.Label(ventana, text="Ingresa tu proposición compuesta:")
etiqueta_instrucciones.pack(pady=10)

# Campo de entrada para el texto
entrada_texto = tk.Entry(ventana, width=50)
entrada_texto.pack(pady=5)

# Botón para mostrar el texto ingresado
boton_mostrar = tk.Button(ventana, text="Fraccionar Texto", command=mostrar_texto)
boton_mostrar.pack(pady=10)

# Botón para guardar el texto
boton_guardar = tk.Button(ventana, text="Guardar Texto", command=guardar_texto)
boton_guardar.pack(pady=5)

# Botón para cargar el texto
boton_cargar = tk.Button(ventana, text="Cargar Texto", command=cargar_texto)
boton_cargar.pack(pady=5)

# Etiqueta para mostrar el resultado
etiqueta_resultado = tk.Label(ventana, text="", justify="left")
etiqueta_resultado.pack(pady=10)

# Iniciar el bucle principal de la interfaz
ventana.mainloop()
