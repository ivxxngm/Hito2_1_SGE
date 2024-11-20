import tkinter as tk
from tkinter import messagebox, filedialog, ttk
import pandas as pd
import matplotlib.pyplot as plt
from db import agregar_encuesta, leer_encuesta, editar_encuesta, eliminar_encuesta, conectar_db
from styles import ModernStyles

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Encuestas de Consumo de Bebidas")
        self.root.geometry("1200x800")

        # Aplicar estilos modernos
        ModernStyles.apply_styles(self.root)

        # Frame de entrada de datos (izquierda)
        self.frame_izquierdo = tk.Frame(self.root, **ModernStyles.get_frame_style())
        self.frame_izquierdo.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.Y)

        # Frame de entrada de datos
        self.frame_encuesta = tk.Frame(self.frame_izquierdo, **ModernStyles.get_frame_style())
        self.frame_encuesta.pack(pady=10)

        # Título de la sección de entrada
        titulo_entrada = tk.Label(
            self.frame_encuesta, 
            text="ENTRADA DE DATOS",
            font=ModernStyles.HEADER_FONT,
            bg=ModernStyles.FRAME_BG,
            fg=ModernStyles.PRIMARY_COLOR
        )
        titulo_entrada.grid(row=0, column=0, columnspan=2, pady=(0, 10))

        # Campos de entrada
        self.crear_campos_entrada()

        # Botones de acción
        frame_botones = tk.Frame(self.frame_izquierdo, **ModernStyles.get_frame_style())
        frame_botones.pack(pady=10)

        # Crear botones con estilos modernos
        self.btn_agregar = ModernStyles.create_custom_button(
            frame_botones, "Agregar Encuesta", self.agregar_encuesta, "success"
        )
        self.btn_agregar.grid(row=0, column=0, padx=5)

        self.btn_editar = ModernStyles.create_custom_button(
            frame_botones, "Editar Encuesta", self.editar_encuesta, "primary"
        )
        self.btn_editar.grid(row=0, column=1, padx=5)

        self.btn_eliminar = ModernStyles.create_custom_button(
            frame_botones, "Eliminar Encuesta", self.eliminar_encuesta, "danger"
        )
        self.btn_eliminar.grid(row=0, column=2, padx=5)

        self.btn_leer = ModernStyles.create_custom_button(
            frame_botones, "Leer Encuesta", self.leer_encuesta, "normal"
        )
        self.btn_leer.grid(row=0, column=3, padx=5)

        # Frame y botones de visualización
        frame_visualizacion = tk.Frame(self.frame_izquierdo, **ModernStyles.get_frame_style())
        frame_visualizacion.pack(pady=10)

        # Título de la sección de visualización
        titulo_viz = tk.Label(
            frame_visualizacion,
            text="VISUALIZACIÓN Y EXPORTACIÓN",
            font=ModernStyles.HEADER_FONT,
            bg=ModernStyles.FRAME_BG,
            fg=ModernStyles.PRIMARY_COLOR
        )
        titulo_viz.grid(row=0, column=0, columnspan=3, pady=(0, 10))

        self.btn_exportar_excel = ModernStyles.create_custom_button(
            frame_visualizacion, "Exportar a Excel", self.exportar_a_excel, "primary"
        )
        self.btn_exportar_excel.grid(row=1, column=0, padx=5)

        self.btn_grafico_consumo = ModernStyles.create_custom_button(
            frame_visualizacion, "Gráfico Consumo por Edad", 
            self.grafico_consumo_por_edad, "primary"
        )
        self.btn_grafico_consumo.grid(row=1, column=1, padx=5)

        self.btn_grafico_salud = ModernStyles.create_custom_button(
            frame_visualizacion, "Gráfico Alcohol vs Salud", 
            self.grafico_alcohol_salud, "primary"
        )
        self.btn_grafico_salud.grid(row=1, column=2, padx=5)

        # Frame derecho para filtros y tabla
        self.frame_derecho = tk.Frame(self.root, **ModernStyles.get_frame_style())
        self.frame_derecho.pack(side=tk.RIGHT, padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Frame para filtros con título
        self.frame_filtros = tk.Frame(self.frame_derecho, **ModernStyles.get_frame_style())
        self.frame_filtros.pack(fill=tk.X, pady=(0, 10))

        # Título de la sección de filtros
        titulo_filtros = tk.Label(
            self.frame_filtros,
            text="FILTROS DE BÚSQUEDA",
            font=ModernStyles.HEADER_FONT,
            bg=ModernStyles.FRAME_BG,
            fg=ModernStyles.PRIMARY_COLOR
        )
        titulo_filtros.pack(anchor=tk.W, pady=(0, 10))
        
        self.crear_filtros()

        # Crear tabla y cargar datos iniciales
        self.crear_tabla()
        self.actualizar_tabla()

        # Variable para almacenar la dirección de ordenación
        self.sort_direction = {}

        # Configurar estilos de la ventana principal
        self.root.configure(bg=ModernStyles.BACKGROUND_COLOR)
        
        # Añadir padding general
        for frame in [self.frame_izquierdo, self.frame_derecho]:
            frame.pack_configure(padx=15, pady=15)

    def crear_campos_entrada(self):
        """Crear los campos de entrada de datos"""
        self.label_id = tk.Label(self.frame_encuesta, text="ID Encuesta:")
        self.label_id.grid(row=0, column=0)
        self.entry_id = tk.Entry(self.frame_encuesta)
        self.entry_id.grid(row=0, column=1)

        self.label_edad = tk.Label(self.frame_encuesta, text="Edad:")
        self.label_edad.grid(row=1, column=0)
        self.entry_edad = tk.Entry(self.frame_encuesta)
        self.entry_edad.grid(row=1, column=1)

        self.label_sexo = tk.Label(self.frame_encuesta, text="Sexo:")
        self.label_sexo.grid(row=2, column=0)
        self.entry_sexo = tk.Entry(self.frame_encuesta)
        self.entry_sexo.grid(row=2, column=1)

        campos = [
            ("Bebidas/Semana:", 3), ("Cervezas/Semana:", 4),
            ("Bebidas Fin de Semana:", 5), ("Bebidas Destiladas/Semana:", 6),
            ("Vinos/Semana:", 7), ("Perdidas de Control:", 8),
            ("Diversión/Dependencia:", 9), ("Problemas Digestivos:", 10),
            ("Tensión Alta:", 11), ("Dolor de Cabeza:", 12)
        ]
        self.entradas = {}
        for label_texto, fila in campos:
            label = tk.Label(self.frame_encuesta, text=label_texto)
            label.grid(row=fila, column=0)
            entry = tk.Entry(self.frame_encuesta)
            entry.grid(row=fila, column=1)
            self.entradas[label_texto] = entry

    def crear_filtros(self):
        """Crear los controles de filtro"""
        # Frame para los filtros
        filtros_label = tk.Label(self.frame_filtros, text="Filtros:", font=('Arial', 10, 'bold'))
        filtros_label.pack(anchor=tk.W)

        # Frame para los controles de filtro
        frame_controles = tk.Frame(self.frame_filtros)
        frame_controles.pack(fill=tk.X)

        # Filtro por edad
        tk.Label(frame_controles, text="Edad:").grid(row=0, column=0, padx=5)
        self.edad_min = tk.Entry(frame_controles, width=5)
        self.edad_min.grid(row=0, column=1, padx=2)
        tk.Label(frame_controles, text="-").grid(row=0, column=2)
        self.edad_max = tk.Entry(frame_controles, width=5)
        self.edad_max.grid(row=0, column=3, padx=2)

        # Filtro por sexo
        tk.Label(frame_controles, text="Sexo:").grid(row=0, column=4, padx=5)
        self.sexo_var = tk.StringVar(value="Todos")
        self.sexo_combo = ttk.Combobox(frame_controles, textvariable=self.sexo_var, 
                                     values=["Todos", "Mujer", "Hombre"], width=8)
        self.sexo_combo.grid(row=0, column=5, padx=5)

        # Filtro por consumo de bebidas
        tk.Label(frame_controles, text="Bebidas/Semana:").grid(row=0, column=6, padx=5)
        self.bebidas_min = tk.Entry(frame_controles, width=5)
        self.bebidas_min.grid(row=0, column=7, padx=2)
        tk.Label(frame_controles, text="-").grid(row=0, column=8)
        self.bebidas_max = tk.Entry(frame_controles, width=5)
        self.bebidas_max.grid(row=0, column=9, padx=2)

        # Botón de aplicar filtros
        self.btn_aplicar = tk.Button(frame_controles, text="Aplicar Filtros", 
                                   command=self.aplicar_filtros)
        self.btn_aplicar.grid(row=0, column=10, padx=10)

        # Botón de limpiar filtros
        self.btn_limpiar = tk.Button(frame_controles, text="Limpiar Filtros", 
                                   command=self.limpiar_filtros)
        self.btn_limpiar.grid(row=0, column=11, padx=5)

    def crear_tabla(self):
            """Crear la tabla de datos con capacidad de ordenación"""
            # Frame para la tabla con scroll
            frame_tabla = tk.Frame(self.frame_derecho)
            frame_tabla.pack(fill=tk.BOTH, expand=True)

            # Scrollbars
            scroll_y = ttk.Scrollbar(frame_tabla)
            scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
            scroll_x = ttk.Scrollbar(frame_tabla, orient='horizontal')
            scroll_x.pack(side=tk.BOTTOM, fill=tk.X)

            # Crear Treeview
            self.tabla = ttk.Treeview(frame_tabla, yscrollcommand=scroll_y.set, 
                                    xscrollcommand=scroll_x.set)
            
            # Configurar scrollbars
            scroll_y.config(command=self.tabla.yview)
            scroll_x.config(command=self.tabla.xview)

            # Definir columnas con los nombres exactos de la base de datos
            self.tabla['columns'] = ('idEncuesta', 'edad', 'Sexo', 'BebidasSemana', 
                                'CervezasSemana', 'BebidasFinSemana', 
                                'BebidasDestiladasSemana', 'VinosSemana',
                                'PerdidasControl', 'DiversionDependenciaAlcohol', 
                                'ProblemasDigestivos', 'TensionAlta', 
                                'DolorCabeza')

            # Formatear columnas
            self.tabla.column('#0', width=0, stretch=tk.NO)
            for col in self.tabla['columns']:
                self.tabla.column(col, anchor=tk.CENTER, width=100)
                self.tabla.heading(col, text=col, anchor=tk.CENTER,
                                command=lambda c=col: self.ordenar_por_columna(c))

            self.tabla.pack(fill=tk.BOTH, expand=True)

    def ordenar_por_columna(self, columna):
        """Ordenar la tabla por la columna seleccionada"""
        # Inicializar dirección si es la primera vez
        if columna not in self.sort_direction:
            self.sort_direction[columna] = 'ascending'
        else:
            # Cambiar dirección si ya existe
            self.sort_direction[columna] = 'descending' if self.sort_direction[columna] == 'ascending' else 'ascending'

        # Obtener todos los items
        items = [(self.tabla.set(item, columna), item) for item in self.tabla.get_children('')]
        
        # Convertir a número si es posible
        try:
            items = [(float(value), item) for value, item in items]
        except ValueError:
            pass

        # Ordenar items
        items.sort(reverse=(self.sort_direction[columna] == 'descending'))

        # Reordenar tabla
        for index, (val, item) in enumerate(items):
            self.tabla.move(item, '', index)

    def aplicar_filtros(self):
            """Aplicar filtros a los datos de la tabla"""
            try:
                conn = conectar_db()
                query = "SELECT * FROM ENCUESTA WHERE 1=1"  # Nota: nombre de tabla en mayúsculas
                params = []

                # Filtro de edad
                if self.edad_min.get() and self.edad_max.get():
                    query += " AND edad >= %s AND edad <= %s"
                    params.extend([int(self.edad_min.get()), int(self.edad_max.get())])

                # Filtro de sexo
                if self.sexo_var.get() != "Todos":
                    query += " AND Sexo = %s"  # Nota: 'Sexo' con S mayúscula
                    params.append(self.sexo_var.get())

                # Filtro de bebidas por semana
                if self.bebidas_min.get() and self.bebidas_max.get():
                    query += " AND BebidasSemana >= %s AND BebidasSemana <= %s"
                    params.extend([int(self.bebidas_min.get()), int(self.bebidas_max.get())])

                print("Query:", query)  # Para depuración
                print("Params:", params)  # Para depuración

                cursor = conn.cursor()
                cursor.execute(query, tuple(params))  # Convertimos la lista a tupla
                rows = cursor.fetchall()

                # Limpiar tabla actual
                for item in self.tabla.get_children():
                    self.tabla.delete(item)

                # Insertar datos filtrados
                for row in rows:
                    self.tabla.insert('', tk.END, values=row)

                cursor.close()
                conn.close()

            except Exception as e:
                messagebox.showerror("Error", f"Error al aplicar filtros: {str(e)}")
                print("Error completo:", str(e))  # Para depuración

    def limpiar_filtros(self):
        """Limpiar todos los filtros y mostrar todos los datos"""
        self.edad_min.delete(0, tk.END)
        self.edad_max.delete(0, tk.END)
        self.sexo_var.set("Todos")
        self.bebidas_min.delete(0, tk.END)
        self.bebidas_max.delete(0, tk.END)
        self.actualizar_tabla()

    def actualizar_tabla(self):
        """Actualizar los datos de la tabla"""
        # Limpiar tabla
        for item in self.tabla.get_children():
            self.tabla.delete(item)

        try:
            # Obtener datos de la base de datos
            conn = conectar_db()
            if conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM encuesta")
                rows = cursor.fetchall()
                
                # Insertar datos en la tabla
                for row in rows:
                    self.tabla.insert('', tk.END, values=row)
                
                cursor.close()
                conn.close()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron cargar los datos: {str(e)}")

    def obtener_datos(self):
        """Obtener datos de los campos de entrada"""
        datos = {
            "id_encuesta": self.entry_id.get(),
            "edad": self.entry_edad.get(),
            "sexo": self.entry_sexo.get()
        }
        for campo, entry in self.entradas.items():
            datos[campo] = entry.get()
        return datos

    def limpiar_campos(self):
        """Método para limpiar todos los campos de entrada"""
        self.entry_id.delete(0, tk.END)
        self.entry_edad.delete(0, tk.END)
        self.entry_sexo.delete(0, tk.END)
        for entry in self.entradas.values():
            entry.delete(0, tk.END)

    def agregar_encuesta(self):
        try:
            # Obtener datos de los campos
            datos = self.obtener_datos()
            
            # Validar que todos los campos necesarios estén llenos
            campos_requeridos = [
                "id_encuesta", "edad", "sexo", 
                "Bebidas/Semana:", "Cervezas/Semana:",
                "Bebidas Fin de Semana:", "Bebidas Destiladas/Semana:",
                "Vinos/Semana:", "Perdidas de Control:",
                "Diversión/Dependencia:", "Problemas Digestivos:",
                "Tensión Alta:", "Dolor de Cabeza:"
            ]
            
            for campo in campos_requeridos:
                if campo in datos and not datos[campo]:
                    messagebox.showwarning("Advertencia", f"Por favor, complete el campo {campo}")
                    return
            
            # Llamar a la función de la base de datos
            agregar_encuesta(
                datos["id_encuesta"],
                int(datos["edad"]),
                datos["sexo"],
                int(datos["Bebidas/Semana:"]),
                int(datos["Cervezas/Semana:"]),
                int(datos["Bebidas Fin de Semana:"]),
                int(datos["Bebidas Destiladas/Semana:"]),
                int(datos["Vinos/Semana:"]),
                int(datos["Perdidas de Control:"]),
                datos["Diversión/Dependencia:"],
                datos["Problemas Digestivos:"],
                datos["Tensión Alta:"],
                datos["Dolor de Cabeza:"]
            )
            
            messagebox.showinfo("Éxito", "Encuesta agregada correctamente")
            self.limpiar_campos()
            self.actualizar_tabla()
            
        except ValueError as e:
            messagebox.showerror("Error", "Por favor, asegúrese de que los campos numéricos contengan números válidos")
            print(f"Error de valor: {str(e)}")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo agregar la encuesta: {str(e)}")
            print(f"Error completo: {str(e)}")

    def editar_encuesta(self):
        try:
            # Obtener datos de los campos
            datos = self.obtener_datos()
            
            # Validar que se haya proporcionado un ID
            if not datos["id_encuesta"]:
                messagebox.showwarning("Advertencia", "Por favor, ingrese el ID de la encuesta a editar")
                return
            
            # Validar que todos los campos necesarios estén llenos
            campos_requeridos = [
                "edad", "sexo", 
                "Bebidas/Semana:", "Cervezas/Semana:",
                "Bebidas Fin de Semana:", "Bebidas Destiladas/Semana:",
                "Vinos/Semana:", "Perdidas de Control:",
                "Diversión/Dependencia:", "Problemas Digestivos:",
                "Tensión Alta:", "Dolor de Cabeza:"
            ]
            
            for campo in campos_requeridos:
                if campo in datos and not datos[campo]:
                    messagebox.showwarning("Advertencia", f"Por favor, complete el campo {campo}")
                    return
            
            # Convertir datos y llamar a la función de edición
            try:
                editar_encuesta(
                    datos["id_encuesta"],
                    int(datos["edad"]),
                    datos["sexo"],
                    int(datos["Bebidas/Semana:"]),
                    int(datos["Cervezas/Semana:"]),
                    int(datos["Bebidas Fin de Semana:"]),
                    int(datos["Bebidas Destiladas/Semana:"]),
                    int(datos["Vinos/Semana:"]),
                    int(datos["Perdidas de Control:"]),
                    datos["Diversión/Dependencia:"],
                    datos["Problemas Digestivos:"],
                    datos["Tensión Alta:"],
                    datos["Dolor de Cabeza:"]
                )
                
                messagebox.showinfo("Éxito", "Encuesta editada correctamente")
                self.actualizar_tabla()
                
            except ValueError:
                messagebox.showerror("Error", "Por favor, asegúrese de que los campos numéricos contengan números válidos")
                
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo editar la encuesta: {str(e)}")
            print(f"Error completo: {str(e)}")

    def eliminar_encuesta(self):
        id_encuesta = self.entry_id.get()
        try:
            eliminar_encuesta(id_encuesta)
            messagebox.showinfo("Éxito", "Encuesta eliminada correctamente.")
            self.limpiar_campos()
            self.actualizar_tabla()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo eliminar la encuesta: {str(e)}")

    def leer_encuesta(self):
        try:
            id_encuesta = self.entry_id.get()
            if not id_encuesta:
                messagebox.showwarning("Advertencia", "Por favor ingrese un ID de encuesta")
                return
                
            # Llamar a la función de la base de datos
            resultado = leer_encuesta(id_encuesta)
            
            if resultado:
                # Limpiar los campos actuales
                self.limpiar_campos()
                
                # Insertar los valores en los campos
                self.entry_id.insert(0, str(resultado[0]))
                self.entry_edad.insert(0, str(resultado[1]))
                self.entry_sexo.insert(0, str(resultado[2]))
                
                # Mapeo de los campos adicionales
                campos = ['Bebidas/Semana:', 'Cervezas/Semana:', 
                        'Bebidas Fin de Semana:', 'Bebidas Destiladas/Semana:', 
                        'Vinos/Semana:', 'Perdidas de Control:', 
                        'Diversión/Dependencia:', 'Problemas Digestivos:', 
                        'Tensión Alta:', 'Dolor de Cabeza:']
                
                # Llenar los campos adicionales
                for i, campo in enumerate(campos):
                    if campo in self.entradas:
                        self.entradas[campo].delete(0, tk.END)
                        self.entradas[campo].insert(0, str(resultado[i + 3]))
                
                messagebox.showinfo("Éxito", "Encuesta cargada correctamente")
            else:
                messagebox.showwarning("Advertencia", "No se encontró la encuesta")
                
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo leer la encuesta: {str(e)}")
            print(f"Error completo: {str(e)}")  # Para depuración

    def exportar_a_excel(self):
        try:
            conn = conectar_db()
            df = pd.read_sql_query("SELECT * FROM encuesta", conn)
            conn.close()

            archivo = filedialog.asksaveasfilename(
                defaultextension=".xlsx",
                filetypes=[("Archivos Excel", "*.xlsx")]
            )
            if archivo:
                df.to_excel(archivo, index=False)
                messagebox.showinfo("Éxito", f"Datos exportados a {archivo}")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo exportar: {str(e)}")

    def grafico_consumo_por_edad(self):
        try:
            conn = conectar_db()
            df = pd.read_sql_query("SELECT * FROM encuesta", conn)
            conn.close()

            df['grupo_edad'] = pd.cut(df['edad'], bins=[0, 20, 30, 40, 50, 60, 100], 
                                    labels=['<20', '20-30', '30-40', '40-50', '50-60', '60+'])
            consumo_promedio = df.groupby('grupo_edad')[['BebidasSemana', 'CervezasSemana', 'BebidasDestiladasSemana']].mean()

            plt.figure(figsize=(10, 6))
            consumo_promedio.plot(kind='bar', ax=plt.gca())
            plt.title('Consumo Promedio de Bebidas por Grupo de Edad')
            plt.xlabel('Grupo de Edad')
            plt.ylabel('Número Promedio de Bebidas')
            plt.legend(title='Tipo de Bebida')
            plt.tight_layout()
            plt.show()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo generar el gráfico: {str(e)}")

    def grafico_alcohol_salud(self):
        try:
            conn = conectar_db()
            df = pd.read_sql_query("SELECT * FROM encuesta", conn)
            conn.close()

            df['consumo_total'] = (df['BebidasSemana'] + df['CervezasSemana'] + 
                                 df['BebidasDestiladasSemana'] + df['VinosSemana'])

            plt.figure(figsize=(12, 6))
            plt.scatter(df['consumo_total'], df['PerdidasControl'], 
                       alpha=0.6, c=df['edad'], cmap='viridis', 
                       s=df['PerdidasControl'] * 20)
            plt.colorbar(label='Edad')
            plt.title('Consumo de Alcohol vs Pérdidas de Control')
            plt.xlabel('Consumo Total de Alcohol (bebidas/semana)')
            plt.ylabel('Pérdidas de Control')
            plt.tight_layout()
            plt.show()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo generar el gráfico: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()