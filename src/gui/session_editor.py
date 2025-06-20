import os
import sys
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from src.config.config import (ICON, SESSION_WINDOW_SIZE, MIN_SESSION_WINDOW_SIZE, 
                               THUMBNAIL_SIZE
                               )
from src.gui.image_editor import ImageEditorWindow
from src.core.annotation_manager import AnnotationManager

class ThumbnailFrame(ttk.Frame):
    """Frame para exibir e gerenciar miniaturas de imagens na sessão."""
    def __init__(self, parent, index, image_path, on_reorder, on_delete, on_edit, annotation_manager, **kwargs):
        super().__init__(parent, **kwargs)
        
        self.parent = parent
        self.index = index
        self.image_path = image_path
        self.on_reorder = on_reorder
        self.on_delete = on_delete
        self.on_edit = on_edit
        self.annotation_manager = annotation_manager
        
        # Carrega a imagem como thumbnail
        self._load_thumbnail()
        
        # Frame para conter a imagem e o índice
        content_frame = ttk.Frame(self)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=3, pady=3)
        
        # Campo de entrada para o número/ordem da imagem
        order_frame = ttk.Frame(content_frame)
        order_frame.pack(side=tk.TOP, fill=tk.X, pady=(0, 5))
        
        ttk.Label(order_frame, text="Ordem:").pack(side=tk.LEFT, padx=(0, 5))
        
        vcmd = (self.register(self._validate_order), '%P')
        self.order_entry = ttk.Entry(order_frame, width=5, validate="key", validatecommand=vcmd)
        self.order_entry.pack(side=tk.LEFT)
        self.order_entry.insert(0, str(index + 1))
        
        # Botão aplicar ordem
        self.apply_btn = ttk.Button(order_frame, text="✓", width=2, 
                                    command=self._apply_order_change)
        self.apply_btn.pack(side=tk.LEFT, padx=(5, 0))
        
        # Imagem em miniatura
        self.image_label = ttk.Label(content_frame, image=self.thumbnail)
        self.image_label.pack(side=tk.TOP, padx=5, pady=5)
        
        # Vincular duplo clique na imagem para abrir o editor
        self.image_label.bind("<Double-Button-1>", lambda e: self._on_edit_click())
        
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
    
    def _validate_order(self, value):
        """Valida a entrada para garantir que seja um número válido."""
        if value == "":
            return True
        try:
            # Verificar se é um número inteiro positivo
            num = int(value)
            return num > 0
        except ValueError:
            return False
    
    def _apply_order_change(self):
        """Aplica a mudança de ordem/posição da imagem."""
        try:
            new_order = int(self.order_entry.get())
            if new_order != self.index + 1:  # Se a ordem realmente mudou
                # A posição no array é 0-based, mas a visualização para o usuário é 1-based
                self.on_reorder(self.index, new_order - 1)
        except ValueError:
            messagebox.showerror("Erro", "Por favor, insira um número válido para a ordem.")
    
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
        self.order_entry.delete(0, tk.END)
        self.order_entry.insert(0, str(new_index + 1))
    
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
        
        # Variável para armazenar o último número de miniaturas por linha
        self.last_thumbnails_per_row = 5
        
        # Flag para controlar o redimensionamento
        self.resizing = False
        
        # Largura e padding de cada miniatura para cálculos de layout
        screen_width = self.parent.winfo_screenwidth() if hasattr(self.parent, 'winfo_screenwidth') else 1920
        self.thumbnail_width = int(screen_width * THUMBNAIL_SIZE[0] / 100)  # Largura total de cada miniatura incluindo padding
        self.thumbnail_height = int(screen_width * THUMBNAIL_SIZE[1] / 100)
        self.min_thumbnails_per_row = 1
        self.max_thumbnails_per_row = 30  # Limite máximo razoável de miniaturas por linha
    
    def show(self):
        """Mostra a janela de edição de sessão."""
        if self.window:
            self.window.destroy()
        
        self.window = tk.Toplevel(self.parent)
        self.window.title("Editar Sessão de Imagens")
        
        # Permitir fechar, maximizar e minimizar - configurar como janela independente
        self.window.resizable(True, True)
        
        # Calcular o tamanho apropriado para a janela usando porcentagem da tela
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()

        width = int(screen_width * SESSION_WINDOW_SIZE[0] / 100)
        height = int(screen_height * SESSION_WINDOW_SIZE[1] / 100)
        window_size = f"{width}x{height}"

        min_width = int(screen_width * MIN_SESSION_WINDOW_SIZE[0] / 100)
        min_height = int(screen_height * MIN_SESSION_WINDOW_SIZE[1] / 100)

        # Aplicar o tamanho
        self.window.geometry(window_size)
        self.window.minsize(min_width, min_height)

        # Posicionar a janela centralizada na tela
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.window.geometry(f"+{x}+{y}")
        
        icon_path = ICON
        if getattr(sys, 'frozen', False):
            icon_path = os.path.join(sys._MEIPASS, ICON)
        self.window.iconbitmap(icon_path)
        
        # Configuração modal que mantém os botões de controle da janela
        # Isso faz com que a janela pai não possa ser interagida até que esta janela seja fechada
        self.window.grab_set()  # Captura todos os eventos, impedindo interação com a janela pai
    
        # Configurar estilos para frames
        style = ttk.Style()
        style.configure("Annotated.TFrame", borderwidth=2, relief="solid", bordercolor="green")
        
        # Layout principal
        main_frame = ttk.Frame(self.window)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Frame de instruções
        instruction_frame = ttk.Frame(main_frame)
        instruction_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(instruction_frame, text="Altere o número de ordem e clique no botão ✓ para reordenar. "
                                        "Clique duas vezes na imagem para editá-la.").pack(anchor=tk.W)
        
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
        
        self.canvas = tk.Canvas(canvas_frame)  # Store reference to canvas
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.canvas.configure(xscrollcommand=h_scrollbar.set, yscrollcommand=v_scrollbar.set)
        h_scrollbar.config(command=self.canvas.xview)
        v_scrollbar.config(command=self.canvas.yview)
        
        # Frame dentro do canvas para as miniaturas (com layout em grid para melhor organização)
        self.thumbnails_frame = ttk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.thumbnails_frame, anchor=tk.NW)
        
        # Configurar o scroll
        self.thumbnails_frame.bind("<Configure>", 
                                 lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        
        # Habilitar rolagem com a roda do mouse
        self.canvas.bind("<MouseWheel>", lambda e: self.canvas.yview_scroll(int(-1*(e.delta/120)), "units"))
        self.canvas.bind("<Shift-MouseWheel>", lambda e: self.canvas.xview_scroll(int(-1*(e.delta/120)), "units"))
        
        # Carregar as miniaturas
        self._load_thumbnails()
        
        # Botões de ação
        action_frame = ttk.Frame(main_frame)
        action_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(action_frame, text="Cancelar", 
                 command=self._on_cancel).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(action_frame, text="Gerar PDF", 
                 command=self._on_generate_pdf).pack(side=tk.RIGHT, padx=5)
        
        # Adicionar handler para redimensionamento da janela
        self.window.bind("<Configure>", self._on_window_resize)
        
        # Forçar um cálculo inicial após a janela ser renderizada
        self.window.after(100, self._initial_thumbnail_layout)
        
        # Esperar que a janela seja fechada
        self.parent.wait_window(self.window)
        
        return self.result
    
    def _initial_thumbnail_layout(self):
        """Configura o layout inicial das miniaturas após a janela ser renderizada."""
        # Calcular quantas miniaturas por linha baseado na largura inicial real
        self.last_thumbnails_per_row = self._calculate_thumbnails_per_row()
        self._load_thumbnails()
    
    def _calculate_thumbnails_per_row(self):
        """Calcula o número de miniaturas por linha com base na largura disponível."""
        if not self.window or not hasattr(self, 'canvas') or not self.canvas:
            return 5  # Valor padrão
        
        try:
            # Obter a largura disponível diretamente do canvas visível
            available_width = self.canvas.winfo_width()
            
            # Verificar se a largura é válida
            if available_width < 100:
                # Se ainda não temos um tamanho válido do canvas,
                # usar a largura da janela com ajuste para bordas e scrollbar
                window_width = self.window.winfo_width()
                available_width = max(150, window_width - 100)  # Ajuste mais conservador
            
            # Padding entre miniaturas - 10px total (5px de cada lado)
            padding_per_thumbnail = 10
            
            # Largura efetiva considerando o padding
            effective_thumbnail_width = self.thumbnail_width + padding_per_thumbnail
            
            # Calcular quantas miniaturas cabem por linha
            thumbnails_per_row = max(self.min_thumbnails_per_row, 
                                    min(self.max_thumbnails_per_row, 
                                        int(available_width / effective_thumbnail_width)))
            
            print(f"Largura disponível: {available_width}px, Largura efetiva: {effective_thumbnail_width}px, " +
                  f"Miniaturas por linha: {thumbnails_per_row}")
            
            return thumbnails_per_row
        except Exception as e:
            print(f"Erro ao calcular miniaturas por linha: {e}")
            return 5  # Valor padrão em caso de erro
    
    def _on_window_resize(self, event):
        """Handler para o evento de redimensionamento da janela."""
        # Verificar se o evento veio da janela principal e não de algum widget interno
        if event.widget != self.window:
            return
            
        # Implementar um debounce para evitar recarga excessiva durante o redimensionamento
        if hasattr(self, '_resize_timer') and self._resize_timer:
            self.window.after_cancel(self._resize_timer)
            
        # Agendar a recarga das miniaturas após um pequeno atraso
        self._resize_timer = self.window.after(200, self._reload_thumbnails_after_resize)
    
    def _reload_thumbnails_after_resize(self):
        """Recarrega as miniaturas após o redimensionamento da janela."""
        if self.resizing:
            return
            
        # Armazenar o valor atual para comparação
        old_thumbnails_per_row = self.last_thumbnails_per_row
        
        # Calcular o novo valor baseado nas dimensões atuais
        new_thumbnails_per_row = self._calculate_thumbnails_per_row()
        
        # Só recarregar se o número de miniaturas por linha realmente mudar
        if new_thumbnails_per_row != old_thumbnails_per_row:
            print(f"Atualizando layout: {old_thumbnails_per_row} -> {new_thumbnails_per_row} miniaturas por linha")
            self.last_thumbnails_per_row = new_thumbnails_per_row
            self.resizing = True
            self._load_thumbnails()
            self.resizing = False
        else:
            print(f"Layout mantido: {new_thumbnails_per_row} miniaturas por linha")
    
    def _load_thumbnails(self):
        """Carrega as miniaturas das imagens."""
        # Limpar frames existentes
        for widget in self.thumbnails_frame.winfo_children():
            widget.destroy()
        self.frames = []
        
        # Usar o número de miniaturas por linha já calculado
        max_per_row = self.last_thumbnails_per_row
        
        print(f"Renderizando miniaturas com {max_per_row} por linha")
        
        # Criar frames para cada imagem
        for i, path in enumerate(self.image_paths):
            row = i // max_per_row
            col = i % max_per_row
            
            frame = ThumbnailFrame(
                self.thumbnails_frame, 
                i, 
                path, 
                self._on_reorder, 
                self._on_delete, 
                self._on_edit,
                self.annotation_manager,
                width=self.thumbnail_width, 
                height=self.thumbnail_height
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
        # Garantir que os índices são válidos
        if from_idx == to_idx or from_idx < 0 or to_idx < 0 or from_idx >= len(self.image_paths) or to_idx >= len(self.image_paths):
            return
        
        # Pegar o caminho da imagem a ser movida
        path = self.image_paths[from_idx]
        
        # Remover da posição atual
        self.image_paths.pop(from_idx)
        
        # Inserir na nova posição
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
            
            # Restaurar a modalidade da janela de sessão após o fechamento do editor
            self.window.grab_set()
            
            # Atualizar o frame para refletir anotações
            if idx < len(self.frames):
                self.frames[idx].update_image(path)
                
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao editar imagem: {str(e)}")
            # Garantir que a modalidade seja restaurada mesmo em caso de erro
            self.window.grab_set()
    
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
