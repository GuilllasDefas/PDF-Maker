import os
import threading
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk, ImageFile
import keyboard
from src.config.config import (
    DEFAULT_WINDOW_SIZE, DEFAULT_IMAGE_DISPLAY_SIZE, 
    DEFAULT_INTERVAL, DEFAULT_NUM_CAPTURES,
    SCREENSHOT_HOTKEY, AUTOMATION_HOTKEY, PDF_OUTPUT
)
from src.core.screenshot import ScreenshotManager
from src.core.pdf_generator import PDFGenerator
from src.core.automation import AutomationManager

# Permite carregar imagens truncadas
ImageFile.LOAD_TRUNCATED_IMAGES = True

class PDFMakerApp:
    def __init__(self, root):
        self.root = root
        self.root.geometry(DEFAULT_WINDOW_SIZE)
        self.root.title("PDF Maker - Screenshot Tool")
        
        # Managers
        self.screenshot_manager = ScreenshotManager()
        self.pdf_generator = PDFGenerator()
        self.automation_manager = AutomationManager(self.screenshot_manager)
        
        # Estado da aplicação
        self.counter = 0
        self.last_image = None
        self.current_image = None
        self.img_display_size = DEFAULT_IMAGE_DISPLAY_SIZE
        
        # Configurar callbacks da automação
        self._setup_automation_callbacks()
        
        # Construir interface
        self._build_ui()
        
        # Iniciar listener de atalhos
        self._start_hotkey_listener()
        
        # Configurar redimensionamento
        self._setup_resize_handling()
    
    def _setup_automation_callbacks(self):
        """Configura os callbacks da automação."""
        self.automation_manager.set_callbacks(
            on_screenshot=self._on_automation_screenshot,
            on_status=self._on_automation_status,
            on_finish=self._on_automation_finish
        )
    
    def _build_ui(self):
        """Constrói a interface do usuário."""
        # Counter label
        self.label_counter = ttk.Label(self.root, text="Prints tirados: 0")
        self.label_counter.pack(pady=5)
        
        # Frame de imagens
        self._build_images_frame()
        
        # Frame de automação
        self._build_automation_frame()
        
        # Botão PDF
        self.btn_pdf = ttk.Button(self.root, text="Gerar PDF", command=self._generate_pdf)
        self.btn_pdf.pack(pady=10)
    
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
    
    def _build_automation_frame(self):
        """Constrói o frame de automação."""
        self.frame_automation = ttk.LabelFrame(self.root, text="Automação de Capturas")
        self.frame_automation.pack(fill=tk.X, padx=10, pady=5)
        
        # Configurações
        frame_config = ttk.Frame(self.frame_automation)
        frame_config.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(frame_config, text="Intervalo (segundos):").grid(row=0, column=0, padx=5)
        self.interval_var = tk.StringVar(value=str(DEFAULT_INTERVAL))
        self.interval_entry = ttk.Entry(frame_config, width=5, textvariable=self.interval_var)
        self.interval_entry.grid(row=0, column=1, padx=5)
        
        ttk.Label(frame_config, text="Número de capturas:").grid(row=0, column=2, padx=5)
        self.num_captures_var = tk.StringVar(value=str(DEFAULT_NUM_CAPTURES))
        self.num_captures_entry = ttk.Entry(frame_config, width=5, textvariable=self.num_captures_var)
        self.num_captures_entry.grid(row=0, column=3, padx=5)
        
        # Botões
        frame_buttons = ttk.Frame(self.frame_automation)
        frame_buttons.pack(fill=tk.X, padx=5, pady=5)
        
        self.btn_start = ttk.Button(frame_buttons, text="Iniciar Automação", command=self._start_automation)
        self.btn_start.pack(side=tk.LEFT, padx=5)
        
        self.btn_stop = ttk.Button(frame_buttons, text="Parar", command=self._stop_automation, state=tk.DISABLED)
        self.btn_stop.pack(side=tk.LEFT, padx=5)
        
        ttk.Label(frame_buttons, text=f"Atalhos: {SCREENSHOT_HOTKEY}, {AUTOMATION_HOTKEY}").pack(side=tk.LEFT, padx=5)
        
        self.automation_status = ttk.Label(frame_buttons, text="Status: Inativo")
        self.automation_status.pack(side=tk.RIGHT, padx=5)
    
    def _setup_resize_handling(self):
        """Configura o tratamento de redimensionamento."""
        self.root.bind("<Configure>", self._on_resize)
        self.frame_images.bind("<Configure>", self._on_resize)
        self.root.after(100, self._initial_resize)
    
    def _start_hotkey_listener(self):
        """Inicia o listener de atalhos de teclado."""
        def listen_hotkeys():
            keyboard.add_hotkey(SCREENSHOT_HOTKEY, self._take_screenshot)
            keyboard.add_hotkey(AUTOMATION_HOTKEY, self._start_automation_hotkey)
            keyboard.wait()
        
        threading.Thread(target=listen_hotkeys, daemon=True).start()
    
    def _take_screenshot(self):
        """Captura uma screenshot."""
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
        try:
            interval = float(self.interval_var.get())
            num_captures = int(self.num_captures_var.get())
            
            if interval <= 0 or num_captures <= 0:
                messagebox.showerror("Erro", "Valores devem ser positivos.")
                return
            
            # Desabilitar controles
            self._set_automation_controls_state(False)
            
            # Iniciar automação
            if not self.automation_manager.start(interval, num_captures):
                messagebox.showerror("Erro", "Falha ao iniciar automação.")
                self._set_automation_controls_state(True)
            
        except ValueError:
            messagebox.showerror("Erro", "Valores numéricos inválidos.")
    
    def _stop_automation(self):
        """Para a automação."""
        self.automation_manager.stop()
    
    def _set_automation_controls_state(self, enabled: bool):
        """Define o estado dos controles de automação."""
        state = tk.NORMAL if enabled else tk.DISABLED
        self.interval_entry.config(state=state)
        self.num_captures_entry.config(state=state)
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
    
    def _initial_resize(self):
        """Redimensionamento inicial."""
        self._on_resize(None)
        self._update_images()
    
    def _on_resize(self, event):
        """Manipula redimensionamento da janela."""
        frame_width = self.frame_images.winfo_width()
        frame_height = self.frame_images.winfo_height()
        
        if frame_width > 100 and frame_height > 100:
            img_width = max(200, (frame_width // 2) - 20)
            img_height = max(150, frame_height - 40)
            self.img_display_size = (img_width, img_height)
            self._update_images()
    
    def _update_images(self):
        """Atualiza as imagens exibidas."""
        self.label_counter.config(text=f"Prints tirados: {self.counter}")
        
        for canvas, img_path in [(self.canvas_last, self.last_image), 
                                (self.canvas_current, self.current_image)]:
            self._update_canvas_image(canvas, img_path)
    
    def _update_canvas_image(self, canvas, img_path):
        """Atualiza uma imagem específica no canvas."""
        if img_path and os.path.exists(img_path):
            try:
                with open(img_path, 'rb') as f:
                    img = Image.open(f)
                    img.load()
                    img = img.resize(self.img_display_size, Image.Resampling.LANCZOS)
                    img_tk = ImageTk.PhotoImage(img)
                    canvas.img = img_tk
                    canvas.config(image=img_tk, text="")
            except Exception as e:
                print(f"Erro ao carregar imagem: {e}")
                canvas.config(image='', text=f"Erro: {str(e)[:20]}...")
        else:
            canvas.config(image='', text="(vazio)")
    
    def _generate_pdf(self):
        """Gera o PDF com as imagens capturadas."""
        paths = self.screenshot_manager.get_image_paths()
        if paths:
            if self.pdf_generator.generate_pdf(paths, PDF_OUTPUT):
                messagebox.showinfo("PDF", f"PDF gerado: {PDF_OUTPUT}")
            else:
                messagebox.showerror("Erro", "Falha ao gerar PDF.")
        else:
            messagebox.showwarning("PDF", "Nenhuma imagem para gerar PDF.")
