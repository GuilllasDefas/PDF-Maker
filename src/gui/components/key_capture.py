import os
import sys
import tkinter as tk
from tkinter import ttk
import threading
import time
import keyboard

from src.config.config import ICON

class KeyCaptureDialog:
    """Diálogo para captura de tecla pressionada pelo usuário"""
    def __init__(self, parent=None):
        self.parent = parent
        self.result = None
        
    def capture_key(self):
        """Abre um diálogo para capturar uma tecla e retorna o nome da tecla"""
        dialog = tk.Toplevel()
        dialog.title("Capturar Tecla")
        dialog.geometry("300x150")
        dialog.resizable(False, False)
        dialog.attributes('-topmost', True)
        
        # Ícone
        icon_path = ICON
        if getattr(sys, 'frozen', False):
            icon_path = os.path.join(sys._MEIPASS, ICON)
        dialog.iconbitmap(icon_path)
        
        # Centralizar na tela
        dialog_width = 270
        dialog_height = 150
        screen_width = dialog.winfo_screenwidth()
        screen_height = dialog.winfo_screenheight()
        x = (screen_width - dialog_width) // 2
        y = (screen_height - dialog_height) // 2
        dialog.geometry(f"{dialog_width}x{dialog_height}+{x}+{y}")
        
        # Label de instrução
        ttk.Label(dialog, text="Pressione a tecla que deseja capturar:", 
                  font=("Arial", 10)).pack(pady=(20, 10))
        
        # Label para mostrar a tecla capturada
        key_label = ttk.Label(dialog, text="Aguardando...", font=("Arial", 10, "bold"))
        key_label.pack(pady=10)
        
        # Variável para controlar o listener
        self.listening = True

        # Função para fechar o diálogo
        def close_dialog():
            self.listening = False
            dialog.destroy()

        # Botão de cancelar
        ttk.Button(dialog, text="Cancelar", command=close_dialog).pack(pady=10)

        # Ao fechar pelo X ou ESC, também parar a thread
        dialog.protocol("WM_DELETE_WINDOW", close_dialog)
        dialog.bind("<Escape>", lambda e: close_dialog())

        # Iniciar captura em thread separada
        capture_thread = threading.Thread(
            target=self._listen_for_key, 
            args=(lambda: self.listening, key_label, dialog)
        )
        capture_thread.daemon = True
        capture_thread.start()

        dialog.wait_window(dialog)
        return self.result

    def _listen_for_key(self, is_listening, label, dialog):
        """Escuta por pressionamento de teclas"""
        special_keys = {
            'space': 'Espaço',
            'return': 'Enter',
            'escape': 'Esc',
            'tab': 'Tab',
            'right': 'Direita →',
            'left': 'Esquerda ←',
            'up': 'Cima ↑',
            'down': 'Baixo ↓'
        }

        while is_listening():
            try:
                event = keyboard.read_event(suppress=True)
                if not is_listening():
                    break
                if event.event_type == keyboard.KEY_DOWN:
                    key_name = event.name
                    display_name = special_keys.get(key_name, key_name.upper())
                    # Só atualiza o label se o widget ainda existir
                    if label.winfo_exists() and dialog.winfo_exists():
                        dialog.after(0, lambda: label.config(text=display_name))
                    self.result = key_name
                    # Fechar o diálogo após um pequeno delay, se ainda existir
                    if dialog.winfo_exists():
                        dialog.after(500, dialog.destroy)
                    self.listening = False
                    break
                time.sleep(0.1)
            except Exception:
                break
