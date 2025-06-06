import os
import sys
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import shutil
from typing import List, Dict, Any, Optional
import json
from src.config.config import ICON
from src.gui.image_editor import ImageEditorWindow
from src.core.annotation_manager import AnnotationManager

class DraggableFrame(ttk.Frame):
    """Frame com funcionalidade de arrastar e soltar para reordenação."""
    def __init__(self, parent, index, image_path, on_reorder, on_delete, on_edit, annotation_manager, **kwargs):
        super().__init__(parent, **kwargs)
        
        self.parent = parent
        self.index = index
        self.image_path = image_path
        self.on_reorder = on_reorder
        self.on_delete = on_delete
        self.on_edit = on_edit
        self.annotation_manager = annotation_manager
        self.selected = False
        
        # Configurar eventos para arrastar e soltar
        self.bind("<ButtonPress-1>", self._start_drag)
        self.bind("<ButtonRelease-1>", self._stop_drag)
        self.bind("<B1-Motion>", self._on_drag)
        self.bind("<Double-Button-1>", self._on_double_click)
        
        # Carrega a imagem como thumbnail
        self._load_thumbnail()
        
        # Frame para conter a imagem e o índice
        content_frame = ttk.Frame(self)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=3, pady=3)
        
        # Número/índice da imagem
        self.index_label = ttk.Label(content_frame, text=f"{index+1}", anchor="center")
        self.index_label.pack(side=tk.TOP, fill=tk.X)
        
        # Imagem em miniatura
        self.image_label = ttk.Label(content_frame, image=self.thumbnail)
        self.image_label.pack(side=tk.TOP, padx=5, pady=5)
        
        # Botões de ações
        actions_frame = ttk.Frame(content_frame)
        actions_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=2, pady=2)
        
        # Botão editar
        self.edit_btn = ttk.Button(actions_frame, text="Editar", 
                                  command=self._on_edit_click, width=6)
        self.edit_btn.pack(side=tk.LEFT, padx=1)
        
        # Botão excluir
        self.delete_btn = ttk.Button(actions_frame, text="Excluir", 
                                   command=self._on_delete_click, width=6)
        self.delete_btn.pack(side=tk.RIGHT, padx=1)
        
        # Verificar se a imagem tem anotações e atualizar a aparência
        self._update_annotation_indicator()
    
    def _load_thumbnail(self, size=(120, 90)):
        """Carrega a imagem como thumbnail."""
        try:
            img = Image.open(self.image_path)
            img.thumbnail(size, Image.Resampling.LANCZOS)
            self.thumbnail = ImageTk.PhotoImage(img)
        except Exception as e:
            # Criar uma imagem vazia em caso de erro
            img = Image.new('RGB', size, color='lightgray')
            self.thumbnail = ImageTk.PhotoImage(img)
            print(f"Erro ao carregar thumbnail: {e}")
    
    def _update_annotation_indicator(self):
        """Atualiza o indicador visual se a imagem tem anotações."""
        has_annotations = self.annotation_manager.has_annotations(self.image_path)
        
        if has_annotations:
            # Adicionar um indicador visual (borda colorida)
            self.configure(style="Annotated.TFrame")
            # Atualizar o texto do botão de editar
            self.edit_btn.configure(text="Ver/Editar")
        else:
            # Remover o indicador visual
            self.configure(style="TFrame")
            # Restaurar o texto do botão de editar
            self.edit_btn.configure(text="Editar")
    
    def _start_drag(self, event):
        """Inicia a operação de arrastar."""
        self.selected = True
        self.config(style="Selected.TFrame")
        # Salvar posição inicial
        self._drag_start_x = event.x
        self._drag_start_y = event.y
        
    def _stop_drag(self, event):
        """Para a operação de arrastar."""
        if self.selected:
            self.selected = False
            self.config(style="TFrame")
            self._update_annotation_indicator()  # Restaurar estilo com base em anotações
    
    def _on_drag(self, event):
        """Manipula o evento de arrastar."""
        if not self.selected:
            return
            
        # Calcular a nova posição
        x = self.winfo_x() + event.x - self._drag_start_x
        y = self.winfo_y() + event.y - self._drag_start_y
        
        # Mover o frame
        self.place(x=x, y=y)
        
        # Verificar sobreposição com outros frames para reordenar
        self._check_overlap()
    
    def _check_overlap(self):
        """Verifica sobreposição com outros frames para reordenar."""
        x1, y1 = self.winfo_x(), self.winfo_y()
        w1, h1 = self.winfo_width(), self.winfo_height()
        
        # Encontrar o centro deste frame
        center_x = x1 + w1 / 2
        center_y = y1 + h1 / 2
        
        # Verificar todos os outros frames
        for child in self.parent.winfo_children():
            if isinstance(child, DraggableFrame) and child != self:
                x2, y2 = child.winfo_x(), child.winfo_y()
                w2, h2 = child.winfo_width(), child.winfo_height()
                
                # Verificar se o centro deste frame está dentro do outro frame
                if (x2 <= center_x <= x2 + w2) and (y2 <= center_y <= y2 + h2):
                    # Trocar posições
                    self.on_reorder(self.index, child.index)
                    return
    
    def _on_double_click(self, event):
        """Manipula o evento de duplo clique para editar."""
        self._on_edit_click()
    
    def _on_edit_click(self):
        """Manipula o clique no botão de editar."""
        self.on_edit(self.index)
    
    def _on_delete_click(self):
        """Manipula o clique no botão de excluir."""
        # Confirmar exclusão
        if messagebox.askyesno("Confirmar Exclusão", 
                             f"Tem certeza que deseja excluir a imagem {self.index+1}?"):
            self.on_delete(self.index)
    
    def update_index(self, new_index):
        """Atualiza o índice do frame."""
        self.index = new_index
        self.index_label.config(text=f"{new_index+1}")
    
    def update_image(self, image_path):
        """Atualiza a imagem do frame."""
        self.image_path = image_path
        self._load_thumbnail()
        self.image_label.config(image=self.thumbnail)
        self._update_annotation_indicator()


class SessionEditorWindow:
    """Janela de edição de sessão para organizar e editar imagens antes de gerar o PDF."""
    def __init__(self, parent, image_paths, session_dir):
        self.parent = parent
        self.image_paths = list(image_paths)  # Cópia para não modificar a original
        self.session_dir = session_dir
        self.window = None
        self.frames = []
        
        # Inicializar o gerenciador de anotações
        self.annotation_manager = AnnotationManager(session_dir)
        
        # Resultados da edição
        self.result = {
            'generate_pdf': False,
            'image_paths': []
        }
    
    def show(self):
        """Mostra a janela de edição de sessão."""
        if self.window:
            self.window.destroy()
        
        self.window = tk.Toplevel(self.parent)
        self.window.title("Editar Sessão de Imagens")
        
        # Permitir fechar, maximizar e minimizar - configurar como janela independente
        self.window.resizable(True, True)
        
        # Calcular o tamanho apropriado para a janela (80% da tela)
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        window_width = int(screen_width * 0.5)
        window_height = int(screen_height * 0.5)
        
        # Aplicar o tamanho
        self.window.geometry(f"{window_width}x{window_height}")
        self.window.minsize(800, 500)
        
        # Posicionar a janela centralizada na tela
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.window.geometry(f"+{x}+{y}")
        
        icon_path = ICON
        if getattr(sys, 'frozen', False):
            icon_path = os.path.join(sys._MEIPASS, ICON)
        self.window.iconbitmap(icon_path)
        
        # Configuração modal que mantém os botões de controle da janela
        # Isso faz com que a janela pai não possa ser interagida até que esta janela seja fechada
        self.window.grab_set()  # Captura todos os eventos, impedindo interação com a janela pai
        
        # Não usar transient() para manter os botões de controle de janela
        # self.window.transient(self.parent)  # Define a janela pai
    
        # Configurar estilos para frames
        style = ttk.Style()
        style.configure("Selected.TFrame", borderwidth=2, relief="solid", bordercolor="blue")
        style.configure("Annotated.TFrame", borderwidth=2, relief="solid", bordercolor="green")
        
        # Layout principal
        main_frame = ttk.Frame(self.window)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Frame de instruções
        instruction_frame = ttk.Frame(main_frame)
        instruction_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(instruction_frame, text="Organize as imagens arrastando-as para reordenar. "
                                        "Clique duas vezes para editar uma imagem.").pack(anchor=tk.W)
        
        # Frame para informações e contagem
        info_frame = ttk.Frame(main_frame)
        info_frame.pack(fill=tk.X, pady=(0, 5))
        
        self.count_label = ttk.Label(info_frame, text=f"Total: {len(self.image_paths)} imagens")
        self.count_label.pack(side=tk.LEFT)
        
        # Frame para visualização das imagens (com scrollbar)
        preview_frame = ttk.LabelFrame(main_frame, text="Imagens da Sessão")
        preview_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Canvas com scrollbars horizontais e verticais
        canvas_frame = ttk.Frame(preview_frame)
        canvas_frame.pack(fill=tk.BOTH, expand=True)
        
        h_scrollbar = ttk.Scrollbar(canvas_frame, orient="horizontal")
        h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        
        v_scrollbar = ttk.Scrollbar(canvas_frame, orient="vertical")
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        canvas = tk.Canvas(canvas_frame)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        canvas.configure(xscrollcommand=h_scrollbar.set, yscrollcommand=v_scrollbar.set)
        h_scrollbar.config(command=canvas.xview)
        v_scrollbar.config(command=canvas.yview)
        
        # Frame dentro do canvas para as miniaturas (com layout em grid para melhor organização)
        self.thumbnails_frame = ttk.Frame(canvas)
        canvas.create_window((0, 0), window=self.thumbnails_frame, anchor=tk.NW)
        
        # Configurar o scroll
        self.thumbnails_frame.bind("<Configure>", 
                                 lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        
        # Habilitar rolagem com a roda do mouse
        canvas.bind("<MouseWheel>", lambda e: canvas.yview_scroll(int(-1*(e.delta/120)), "units"))
        canvas.bind("<Shift-MouseWheel>", lambda e: canvas.xview_scroll(int(-1*(e.delta/120)), "units"))
        
        # Carregar as miniaturas
        self._load_thumbnails()
        
        # Botões de ação
        action_frame = ttk.Frame(main_frame)
        action_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(action_frame, text="Cancelar", 
                 command=self._on_cancel).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(action_frame, text="Gerar PDF", 
                 command=self._on_generate_pdf).pack(side=tk.RIGHT, padx=5)
        
        # Esperar que a janela seja fechada
        self.parent.wait_window(self.window)
        
        return self.result
    
    def _load_thumbnails(self):
        """Carrega as miniaturas das imagens."""
        # Limpar frames existentes
        for widget in self.thumbnails_frame.winfo_children():
            widget.destroy()
        self.frames = []
        
        # Organizar as miniaturas em uma grade em vez de uma única linha
        max_per_row = 5  # Número máximo de miniaturas por linha
        
        # Criar frames para cada imagem
        for i, path in enumerate(self.image_paths):
            row = i // max_per_row
            col = i % max_per_row
            
            frame = DraggableFrame(
                self.thumbnails_frame, 
                i, 
                path, 
                self._on_reorder, 
                self._on_delete, 
                self._on_edit,
                self.annotation_manager,
                width=140, 
                height=170
            )
            frame.grid(row=row, column=col, padx=5, pady=5)
            self.frames.append(frame)
            
        # Configurar pesos de linha e coluna para permitir expansão uniforme
        for i in range(max_per_row):
            self.thumbnails_frame.columnconfigure(i, weight=1)
            
        for i in range((len(self.image_paths) + max_per_row - 1) // max_per_row):
            self.thumbnails_frame.rowconfigure(i, weight=1)

    def _on_reorder(self, from_idx, to_idx):
        """Manipula a reordenação de imagens."""
        # Reordenar a lista de caminhos
        path = self.image_paths.pop(from_idx)
        self.image_paths.insert(to_idx, path)
        
        # Atualizar todos os frames
        self._load_thumbnails()
        
        # Atualizar contagem (por precaução)
        self.count_label.config(text=f"Total: {len(self.image_paths)} imagens")
    
    def _on_delete(self, idx):
        """Manipula a exclusão de imagens."""
        # Caminho da imagem a ser excluída
        path = self.image_paths[idx]
        
        try:
            # Remover do sistema de arquivos (exclusão física)
            if os.path.exists(path):
                try:
                    os.remove(path)
                except Exception as e:
                    print(f"Erro ao remover arquivo físico: {e}")
            
            # Remover da lista
            self.image_paths.pop(idx)
            
            # Remover quaisquer anotações associadas
            self.annotation_manager.remove_annotations(path)
            
            # Atualizar frames
            self._load_thumbnails()
            
            # Atualizar contagem
            self.count_label.config(text=f"Total: {len(self.image_paths)} imagens")
            
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao excluir imagem: {str(e)}")
    
    def _on_edit(self, idx):
        """Abre o editor de imagem para a imagem selecionada."""
        path = self.image_paths[idx]
        
        try:
            # Abrir o editor de imagem
            editor = ImageEditorWindow(self.window, path, self.annotation_manager)
            
            # Mostrar o editor - ele já tem comportamento modal implementado
            editor.show()
            
            # Atualizar o frame para refletir anotações
            if idx < len(self.frames):
                self.frames[idx].update_image(path)
                
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao editar imagem: {str(e)}")
    
    def _on_cancel(self):
        """Cancela a edição e fecha a janela."""
        self.result = {
            'generate_pdf': False,
            'image_paths': []
        }
        self.window.destroy()
    
    def _on_generate_pdf(self):
        """Finaliza a edição e retorna os caminhos para gerar PDF."""
        self.result = {
            'generate_pdf': True,
            'image_paths': self.image_paths
        }
        self.window.destroy()
