from gc import enable
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import json
from tkinter import messagebox
import webbrowser

def mostrar_creditos():
    # Crear una ventana secundaria para mostrar los créditos
    ventana_creditos = tk.Toplevel(root)
    ventana_creditos.title("Créditos")
    
    # Cargar la imagen de los créditos desde un archivo
    imagen_creditos = Image.open("LogoUPTC.png")
    imagen_creditos = imagen_creditos.resize((800, 300))  # Ajustar el tamaño de la imagen si es necesario
    foto_creditos = ImageTk.PhotoImage(imagen_creditos)
    foto_creditos.padding = 100
    
    # Mostrar la imagen en un widget Label en la ventana de créditos
    label_imagen = tk.Label(ventana_creditos, image=foto_creditos)
    label_imagen.pack(pady=10)
    
    # Texto de los créditos
    texto_creditos = (
        "Desarrollado por [Tu Nombre]\n"
        "Fecha: [Fecha de Creación]\n"
        "Versión: [Número de Versión]\n"
        "Contacto: [Tu Correo Electrónico]\n"
        "Sitio Web: [Tu Sitio Web]\n"
    )
    
    # Mostrar el texto de los créditos en un widget Label en la ventana de créditos
    label_texto = tk.Label(ventana_creditos, text=texto_creditos, font=("Arial", 12))
    label_texto.pack(pady=10)
    
    # Botón para cerrar la ventana de créditos
    boton_cerrar = tk.Button(ventana_creditos, text="Cerrar", command=ventana_creditos.destroy)
    boton_cerrar.pack(pady=10)
    
    # Configurar la imagen para que persista (evitar que sea eliminada por el recolector de basura)
    label_imagen.image = foto_creditos

    # Centrar la ventana de créditos en la pantalla principal
    ventana_creditos.update_idletasks()  # Actualizar la ventana antes de calcular la posición
    
    # Obtener el tamaño de la ventana de créditos y de la pantalla principal
    ventana_ancho = ventana_creditos.winfo_width()
    ventana_alto = ventana_creditos.winfo_height()
    pantalla_ancho = ventana_creditos.winfo_screenwidth()
    pantalla_alto = ventana_creditos.winfo_screenheight()
    
    # Calcular la posición centrada
    posicion_x = (pantalla_ancho - ventana_ancho) // 2
    posicion_y = (pantalla_alto - ventana_alto) // 2
    
    # Establecer la geometría de la ventana centrada
    ventana_creditos.geometry(f"+{posicion_x}+{posicion_y}")

    # Hacer que la ventana de créditos sea modal (bloquear la ventana principal mientras está abierta)
    ventana_creditos.transient(root)
    ventana_creditos.grab_set()
    root.wait_window(ventana_creditos)
def mostrar_instrucciones():
    # Contenido del instructivo paso a paso
    instrucciones = [
        "Instrucciones de Uso:",
        "",
        "1. Introduzca los valores requeridos en los campos correspondientes.",
        "2. Haga clic en el botón 'Calcular k' para calcular el valor de k.",
        "3. Una vez calculado k, complete los campos restantes.",
        "4. Haga clic en el botón 'Calcular Calor Específico (c)' para obtener el resultado.",
        "",
        "Nota: Asegúrese de ingresar valores numéricos válidos en todos los campos.",
        "      Algunos campos se deshabilitarán después de su uso para evitar errores."
    ]

    # Mostrar las instrucciones como un mensaje informativo
    messagebox.showinfo("Instrucciones de Uso", "\n".join(instrucciones))

# Función para cargar datos de materiales desde un archivo JSON
def cargar_datos_materiales(ruta_archivo):
    with open(ruta_archivo, 'r', encoding='utf-8' ) as archivo:
        datos_materiales = json.load(archivo)
    return datos_materiales

# Función para calcular el valor de k
def calcular_k():
    try:
        mh20k = float(entry_mh20k.get())
        mTh20k = float(entry_mTh20k.get())
        MT0h20k = float(entry_MT0h20k.get())
        Teh20K = float(entry_Teh20K.get())
        MT0k = float(entry_MT0k.get())

        k = ((mh20k * (mTh20k - Teh20K)) / (Teh20K - MT0h20k))-MT0k
        textLabel= "K= " + str(f"{k:.2f}")
        tk.Label(root, text=textLabel, font=("Arial",20) ).grid(row=6, column=1, padx=10, pady=10, sticky=tk.E)
        return k 
    except ValueError:
        messagebox.showerror("Error", "Por favor, ingrese valores numéricos válidos.")

# Función para calcular el calor específico del sólido (c)
def calcular_calor_especifico():
    try:
        msc = float(entry_msc.get())
        Mc = float(entry_Mc.get())
        Tc = float(entry_Tc.get())
        T0c = float(entry_T0c.get())
        Teh20c = float(entry_Teh20c.get())

        c = ((Mc + calcular_k()) * (Teh20c - T0c)) / (msc * (Tc - Teh20c))
        c = c * 4186.8

        datos_materiales = cargar_datos_materiales('datos_materiales.json')

        material_aproximado = None
        mejor_aproximacion = float('inf')

        for material, valor_referencia in datos_materiales.items():
            diferencia = abs(valor_referencia['calor_especifico'] - c)
            if diferencia < mejor_aproximacion:
                mejor_aproximacion = diferencia
                material_aproximado = material

        if material_aproximado:
            messagebox.showinfo("Resultado c", f"El calor específico del sólido es: {c:.2f} J/(kg·K)\nMaterial aproximado: {material_aproximado}")
        else:
            messagebox.showinfo("Resultado c", f"El calor específico del sólido es: {c:.2f} J/(kg·K)\nNo se encontró un material aproximado en los datos.")

    except ValueError:
        messagebox.showerror("Error", "Por favor, ingrese valores numéricos válidos.")
def agregar(case):
    if case == 1:
        entry_mh20k.configure(state='disabled')
    elif case == 2:
        entry_mTh20k.configure(state='disabled')
    elif case == 3:
        entry_MT0h20k.configure(state='disabled')
    elif case == 4:
        entry_Teh20K.configure(state='disabled')
    elif case == 5:
        entry_msc.configure(state='disabled')
    elif case == 6:
        entry_Mc.configure(state='disabled')
    elif case == 7:
        entry_Tc.configure(state='disabled')
    elif case == 8:
        entry_T0c.configure(state='disabled')
    elif case == 9:
        entry_Teh20c.configure(state='disabled')
    
# Crear la ventana principal
root = tk.Tk()
root.title("Cálculo de k y Calor Específico del Sólido")
root.config(bg="white")
# Obtener el ancho de la pantalla
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Establecer el ancho de la ventana igual al ancho de la pantalla
root.geometry(f"{screen_width}x{screen_height}")  # Ajusta la altura según lo necesites
# Crear la barra de menú
menubar = tk.Menu(root)

# Crear el menú 'Ayuda' en la barra de menú
menu_ayuda = tk.Menu(menubar, tearoff=0)
menu_ayuda.add_command(label="Créditos", command=mostrar_creditos)
menu_ayuda.add_command(label="Instrucciones de Uso", command=mostrar_instrucciones)

# Agregar el menú 'Ayuda' a la barra de menú
menubar.add_cascade(label="Ayuda", menu=menu_ayuda)

# Configurar la barra de menú en la ventana principal
root.config(menu=menubar)

 # Cargar la imagen desde un archivo
image_path = "vacio2.jpg"
image = Image.open(image_path)  # Abrir la imagen usando PIL
photo = ImageTk.PhotoImage(image)  # Convertir la imagen a PhotoImage

# Crear un widget Label para mostrar la imagen
label = tk.Label(root, image=photo)
label.grid(row=0, column=5, padx=10, pady=10,columnspan=3)  

image_path2 = "vacio1.jpg"
image2 = Image.open(image_path2)  # Abrir la imagen usando PIL
photo2 = ImageTk.PhotoImage(image2)  # Convertir la imagen a PhotoImage

# Crear un widget Label para mostrar la imagen
label2 = tk.Label(root, image=photo2)
label2.grid(row=0, column=0, padx=10, pady=10,columnspan=4)  

 # Etiquetas y campos de entrada para el cálculo de k
tk.Label(root, text="m (gramos de agua a  temperatura T):").grid(row=1, column=0, padx=10, pady=10, sticky=tk.E)
entry_mh20k = tk.Scale(root, from_=50, to=125, orient=tk.HORIZONTAL, length=300,sliderlength=20, tickinterval=10, 
                       bg="lightblue", highlightthickness=0,troughcolor="white")
entry_mh20k.grid(row=1, column=2, padx=20, pady=20)
btn_agregar_mh20k= tk.Button (root, text="Agregar", command=lambda c=1: agregar(c))
btn_agregar_mh20k.grid(row=1, column=3, columnspan=1, padx=10, pady=10)

tk.Label(root, text="M (gramos de agua en el calorimetro a  temperatura T0):").grid(row=2, column=0, padx=10, pady=10, sticky=tk.E)
entry_MT0k = tk.Scale(root, from_=50, to=125, orient=tk.HORIZONTAL, length=300,sliderlength=20, tickinterval=10, 
                       bg="lightblue", highlightthickness=0,troughcolor="white")
entry_MT0k.grid(row=2, column=2, padx=20, pady=20)
btn_agregar_MT0k= tk.Button (root, text="Agregar", command=lambda c=1: agregar(c))
btn_agregar_MT0k.grid(row=2, column=3, columnspan=1, padx=10, pady=10)


tk.Label(root, text="T (Temperatura del agua hirviendo):").grid(row=3, column=0, padx=10, pady=10, sticky=tk.E)
entry_mTh20k = tk.Scale(root, from_=80, to=100, orient=tk.HORIZONTAL, length=300,sliderlength=20,  tickinterval=2, 
                       bg="lightblue", highlightthickness=0,troughcolor="white")
entry_mTh20k.grid(row=3, column=2, padx=10, pady=10)
btn_agregar_mh20k= tk.Button(root, text="Agregar", command=lambda c=2: agregar(c))
btn_agregar_mh20k.grid(row=3, column=3, columnspan=1, padx=10, pady=10)

tk.Label(root, text="T0 ( T0 del agua en el calorimetro):").grid(row=4, column=0, padx=10, pady=10, sticky=tk.E)
entry_MT0h20k = tk.Scale(root, from_=10, to=30, orient=tk.HORIZONTAL, length=300,sliderlength=20,  tickinterval=5, 
                       bg="lightblue", highlightthickness=0,troughcolor="white")
entry_MT0h20k.grid(row=4, column=2, padx=10, pady=10)
btn_agregar_mh20k= tk.Button(root, text="Agregar", command=lambda c=3: agregar(c))
btn_agregar_mh20k.grid(row=4, column=3, columnspan=1, padx=10, pady=10)

tk.Label(root, text="Te (temperatura de equilibrio del agua en el calorimetro):").grid(row=5, column=0, padx=10, pady=10, sticky=tk.E)
entry_Teh20K = tk.Scale(root, from_=10, to=50, orient=tk.HORIZONTAL, length=300,sliderlength=20, tickinterval=5, 
                       bg="lightblue", highlightthickness=0,troughcolor="white")
entry_Teh20K.grid(row=5, column=2, padx=10, pady=10)
btn_agregar_mh20k= tk.Button(root, text="Agregar", command=lambda c=4: agregar(c))
btn_agregar_mh20k.grid(row=5, column=3, columnspan=1, padx=10, pady=10)

# Botón para calcular k

btn_calcular_k = tk.Button(root, text="Calcular k", command=calcular_k)
btn_calcular_k.grid(row=6, column=1, columnspan=2, padx=10, pady=10)


#separator
separator = tk.Frame(root, width=2, bd=1, relief=tk.SUNKEN)
separator.grid(row=0, column=4, rowspan=7, sticky="ns", padx=5, pady=5)

# Etiquetas y campos de entrada para el cálculo de c
tk.Label(root, text="m (masa del sólido en gramos):").grid(row=1, column=5, padx=10, pady=10, sticky=tk.E)
entry_msc = tk.Scale(root, from_=50, to=100, orient=tk.HORIZONTAL, length=300,sliderlength=20,  tickinterval=10, 
                       bg="lightblue", highlightthickness=0,troughcolor="white")
entry_msc.grid(row=1, column=6, padx=10, pady=10)
btn_agregar_mh20k= tk.Button(root, text="Agregar",  command=lambda c=5: agregar(c))
btn_agregar_mh20k.grid(row=1, column=7, columnspan=1, padx=10, pady=10)


tk.Label(root, text="M (masa del fluido - agua en gramos):").grid(row=2, column=5, padx=10, pady=10, sticky=tk.E)
entry_Mc = tk.Scale(root, from_=50, to=125, orient=tk.HORIZONTAL, length=300,sliderlength=20, tickinterval=10, 
                       bg="lightblue", highlightthickness=0,troughcolor="white")
entry_Mc.grid(row=2, column=6, padx=10, pady=10)
btn_agregar_mh20k= tk.Button(root, text="Agregar", command=lambda c=6: agregar(c))
btn_agregar_mh20k.grid(row=2, column=7, columnspan=1, padx=10, pady=10)

tk.Label(root, text="T (temperatura del fluido hirviendo > 80°C):").grid(row=3, column=5, padx=10, pady=10, sticky=tk.E)
entry_Tc = tk.Scale(root, from_=80, to=100, orient=tk.HORIZONTAL, length=300,sliderlength=20, tickinterval=2, 
                       bg="lightblue", highlightthickness=0,troughcolor="white")
entry_Tc.grid(row=3, column=6, padx=10, pady=10)
btn_agregar_mh20k= tk.Button(root, text="Agregar", command=lambda c=7: agregar(c))
btn_agregar_mh20k.grid(row=3, column=7, columnspan=1, padx=10, pady=10)

tk.Label(root, text="T0 (temperatura inicial del fluido):").grid(row=4, column=5, padx=10, pady=10, sticky=tk.E)
entry_T0c = tk.Scale(root, from_=10, to=30, orient=tk.HORIZONTAL, length=300,sliderlength=20, tickinterval=5, 
                       bg="lightblue", highlightthickness=0,troughcolor="white")
entry_T0c.grid(row=4, column=6, padx=10, pady=10)
btn_agregar_mh20k= tk.Button(root, text="Agregar", command=lambda c=8: agregar(c))
btn_agregar_mh20k.grid(row=4, column=7, columnspan=1, padx=10, pady=10)

tk.Label(root, text="Te (temperatura de equilibrio del fluido):").grid(row=5, column=5, padx=10, pady=10, sticky=tk.E)
entry_Teh20c = tk.Scale(root, from_=10, to=50, orient=tk.HORIZONTAL, length=300,sliderlength=20, tickinterval=5, 
                       bg="lightblue", highlightthickness=0,troughcolor="white")
entry_Teh20c.grid(row=5, column=6, padx=10, pady=10)
btn_agregar_mh20k= tk.Button(root, text="Agregar", command=lambda c=9: agregar(c))
btn_agregar_mh20k.grid(row=5, column=7, columnspan=1, padx=10, pady=10)

# Botón para calcular el calor específico del sólido (c)
btn_calcular_c = tk.Button(root, text="Calcular Calor Específico (c)", command=calcular_calor_especifico)
btn_calcular_c.grid(row=6, column=5, columnspan=2, padx=10, pady=10)


root.mainloop()
