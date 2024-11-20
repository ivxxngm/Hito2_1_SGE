from tkinter import ttk
import tkinter as tk

class ModernStyles:
    # Colores
    PRIMARY_COLOR = "#2557a7"  # Azul principal
    SECONDARY_COLOR = "#1e88e5"  # Azul secundario
    BACKGROUND_COLOR = "#f5f5f5"  # Gris muy claro para el fondo
    FRAME_BG = "#ffffff"  # Blanco para los frames
    TEXT_COLOR = "#333333"  # Gris oscuro para texto
    ACCENT_COLOR = "#ff6b6b"  # Color de acento para elementos importantes
    SUCCESS_COLOR = "#4caf50"  # Verde para éxito
    WARNING_COLOR = "#ff9800"  # Naranja para advertencias
    ERROR_COLOR = "#f44336"  # Rojo para errores
    
    # Fuentes
    FONT_FAMILY = "Segoe UI"  # Fuente moderna y legible
    HEADER_FONT = (FONT_FAMILY, 12, "bold")
    NORMAL_FONT = (FONT_FAMILY, 10)
    SMALL_FONT = (FONT_FAMILY, 9)
    BUTTON_FONT = (FONT_FAMILY, 10, "bold")

    @classmethod
    def apply_styles(cls, root):
        # Configuración general de la ventana
        root.configure(bg=cls.BACKGROUND_COLOR)
        
        # Estilo para frames
        style = ttk.Style()
        style.configure("Modern.TFrame", background=cls.FRAME_BG)
        
        # Estilo para etiquetas
        style.configure("Modern.TLabel",
                       background=cls.FRAME_BG,
                       foreground=cls.TEXT_COLOR,
                       font=cls.NORMAL_FONT)
        
        # Estilo para botones normales
        style.configure("Modern.TButton",
                       background=cls.PRIMARY_COLOR,
                       foreground="white",
                       font=cls.BUTTON_FONT,
                       padding=(10, 5))
        
        # Estilo para botón de acción principal
        style.configure("Primary.TButton",
                       background=cls.PRIMARY_COLOR,
                       foreground="white",
                       font=cls.BUTTON_FONT,
                       padding=(10, 5))
        
        # Estilo para botón de éxito
        style.configure("Success.TButton",
                       background=cls.SUCCESS_COLOR,
                       foreground="white",
                       font=cls.BUTTON_FONT,
                       padding=(10, 5))
        
        # Estilo para botón de advertencia
        style.configure("Warning.TButton",
                       background=cls.WARNING_COLOR,
                       foreground="white",
                       font=cls.BUTTON_FONT,
                       padding=(10, 5))
        
        # Estilo para botón de eliminar
        style.configure("Danger.TButton",
                       background=cls.ERROR_COLOR,
                       foreground="white",
                       font=cls.BUTTON_FONT,
                       padding=(10, 5))
        
        # Estilo para entradas
        style.configure("Modern.TEntry",
                       fieldbackground="white",
                       background="white",
                       foreground=cls.TEXT_COLOR,
                       font=cls.NORMAL_FONT,
                       padding=5)
        
        # Estilo para el Treeview (tabla)
        style.configure("Modern.Treeview",
                       background="white",
                       foreground=cls.TEXT_COLOR,
                       fieldbackground="white",
                       font=cls.NORMAL_FONT)
        
        style.configure("Modern.Treeview.Heading",
                       background=cls.PRIMARY_COLOR,
                       foreground="white",
                       font=cls.HEADER_FONT)
        
        # Estilo para Combobox
        style.configure("Modern.TCombobox",
                       background="white",
                       font=cls.NORMAL_FONT)

    @classmethod
    def get_frame_style(cls):
        return {
            "bg": cls.FRAME_BG,
            "padx": 10,
            "pady": 10,
            "relief": "flat"
        }

    @classmethod
    def get_label_style(cls):
        return {
            "bg": cls.FRAME_BG,
            "fg": cls.TEXT_COLOR,
            "font": cls.NORMAL_FONT,
            "pady": 5
        }

    @classmethod
    def get_entry_style(cls):
        return {
            "font": cls.NORMAL_FONT,
            "bg": "white",
            "fg": cls.TEXT_COLOR,
            "relief": "solid",
            "borderwidth": 1
        }

    @classmethod
    def get_button_style(cls):
        return {
            "font": cls.BUTTON_FONT,
            "bg": cls.PRIMARY_COLOR,
            "fg": "white",
            "activebackground": cls.SECONDARY_COLOR,
            "activeforeground": "white",
            "relief": "flat",
            "padx": 15,
            "pady": 5,
            "cursor": "hand2"
        }

    @classmethod
    def get_table_style(cls):
        return {
            "background": "white",
            "foreground": cls.TEXT_COLOR,
            "font": cls.NORMAL_FONT,
            "rowheight": 25,
            "padding": 5
        }

    @classmethod
    def create_custom_button(cls, parent, text, command, style_type="normal"):
        """
        Crear un botón personalizado con diferentes estilos
        style_type puede ser: "normal", "primary", "success", "warning", "danger"
        """
        styles = {
            "normal": {
                "bg": cls.PRIMARY_COLOR,
                "hover_bg": cls.SECONDARY_COLOR
            },
            "primary": {
                "bg": cls.PRIMARY_COLOR,
                "hover_bg": cls.SECONDARY_COLOR
            },
            "success": {
                "bg": cls.SUCCESS_COLOR,
                "hover_bg": "#45a049"
            },
            "warning": {
                "bg": cls.WARNING_COLOR,
                "hover_bg": "#f57c00"
            },
            "danger": {
                "bg": cls.ERROR_COLOR,
                "hover_bg": "#d32f2f"
            }
        }
        
        style = styles.get(style_type, styles["normal"])
        
        btn = tk.Button(parent, text=text, command=command,
                       font=cls.BUTTON_FONT,
                       bg=style["bg"],
                       fg="white",
                       activebackground=style["hover_bg"],
                       activeforeground="white",
                       relief="flat",
                       padx=15,
                       pady=5,
                       cursor="hand2")
        
        # Efectos hover
        def on_enter(e):
            btn['background'] = style["hover_bg"]
        
        def on_leave(e):
            btn['background'] = style["bg"]
        
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)
        
        return btn