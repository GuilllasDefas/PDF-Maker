import os
import sys
import json
import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time
import platform
from typing import Dict, Any, Optional, Tuple, List

# Importar módulos separados
from src.gui.preset_components.area_selector import AreaSelector
from src.gui.preset_components.window_selector import WindowSelector
from src.gui.preset_components.key_capture import KeyCaptureDialog

from src.config.config import ICON, PRESET_WINDOW_SIZE, MIN_PRESET_WINDOW_SIZE

class PresetConfigWindow:
    """Janela de configuração de presets para automação de capturas"""
    def __init__(self, parent, base_dir, callback=None, initial_preset=None):
        self.parent = parent
        self.base_dir = base_dir
        self.callback = callback
        self.window = None
        self.capture_area = None
        self.area_feedback_label = None
        self.initial_preset = initial_preset  # Armazena o preset inicial
        
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
        
        # Variáveis para armazenar configurações de janela e área
        self.capture_area = None
        self.selected_window = None
    
    def show(self):
        """Mostra a janela de configuração"""
        if self.window is not None:
            self.window.lift()
            return
        
        # Calcular o tamanho apropriado para a janela usando porcentagem da tela
        screen_width = self.parent.winfo_screenwidth()
        screen_height = self.parent.winfo_screenheight()

        width = int(screen_width * PRESET_WINDOW_SIZE[0] / 100)
        height = int(screen_height * PRESET_WINDOW_SIZE[1] / 100)
        window_size = f"{width}x{height}"


        self.window = tk.Toplevel(self.parent)
        self.window.title("Configurar Captura Automática")
        self.window.geometry(window_size)

        min_width = int(screen_width * MIN_PRESET_WINDOW_SIZE[0] / 100)
        min_height = int(screen_height * MIN_PRESET_WINDOW_SIZE[1] / 100)

        self.window.minsize(min_width, min_height)
        self.window.resizable(True, True)
        
        icon_path = ICON
        if getattr(sys, 'frozen', False):
            icon_path = os.path.join(sys._MEIPASS, ICON)
        self.window.iconbitmap(icon_path)
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
        
        # Adicionar evento de binding para carregar automaticamente quando selecionar
        self.preset_combobox.bind("<<ComboboxSelected>>", self._on_preset_selected)
        
        preset_btn_frame = ttk.Frame(preset_list_frame)
        preset_btn_frame.pack(side=tk.RIGHT)
        
        # Botão de excluir (removido o botão "Recarregar")
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
        
        # Mudar de "Janela ativa" para apenas "Janela"
        window_frame = ttk.Frame(capture_frame)
        window_frame.pack(anchor=tk.W, fill=tk.X)
        
        ttk.Radiobutton(window_frame, text="Janela", variable=self.capture_type, value="window").pack(side=tk.LEFT)
        self.window_btn = ttk.Button(window_frame, text="Selecionar Janela", command=self._select_window)
        self.window_btn.pack(side=tk.LEFT, padx=5)
        
        # Feedback da janela selecionada
        self.window_feedback_label = ttk.Label(window_frame, text="(Nenhuma janela selecionada)")
        self.window_feedback_label.pack(side=tk.LEFT, padx=5)
        
        area_frame = ttk.Frame(capture_frame)
        area_frame.pack(anchor=tk.W, fill=tk.X)
        
        ttk.Radiobutton(area_frame, text="Área específica", variable=self.capture_type, value="area").pack(side=tk.LEFT)
        self.area_btn = ttk.Button(area_frame, text="Selecionar Área", command=self._select_area)
        self.area_btn.pack(side=tk.LEFT, padx=5)
        
        # Feedback da área selecionada
        self.area_feedback_label = ttk.Label(area_frame, text="(Nenhuma área selecionada)")
        self.area_feedback_label.pack(side=tk.LEFT, padx=5)
        
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
        
        # Atualizar lista de presets e selecionar o preset inicial
        self._update_preset_list()
        self.window.grab_set()  # Modal, mas mantém os botões de controle
        self.parent.wait_window(self.window)
    
    def _on_close(self):
        """Fecha a janela"""
        self.window.destroy()
        self.window = None
    
    def _on_preset_selected(self, event):
        """Callback chamado quando o usuário seleciona um preset na ComboBox"""
        # Carregar automaticamente o preset selecionado
        self._load_preset(silent=True)
    
    def _update_preset_list(self):
        """Atualiza a lista de presets disponíveis e seleciona o preset inicial ou anterior"""
        # Preservar a seleção atual
        current_selection = self.preset_combobox.get()
        
        presets = []
        if os.path.exists(self.presets_dir):
            for filename in os.listdir(self.presets_dir):
                if filename.endswith(".json"):
                    presets.append(filename[:-5])  # Remove .json
        
        self.preset_combobox["values"] = presets
        
        # Se não houver presets, não precisa tentar selecionar
        if not presets:
            return
            
        # Tentar manter a seleção atual, se possível
        if current_selection and current_selection in presets:
            self.preset_combobox.set(current_selection)
        # Ou tentar selecionar o preset inicial, se fornecido
        elif self.initial_preset and self.initial_preset in presets:
            self.preset_combobox.set(self.initial_preset)
            
            # Carrega o preset selecionado sem mostrar mensagem
            try:
                self._load_preset(silent=True)
            except Exception as e:
                print(f"Erro ao carregar preset inicial: {e}")
        # Caso contrário, carrega o primeiro preset
        elif presets:
            self.preset_combobox.current(0)
            try:
                self._load_preset(silent=True)
            except Exception as e:
                print(f"Erro ao carregar preset inicial: {e}")
    
    def _select_area(self):
        """Abre a seleção de área"""
        # Minimizar a janela principal antes de abrir o seletor
        main_win = self.parent.winfo_toplevel() if self.parent else None
        main_win_minimized = False
        if main_win:
            main_win_minimized = main_win.state() == 'iconic'
            if not main_win_minimized:
                main_win.iconify()
        # Minimizar a janela de configuração também
        config_win_minimized = False
        if self.window:
            config_win_minimized = self.window.state() == 'iconic'
            if not config_win_minimized:
                self.window.iconify()
        try:
            selector = AreaSelector()
            area = selector.select_area()
            if area:
                self.capture_area = area
                self.capture_type.set("area")
                self.area_feedback_label.config(text=f"Área: {area[0]},{area[1]} até {area[2]},{area[3]}")
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao selecionar área: {str(e)}")
        finally:
            # Restaurar a janela principal após a seleção
            if main_win and not main_win_minimized:
                main_win.deiconify()
            # Restaurar a janela de configuração após a seleção
            if self.window and not config_win_minimized:
                self.window.deiconify()
    
    def _select_window(self):
        """Abre a seleção de janela"""
        # Guardar posição atual da janela
        window_position = self.window.geometry().split("+")[1:]
        x, y = int(window_position[0]), int(window_position[1])
        
        # Esconder a janela temporariamente e minimizar a principal
        main_window = self.parent.winfo_toplevel() if self.parent else None
        main_window_minimized = False
        
        if main_window:
            main_window_minimized = main_window.state() == 'iconic'
            if not main_window_minimized:
                main_window.iconify()
                
        self.window.withdraw()
        
        try:
            window_selector = WindowSelector()
            print("Iniciando seleção de janela...")
            selected_window = window_selector.select_window()
            
            # Verificar se uma janela foi selecionada
            if selected_window:
                print(f"Janela selecionada com sucesso: {selected_window['title']}")
                print(f"Detalhes: {selected_window}")
                
                # Armazenar a janela selecionada
                self.selected_window = selected_window
                
                # Selecionar o radiobutton de janela automaticamente
                self.capture_type.set("window")
                
                # Preparar o texto truncado para mostrar na label
                title = selected_window['title']
                truncated_title = (title[:27] + "...") if len(title) > 30 else title
                
                # Atualizar a label com feedback visual
                if hasattr(self, 'window_feedback_label') and self.window_feedback_label.winfo_exists():
                    self.window_feedback_label.configure(text=f"Janela: {truncated_title}")
                    # Forçar atualização do widget
                    self.window_feedback_label.update()
                
                # Mostrar mensagem de sucesso
                messagebox.showinfo("Sucesso", f"Janela '{truncated_title}' selecionada com sucesso!")
            else:
                print("Nenhuma janela foi selecionada pelo usuário.")
                messagebox.showinfo("Aviso", "Nenhuma janela foi selecionada.")
        
        except Exception as e:
            print(f"Erro detalhado ao selecionar janela: {str(e)}")
            import traceback
            traceback.print_exc()
            messagebox.showerror("Erro", f"Falha ao selecionar janela: {str(e)}")
        finally:
            # Restaurar a janela principal e de configuração
            self.window.deiconify()
            self.window.geometry(f"+{x}+{y}")
            
            # Restaurar a janela principal se não estava minimizada antes
            if main_window and not main_window_minimized:
                main_window.deiconify()
    
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
            
            # Atualizar lista e selecionar explicitamente o preset atual
            old_values = self.preset_combobox["values"]
            self._update_preset_list()
            
            # Garantir que o preset salvo seja selecionado
            if name not in old_values:
                # Se é um novo preset, selecionar na lista
                values = list(self.preset_combobox["values"])
                if name in values:
                    index = values.index(name)
                    self.preset_combobox.current(index)
            else:
                # Se é um preset existente, simplesmente definir
                self.preset_combobox.set(name)
            
            messagebox.showinfo("Sucesso", f"Preset '{name}' salvo com sucesso!")
            
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
            
        # Adicionar janela selecionada se disponível
        if self.selected_window and self.capture_type.get() == "window":
            preset_data["selected_window"] = self.selected_window
            
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
        
        # Recuperar janela selecionada
        self.selected_window = preset_data.get("selected_window")
        if self.selected_window and hasattr(self, 'window_feedback_label'):
            # Atualiza o feedback visual da janela selecionada
            window_title = self.selected_window.get('title', 'Janela sem título')
            self.window_feedback_label.config(text=f"Janela: {window_title[:30]}...")
        else:
            self.window_feedback_label.config(text="(Nenhuma janela selecionada)")
        
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
                # Antes de fechar a janela, armazenar o nome do preset que estamos aplicando
                preset_name = preset_data.get('name')
                
                # Se o nome do preset não corresponder à seleção atual do ComboBox
                # (isso pode acontecer se o usuário editou o nome), atualizar a ComboBox
                if preset_name != self.preset_combobox.get():
                    # Verificar se o nome está na lista
                    values = list(self.preset_combobox['values'])
                    if preset_name in values:
                        self.preset_combobox.set(preset_name)
                
                # Passar os dados para o callback
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
