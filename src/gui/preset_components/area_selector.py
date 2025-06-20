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
        self.root = tk.Toplevel()
        self.root.attributes('-fullscreen', True)
        self.root.attributes('-alpha', 0.3)
        self.root.attributes('-topmost', True)
        self.root.configure(background='gray')
        self.root.title("Selecione a Área")

        # Canvas para desenho da seleção (ocupa toda a tela)
        self.canvas = tk.Canvas(self.root, cursor="cross", bg="gray", highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.root.update_idletasks()

        # Desenhar instrução no canvas (centralizado no topo)
        width = self.root.winfo_screenwidth()
        self.canvas.create_rectangle(0, 0, width, 50, fill="white", outline="")
        self.canvas.create_text(
            width // 2, 25,
            text="Clique e arraste para selecionar a área. Pressione ESC para cancelar.",
            fill="black", font=("Arial", 20)
        )

        # Eventos
        self.canvas.bind("<ButtonPress-1>", self._on_press)
        self.canvas.bind("<B1-Motion>", self._on_drag)
        self.canvas.bind("<ButtonRelease-1>", self._on_release)
        self.root.bind("<Escape>", lambda e: self._cancel())
        self.canvas.bind("<Escape>", lambda e: self._cancel())

        self.root.grab_set()
        self.root.focus_force()

        self.result = None

        self.root.wait_window(self.root)
        return self.result

    def _cancel(self):
        """Cancela a seleção e fecha a janela"""
        self.result = None
        try:
            if self.root and self.root.winfo_exists():
                self.root.destroy()
        except Exception:
            pass

    def _on_press(self, event):
        self.start_x = self.canvas.canvasx(event.x)
        self.start_y = self.canvas.canvasy(event.y)
        self.current_x = self.start_x
        self.current_y = self.start_y
        if hasattr(self, 'rect'):
            self.canvas.delete(self.rect)
        self.rect = self.canvas.create_rectangle(
            self.start_x, self.start_y, self.start_x, self.start_y,
            outline='red', width=2, fill='blue', stipple='gray25'
        )

    def _on_drag(self, event):
        self.current_x = self.canvas.canvasx(event.x)
        self.current_y = self.canvas.canvasy(event.y)
        if hasattr(self, 'rect'):
            self.canvas.coords(self.rect, self.start_x, self.start_y,
                              self.current_x, self.current_y)

    def _on_release(self, event):
        self.current_x = self.canvas.canvasx(event.x)
        self.current_y = self.canvas.canvasy(event.y)
        x1 = min(self.start_x, self.current_x)
        y1 = min(self.start_y, self.current_y)
        x2 = max(self.start_x, self.current_x)
        y2 = max(self.start_y, self.current_y)
        if (x2 - x1) > 10 and (y2 - y1) > 10:
            self.result = (int(x1), int(y1), int(x2), int(y2))
            self.root.destroy()
        else:
            messagebox.showwarning("Área inválida",
                                  "A área selecionada é muito pequena. Selecione uma área maior.")
            # Permitir nova seleção após aviso
            if hasattr(self, 'rect'):
                self.canvas.delete(self.rect)
