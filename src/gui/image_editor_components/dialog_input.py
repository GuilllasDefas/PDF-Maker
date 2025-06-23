import os
import sys
import tkinter as tk
from tkinter import ttk

from src.config.config import ICON, IMAGE_EDITOR_DIALOG_WINDOW_SIZE

class TextInputDialog:
    """Diálogo personalizado para entrada de texto."""
    def __init__(self, parent, title="Digite o texto"):
        self.result = None
        self.parent = parent
        
        # Calcular o tamanho apropriado para a janela usando porcentagem da tela
        screen_width = parent.winfo_screenwidth()
        screen_height = parent.winfo_screenheight()

        width = int(screen_width * IMAGE_EDITOR_DIALOG_WINDOW_SIZE[0] / 100)
        height = int(screen_height * IMAGE_EDITOR_DIALOG_WINDOW_SIZE[1] / 100)
        window_size = f"{width}x{height}"

        # Criar uma janela de diálogo
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(title)
        self.dialog.geometry(window_size)
        self.dialog.minsize(width, height)
        
        # Permitir maximizar/minimizar a janela de diálogo
        self.dialog.resizable(True, True)
        
        # Centralizar no pai
        self.dialog.update_idletasks()
        width = self.dialog.winfo_width()
        height = self.dialog.winfo_height()
        parent_x = parent.winfo_rootx()
        parent_y = parent.winfo_rooty()
        parent_width = parent.winfo_width()
        parent_height = parent.winfo_height()
        
        x = parent_x + (parent_width - width) // 2
        y = parent_y + (parent_height - height) // 2
        self.dialog.geometry(f"+{x}+{y}")
        
        # Adicionar ícone
        icon_path = ICON
        if getattr(sys, 'frozen', False):
            icon_path = os.path.join(sys._MEIPASS, ICON)
        self.dialog.iconbitmap(icon_path)
        
        # Configurar a janela de diálogo como modal
        self.dialog.grab_set()  # Captura todos os eventos, impedindo interação com a janela pai
        
        # Desabilitar todos os widgets da janela pai
        for widget in parent.winfo_children():
            if isinstance(widget, (ttk.Frame, tk.Frame)):
                for child in widget.winfo_children():
                    if isinstance(child, (ttk.Button, ttk.Entry, tk.Canvas, ttk.Combobox)):
                        child.configure(state='disabled')
        
        # Adicionar componentes
        frame = ttk.Frame(self.dialog, padding=20)
        frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(frame, text="Digite o texto que deseja adicionar:").pack(anchor=tk.W, pady=(0, 10))
        
        # Usar um Text com múltiplas linhas em vez de Entry
        self.text_widget = tk.Text(frame, width=40, height=5, wrap="word")
        self.text_widget.pack(fill=tk.BOTH, expand=True, pady=10)
        self.text_widget.focus_set()
        
        # Botões
        btn_frame = ttk.Frame(frame)
        btn_frame.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Button(btn_frame, text="Cancelar", width=10, command=self.cancel).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="OK", width=10, command=self.ok).pack(side=tk.RIGHT, padx=5)
        
        # Configurar pressionamento de Enter para enviar
        self.dialog.bind("<Return>", lambda e: self.ok())
        self.dialog.bind("<Escape>", lambda e: self.cancel())
        
        # Esperar até que a janela seja fechada
        parent.wait_window(self.dialog)

        # Reabilitar todos os widgets da janela pai
        for widget in parent.winfo_children():
            if isinstance(widget, (ttk.Frame, tk.Frame)):
                for child in widget.winfo_children():
                    if isinstance(child, (ttk.Button, ttk.Entry, tk.Canvas, ttk.Combobox)):
                        child.configure(state='normal')
    
    def ok(self):
        """Processa o texto inserido e fecha o diálogo."""
        self.result = self.text_widget.get("1.0", "end-1c").strip()
        self.dialog.destroy()
    
    def cancel(self):
        """Cancela a operação e fecha o diálogo."""
        self.result = None
        self.dialog.destroy()