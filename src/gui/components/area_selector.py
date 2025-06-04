import os
import sys
import tkinter as tk
from tkinter import messagebox
from typing import Optional, Tuple

class AreaSelector:
    """Classe para seleção de área na tela"""
    def __init__(self, parent=None):
        self.parent = parent
        self.start_x = 0
        self.start_y = 0
        self.current_x = 0 
        self.current_y = 0
        self.root = None
        self.canvas = None
        
    def select_area(self) -> Optional[Tuple[int, int, int, int]]:
        """Abre uma janela de seleção de área e retorna as coordenadas (x1, y1, x2, y2)"""
        # Criar uma nova janela independente (sem parent para evitar problemas com transient)
        self.root = tk.Toplevel()
        self.root.attributes('-fullscreen', True)
        self.root.attributes('-alpha', 0.3)
        self.root.attributes('-topmost', True)
        self.root.configure(background='gray')
        self.root.title("Selecione a Área")
        
        # Mensagem de instruções
        label = tk.Label(self.root, text="Clique e arraste para selecionar a área. Pressione ESC para cancelar.",
                          bg="white", fg="black", font=("Arial", 20))
        label.pack(pady=10)
        
        # Canvas para desenho da seleção
        self.canvas = tk.Canvas(self.root, cursor="cross", bg="gray")
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # Eventos
        self.canvas.bind("<ButtonPress-1>", self._on_press)
        self.canvas.bind("<B1-Motion>", self._on_drag)
        self.canvas.bind("<ButtonRelease-1>", self._on_release)
        self.root.bind("<Escape>", lambda e: self.root.destroy())
        
        # Variável para armazenar o resultado
        self.result = None
        
        # Aguardar até que a janela seja fechada
        self.root.wait_window(self.root)
        return self.result
    
    def _on_press(self, event):
        self.start_x = self.canvas.canvasx(event.x)
        self.start_y = self.canvas.canvasy(event.y)
        
        # Criar um retângulo se não existir
        if hasattr(self, 'rect'):
            self.canvas.delete(self.rect)
        self.rect = self.canvas.create_rectangle(
            self.start_x, self.start_y, self.start_x, self.start_y,
            outline='red', width=2, fill='blue', stipple='gray25'
        )
    
    def _on_drag(self, event):
        self.current_x = self.canvas.canvasx(event.x)
        self.current_y = self.canvas.canvasy(event.y)
        
        # Atualizar o retângulo
        self.canvas.coords(self.rect, self.start_x, self.start_y,
                          self.current_x, self.current_y)
    
    def _on_release(self, event):
        # Coordenadas finais
        x1 = min(self.start_x, self.current_x)
        y1 = min(self.start_y, self.current_y)
        x2 = max(self.start_x, self.current_x)
        y2 = max(self.start_y, self.current_y)
        
        # Verificar se a área é válida (mínimo 10x10)
        if (x2 - x1) > 10 and (y2 - y1) > 10:
            self.result = (int(x1), int(y1), int(x2), int(y2))
            self.root.destroy()
        else:
            messagebox.showwarning("Área inválida", 
                                  "A área selecionada é muito pequena. Selecione uma área maior.")
