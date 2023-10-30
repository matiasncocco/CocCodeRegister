import tkinter as tk
from datetime import datetime
import openpyxl
from openpyxl import Workbook

# Función para eliminar el mensaje inicial cuando el usuario hace clic en el campo
def eliminar_mensaje_inicial(event):
    mensaje_inicial_label.config(text="")  # Elimina el mensaje inicial
    if codigo_entry.get() == mensaje_inicial:
        codigo_entry.delete(0, 'end')
        codigo_entry.config(fg="black")  # Restaura el color del texto a negro
        codigo_entry.config(justify="left")  # Restaura la alineación a la izquierda

# Función para guardar códigos de barras en un archivo de texto con fecha y hora
def guardar_codigo():
    codigo = codigo_entry.get()

    if codigo:
        if codigo not in codigos_guardados:
            codigos_guardados.add(codigo)
            fecha_hora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            with open("codigos.txt", "a") as file:
                file.write(f"{codigo} - {fecha_hora}\n")
            mensaje_label.config(text=f"Código guardado: {fecha_hora}", fg="green")
        else:
            with open("codigos.txt", "r") as file:
                lines = file.readlines()
                for line in lines:
                    parts = line.strip().split(" - ")
                    if len(parts) == 2 and parts[0] == codigo:
                        fecha_hora = parts[1]
                        mensaje_label.config(text=f"El código {codigo} ya fue guardado el: {fecha_hora}", fg="red")
                        break
    else:
        mensaje_label.config(text="El campo está vacío", fg="red")

    codigo_entry.delete(0, 'end')

# Función para descargar la lista de códigos guardados en un archivo Excel
def descargar_lista():
    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "Códigos Guardados"

    # Agrega los títulos una sola vez
    sheet.append(["Fecha", "Código"])

    for codigo in codigos_guardados:
        fecha_hora = "No encontrado"  # Por defecto, si no se encuentra la fecha/hora
        with open("codigos.txt", "r") as file:
            lines = file.readlines()
            for line in lines:
                parts = line.strip().split(" - ")
                if len(parts) == 2 and parts[0] == codigo:
                    fecha_hora = parts[1]
                    break

        sheet.append([fecha_hora, codigo])

    nombre_archivo = "codigos_guardados.xlsx"
    workbook.save(nombre_archivo)
    mensaje_label.config(text=f"Lista descargada como '{nombre_archivo}'", fg="blue")


# Crear ventana principal
ventana = tk.Tk()
ventana.title("CocCodeRegister")
ventana.geometry("800x400")

# Establecer el icono de la ventana (reemplaza "ruta_del_icono.ico" con la ruta de tu archivo .ico)
ventana.iconbitmap("sources/code.ico")

# Mensaje inicial
mensaje_inicial = "Haga click en el campo para comenzar"
mensaje_inicial_label = tk.Label(ventana, text=mensaje_inicial, font=("Arial", 16), fg="gray")
mensaje_inicial_label.pack(side="top", pady=10)

# Campo de entrada para el código de barras
codigo_entry = tk.Entry(ventana, font=("Arial", 16), justify="center")
codigo_entry.pack(side="top", pady=10)
codigo_entry.bind("<FocusIn>", eliminar_mensaje_inicial)  # Registra el evento de clic

# Botón para guardar el código
guardar_boton = tk.Button(ventana, text="Guardar", command=guardar_codigo)
guardar_boton.pack(side="top", pady=10)

# Botón para descargar la lista
descargar_boton = tk.Button(ventana, text="Descargar Lista (Excel)", command=descargar_lista,)
descargar_boton.pack(side="top", pady=10)

# Etiqueta para mensajes
mensaje_label = tk.Label(ventana, text="", font=("Arial", 16))
mensaje_label.pack(side="top", pady=10)

# Conjunto para mantener un seguimiento de los códigos guardados
codigos_guardados = set()

# Cargar códigos previamente guardados desde el archivo
try:
    with open("codigos.txt", "r") as file:
        lines = file.readlines()
        for line in lines:
            parts = line.strip().split(" - ")
            if len(parts) == 2:
                codigo, fecha_hora = parts
                codigos_guardados.add(codigo)
                mensaje_label.config(text=f"Código guardado: {fecha_hora}", fg="green")
except FileNotFoundError:
    pass

# Configurar la tecla Enter para guardar
ventana.bind('<Return>', lambda event=None: guardar_codigo())

# Iniciar la aplicación
ventana.mainloop()
