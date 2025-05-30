import os
import threading
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import pyautogui
import keyboard
import time
from utils import save_screenshot, get_image_paths, generate_pdf
from PIL import ImageFile

# Permite carregar imagens truncadas
ImageFile.LOAD_TRUNCATED_IMAGES = True

IMAGES_DIR = "images"
PDF_OUTPUT = "output.pdf"

class PDFMakerApp:
    def __init__(self, root):
        self.root = root
        self.root.geometry("800x500")
        self.root.title("PDF Maker - Screenshot Tool")
        self.counter = 0
        self.last_image = None
        self.current_image = None
        self.img_display_size = (350, 250)  # Tamanho inicial maior

        os.makedirs(IMAGES_DIR, exist_ok=True)

        # UI
        self.label_counter = ttk.Label(root, text="Prints tirados: 0")
        self.label_counter.pack(pady=5)

        # Configure o frame para preencher o espaço disponível
        self.frame_images = ttk.Frame(root)
        self.frame_images.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Configure as colunas para terem o mesmo peso
        self.frame_images.columnconfigure(0, weight=1)
        self.frame_images.columnconfigure(1, weight=1)
        # Configure a linha para expandir
        self.frame_images.rowconfigure(1, weight=1)

        self.label_last = ttk.Label(self.frame_images, text="Anterior")
        self.label_last.grid(row=0, column=0)
        self.label_current = ttk.Label(self.frame_images, text="Atual")
        self.label_current.grid(row=0, column=1)

        self.canvas_last = tk.Label(self.frame_images, background="lightgray")
        self.canvas_last.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        self.canvas_current = tk.Label(self.frame_images, background="lightgray")
        self.canvas_current.grid(row=1, column=1, sticky="nsew", padx=5, pady=5)

        # Adiciona controles para automação
        self.frame_automation = ttk.LabelFrame(root, text="Automação de Capturas")
        self.frame_automation.pack(fill=tk.X, padx=10, pady=5)
        
        # Linha 1: Intervalo e número de capturas
        frame_config = ttk.Frame(self.frame_automation)
        frame_config.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(frame_config, text="Intervalo (segundos):").grid(row=0, column=0, padx=5)
        self.interval_var = tk.StringVar(value="2")
        self.interval_entry = ttk.Entry(frame_config, width=5, textvariable=self.interval_var)
        self.interval_entry.grid(row=0, column=1, padx=5)
        
        ttk.Label(frame_config, text="Número de capturas:").grid(row=0, column=2, padx=5)
        self.num_captures_var = tk.StringVar(value="10")
        self.num_captures_entry = ttk.Entry(frame_config, width=5, textvariable=self.num_captures_var)
        self.num_captures_entry.grid(row=0, column=3, padx=5)
        
        # Linha 2: Botões de controle
        frame_buttons = ttk.Frame(self.frame_automation)
        frame_buttons.pack(fill=tk.X, padx=5, pady=5)
        
        self.btn_start = ttk.Button(frame_buttons, text="Iniciar Automação", command=self.start_automation)
        self.btn_start.pack(side=tk.LEFT, padx=5)
        
        self.btn_stop = ttk.Button(frame_buttons, text="Parar", command=self.stop_automation, state=tk.DISABLED)
        self.btn_stop.pack(side=tk.LEFT, padx=5)
        
        # Informação sobre o atalho (atualizada)
        ttk.Label(frame_buttons, text="Atalho: Ctrl+Alt+R").pack(side=tk.LEFT, padx=5)
        
        # Status da automação
        self.automation_status = ttk.Label(frame_buttons, text="Status: Inativo")
        self.automation_status.pack(side=tk.RIGHT, padx=5)
        
        # Flag para controlar a automação
        self.automation_running = False
        self.automation_thread = None

        self.btn_pdf = ttk.Button(root, text="Gerar PDF", command=self.on_generate_pdf)
        self.btn_pdf.pack(pady=10)

        # Atalho global
        threading.Thread(target=self.listen_hotkey, daemon=True).start()
        
        # Vincule o evento de redimensionamento não apenas à janela, mas também ao frame
        self.root.bind("<Configure>", self.on_resize)
        self.frame_images.bind("<Configure>", self.on_resize)
        
        # Atualize as imagens após a GUI ser renderizada completamente
        self.root.after(100, self.initial_resize)
        
    def initial_resize(self):
        # Força o redimensionamento inicial
        self.on_resize(None)
        self.update_images()

    def listen_hotkey(self):
        keyboard.add_hotkey('ctrl+shift+s', self.take_screenshot)
        keyboard.add_hotkey('ctrl+alt+r', self.start_automation_hotkey)  # Novo atalho
        keyboard.wait()  # Mantém thread ativa
    
    def start_automation_hotkey(self):
        """Inicia a automação via atalho de teclado, se não estiver já em execução"""
        if not self.automation_running and self.btn_start['state'] != tk.DISABLED:
            self.root.after(0, self.start_automation)

    def take_screenshot(self):
        img_path = save_screenshot(IMAGES_DIR)
        if img_path:  # Verificar se o screenshot foi salvo com sucesso
            self.counter += 1
            self.last_image = self.current_image
            self.current_image = img_path
            # Adiciona um pequeno atraso para garantir que o arquivo foi salvo completamente
            self.root.after(100, self.update_images)
        else:
            print("Falha ao capturar screenshot")

    def on_resize(self, event):
        # Obtenha o tamanho atual do frame
        frame_width = self.frame_images.winfo_width()
        frame_height = self.frame_images.winfo_height()
        
        # Só prossiga se o frame tiver um tamanho sensato
        if frame_width > 100 and frame_height > 100:
            # Deixe uma margem de 20 pixels e divida a largura por 2 (duas imagens lado a lado)
            img_width = max(200, (frame_width // 2) - 20)
            # Use a maior parte da altura disponível
            img_height = max(150, frame_height - 40)
            
            # Atualize o tamanho de exibição
            self.img_display_size = (img_width, img_height)
            self.update_images()

    def update_images(self):
        self.label_counter.config(text=f"Prints tirados: {self.counter}")
        # Atualiza imagens
        for canvas, img_path in [(self.canvas_last, self.last_image), (self.canvas_current, self.current_image)]:
            if img_path and os.path.exists(img_path):
                try:
                    # Tenta carregar a imagem com um tratamento de erros melhorado
                    with open(img_path, 'rb') as f:
                        img = Image.open(f)
                        img.load()  # Carrega a imagem completamente
                        img = img.resize(self.img_display_size, Image.Resampling.LANCZOS)  # Use LANCZOS para melhor qualidade
                        img_tk = ImageTk.PhotoImage(img)
                        canvas.img = img_tk
                        canvas.config(image=img_tk, text="")
                except Exception as e:
                    print(f"Erro ao carregar imagem: {e}")
                    canvas.config(image='', text=f"Erro: {str(e)[:20]}...")
            else:
                canvas.config(image='', text="(vazio)")

    def on_generate_pdf(self):
        paths = get_image_paths(IMAGES_DIR)
        if paths:
            generate_pdf(paths, PDF_OUTPUT)
            messagebox.showinfo("PDF", f"PDF gerado: {PDF_OUTPUT}")
        else:
            messagebox.showwarning("PDF", "Nenhuma imagem para gerar PDF.")

    def start_automation(self):
        """Inicia o processo de automação de capturas."""
        try:
            interval = float(self.interval_var.get())
            num_captures = int(self.num_captures_var.get())
            
            if interval <= 0 or num_captures <= 0:
                messagebox.showerror("Erro", "Intervalo e número de capturas devem ser valores positivos.")
                return
            
            # Desabilita os controles durante a automação
            self.interval_entry.config(state=tk.DISABLED)
            self.num_captures_entry.config(state=tk.DISABLED)
            self.btn_start.config(state=tk.DISABLED)
            self.btn_stop.config(state=tk.NORMAL)
            
            # Define a flag para permitir o loop de automação
            self.automation_running = True
            
            # Inicia a automação em uma thread separada
            self.automation_thread = threading.Thread(target=self.run_automation, 
                                                     args=(interval, num_captures),
                                                     daemon=True)
            self.automation_thread.start()
            
            # Atualiza o status
            self.automation_status.config(text="Status: Em execução")
            
        except ValueError:
            messagebox.showerror("Erro", "Por favor, insira valores numéricos válidos.")
    
    def stop_automation(self):
        """Para o processo de automação."""
        self.automation_running = False
        self.automation_status.config(text="Status: Parando...")
        # Os controles serão reativados quando a thread terminar
    
    def run_automation(self, interval, num_captures):
        """Executa o loop de automação."""
        try:
            for i in range(num_captures):
                if not self.automation_running:
                    break
                
                # Atualiza o status na interface
                self.root.after(0, lambda count=i+1, total=num_captures: 
                           self.automation_status.config(text=f"Status: Capturando {count}/{total}"))
                
                # Aguarda o intervalo especificado
                time.sleep(interval)
                
                # Tira o screenshot
                img_path = save_screenshot(IMAGES_DIR)
                if img_path:
                    self.counter += 1
                    self.last_image = self.current_image
                    self.current_image = img_path
                    # Atualiza a interface
                    self.root.after(0, self.update_images)
                
                # Simula o pressionamento da tecla de seta para direita
                if self.automation_running and i < num_captures - 1:  # Não pressiona na última iteração
                    pyautogui.press('right')
            
            # Atualiza a interface quando terminar
            self.root.after(0, self.finish_automation)
            
        except Exception as e:
            print(f"Erro na automação: {e}")
            self.root.after(0, lambda: messagebox.showerror("Erro na Automação", str(e)))
            self.root.after(0, self.finish_automation)
    
    def finish_automation(self):
        """Finaliza o processo de automação, reativando os controles."""
        self.automation_running = False
        self.interval_entry.config(state=tk.NORMAL)
        self.num_captures_entry.config(state=tk.NORMAL)
        self.btn_start.config(state=tk.NORMAL)
        self.btn_stop.config(state=tk.DISABLED)
        self.automation_status.config(text="Status: Concluído")

if __name__ == "__main__":
    root = tk.Tk()
    app = PDFMakerApp(root)
    root.mainloop()