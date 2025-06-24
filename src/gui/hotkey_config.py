import os
import sys
import json
import tkinter as tk
from tkinter import ttk, messagebox
import keyboard
from src.config.config import (
    DEFAULT_SCREENSHOT_HOTKEY, DEFAULT_AUTOMATION_HOTKEY,
    SCREENSHOT_HOTKEY, AUTOMATION_HOTKEY, ICON, HOTKEY_WINDOW_SIZE
)

class HotkeyConfigWindow:
    def __init__(self, parent, on_save_callback=None):
        self.parent = parent
        self.window = None
        self.on_save_callback = on_save_callback
        
        # Valores atuais
        self.screenshot_hotkey_var = tk.StringVar(value=SCREENSHOT_HOTKEY)
        self.automation_hotkey_var = tk.StringVar(value=AUTOMATION_HOTKEY)
        
        # Flag para indicar que estamos capturando um atalho
        self.capturing_hotkey = False
        self.current_entry = None
        self.current_var = None
        self.hotkey_listener = None
        self.timer = None  # Timer para garantir o fim da captura
        
    def show(self):
        if self.window is not None:
            self.window.destroy()
            
        # Calcular o tamanho apropriado para a janela usando porcentagem da tela
        screen_width = self.parent.winfo_screenwidth()
        screen_height = self.parent.winfo_screenheight()
        width = int(screen_width * HOTKEY_WINDOW_SIZE[0] / 100)
        height = int(screen_height * HOTKEY_WINDOW_SIZE[1] / 100)
        window_size = f"{width}x{height}"

        # Cria a janela de configuração de atalhos
        self.window = tk.Toplevel(self.parent)
        self.window.title("Configurar Atalhos")
        self.window.geometry(window_size)  # Aumentei um pouco a altura para acomodar as labels de instrução
        self.window.resizable(True, True)
        icon_path = ICON
        if getattr(sys, 'frozen', False):
            icon_path = os.path.join(sys._MEIPASS, ICON)
        self.window.iconbitmap(icon_path)
        self.window.transient(self.parent)
        self.window.grab_set()
        
        # Centralizar
        self.window.update_idletasks()
        w = self.window.winfo_width()
        h = self.window.winfo_height()
        x = (self.parent.winfo_width() - w) // 2 + self.parent.winfo_x()
        y = (self.parent.winfo_height() - h) // 2 + self.parent.winfo_y()
        self.window.geometry(f"+{x}+{y}")
        
        # Frame principal
        main_frame = ttk.Frame(self.window, padding=10)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Instruções
        ttk.Label(main_frame, text="Configure os atalhos de teclado da aplicação:").pack(anchor=tk.W, pady=(0, 10))
        
        # Configuração de atalho para Screenshot
        screenshot_frame = ttk.Frame(main_frame)
        screenshot_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(screenshot_frame, text="Tirar Screenshot:").pack(side=tk.LEFT, padx=(0, 10))
        
        self.screenshot_entry = ttk.Entry(screenshot_frame, textvariable=self.screenshot_hotkey_var)
        self.screenshot_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        ttk.Button(screenshot_frame, text="Capturar", 
                  command=lambda: self._start_hotkey_capture(self.screenshot_entry, self.screenshot_hotkey_var)).pack(side=tk.RIGHT)
        
        # Label de instrução para o screenshot
        self.screenshot_instruction = ttk.Label(main_frame, text="", font=("", 8), foreground="gray")
        self.screenshot_instruction.pack(fill=tk.X, padx=5)
        
        # Configuração de atalho para Automação
        automation_frame = ttk.Frame(main_frame)
        automation_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(automation_frame, text="Iniciar Automação:").pack(side=tk.LEFT)
        
        self.automation_entry = ttk.Entry(automation_frame, textvariable=self.automation_hotkey_var)
        self.automation_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        ttk.Button(automation_frame, text="Capturar", 
                  command=lambda: self._start_hotkey_capture(self.automation_entry, self.automation_hotkey_var)).pack(side=tk.RIGHT)
        
        # Label de instrução para a automação
        self.automation_instruction = ttk.Label(main_frame, text="", font=("", 8), foreground="gray")
        self.automation_instruction.pack(fill=tk.X, padx=5)
        
        # Mensagem explicativa
        ttk.Label(main_frame, text="Nota: Reinicie a aplicação após salvar para aplicar os novos atalhos.",
                 font=("", 8), foreground="gray").pack(anchor=tk.W, pady=(10, 0))
        
        # Botões
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill=tk.X, pady=(15, 0))
        
        ttk.Button(btn_frame, text="Restaurar Padrões", command=self._reset_defaults).pack(side=tk.LEFT)
        ttk.Button(btn_frame, text="Cancelar", command=self.window.destroy).pack(side=tk.RIGHT)
        ttk.Button(btn_frame, text="Salvar", command=self._save_settings).pack(side=tk.RIGHT, padx=5)
        
    def _start_hotkey_capture(self, entry, var):
        """Inicia a captura de um atalho."""
        # Certifica-se de limpar qualquer captura anterior
        self._ensure_capture_stopped()
        
        # Limpa a entrada
        entry.delete(0, tk.END)
        
        # Limpa as teclas pressionadas
        self.pressed_keys = set()
        
        # Exibe mensagem de instrução
        instruction_label = self.screenshot_instruction if entry == self.screenshot_entry else self.automation_instruction
        instruction_label.config(text="Pressione as teclas desejadas e solte-as para registrar")
        
        # Pega as referências para a entrada atual
        self.current_entry = entry
        self.current_var = var
        
        # Marca o modo de captura
        self.capturing_hotkey = True
        
        # Configura um temporizador de segurança
        if self.timer:
            self.window.after_cancel(self.timer)
        self.timer = self.window.after(30000, self._ensure_capture_stopped)
        
        # Configura um bind temporário para capturar eventos de teclado no nível da janela
        self.window.bind("<KeyPress>", self._on_tkinter_key_press)
        self.window.bind("<KeyRelease>", self._on_tkinter_key_release)
        
        # Foca na janela para receber eventos de teclado
        self.window.focus_force()

    def _on_tkinter_key_press(self, event):
        """Manipula eventos de tecla pressionada do Tkinter."""
        if not self.capturing_hotkey:
            return
        
        # Converte o nome da tecla para o formato esperado
        key_name = self._convert_tk_key_to_name(event.keysym)
        
        # Adiciona a tecla ao conjunto
        if key_name:
            self.pressed_keys.add(key_name)
            self._update_hotkey_display()

    def _on_tkinter_key_release(self, event):
        """Manipula eventos de tecla solta do Tkinter."""
        if not self.capturing_hotkey:
            return
        
        # Converte o nome da tecla para o formato esperado
        key_name = self._convert_tk_key_to_name(event.keysym)
        
        # Remove a tecla do conjunto quando liberada
        if key_name in self.pressed_keys:
            self.pressed_keys.remove(key_name)
        
        # Se não houver mais teclas pressionadas E tivermos registrado alguma combinação
        if not self.pressed_keys and hasattr(self, 'last_hotkey') and self.last_hotkey:
            # Aplica o último atalho capturado
            self.current_var.set(self.last_hotkey)
            self.current_entry.delete(0, tk.END)
            self.current_entry.insert(0, self.last_hotkey)
            
            # Atualiza a mensagem para mostrar que o atalho foi registrado
            instruction_label = self.screenshot_instruction if self.current_entry == self.screenshot_entry else self.automation_instruction
            instruction_label.config(text=f"Atalho registrado: {self.last_hotkey}")
            
            # Finaliza a captura
            self._ensure_capture_stopped()

    def _convert_tk_key_to_name(self, keysym):
        """Converte o keysym do Tkinter para o nome da tecla."""
        # Mapeamento de nomes de teclas especiais
        key_map = {
            'Control_L': 'ctrl', 'Control_R': 'ctrl',
            'Alt_L': 'alt', 'Alt_R': 'alt',
            'Shift_L': 'shift', 'Shift_R': 'shift',
            'Return': 'enter', 'Escape': 'esc',
            'BackSpace': 'backspace', 'Tab': 'tab',
            'space': 'space', 'Delete': 'delete',
            'Up': 'up', 'Down': 'down', 'Left': 'left', 'Right': 'right'
        }
        
        # Converte keysym para nome
        if keysym in key_map:
            return key_map[keysym]
        elif len(keysym) == 1:
            # Teclas alfanuméricas
            return keysym.lower()
        else:
            # Outras teclas - tentar converter para minúsculas
            return keysym.lower()

    def _finish_capture(self):
        """Finaliza a captura de teclas manualmente."""
        if not self.capturing_hotkey:
            return
        
        # Obtém o atalho formatado
        hotkey = self._format_hotkey()
        
        # Se for válido, aplica-o
        if hotkey:
            self.current_var.set(hotkey)
            self.current_entry.delete(0, tk.END)
            self.current_entry.insert(0, hotkey)
        else:
            # Se não houve teclas pressionadas, mantém o valor anterior
            self.current_entry.delete(0, tk.END)
            self.current_entry.insert(0, self.current_var.get())
        
        # Limpa o estado de captura
        self._ensure_capture_stopped()

    def _ensure_capture_stopped(self):
        """Garante que a captura seja interrompida."""
        if not self.capturing_hotkey:
            return
        
        # Remove os binds de teclado
        self.window.unbind("<KeyPress>")
        self.window.unbind("<KeyRelease>")
        
        # Cancela o temporizador de segurança
        if self.timer:
            self.window.after_cancel(self.timer)
            self.timer = None
        
        # Limpa as variáveis de estado
        self.capturing_hotkey = False
        self.pressed_keys = set()
        self.hotkey_listener = None
        # Não limpa current_entry ou current_var para manter a referência para a mensagem

    def _format_hotkey(self):
        """Formata as teclas pressionadas em um atalho."""
        # Ordena as teclas com modificadores primeiro
        modifiers = []
        regular_keys = []
        
        for key in self.pressed_keys:
            if key in ['ctrl', 'alt', 'shift']:
                modifiers.append(key)
            else:
                regular_keys.append(key)
        
        # Combina as teclas na ordem correta
        keys = sorted(modifiers) + sorted(regular_keys)
        return '+'.join(keys) if keys else ""

    def _update_hotkey_display(self):
        """Atualiza a exibição do atalho atual."""
        hotkey = self._format_hotkey()
        if hotkey:
            # Armazena o último hotkey válido para uso ao soltar as teclas
            self.last_hotkey = hotkey
            self.current_entry.delete(0, tk.END)
            self.current_entry.insert(0, hotkey)
        
    def _reset_defaults(self):
        """Restaura os atalhos para os valores padrão."""
        self.screenshot_hotkey_var.set(DEFAULT_SCREENSHOT_HOTKEY)
        self.automation_hotkey_var.set(DEFAULT_AUTOMATION_HOTKEY)
        
        # Atualiza a mensagem para mostrar que os atalhos foram restaurados
        self.screenshot_instruction.config(text="Atalho restaurado para o padrão")
        self.automation_instruction.config(text="Atalho restaurado para o padrão")
        
    def _save_settings(self):
        """Salva as configurações e fecha a janela."""
        # Validar se os atalhos são diferentes
        if self.screenshot_hotkey_var.get() == self.automation_hotkey_var.get():
            messagebox.showerror("Erro", "Os atalhos devem ser diferentes!")
            return
        
        # Validar se os atalhos são válidos
        screenshot_hotkey = self.screenshot_hotkey_var.get()
        automation_hotkey = self.automation_hotkey_var.get()
        
        if not screenshot_hotkey or not automation_hotkey:
            messagebox.showerror("Erro", "Os atalhos não podem estar vazios!")
            return
            
        # Salvar em arquivo
        try:
            config_path = os.path.join(os.path.expanduser("~"), "pdf_maker_config.json")
            
            # Verificar se o arquivo de configuração já existe
            existing_config = {}
            if os.path.exists(config_path):
                try:
                    with open(config_path, 'r') as f:
                        existing_config = json.load(f)
                except:
                    # Se houver erro na leitura, usar um dicionário vazio
                    existing_config = {}
            
            # Atualizar apenas as chaves de atalhos, preservando outras configurações
            existing_config['screenshot_hotkey'] = screenshot_hotkey
            existing_config['automation_hotkey'] = automation_hotkey
            
            # Salvar o arquivo atualizado
            with open(config_path, 'w') as f:
                json.dump(existing_config, f, indent=2)
                
            # Chamar callback se existir
            if self.on_save_callback:
                self.on_save_callback(existing_config)
                
            self.window.destroy()
            # Nota: removida a mensagem sobre reiniciar, pois agora os atalhos são aplicados imediatamente
            
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao salvar configurações: {str(e)}")
