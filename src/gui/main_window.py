import os
import sys
import threading
import shutil
import tkinter as tk
from tkinter import ttk, messagebox, filedialog, simpledialog
from PIL import Image, ImageTk, ImageFile
import keyboard
import json
import platform
from datetime import datetime
from src.config.config import (
    DEFAULT_WINDOW_SIZE, DEFAULT_IMAGE_DISPLAY_SIZE, 
    DEFAULT_INTERVAL, DEFAULT_NUM_CAPTURES, ICON,
    SCREENSHOT_HOTKEY, AUTOMATION_HOTKEY, APP_VERSION
)
from src.core.screenshot import ScreenshotManager
from src.core.pdf_generator import PDFGenerator
from src.core.automation import AutomationManager
from src.core.update_checker import UpdateChecker
from src.gui.preset_window import PresetConfigWindow
from src.gui.hotkey_config import HotkeyConfigWindow
from src.gui.session_editor import SessionEditorWindow  # Nova importação para o editor de sessão


# Permite carregar imagens truncadas
ImageFile.LOAD_TRUNCATED_IMAGES = True

class CustomStringDialog:
    """Diálogo personalizado para entrada de texto com tamanho adequado e ícone."""
    def __init__(self, parent, title, prompt, initialvalue=None):
        self.result = None
        
        # Criar janela de diálogo
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(title)
        self.dialog.geometry("400x150")  # Tamanho maior que o padrão
        self.dialog.resizable(False, False)
        
        # Configurar ícone
        icon_path = ICON
        if getattr(sys, 'frozen', False):
            icon_path = os.path.join(sys._MEIPASS, ICON)
        self.dialog.iconbitmap(icon_path)
        
        # Tornar modal
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Centralizar na tela
        self.dialog.update_idletasks()
        w = self.dialog.winfo_width()
        h = self.dialog.winfo_height()
        x = (parent.winfo_width() - w) // 2 + parent.winfo_x()
        y = (parent.winfo_height() - h) // 2 + parent.winfo_y()
        self.dialog.geometry(f"+{x}+{y}")
        
        # Criar widgets
        frame = ttk.Frame(self.dialog, padding=20)
        frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(frame, text=prompt).pack(anchor=tk.W, pady=(0, 10))
        
        self.entry = ttk.Entry(frame, width=40)
        self.entry.pack(fill=tk.X, pady=(0, 20))
        if initialvalue:
            self.entry.insert(0, initialvalue)
        self.entry.focus_set()
        
        # Botões
        btn_frame = ttk.Frame(frame)
        btn_frame.pack(fill=tk.X)
        
        ttk.Button(btn_frame, text="Cancelar", command=self.cancel).pack(side=tk.RIGHT, padx=5)
        ttk.Button(btn_frame, text="OK", command=self.ok).pack(side=tk.RIGHT, padx=5)
        
        # Binds para teclas
        self.dialog.bind("<Return>", lambda e: self.ok())
        self.dialog.bind("<Escape>", lambda e: self.cancel())
        
        # Esperar até que a janela seja fechada
        parent.wait_window(self.dialog)
    
    def ok(self):
        """Confirma e fecha o diálogo."""
        self.result = self.entry.get()
        self.dialog.destroy()
    
    def cancel(self):
        """Cancela e fecha o diálogo."""
        self.dialog.destroy()

class PDFMakerApp:
    def __init__(self, root):
        self.root = root
        self.root.geometry(DEFAULT_WINDOW_SIZE)
        self.root.title(f"PDF Maker v{APP_VERSION} Beta")
        icon_path = ICON
        if getattr(sys, 'frozen', False):
            icon_path = os.path.join(sys._MEIPASS, ICON)
        self.root.iconbitmap(icon_path)
        width, height = map(int, DEFAULT_WINDOW_SIZE.split('x'))
        self.root.minsize(width, height)
        
        # Definir o protocolo de fechamento da janela para usar nosso método _on_exit
        # Garantir que isso seja chamado corretamente quando o usuário clica no X da janela
        self.root.protocol("WM_DELETE_WINDOW", self._on_exit)
        
        # Managers
        self.screenshot_manager = ScreenshotManager()
        self.pdf_generator = PDFGenerator()
        self.automation_manager = AutomationManager(self.screenshot_manager)
        self.update_checker = UpdateChecker()
        
        # Estado da aplicação
        self.counter = 0
        self.last_image = None
        self.current_image = None
        self.img_display_size = DEFAULT_IMAGE_DISPLAY_SIZE
        self.update_download_url = None
        self.base_directory = self._load_last_directory()  # Carrega a última pasta usada
        self.session_screenshots_dir = None  # Novo: diretório da sessão atual
        self.session_name = None  # Nome da sessão atual

        # Variáveis para automação
        self.interval_var = tk.StringVar(value=str(DEFAULT_INTERVAL))
        self.num_captures_var = tk.StringVar(value=str(DEFAULT_NUM_CAPTURES))
        
        # Configurar callbacks da automação
        self._setup_automation_callbacks()
        
        # Criar barra de menus
        self._create_menu_bar()
        
        # Construir interface
        self._build_ui()
        
        # Se tiver diretório salvo, configure-o
        if self.base_directory:
            self.dir_var.set(self.base_directory)
            self._reset_session()  # Inicializa a sessão ao abrir o diretório
        # Iniciar listener de atalhos
        self._start_hotkey_listener()
        
        # Configurar redimensionamento
        self._setup_resize_handling()
        
        # Verificar atualizações ao iniciar
        self._check_updates_on_startup()
        
        # Desabilitar funcionalidades até que um diretório seja selecionado
        self._update_controls_state()
        
        # Novo: variável para armazenar o último preset aplicado
        self.last_applied_preset = None

        # Iniciar com a última sessão se disponível
        self._try_load_last_session()
    
    def _create_menu_bar(self):
        """Cria a barra de menus da aplicação."""
        self.menu_bar = tk.Menu(self.root)
        self.root.config(menu=self.menu_bar)
        
        # Menu Arquivo
        file_menu = tk.Menu(self.menu_bar, tearoff=0)
        file_menu.add_command(label="Selecionar Diretório...", command=self._browse_directory)
        file_menu.add_command(label="Abrir Pasta", command=self._open_selected_directory)
        
        file_menu.add_separator()

        # Sessões
        file_menu.add_command(label="Nova Sessão", command=self._reset_session)
        
        # Submenu para sessões salvas
        self.sessions_menu = tk.Menu(file_menu, tearoff=0)
        file_menu.add_cascade(label="Carregar Sessão", menu=self.sessions_menu)
        self._update_sessions_menu()  # Preenche o menu com as sessões salvas
        
        file_menu.add_command(label="Salvar Sessão Atual", command=self._save_current_session)
        file_menu.add_command(label="Renomear Sessão Atual", command=self._rename_current_session)
        
        file_menu.add_command(label="Editar Sessão", command=self._edit_session)

        file_menu.add_separator()

        file_menu.add_command(label="Gerar PDF", command=self._generate_pdf)

        file_menu.add_separator()

        file_menu.add_command(label="Sair", command=self._on_exit)
        self.menu_bar.add_cascade(label="Arquivo", menu=file_menu)
        
        # Menu Ferramentas
        tools_menu = tk.Menu(self.menu_bar, tearoff=0)
        tools_menu.add_command(label="Tirar Screenshot", command=self._take_screenshot, 
                              accelerator=f"({SCREENSHOT_HOTKEY})")
        tools_menu.add_command(label="Configurar Atalhos", command=self._open_hotkey_config)
        self.menu_bar.add_cascade(label="Ferramentas", menu=tools_menu)
        
        tools_menu.add_separator()
        tools_menu.add_command(label="Iniciar Automação", command=self._start_automation, 
                              accelerator=f"({AUTOMATION_HOTKEY})")
        tools_menu.add_command(label="Parar Automação", command=self._stop_automation)     
        tools_menu.add_command(label="Configurar Automação", command=self._open_preset_config)   
        
        # Menu Ajuda
        help_menu = tk.Menu(self.menu_bar, tearoff=0)
        help_menu.add_command(label="Verificar Atualizações", command=self._manual_check_updates)
        help_menu.add_separator()
        help_menu.add_command(label=f"Sobre", 
                             command=lambda: messagebox.showinfo(
                                 "Sobre", 
                                 f"PDF Maker v{APP_VERSION}\n\n"
                                 "Aplicativo para capturar e organizar screenshots em PDF."
                             ))
        self.menu_bar.add_cascade(label="Ajuda", menu=help_menu)
    
    def _load_last_directory(self):
        """Carrega o último diretório usado de um arquivo simples."""
        try:
            last_dir_file = os.path.join(os.path.expanduser("~"), ".pdf_maker_lastdir")
            if os.path.exists(last_dir_file):
                with open(last_dir_file, 'r') as f:
                    last_dir = f.read().strip()
                    if os.path.isdir(last_dir):
                        return last_dir
        except:
            pass  # Se houver qualquer erro, apenas retorna vazio
        return ""
    
    def _save_last_directory(self, directory):
        """Salva o último diretório usado em um arquivo simples."""
        try:
            last_dir_file = os.path.join(os.path.expanduser("~"), ".pdf_maker_lastdir")
            with open(last_dir_file, 'w') as f:
                f.write(directory)
        except:
            pass  # Se houver qualquer erro, ignore silenciosamente
    
    def _setup_automation_callbacks(self):
        """Configura os callbacks da automação."""
        self.automation_manager.set_callbacks(
            on_screenshot=self._on_automation_screenshot,
            on_status=self._on_automation_status,
            on_finish=self._on_automation_finish
        )
    
    def _build_ui(self):
        """Constrói a interface do usuário."""
        # Frame superior com contador e status
        top_frame = ttk.Frame(self.root)
        top_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Counter label
        self.label_counter = ttk.Label(top_frame, text="Prints tirados: 0")
        self.label_counter.pack(side=tk.LEFT)
        
        # Status label (substitui o botão de atualização que agora está no menu)
        self.automation_status = ttk.Label(top_frame, text="Status: Inativo")
        self.automation_status.pack(side=tk.RIGHT, padx=5)
        
        # Frame para seleção de diretório base
        self._build_directory_frame()

        # Frame de imagens
        self._build_images_frame()
        
        # Frame de botões rápidos (versão simplificada)
        self._build_quick_actions_frame()
    
    def _open_selected_directory(self):
        """Abre o diretório selecionado no Explorer."""
        if self.base_directory and os.path.isdir(self.base_directory):
            try:
                os.startfile(self.base_directory)
            except Exception as e:
                messagebox.showerror("Erro", f"Não foi possível abrir a pasta:\n{e}")
        else:
            messagebox.showwarning("Aviso", "Selecione um diretório válido primeiro.")

    def _build_directory_frame(self):
        """Constrói o frame para seleção do diretório base."""
        frame_dir = ttk.LabelFrame(self.root, text="Diretório para Salvar Imagens e PDF")
        frame_dir.pack(fill=tk.X, padx=10, pady=5)
        
        # Campo de texto para o caminho
        self.dir_var = tk.StringVar()
        dir_entry = ttk.Entry(frame_dir, textvariable=self.dir_var, width=50)
        dir_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5, pady=5)
        
        # Botão para selecionar diretório
        btn_browse = ttk.Button(frame_dir, text="Procurar...", command=self._browse_directory)
        btn_browse.pack(side=tk.LEFT, padx=5, pady=5)

        # Botão para abrir diretório
        btn_open = ttk.Button(frame_dir, text="Abrir Pasta", command=self._open_selected_directory)
        btn_open.pack(side=tk.RIGHT, padx=5, pady=5)
    
    def _build_quick_actions_frame(self):
        """Constrói o frame para ações rápidas."""
        frame_actions = ttk.Frame(self.root)
        frame_actions.pack(fill=tk.X, padx=10, pady=5)
        
        # Botão para tirar screenshot
        btn_screenshot = ttk.Button(frame_actions, text=f"Tirar Screenshot ({SCREENSHOT_HOTKEY})", 
                                   command=self._take_screenshot)
        btn_screenshot.pack(side=tk.LEFT, padx=5, pady=5)
        
        # Botão para iniciar automação
        self.btn_start = ttk.Button(frame_actions, text=f"Iniciar Automação ({AUTOMATION_HOTKEY})", 
                                  command=self._start_automation)
        self.btn_start.pack(side=tk.LEFT, padx=5, pady=5)
        
        # Botão para parar automação
        self.btn_stop = ttk.Button(frame_actions, text="Parar", 
                                 command=self._stop_automation, state=tk.DISABLED)
        self.btn_stop.pack(side=tk.LEFT, padx=5, pady=5)
        
        # Botão para gerar PDF
        self.btn_pdf = ttk.Button(frame_actions, text="Gerar PDF", command=self._generate_pdf)
        self.btn_pdf.pack(side=tk.RIGHT, padx=5, pady=5)
        
        # Novo botão para editar sessão (adicionado antes do botão Gerar PDF)
        self.btn_edit_session = ttk.Button(frame_actions, text="Editar Sessão", command=self._edit_session)
        self.btn_edit_session.pack(side=tk.RIGHT, padx=5, pady=5)
        
        # Botão para nova sessão
        self.btn_reset_session = ttk.Button(frame_actions, text="Nova Sessão", 
                                         command=self._reset_session)
        self.btn_reset_session.pack(side=tk.RIGHT, padx=5, pady=5)
    
    def _browse_directory(self):
        """Abre diálogo para selecionar diretório base."""
        # Usar o último diretório como inicial, se disponível
        initial_dir = self.base_directory if self.base_directory else os.path.expanduser("~")
        
        directory = filedialog.askdirectory(
            title="Selecione o diretório para salvar imagens e PDF",
            initialdir=initial_dir
        )
        
        if directory:
            self.dir_var.set(directory)
            self.base_directory = directory
            self._reset_session()  # Resetar sessão ao trocar de diretório
            self._update_controls_state()
            self._save_last_directory(directory)
    
    def _reset_session(self):
        """Reseta a sessão de screenshots, criando uma nova pasta para a próxima leva."""
        if not self.base_directory or not os.path.isdir(self.base_directory):
            self.session_screenshots_dir = None
            self.screenshot_manager.set_directory(None)
            self.counter = 0
            self.last_image = None
            self.current_image = None
            self.session_name = None
            self._update_images()
            self._update_controls_state()
            self.root.title(f"PDF Maker v{APP_VERSION} Beta")
            return

        # Cria apenas UMA pasta de sessão diretamente no diretório base
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        session_dir = os.path.join(self.base_directory, f"sessao_prints_{timestamp}")
        os.makedirs(session_dir, exist_ok=True)
        self.session_screenshots_dir = session_dir
        self.screenshot_manager.set_directory(session_dir)
        self.counter = 0
        self.last_image = None
        self.current_image = None
        self._update_images()
        self._update_controls_state()
        
        # Resetar o nome da sessão
        self.session_name = None
        
        # Atualizar título da janela
        self.root.title(f"PDF Maker v{APP_VERSION} Beta")

    def _update_controls_state(self):
        """Atualiza o estado dos controles com base na seleção de diretório."""
        if self.base_directory and os.path.isdir(self.base_directory):
            state = tk.NORMAL
        else:
            state = tk.DISABLED
        
        self.btn_pdf.config(state=state)
        self.btn_start.config(state=state)
        self.btn_reset_session.config(state=state)
        self.btn_edit_session.config(state=state)  # Atualiza estado do botão de editar sessão
        
        # Também atualiza menus
        if hasattr(self, "menu_bar"):
            file_menu = self.menu_bar.winfo_children()[0]
            file_menu.entryconfig("Gerar PDF", state=state)
            file_menu.entryconfig("Nova Sessão", state=state)
            file_menu.entryconfig("Editar Sessão", state=state)  # Atualiza estado do item de menu
            
            tools_menu = self.menu_bar.winfo_children()[1]
            tools_menu.entryconfig("Tirar Screenshot", state=state)
            tools_menu.entryconfig("Iniciar Automação", state=state)
            tools_menu.entryconfig("Configurar Automação", state=state)

        if not self.base_directory:
            self.automation_status.config(text="Status: Selecione um diretório")

    def _check_updates_on_startup(self):
        """Verifica atualizações automaticamente ao iniciar."""
        def callback(has_update, latest_version, download_url):
            if has_update:
                self.update_download_url = download_url
                self.root.after(0, lambda: self._show_update_notification(latest_version))
        
        self.update_checker.check_for_updates_async(callback)
    
    def _manual_check_updates(self):
        """Verifica atualizações manualmente."""
        # Exibe mensagem de verificação no label de status
        self.automation_status.config(text="Status: Verificando atualizações...")
        
        def callback(has_update, latest_version, download_url):
            self.root.after(0, lambda: self._manual_check_complete(has_update, latest_version, download_url))
        
        self.update_checker.check_for_updates_async(callback)
    
    def _manual_check_complete(self, has_update, latest_version, download_url):
        """Callback para verificação manual."""
        # Restaura o status ao término da verificação
        self.automation_status.config(text="Status: Inativo")
        
        if has_update:
            self.update_download_url = download_url
            self._show_update_notification(latest_version)
        else:
            messagebox.showinfo("Atualizações", "Você está usando a versão mais recente!")
    
    def _show_update_notification(self, latest_version):
        """Mostra notificação de atualização disponível."""
        result = messagebox.askyesno(
            "Atualização Disponível", 
            f"Nova versão disponível: v{latest_version}\n"
            f"Versão atual: v{APP_VERSION}\n\n"
            "Deseja baixar a nova versão?"
        )
        
        if result and self.update_download_url:
            self.update_checker.open_download_page(self.update_download_url)
    
    def _build_images_frame(self):
        """Constrói o frame de exibição de imagens."""
        self.frame_images = ttk.Frame(self.root)
        self.frame_images.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.frame_images.columnconfigure(0, weight=1)
        self.frame_images.columnconfigure(1, weight=1)
        self.frame_images.rowconfigure(1, weight=1)
        
        self.label_last = ttk.Label(self.frame_images, text="Anterior")
        self.label_last.grid(row=0, column=0)
        self.label_current = ttk.Label(self.frame_images, text="Atual")
        self.label_current.grid(row=0, column=1)
        
        self.canvas_last = tk.Label(self.frame_images, background="lightgray")
        self.canvas_last.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        self.canvas_current = tk.Label(self.frame_images, background="lightgray")
        self.canvas_current.grid(row=1, column=1, sticky="nsew", padx=5, pady=5)
    
    def _open_preset_config(self):
        """Abre a janela de configuração de presets."""
        # Verificar se o diretório está configurado
        if not self.base_directory or not os.path.isdir(self.base_directory):
            messagebox.showerror("Erro", "Selecione um diretório válido antes de configurar presets.")
            return
        
        # Criar e mostrar a janela de presets (agora passando o último preset usado)
        preset_window = PresetConfigWindow(self.root, self.base_directory, 
                                         callback=self._apply_preset,
                                         initial_preset=self.last_applied_preset)
        preset_window.show()
    
    def _apply_preset(self, preset_data):
        """Aplica as configurações do preset selecionado."""
        if not preset_data:
            return

        # Armazenar o nome do preset aplicado
        self.last_applied_preset = preset_data.get('name')
        
        # Atualiza as configurações básicas
        self.interval_var.set(str(preset_data.get('interval', DEFAULT_INTERVAL)))
        self.num_captures_var.set(str(preset_data.get('num_captures', DEFAULT_NUM_CAPTURES)))
        
        # Novo: armazenar o start_delay do preset
        self.start_delay = float(preset_data.get('start_delay', 0))

        # Configura o screenshot manager com as opções de captura
        capture_type = preset_data.get('capture_type', 'fullscreen')
        
        # Redefinir as configurações de captura
        self.screenshot_manager.set_capture_area(None)
        self.screenshot_manager.set_window(None)
        
        if capture_type == 'area' and 'capture_area' in preset_data:
            self.screenshot_manager.set_capture_area(preset_data['capture_area'])
        elif capture_type == 'window' and 'selected_window' in preset_data:
            self.screenshot_manager.set_window(preset_data['selected_window'])
        
        # Configura o automation manager com ações e condições
        self.automation_manager.set_action_between_captures(
            preset_data.get('action_type'),
            preset_data.get('action_key')
        )
        
        self.automation_manager.set_stop_conditions(
            preset_data.get('stop_on_key'),
            preset_data.get('stop_key'),
            preset_data.get('stop_after_time'),
            preset_data.get('stop_time_value')
        )
        
        messagebox.showinfo("Preset", "Preset aplicado com sucesso! Pronto para iniciar automação.")
    
    def _open_hotkey_config(self):
        """Abre a janela de configuração de atalhos."""
        config_window = HotkeyConfigWindow(self.root, on_save_callback=self._on_hotkey_save)
        config_window.show()

    def _on_hotkey_save(self, config_data):
        """Callback chamado quando os atalhos são salvos."""
        # Atualiza os rótulos dos botões e menus (mesmo que os atalhos só funcionem após reiniciar)
        tools_menu = self.menu_bar.winfo_children()[1]
        tools_menu.entryconfig("Tirar Screenshot", 
                             accelerator=f"({config_data['screenshot_hotkey']})")
        tools_menu.entryconfig("Iniciar Automação", 
                             accelerator=f"({config_data['automation_hotkey']})")
        
        # Atualiza texto dos botões na interface
        for widget in self.root.winfo_children():
            if isinstance(widget, ttk.Frame):
                for child in widget.winfo_children():
                    if isinstance(child, ttk.Button):
                        if "Tirar Screenshot" in child['text']:
                            child['text'] = f"Tirar Screenshot ({config_data['screenshot_hotkey']})"
                        elif "Iniciar Automação" in child['text']:
                            child['text'] = f"Iniciar Automação ({config_data['automation_hotkey']})"

    def _start_hotkey_listener(self):
        """Inicia o listener de atalhos de teclado."""
        # Carrega as configurações atuais (que podem ter sido carregadas no config.py)
        screenshot_hotkey = SCREENSHOT_HOTKEY
        automation_hotkey = AUTOMATION_HOTKEY
        
        def listen_hotkeys():
            keyboard.add_hotkey(screenshot_hotkey, self._take_screenshot)
            keyboard.add_hotkey(automation_hotkey, self._start_automation_hotkey)
            keyboard.wait()
        
        threading.Thread(target=listen_hotkeys, daemon=True).start()
    
    def _take_screenshot(self):
        """Captura uma screenshot."""
        # Verificar se o diretório está configurado
        if not self.base_directory or not os.path.isdir(self.base_directory):
            messagebox.showerror("Erro", "Selecione um diretório válido antes de capturar screenshots.")
            return
        
        # Garante que o diretório da sessão está definido
        if not self.session_screenshots_dir:
            self._reset_session()
        # Garante que o ScreenshotManager está usando a pasta correta
        if self.screenshot_manager.get_images_dir() != self.session_screenshots_dir:
            self.screenshot_manager.set_directory(self.session_screenshots_dir)
        img_path = self.screenshot_manager.take_screenshot()
        if img_path:
            self.counter += 1
            self.last_image = self.current_image
            self.current_image = img_path
            self.root.after(100, self._update_images)
        else:
            print("Falha ao capturar screenshot")
    
    def _start_automation_hotkey(self):
        """Inicia automação via atalho se disponível."""
        if not self.automation_manager.is_running and self.btn_start['state'] != tk.DISABLED:
            self.root.after(0, self._start_automation)
    
    def _start_automation(self):
        """Inicia o processo de automação."""
        # Verificar se o diretório está configurado
        if not self.base_directory or not os.path.isdir(self.base_directory):
            messagebox.showerror("Erro", "Selecione um diretório válido antes de iniciar a automação.")
            return
        
        try:
            interval = float(self.interval_var.get())
            num_captures = int(self.num_captures_var.get())
            # Usar start_delay se definido, senão 0
            start_delay = getattr(self, 'start_delay', 0)
            if hasattr(self, 'start_delay'):
                del self.start_delay  # Limpar para não afetar próximas execuções

            if interval <= 0 or num_captures <= 0:
                messagebox.showerror("Erro", "Valores devem ser positivos.")
                return
            
            self._set_automation_controls_state(False)

            # Se houver start_delay, aguardar antes de iniciar
            if start_delay > 0:
                self.automation_status.config(text=f"Aguardando {start_delay:.0f} segundos para iniciar...")
                self.root.update()
                self.root.after(int(start_delay * 1000), lambda: self._do_start_automation(interval, num_captures))
            else:
                self._do_start_automation(interval, num_captures)

        except ValueError:
            messagebox.showerror("Erro", "Valores numéricos inválidos.")

    def _do_start_automation(self, interval, num_captures):
        """Inicia a automação após o delay (ou imediatamente)."""
        if not self.automation_manager.start(interval, num_captures):
            messagebox.showerror("Erro", "Falha ao iniciar automação.")
            self._set_automation_controls_state(True)
    
    def _stop_automation(self):
        """Para a automação."""
        self.automation_manager.stop()
    
    def _set_automation_controls_state(self, enabled: bool):
        """Define o estado dos controles de automação."""
        state = tk.NORMAL if enabled else tk.DISABLED
        self.btn_start.config(state=state)
        self.btn_stop.config(state=tk.DISABLED if enabled else tk.NORMAL)
    
    def _on_automation_screenshot(self, img_path: str):
        """Callback chamado quando uma screenshot é capturada na automação."""
        self.counter += 1
        self.last_image = self.current_image
        self.current_image = img_path
        self.root.after(0, self._update_images)
    
    def _on_automation_status(self, status: str):
        """Callback para atualização de status da automação."""
        self.automation_status.config(text=status)
    
    def _on_automation_finish(self):
        """Callback chamado quando a automação termina."""
        self._set_automation_controls_state(True)
        self.automation_status.config(text="Status: Concluído")
        messagebox.showinfo("Automação", "Concluída com sucesso!")
    
    def _initial_resize(self):
        """Redimensionamento inicial."""
        self._on_resize(None)
        self._update_images()
    
    def _on_resize(self, event):
        """Manipula redimensionamento da janela com debounce."""
        if hasattr(self, '_resize_after_id') and self._resize_after_id:
            self.root.after_cancel(self._resize_after_id)
        self._resize_after_id = self.root.after(200, self._do_resize)

    def _do_resize(self):
        """Executa o redimensionamento real das imagens."""
        frame_width = self.frame_images.winfo_width()
        frame_height = self.frame_images.winfo_height()
        if frame_width > 100 and frame_height > 100:
            img_width = max(200, (frame_width // 2) - 20)
            img_height = max(150, frame_height - 40)
            self.img_display_size = (img_width, img_height)
            self._update_images()
        self._resize_after_id = None

    def _setup_resize_handling(self):
        """Configura o tratamento de redimensionamento."""
        self.root.bind("<Configure>", self._on_resize)
        self.frame_images.bind("<Configure>", self._on_resize)
        self.root.after(100, self._initial_resize)
    
    def _update_images(self):
        """Atualiza as imagens exibidas."""
        # Corrigir: contar o número real de imagens na pasta da sessão
        paths = self.screenshot_manager.get_image_paths()
        self.counter = len(paths)
        self.label_counter.config(text=f"Prints tirados: {self.counter}")

        for canvas, img_path in [(self.canvas_last, self.last_image),
                                 (self.canvas_current, self.current_image)]:
            self._update_canvas_image(canvas, img_path)
    
    def _update_canvas_image(self, canvas, img_path):
        """Atualiza uma imagem específica no canvas mantendo proporção."""
        if img_path and os.path.exists(img_path):
            try:
                with open(img_path, 'rb') as f:
                    img = Image.open(f)
                    img.load()
                    # Mantém proporção usando thumbnail
                    img_copy = img.copy()
                    img_copy.thumbnail(self.img_display_size, Image.Resampling.LANCZOS)
                    img_tk = ImageTk.PhotoImage(img_copy)
                    canvas.img = img_tk
                    canvas.config(image=img_tk, text="")
            except Exception as e:
                print(f"Erro ao carregar imagem: {e}")
                canvas.config(image='', text=f"Erro: {str(e)[:20]}...")
        else:
            canvas.config(image='', text="(vazio)")
            
    def _generate_pdf(self):
        """Gera o PDF com as imagens capturadas no diretório selecionado."""
        # Verificar se temos o diretório base configurado
        if not self.base_directory or not os.path.isdir(self.base_directory):
            messagebox.showerror("Erro", "Selecione um diretório válido antes de gerar o PDF.")
            return
        
        # Obter caminhos das imagens e diretório onde estão armazenadas
        paths = self.screenshot_manager.get_image_paths()
        if not paths:
            messagebox.showwarning("PDF", "Nenhuma imagem para gerar PDF.")
            return
        
        # Usar o diretório da sessão para salvar o PDF
        screenshots_dir = self.session_screenshots_dir or self.screenshot_manager.get_images_dir()
        
        # Definir caminho para o PDF com timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        pdf_path = os.path.join(screenshots_dir, f"PDF Maker_{timestamp}.pdf")
        
        # Gerar o PDF
        if self.pdf_generator.generate_pdf(paths, pdf_path):
            messagebox.showinfo("PDF", f"PDF gerado: {pdf_path}")
        else:
            messagebox.showerror("Erro", "Falha ao gerar PDF.")
    
    def _edit_session(self):
        """Abre o editor de sessão para organizar e editar as imagens capturadas."""
        # Verificar se temos o diretório base configurado
        if not self.base_directory or not os.path.isdir(self.base_directory):
            messagebox.showerror("Erro", "Selecione um diretório válido antes de editar a sessão.")
            return
        
        # Obter os caminhos das imagens da sessão atual
        paths = self.screenshot_manager.get_image_paths()
        if not paths:
            messagebox.showwarning("Editar Sessão", "Nenhuma imagem encontrada para editar.")
            return
        
        # Usar o diretório da sessão atual
        screenshots_dir = self.session_screenshots_dir or self.screenshot_manager.get_images_dir()
        
        # Abrir a janela do editor de sessão com configuração modal
        editor = SessionEditorWindow(self.root, paths, screenshots_dir)
        
        # Mostrar a janela do editor - ela já implementa comportamento modal
        result = editor.show()
        
        # Se o usuário concluiu a edição e solicitou gerar o PDF
        if result.get('generate_pdf', False):
            # Usar os caminhos reordenados/editados para gerar o PDF
            self._generate_pdf_with_edited_paths(result.get('image_paths', []))
    
    def _generate_pdf_with_edited_paths(self, paths):
        """Gera o PDF usando os caminhos editados/reordenados."""
        if not paths:
            messagebox.showwarning("PDF", "Nenhuma imagem para gerar PDF.")
            return
        
        # Usar o diretório da sessão para salvar o PDF
        screenshots_dir = self.session_screenshots_dir or self.screenshot_manager.get_images_dir()
        
        # Definir caminho para o PDF com timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        pdf_path = os.path.join(screenshots_dir, f"PDF Maker_{timestamp}.pdf")
        
        # Gerar o PDF com os caminhos reordenados e possíveis anotações
        if self.pdf_generator.generate_pdf(paths, pdf_path):
            messagebox.showinfo("PDF", f"PDF gerado: {pdf_path}")
        else:
            messagebox.showerror("Erro", "Falha ao gerar PDF.")
    
    def _open_sessions_menu(self):
        """Abre o menu de sessões salvas."""
        # Atualizar o menu de sessões salvas
        self._update_sessions_menu()
        
        # Exibir o menu
        try:
            x = self.root.winfo_x()
            y = self.root.winfo_y() + self.root.winfo_height()
            
            self.saved_sessions_menu.post(x, y)
        except Exception as e:
            print(f"Erro ao exibir menu de sessões: {e}")

    def _try_load_last_session(self):
        """Tenta carregar a última sessão usada."""
        try:
            sessions_dir = self._get_sessions_directory()
            last_session_file = os.path.join(sessions_dir, "last_session.json")
            
            if os.path.exists(last_session_file):
                with open(last_session_file, 'r') as f:
                    session_data = json.load(f)
                    
                # Verificar se o diretório ainda existe
                if os.path.isdir(session_data.get('directory', '')):
                    # Restaurar a sessão
                    self._load_session_data(session_data)
                    
                    # Atualizar o título da janela
                    session_name = session_data.get('name', 'Sessão sem nome')
                    self.root.title(f"PDF Maker v{APP_VERSION} Beta - {session_name}")
                    
                    # Atualizar o diretório base se necessário
                    directory = session_data.get('directory', '')
                    parent_dir = os.path.dirname(directory)
                    if parent_dir and os.path.isdir(parent_dir):
                        self.base_directory = parent_dir
                        self.dir_var.set(parent_dir)
                        
                    return True
        except Exception as e:
            print(f"Erro ao carregar última sessão: {e}")
        
        return False

    def _save_current_session(self):
        """Salva a sessão atual."""
        if not self.session_screenshots_dir or not os.path.isdir(self.session_screenshots_dir):
            messagebox.showwarning("Aviso", "Não há uma sessão ativa para salvar.")
            return
            
        # Obter nome padrão da sessão (baseado no nome da pasta)
        current_name = self.session_name or os.path.basename(self.session_screenshots_dir)
        
        # Usar nosso diálogo personalizado em vez do simpledialog
        dialog = CustomStringDialog(
            self.root,
            "Salvar Sessão",
            "Nome da sessão:",
            initialvalue=current_name
        )
        new_name = dialog.result
        
        if not new_name:
            return  # Usuário cancelou
            
        try:
            # Salvar a sessão com o novo nome
            self._save_session_to_file(new_name)
            
            # Atualizar o nome da sessão atual
            self.session_name = new_name
            
            # Atualizar o título da janela
            self.root.title(f"PDF Maker v{APP_VERSION} Beta - {new_name}")
            
            # Atualizar o menu de sessões
            self._update_sessions_menu()
            
            messagebox.showinfo("Sucesso", f"Sessão '{new_name}' salva com sucesso!")
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao salvar sessão: {str(e)}")

    def _save_session_to_file(self, session_name):
        """Salva os dados da sessão em um arquivo."""
        # Obter metadados da sessão
        session_data = {
            'name': session_name,
            'directory': self.session_screenshots_dir,
            'images': self.screenshot_manager.get_image_paths(),
            'saved_date': datetime.now().isoformat(),
            'image_count': self.counter
        }
        
        # Obter diretório de sessões salvas
        sessions_dir = self._get_sessions_directory()
        
        # Salvar em arquivo JSON
        filename = os.path.join(sessions_dir, f"{session_name}.json")
        with open(filename, 'w') as f:
            json.dump(session_data, f, indent=4)
            
        # Também salvar como "last_session.json" para facilitar o carregamento automático
        last_session_file = os.path.join(sessions_dir, "last_session.json")
        with open(last_session_file, 'w') as f:
            json.dump(session_data, f, indent=4)

    def _get_sessions_directory(self):
        """Retorna o diretório onde são armazenadas as sessões salvas."""
        app_name = "PDF Maker"
        
        # Diretório principal da aplicação
        if platform.system() == "Windows":
            app_data = os.path.join(os.environ.get('APPDATA', os.path.expanduser("~")), app_name)
        else:
            app_data = os.path.join(os.path.expanduser("~"), f".{app_name.lower()}")
        
        # Diretório específico para sessões
        sessions_dir = os.path.join(app_data, "sessions")
        
        # Garantir que o diretório existe
        os.makedirs(sessions_dir, exist_ok=True)
        
        return sessions_dir

    def _update_sessions_menu(self):
        """Atualiza o menu de sessões salvas."""
        # Limpar menu existente
        if hasattr(self, 'sessions_menu'):
            self.sessions_menu.delete(0, tk.END)
        else:
            return
        
        try:
            sessions_dir = self._get_sessions_directory()
            
            if not os.path.exists(sessions_dir):
                self.sessions_menu.add_command(label="Nenhuma sessão salva", state=tk.DISABLED)
                return
            
            # Coletar sessões
            sessions = []
            for filename in os.listdir(sessions_dir):
                if filename.endswith(".json") and filename != "last_session.json":
                    try:
                        with open(os.path.join(sessions_dir, filename), 'r') as f:
                            session_data = json.load(f)
                        
                        # Verificar se o diretório ainda existe
                        if os.path.isdir(session_data.get('directory', '')):
                            sessions.append(session_data)
                    except:
                        continue
        
            # Ordenar por data (mais recente primeiro)
            sessions.sort(key=lambda x: x.get('saved_date', ''), reverse=True)
            
            # Adicionar ao menu
            if not sessions:
                self.sessions_menu.add_command(label="Nenhuma sessão salva", state=tk.DISABLED)
            else:
                for session in sessions:
                    name = session.get('name', 'Sem nome')
                    date_str = self._format_date(session.get('saved_date', ''))
                    
                    # Criar uma função de callback com closure para este item específico
                    callback = lambda s=session: self._load_session_data(s)
                    
                    # Adicionar ao menu (mostrar nome e data)
                    self.sessions_menu.add_command(
                        label=f"{name} ({date_str})",
                        command=callback
                    )
        except Exception as e:
            print(f"Erro ao atualizar menu de sessões: {str(e)}")
            if hasattr(self, 'sessions_menu'):
                self.sessions_menu.add_command(label="Erro ao carregar sessões", state=tk.DISABLED)

    def _format_date(self, date_string):
        """Formata a string de data para exibição amigável."""
        if not date_string:
            return "-"
            
        try:
            # Converter ISO format para objeto datetime
            dt = datetime.fromisoformat(date_string)
            # Formatar para exibição
            return dt.strftime("%d/%m/%Y %H:%M")
        except:
            return date_string

    def _load_session_data(self, session_data):
        """Carrega uma sessão a partir dos dados."""
        if not session_data:
            return False
            
        directory = session_data.get('directory')
        if not directory or not os.path.isdir(directory):
            messagebox.showerror("Erro", f"Diretório da sessão não encontrado: {directory}")
            return False
            
        try:
            # Configurar o gerenciador de screenshots para usar o diretório da sessão
            self.session_screenshots_dir = directory
            self.session_name = session_data.get('name')
            self.screenshot_manager.set_directory(directory)
            
            # Carregar contagem de imagens
            self.counter = session_data.get('image_count', 0)
            
            # Atualizar referências de imagens
            paths = self.screenshot_manager.get_image_paths()
            if paths:
                self.current_image = paths[-1]  # Última imagem
                self.last_image = paths[-2] if len(paths) > 1 else None
                
            # Atualizar interface
            self._update_images()
            self._update_controls_state()
            
            # Atualizar título da janela
            if self.session_name:
                self.root.title(f"PDF Maker v{APP_VERSION} Beta - {self.session_name}")
            
            # Verificar se é preciso atualizar diretório base
            if self.base_directory != os.path.dirname(directory):
                self.base_directory = os.path.dirname(directory)
                self.dir_var.set(self.base_directory)
            
            return True
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao carregar sessão: {str(e)}")
            return False

    def _rename_current_session(self):
        """Renomeia a sessão atual."""
        if not self.session_screenshots_dir or not os.path.isdir(self.session_screenshots_dir):
            messagebox.showwarning("Aviso", "Não há uma sessão ativa para renomear.")
            return
            
        # Obter nome atual da sessão
        current_name = self.session_name or os.path.basename(self.session_screenshots_dir)
        
        # Usar nosso diálogo personalizado em vez do simpledialog
        dialog = CustomStringDialog(
            self.root,
            "Renomear Sessão",
            "Novo nome para a sessão:",
            initialvalue=current_name
        )
        new_name = dialog.result
        
        if not new_name or new_name == current_name:
            return  # Usuário cancelou ou não alterou
            
        try:
            # Salvar a sessão com o novo nome
            self._save_session_to_file(new_name)
            
            # Atualizar o nome da sessão atual
            self.session_name = new_name
            
            # Atualizar o título da janela
            self.root.title(f"PDF Maker v{APP_VERSION} Beta - {new_name}")
            
            # Atualizar o menu de sessões
            self._update_sessions_menu()
            
            messagebox.showinfo("Sucesso", f"Sessão renomeada para '{new_name}'.")
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao renomear sessão: {str(e)}")
    
    def _on_exit(self):
        """Manipula o evento de saída do programa."""
        # Verificar se a janela ainda existe antes de prosseguir
        if not self.root.winfo_exists():
            return
            
        # Exibir mensagem com detalhes mais explícitos
        print("Método _on_exit chamado, exibindo diálogo de confirmação...")
        
        # Pedir confirmação ao usuário antes de sair
        confirm = messagebox.askyesno(
            "Confirmar Saída", 
            "Deseja realmente sair do PDF Maker?\n\n"
            "Pastas vazias serão automaticamente removidas para evitar acúmulo de arquivos desnecessários.",
            icon="question"
        )
        
        if not confirm:
            print("Usuário cancelou a saída")
            return  # Usuário cancelou, não sai do programa
        
        print("Usuário confirmou a saída, limpando sessões vazias...")
        
        # Verificar se a sessão atual está vazia
        if self.session_screenshots_dir and os.path.exists(self.session_screenshots_dir):
            # Verificar se tem arquivos reais (não ocultos/temporários)
            files = [f for f in os.listdir(self.session_screenshots_dir) 
                     if not f.startswith('.') and os.path.isfile(os.path.join(self.session_screenshots_dir, f)) and
                     any(f.lower().endswith(ext) for ext in ['.png', '.jpg', '.jpeg', '.gif', '.bmp', '.pdf'])]
            
            if not files:
                # Sessão vazia: deletar a pasta
                print(f"Sessão atual vazia, removendo: {self.session_screenshots_dir}")
                try:
                    shutil.rmtree(self.session_screenshots_dir)
                    print(f"Sessão vazia removida: {self.session_screenshots_dir}")
                except Exception as e:
                    print(f"Erro ao tentar remover sessão vazia: {e}")
            else:
                # Sessão não está vazia: salvar normalmente
                try:
                    # Usar o nome da pasta como nome da sessão se não tiver um nome personalizado
                    session_name = self.session_name or os.path.basename(self.session_screenshots_dir)
                    self._save_session_to_file(session_name)
                except Exception as e:
                    print(f"Erro ao salvar sessão automaticamente: {e}")
        
        # Limpar outras pastas vazias (sem usar o método que está ausente)
        try:
            self._remove_empty_session_folders()
        except Exception as e:
            print(f"Erro ao limpar pastas vazias: {e}")
        
        # Finalizar a aplicação
        try:
            if self.root.winfo_exists():
                self.root.destroy()  # Usar destroy() em vez de quit() para encerrar completamente
        except Exception as e:
            print(f"Erro ao destruir janela: {e}")
            # Se não conseguir destruir a janela, tentar encerrar de outra forma
            self.root.quit()
    
    def _remove_empty_session_folders(self):
        """Remove pastas de sessão vazias no diretório base."""
        if not self.base_directory or not os.path.isdir(self.base_directory):
            return
            
        print(f"Procurando sessões vazias em: {self.base_directory}")
        try:
            # Procurar diretórios que parecem ser sessões
            for item in os.listdir(self.base_directory):
                session_path = os.path.join(self.base_directory, item)
                
                # Verificar se é uma pasta de sessão
                if os.path.isdir(session_path) and item.startswith("sessao_prints_"):
                    # Pular a sessão atual que está em uso
                    if session_path == self.session_screenshots_dir:
                        continue
                        
                    # Verificar se contém arquivos reais (excluindo arquivos temporários/ocultos)
                    has_content = False
                    if os.path.exists(session_path):
                        files = [f for f in os.listdir(session_path) 
                                if not f.startswith('.') and 
                                os.path.isfile(os.path.join(session_path, f)) and
                                any(f.lower().endswith(ext) for ext in ['.png', '.jpg', '.jpeg', '.gif', '.bmp', '.pdf'])]
                        has_content = len(files) > 0
                    
                    # Se não tiver conteúdo, deletar
                    if not has_content:
                        print(f"Removendo sessão vazia: {session_path}")
                        try:
                            shutil.rmtree(session_path)
                            print(f"Sessão vazia removida: {session_path}")
                        except Exception as e:
                            print(f"Erro ao remover sessão vazia {session_path}: {e}")
        except Exception as e:
            print(f"Erro durante limpeza de sessões vazias: {e}")

    # Remova ou comente esta função se estiver duplicada ou não for usada
    def _cleanup_all_screenshot_folders(self):
        """Procura e remove todas as pastas de screenshots vazias em todos os diretórios conhecidos."""
        # Listar todos os diretórios que podem conter pastas de screenshots
        directories_to_check = []
        
        # Adicionar o diretório base atual
        if self.base_directory and os.path.isdir(self.base_directory):
            directories_to_check.append(self.base_directory)
            
        # Adicionar outros diretórios de sessões antigas (carregando dos arquivos de sessão)
        try:
            sessions_dir = self._get_sessions_directory()
            if os.path.exists(sessions_dir):
                for filename in os.listdir(sessions_dir):
                    if filename.endswith(".json") and filename != "last_session.json":
                        try:
                            with open(os.path.join(sessions_dir, filename), 'r') as f:
                                session_data = json.load(f)
                                
                            directory = session_data.get('directory', '')
                            if directory and os.path.isdir(directory):
                                parent_dir = os.path.dirname(directory)
                                if parent_dir and os.path.isdir(parent_dir) and parent_dir not in directories_to_check:
                                    directories_to_check.append(parent_dir)
                        except:
                            continue
        except Exception as e:
            print(f"Erro ao procurar diretórios de sessões antigas: {e}")
        
        # Para cada diretório encontrado, limpar pastas vazias
        for directory in directories_to_check:
            try:
                print(f"Verificando pastas em: {directory}")
                for item in os.listdir(directory):
                    if item.startswith("sessao_prints_"):
                        folder_path = os.path.join(directory, item)
                        if os.path.isdir(folder_path):
                            # Verificar se a pasta está vazia ou contém apenas arquivos temporários/ocultos
                            files = [f for f in os.listdir(folder_path) 
                                     if not f.startswith('.') and 
                                     os.path.isfile(os.path.join(folder_path, f)) and
                                     any(f.lower().endswith(ext) for ext in ['.png', '.jpg', '.jpeg', '.gif', '.bmp', '.pdf'])]
                            
                            if not files:
                                print(f"Removendo pasta vazia: {folder_path}")
                                try:
                                    shutil.rmtree(folder_path)
                                    print(f"Pasta vazia removida: {folder_path}")
                                except Exception as e:
                                    print(f"Erro ao remover pasta vazia: {e}")
            except Exception as e:
                print(f"Erro ao verificar pastas em {directory}: {e}")