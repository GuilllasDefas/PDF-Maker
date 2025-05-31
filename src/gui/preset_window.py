import os
import json
import tkinter as tk
from tkinter import ttk, messagebox
import keyboard
import threading
import time
import sys
import platform
from typing import Dict, Any, Callable, Optional, Tuple

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
                          bg="white", fg="black", font=("Arial", 12))
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

class KeyCaptureDialog:
    """Diálogo para captura de tecla pressionada pelo usuário"""
    def __init__(self, parent=None):
        self.parent = parent
        self.result = None
        
    def capture_key(self):
        """Abre um diálogo para capturar uma tecla e retorna o nome da tecla"""
        # Criar janela independente (sem parent para evitar problemas de transient)
        dialog = tk.Toplevel()
        dialog.title("Capturar Tecla")
        dialog.geometry("300x150")
        dialog.resizable(False, False)
        dialog.attributes('-topmost', True)
        
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
        
        # Iniciar captura em thread separada
        capture_thread = threading.Thread(target=self._listen_for_key, 
                                         args=(key_label, dialog))
        capture_thread.daemon = True
        capture_thread.start()
        
        # Aguardar até que o diálogo seja fechado
        dialog.wait_window(dialog)
        return self.result
    
    def _listen_for_key(self, label, dialog):
        """Escuta por pressionamento de teclas"""
        # Dicionário de teclas especiais para nomes mais amigáveis
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
        
        while self.listening:
            event = keyboard.read_event(suppress=True)
            if event.event_type == keyboard.KEY_DOWN:
                # Armazenar o nome da tecla
                key_name = event.name
                # Converter teclas especiais para nomes mais amigáveis
                display_name = special_keys.get(key_name, key_name.upper())
                
                # Atualizar o label com a tecla capturada
                dialog.after(0, lambda: label.config(text=display_name))
                
                # Salvar o resultado
                self.result = key_name
                
                # Fechar o diálogo após um pequeno delay
                dialog.after(500, dialog.destroy)
                self.listening = False
                break
            
            time.sleep(0.1)

class PresetConfigWindow:
    """Janela de configuração de presets para automação de capturas"""
    def __init__(self, parent, base_dir, callback=None):
        self.parent = parent
        self.base_dir = base_dir
        self.callback = callback
        self.window = None
        self.capture_area = None
        self.area_feedback_label = None
        
         # Determinar o diretório apropriado para armazenar presets baseado no sistema operacional
        self.presets_dir = self._get_app_data_dir()

        # Criar diretório de presets se não existir
        try:
            os.makedirs(self.presets_dir, exist_ok=True)
        except Exception as e:
            messagebox.showwarning(f"Erro ao criar diretório de presets: {e}")
        
        # Variáveis para os campos do formulário
        self.preset_name = tk.StringVar()
        self.num_captures = tk.StringVar(value="5")
        self.interval_time = tk.StringVar(value="2")
        self.interval_unit = tk.StringVar(value="segundos")
        self.start_delay = tk.StringVar(value="3")
        self.capture_type = tk.StringVar(value="fullscreen")
        self.use_same_area = tk.BooleanVar(value=True)
        
        # Variáveis para opções avançadas
        self.stop_on_key = tk.BooleanVar(value=False)
        self.stop_key = None
        self.stop_after_time = tk.BooleanVar(value=False)
        self.stop_time = tk.StringVar(value="60")
        
        # Ação entre capturas
        self.action_type = tk.StringVar(value="none")
        self.action_key = None
    
    def show(self):
        """Mostra a janela de configuração"""
        if self.window is not None:
            self.window.lift()
            return
            
        self.window = tk.Toplevel(self.parent)
        self.window.title("🖼️ Configurar Captura Automática")
        self.window.geometry("570x630")  # Aumentado para melhor acomodar todos os elementos
        self.window.minsize(550, 500)    # Define tamanho mínimo para garantir visibilidade dos botões
        self.window.resizable(True, True)
        self.window.transient(self.parent)
        self.window.protocol("WM_DELETE_WINDOW", self._on_close)
        
        # Layout principal com scrollbar para garantir que todos os elementos sejam visíveis
        main_canvas = tk.Canvas(self.window)
        scrollbar = ttk.Scrollbar(self.window, orient="vertical", command=main_canvas.yview)
        scrollable_frame = ttk.Frame(main_canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: main_canvas.configure(
                scrollregion=main_canvas.bbox("all")
            )
        )
        
        main_canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        main_canvas.configure(yscrollcommand=scrollbar.set)
        
        main_canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Main Frame
        main_frame = ttk.Frame(scrollable_frame, padding=10)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Área de presets existentes
        preset_frame = ttk.LabelFrame(main_frame, text="Presets Salvos")
        preset_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Lista de presets e botões de ação
        preset_list_frame = ttk.Frame(preset_frame)
        preset_list_frame.pack(fill=tk.X, pady=5)
        
        self.preset_combobox = ttk.Combobox(preset_list_frame)
        self.preset_combobox.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        preset_btn_frame = ttk.Frame(preset_list_frame)
        preset_btn_frame.pack(side=tk.RIGHT)
        
        ttk.Button(preset_btn_frame, text="Carregar", command=self._load_preset).pack(side=tk.LEFT, padx=2)
        ttk.Button(preset_btn_frame, text="Excluir", command=self._delete_preset).pack(side=tk.LEFT, padx=2)
        
        # Configurações básicas
        basic_frame = ttk.LabelFrame(main_frame, text="Configuração Básica")
        basic_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Grid para os campos básicos
        grid = ttk.Frame(basic_frame)
        grid.pack(fill=tk.X, padx=5, pady=5)
        
        # Nome do preset
        ttk.Label(grid, text="Nome do preset:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        ttk.Entry(grid, textvariable=self.preset_name, width=30).grid(row=0, column=1, columnspan=3, sticky=tk.W, padx=5, pady=5)
        
        # Quantidade de telas
        ttk.Label(grid, text="Quantidade de telas:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        ttk.Entry(grid, textvariable=self.num_captures, width=5).grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)
        
        # Esperar entre capturas
        ttk.Label(grid, text="Esperar entre capturas:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        interval_frame = ttk.Frame(grid)
        interval_frame.grid(row=2, column=1, columnspan=2, sticky=tk.W, padx=5, pady=5)
        
        ttk.Entry(interval_frame, textvariable=self.interval_time, width=5).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Combobox(interval_frame, textvariable=self.interval_unit, values=["segundos", "minutos"], width=8).pack(side=tk.LEFT)
        
        # Começar após
        ttk.Label(grid, text="Começar após:").grid(row=3, column=0, sticky=tk.W, padx=5, pady=5)
        ttk.Entry(grid, textvariable=self.start_delay, width=5).grid(row=3, column=1, sticky=tk.W, padx=5, pady=5)
        ttk.Label(grid, text="segundos").grid(row=3, column=2, sticky=tk.W, padx=0, pady=5)
        
        # O que capturar
        ttk.Label(grid, text="O que capturar:").grid(row=4, column=0, sticky=tk.W, padx=5, pady=5)
        capture_frame = ttk.Frame(grid)
        capture_frame.grid(row=4, column=1, columnspan=3, sticky=tk.W, padx=5, pady=5)
        
        ttk.Radiobutton(capture_frame, text="Tela inteira", variable=self.capture_type, value="fullscreen").pack(anchor=tk.W)
        ttk.Radiobutton(capture_frame, text="Janela ativa", variable=self.capture_type, value="active_window").pack(anchor=tk.W)
        
        area_frame = ttk.Frame(capture_frame)
        area_frame.pack(anchor=tk.W, fill=tk.X)
        
        ttk.Radiobutton(area_frame, text="Área específica", variable=self.capture_type, value="area").pack(side=tk.LEFT)
        self.area_btn = ttk.Button(area_frame, text="Selecionar Área", command=self._select_area)
        self.area_btn.pack(side=tk.LEFT, padx=5)
        
        # Feedback da área selecionada
        self.area_feedback_label = ttk.Label(area_frame, text="(Nenhuma área selecionada)")
        self.area_feedback_label.pack(side=tk.LEFT, padx=5)
        
        # Usar mesma área
        ttk.Checkbutton(grid, text="Usar mesma área para todas as capturas", variable=self.use_same_area).grid(
            row=5, column=0, columnspan=4, sticky=tk.W, padx=5, pady=5)
        
        # Configurações avançadas
        advanced_frame = ttk.LabelFrame(main_frame, text="Comportamentos Inteligentes")
        advanced_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Interromper quando
        stop_frame = ttk.Frame(advanced_frame)
        stop_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(stop_frame, text="Interromper quando:").pack(anchor=tk.W, pady=(5, 0))
        
        # Parar com tecla
        stop_key_frame = ttk.Frame(stop_frame)
        stop_key_frame.pack(fill=tk.X, padx=15, pady=2)
        
        ttk.Checkbutton(stop_key_frame, text="Apertar uma tecla:", variable=self.stop_on_key).pack(side=tk.LEFT)
        self.stop_key_btn = ttk.Button(stop_key_frame, text="Capturar Tecla", command=self._capture_stop_key)
        self.stop_key_btn.pack(side=tk.LEFT, padx=5)
        self.stop_key_label = ttk.Label(stop_key_frame, text="(Não definido)")
        self.stop_key_label.pack(side=tk.LEFT, padx=5)
        
        # Parar após tempo
        stop_time_frame = ttk.Frame(stop_frame)
        stop_time_frame.pack(fill=tk.X, padx=15, pady=2)
        
        ttk.Checkbutton(stop_time_frame, text="Após um período:", variable=self.stop_after_time).pack(side=tk.LEFT)
        ttk.Entry(stop_time_frame, textvariable=self.stop_time, width=5).pack(side=tk.LEFT, padx=5)
        ttk.Label(stop_time_frame, text="segundos").pack(side=tk.LEFT)
        
        # Ação entre capturas
        action_frame = ttk.Frame(advanced_frame)
        action_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(action_frame, text="Ação entre capturas:").pack(anchor=tk.W, pady=(5, 0))
        
        action_type_frame = ttk.Frame(action_frame)
        action_type_frame.pack(fill=tk.X, padx=15, pady=2)
        
        ttk.Radiobutton(action_type_frame, text="Nada", variable=self.action_type, value="none").pack(anchor=tk.W)
        
        # Simular tecla
        key_action_frame = ttk.Frame(action_type_frame)
        key_action_frame.pack(anchor=tk.W, fill=tk.X, pady=2)
        
        ttk.Radiobutton(key_action_frame, text="Simular pressionamento de tecla:", 
                      variable=self.action_type, value="key").pack(side=tk.LEFT)
        self.action_key_btn = ttk.Button(key_action_frame, text="Capturar Tecla", command=self._capture_action_key)
        self.action_key_btn.pack(side=tk.LEFT, padx=5)
        self.action_key_label = ttk.Label(key_action_frame, text="(Não definido)")
        self.action_key_label.pack(side=tk.LEFT, padx=5)
        
        # Botões de ação
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(button_frame, text="Cancelar", width=15, command=self._on_close).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Aplicar", width=15, command=self._apply_preset).pack(side=tk.RIGHT, padx=5)
        ttk.Button(button_frame, text="Salvar Preset", width=15, command=self._save_preset).pack(side=tk.RIGHT, padx=5)
        
        # Centralizar a janela na tela
        self.window.update_idletasks()
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)
        self.window.geometry(f'+{x}+{y}')
        
        # Atualizar lista de presets e carregar o primeiro se disponível
        self._update_preset_list()
    
    def _on_close(self):
        """Fecha a janela"""
        self.window.destroy()
        self.window = None
    
    def _update_preset_list(self):
        """Atualiza a lista de presets disponíveis e carrega o primeiro automaticamente"""
        presets = []
        if os.path.exists(self.presets_dir):
            for filename in os.listdir(self.presets_dir):
                if filename.endswith(".json"):
                    presets.append(filename[:-5])  # Remove .json
        
        self.preset_combobox["values"] = presets
        if presets:
            self.preset_combobox.current(0)
            # Carregar automaticamente o primeiro preset
            try:
                self._load_preset(silent=True)
            except Exception as e:
                messagebox.showerror(f"Erro ao carregar preset inicial: {e}")
    
    def _select_area(self):
        """Abre a seleção de área"""
        # Guardar posição atual da janela
        window_position = self.window.geometry().split("+")[1:]
        x, y = int(window_position[0]), int(window_position[1])
        
        # Esconder a janela temporariamente
        self.window.withdraw()
        
        # Pequeno delay antes de mostrar o seletor
        self.window.after(100, lambda: self._show_area_selector(x, y))
    
    def _show_area_selector(self, x, y):
        """Mostra o seletor de área após delay"""
        try:
            selector = AreaSelector()  # Sem parent para evitar problemas de transient
            area = selector.select_area()
            
            if area:
                self.capture_area = area
                self.capture_type.set("area")  # Seleciona o radiobutton de área automaticamente
                # Atualiza o feedback visual
                self.area_feedback_label.config(text=f"Área: {area[0]},{area[1]} até {area[2]},{area[3]}")
            
            # Restaurar a janela principal na mesma posição
            self.window.deiconify()
            self.window.geometry(f"+{x}+{y}")
            
        except Exception as e:
            messagebox.showerror(f"Erro ao selecionar área: {e}")
            self.window.deiconify()
            messagebox.showerror("Erro", f"Falha ao selecionar área: {str(e)}")
    
    def _capture_stop_key(self):
        """Captura a tecla para interromper a automação"""
        # Guardar posição atual da janela
        window_position = self.window.geometry().split("+")[1:]
        x, y = int(window_position[0]), int(window_position[1])
        
        # Esconder a janela temporariamente
        self.window.withdraw()
        
        try:
            key_capture = KeyCaptureDialog()  # Sem parent para evitar problemas de transient
            key = key_capture.capture_key()
            
            if key:
                self.stop_key = key
                # Mostrar o nome "amigável" da tecla quando possível
                display_name = self._get_friendly_key_name(key)
                self.stop_key_label.config(text=display_name)
                self.stop_on_key.set(True)
                messagebox.showinfo("Info", f"Tecla de ação configurada: {key}")
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao capturar tecla: {str(e)}")
        finally:
            # Restaurar a janela principal na mesma posição
            self.window.deiconify()
            self.window.geometry(f"+{x}+{y}")
    
    def _capture_action_key(self):
        """Captura a tecla para ação entre capturas"""
        # Guardar posição atual da janela
        window_position = self.window.geometry().split("+")[1:]
        x, y = int(window_position[0]), int(window_position[1])
        
        # Esconder a janela temporariamente
        self.window.withdraw()
        
        try:
            key_capture = KeyCaptureDialog()  # Sem parent para evitar problemas de transient
            key = key_capture.capture_key()
            
            if key:
                self.action_key = key
                # Mostrar o nome "amigável" da tecla quando possível
                display_name = self._get_friendly_key_name(key)
                self.action_key_label.config(text=display_name)
                self.action_type.set("key")
                messagebox.showinfo("Info", f"Tecla de ação configurada: {key}")
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao capturar tecla: {str(e)}")
        finally:
            # Restaurar a janela principal na mesma posição
            self.window.deiconify()
            self.window.geometry(f"+{x}+{y}")
    
    def _get_friendly_key_name(self, key):
        """Retorna um nome amigável para a tecla"""
        special_keys = {
            'space': 'Espaço',
            'return': 'Enter',
            'escape': 'Esc',
            'tab': 'Tab',
            'right': 'Direita →',
            'left': 'Esquerda ←',
            'up': 'Cima ↑',
            'down': 'Baixo ↓',
            'pageup': 'Page Up',
            'pagedown': 'Page Down',
            'home': 'Home',
            'end': 'End',
            'delete': 'Delete',
            'insert': 'Insert'
        }
        return special_keys.get(key, key.upper())
    
    def _save_preset(self):
        """Salva o preset atual"""
        name = self.preset_name.get().strip()
        if not name:
            messagebox.showerror("Erro", "Digite um nome para o preset.")
            return
            
        try:
            # Criar dados do preset
            preset_data = self._collect_preset_data()
            
            # Verificar se o diretório existe, se não, criá-lo
            if not os.path.exists(self.presets_dir):
                os.makedirs(self.presets_dir, exist_ok=True)
                
            # Salvar como JSON
            filename = os.path.join(self.presets_dir, f"{name}.json")
            with open(filename, "w") as f:
                json.dump(preset_data, f, indent=4)
            
            messagebox.showinfo("Sucesso", f"Preset '{name}' salvo com sucesso!")
            self._update_preset_list()
            
        except PermissionError:
            # Tratamento específico para erros de permissão
            error_msg = f"Sem permissão para salvar no diretório: {self.presets_dir}\n"
            error_msg += "O programa não possui permissões de escrita neste local."
            messagebox.showerror("Erro de Permissão", error_msg)
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao salvar preset: {str(e)}\nDiretório: {self.presets_dir}")
    
    def _collect_preset_data(self) -> Dict[str, Any]:
        """Coleta os dados do formulário para um dicionário"""
        # Conversão de unidades para segundos
        interval = float(self.interval_time.get() or "0")
        if self.interval_unit.get() == "minutos":
            interval *= 60
            
        preset_data = {
            "name": self.preset_name.get().strip(),
            "num_captures": int(self.num_captures.get() or "0"),
            "interval": interval,
            "start_delay": float(self.start_delay.get() or "0"),
            "capture_type": self.capture_type.get(),
            "use_same_area": self.use_same_area.get(),
            "stop_on_key": self.stop_on_key.get(),
            "stop_key": self.stop_key,
            "stop_after_time": self.stop_after_time.get(),
            "stop_time_value": float(self.stop_time.get() or "0"),
            "action_type": self.action_type.get(),
            "action_key": self.action_key
        }
        
        # Adicionar área capturada se disponível
        if self.capture_area and self.capture_type.get() == "area":
            preset_data["capture_area"] = self.capture_area
            
        return preset_data
    
    def _load_preset(self, silent=False):
        """Carrega um preset selecionado"""
        selected = self.preset_combobox.get()
        if not selected:
            if not silent:
                messagebox.showwarning("Aviso", "Selecione um preset para carregar.")
            return
            
        try:
            # Carregar do arquivo
            filename = os.path.join(self.presets_dir, f"{selected}.json")
            with open(filename, "r") as f:
                preset_data = json.load(f)
                
            # Preencher formulário
            self._populate_form(preset_data)
            if not silent:
                messagebox.showinfo("Sucesso", f"Preset '{selected}' carregado com sucesso!")
            
        except Exception as e:
            if not silent:
                messagebox.showerror("Erro", f"Falha ao carregar preset: {str(e)}")
            raise
    
    def _populate_form(self, preset_data: Dict[str, Any]):
        """Preenche o formulário com os dados do preset"""
        # Configurações básicas
        self.preset_name.set(preset_data.get("name", ""))
        self.num_captures.set(str(preset_data.get("num_captures", 5)))
        
        # Configurar intervalo e unidade
        interval = preset_data.get("interval", 2.0)
        if interval >= 60 and interval % 60 == 0:  # É múltiplo de 60, usar minutos
            self.interval_time.set(str(int(interval // 60)))
            self.interval_unit.set("minutos")
        else:
            self.interval_time.set(str(interval))
            self.interval_unit.set("segundos")
            
        self.start_delay.set(str(preset_data.get("start_delay", 3)))
        self.capture_type.set(preset_data.get("capture_type", "fullscreen"))
        self.use_same_area.set(preset_data.get("use_same_area", True))
        
        # Recuperar área capturada
        self.capture_area = preset_data.get("capture_area")
        if self.capture_area and hasattr(self, 'area_feedback_label'):
            # Atualiza o feedback visual da área selecionada
            area = self.capture_area
            self.area_feedback_label.config(text=f"Área: {area[0]},{area[1]} até {area[2]},{area[3]}")
        else:
            self.area_feedback_label.config(text="(Nenhuma área selecionada)")
        
        # Opções avançadas
        self.stop_on_key.set(preset_data.get("stop_on_key", False))
        self.stop_key = preset_data.get("stop_key")
        if self.stop_key:
            display_name = self._get_friendly_key_name(self.stop_key)
            self.stop_key_label.config(text=display_name)
        else:
            self.stop_key_label.config(text="(Não definido)")
        
        self.stop_after_time.set(preset_data.get("stop_after_time", False))
        self.stop_time.set(str(preset_data.get("stop_time_value", 60)))
        
        self.action_type.set(preset_data.get("action_type", "none"))
        self.action_key = preset_data.get("action_key")
        if self.action_key:
            display_name = self._get_friendly_key_name(self.action_key)
            self.action_key_label.config(text=display_name)
        else:
            self.action_key_label.config(text="(Não definido)")
    
    def _delete_preset(self):
        """Exclui o preset selecionado"""
        selected = self.preset_combobox.get()
        if not selected:
            messagebox.showwarning("Aviso", "Selecione um preset para excluir.")
            return
            
        confirm = messagebox.askyesno(
            "Confirmar exclusão", 
            f"Tem certeza que deseja excluir o preset '{selected}'?")
            
        if not confirm:
            return
            
        try:
            # Excluir arquivo
            filename = os.path.join(self.presets_dir, f"{selected}.json")
            os.remove(filename)
            messagebox.showinfo("Sucesso", f"Preset '{selected}' excluído com sucesso!")
            self._update_preset_list()
            
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao excluir preset: {str(e)}")
    
    def _apply_preset(self):
        """Aplica o preset atual sem salvar"""
        try:
            preset_data = self._collect_preset_data()
            
            if self.callback:
                self.callback(preset_data)
                messagebox.showinfo("Aplicado", "Configurações aplicadas com sucesso!")
                self._on_close()
            else:
                messagebox.showwarning("Aviso", "Função de callback não configurada.")
                
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao aplicar configurações: {str(e)}")
    
    def _get_app_data_dir(self):
        """
        Retorna o diretório de dados apropriado para a aplicação com base no sistema operacional.
        Garante compatibilidade com versões compiladas.
        """
        app_name = "PDF Maker"
        
        try:            
            # Windows: AppData/Roaming
            if platform.system() == "Windows":
                app_data = os.path.join(os.environ.get('APPDATA', os.path.expanduser("~")), app_name)
            
            # Adicionar subdiretório presets
            presets_dir = os.path.join(app_data, "presets")
            return presets_dir
            
        except Exception as e:
            # Fallback para Documents
            messagebox.showerror(f"Erro ao determinar diretório de dados: {e}")
            user_home = os.path.expanduser("~")
            documents_dir = os.path.join(user_home, "Documents", app_name, "presets")
            return documents_dir
