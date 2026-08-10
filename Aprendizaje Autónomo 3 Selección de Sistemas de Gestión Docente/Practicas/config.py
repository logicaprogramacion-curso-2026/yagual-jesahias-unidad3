import tkinter as tk
from tkinter import messagebox, ttk


# --- Clase Persona (Modelo de Datos) ---
class Persona:
    """Clase que representa a una persona con sus datos básicos"""

    # CORRECCIÓN: __init__
    def __init__(self, nombre="", direccion="", telefono=""):
        self.nombre = nombre
        self.direccion = direccion
        self.telefono = telefono

    # CORRECCIÓN: __str__
    def __str__(self):
        """Representación en texto de la persona"""
        return f"👤 {self.nombre}\n📍 {self.direccion}\n📞 {self.telefono}"

    def obtener_datos(self):
        """Retorna un diccionario con los datos"""
        return {
            "nombre": self.nombre,
            "direccion": self.direccion,
            "telefono": self.telefono
        }


# --- Aplicación Tkinter ---
class AplicacionPersona:
    # CORRECCIÓN: __init__
    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.title("Gestor de Personas")
        self.ventana.geometry("600x550")  # Ajustado para mejor visualización

        # Lista para almacenar personas
        self.lista_personas = []

        # Variables de control (asociadas a los campos de entrada)
        self.nombre_var = tk.StringVar()
        self.direccion_var = tk.StringVar()
        self.telefono_var = tk.StringVar()

        # --- Crear la interfaz ---
        self.crear_widgets()

    def crear_widgets(self):
        """Crea todos los elementos visuales"""
        # Título principal
        titulo = tk.Label(self.ventana, text="Datos de la Persona", font=("Arial", 16, "bold"))
        titulo.pack(pady=10)

        # --- Marco para el formulario ---
        marco_formulario = tk.LabelFrame(self.ventana, text="Ingresar Datos", padx=10, pady=10)
        marco_formulario.pack(pady=10, padx=20, fill="x")

        # Fila 1: Nombre
        tk.Label(marco_formulario, text="Nombre:").grid(row=0, column=0, sticky="w", pady=5)
        tk.Entry(marco_formulario, textvariable=self.nombre_var, width=40).grid(row=0, column=1, pady=5, padx=5)

        # Fila 2: Dirección
        tk.Label(marco_formulario, text="Dirección:").grid(row=1, column=0, sticky="w", pady=5)
        tk.Entry(marco_formulario, textvariable=self.direccion_var, width=40).grid(row=1, column=1, pady=5, padx=5)

        # Fila 3: Teléfono
        tk.Label(marco_formulario, text="Teléfono:").grid(row=2, column=0, sticky="w", pady=5)
        tk.Entry(marco_formulario, textvariable=self.telefono_var, width=40).grid(row=2, column=1, pady=5, padx=5)

        # --- Botones de acción ---
        marco_botones = tk.Frame(self.ventana)
        marco_botones.pack(pady=10)

        tk.Button(marco_botones, text="➕ Guardar Persona", command=self.guardar_persona,
                  bg="#4CAF50", fg="white", padx=10).pack(side="left", padx=5)
        tk.Button(marco_botones, text="📋 Mostrar Todas", command=self.mostrar_todas,
                  bg="#2196F3", fg="white", padx=10).pack(side="left", padx=5)
        tk.Button(marco_botones, text="🗑️ Limpiar Campos", command=self.limpiar_campos,
                  bg="#FF9800", fg="white", padx=10).pack(side="left", padx=5)

        # --- Área para mostrar los datos ---
        marco_visualizacion = tk.LabelFrame(self.ventana, text="Personas Registradas", padx=10, pady=10)
        marco_visualizacion.pack(pady=10, padx=20, fill="both", expand=True)

        # Treeview (tabla para mostrar datos)
        self.tabla = ttk.Treeview(marco_visualizacion, columns=("Nombre", "Dirección", "Teléfono"), show="headings")
        self.tabla.heading("Nombre", text="Nombre")
        self.tabla.heading("Dirección", text="Dirección")
        self.tabla.heading("Teléfono", text="Teléfono")
        self.tabla.column("Nombre", width=120)
        self.tabla.column("Dirección", width=150)
        self.tabla.column("Teléfono", width=100)
        self.tabla.pack(side="left", fill="both", expand=True)

        # Scrollbar para la tabla
        scrollbar = ttk.Scrollbar(marco_visualizacion, orient="vertical", command=self.tabla.yview)
        self.tabla.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        # Botón para eliminar seleccionado
        tk.Button(self.ventana, text="❌ Eliminar Seleccionado", command=self.eliminar_seleccionado,
                  bg="#f44336", fg="white").pack(pady=10)

    def guardar_persona(self):
        """Guarda una nueva persona en la lista"""
        nombre = self.nombre_var.get().strip()
        direccion = self.direccion_var.get().strip()
        telefono = self.telefono_var.get().strip()

        # Validaciones
        if not nombre or not direccion or not telefono:
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return

        # Crear la persona y guardarla
        persona = Persona(nombre, direccion, telefono)
        self.lista_personas.append(persona)

        # Agregar a la tabla
        self.tabla.insert("", "end", values=(nombre, direccion, telefono))

        # Limpiar campos
        self.limpiar_campos()

        messagebox.showinfo("Éxito", f"Persona '{nombre}' guardada correctamente.")

    def mostrar_todas(self):
        """Muestra todas las personas en un cuadro de diálogo"""
        if not self.lista_personas:
            messagebox.showinfo("Lista vacía", "No hay personas registradas.")
            return

        texto = "📋 LISTA DE PERSONAS:\n\n"
        for i, persona in enumerate(self.lista_personas, 1):
            texto += f"{i}. {persona}\n" + "-" * 20 + "\n"

        # Crear una ventana emergente para mostrar la lista
        ventana_lista = tk.Toplevel(self.ventana)
        ventana_lista.title("Lista de Personas")
        ventana_lista.geometry("400x400")

        tk.Label(ventana_lista, text="Personas Registradas", font=("Arial", 14, "bold")).pack(pady=10)

        marco_texto = tk.Frame(ventana_lista)
        marco_texto.pack(pady=10, padx=20, fill="both", expand=True)

        scrollbar = tk.Scrollbar(marco_texto)
        scrollbar.pack(side="right", fill="y")

        texto_area = tk.Text(marco_texto, yscrollcommand=scrollbar.set, wrap="word")
        texto_area.insert("1.0", texto)
        texto_area.config(state="disabled")
        texto_area.pack(side="left", fill="both", expand=True)

        scrollbar.config(command=texto_area.yview)

        tk.Button(ventana_lista, text="Cerrar", command=ventana_lista.destroy).pack(pady=10)

    def limpiar_campos(self):
        """Limpia todos los campos de entrada"""
        self.nombre_var.set("")
        self.direccion_var.set("")
        self.telefono_var.set("")

    def eliminar_seleccionado(self):
        """Elimina la persona seleccionada en la tabla"""
        seleccion = self.tabla.selection()
        if not seleccion:
            messagebox.showwarning("Atención", "Selecciona una persona para eliminar.")
            return

        if messagebox.askyesno("Confirmar", "¿Estás seguro de eliminar esta persona?"):
            item = seleccion[0]
            valores = self.tabla.item(item, "values")
            self.tabla.delete(item)

            # Eliminar de la lista interna
            for persona in self.lista_personas:
                if (persona.nombre == valores[0] and
                        persona.direccion == valores[1] and
                        persona.telefono == valores[2]):
                    self.lista_personas.remove(persona)
                    break

            messagebox.showinfo("Eliminado", "Persona eliminada correctamente.")
# --- Ejecutar la aplicación ---
# CORRECCIÓN: __name__ == "__main__"
if __name__ == "__main__":
    ventana_principal = tk.Tk()
    app = AplicacionPersona(ventana_principal)
    ventana_principal.mainloop()
