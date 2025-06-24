import os
import sys
import tkinter as tk
from tkinter import ttk, colorchooser, messagebox
from PIL import Image, ImageTk
from src.config.config import (ICON, IMAGE_EDITOR_DIALOG_WINDOW_SIZE,
                             ANNOTATION_COLOR, ANNOTATION_FONT_FAMILY, ANNOTATION_FONT_SIZE,
                             save_config)
from src.core.annotation_manager import AnnotationManager
from src.gui.image_editor_components.dialog_input import TextInputDialog
from src.gui.image_editor_components.annotation_element import AnnotationElement
from src.gui.image_editor_components.image_navigator import ImageNavigator

class ImageEditorWindow:
    """Janela de edição de imagem para adicionar anotações."""
    def __init__(self, parent, image_path, annotation_manager, image_paths=None, current_index=0):
        """
        Adicionei os parâmetros 'image_paths' e 'current_index' para
        possibilitar a navegação entre imagens por meio da classe ImageNavigator.
        """
        self.parent = parent
        self.image_paths = image_paths if image_paths else [image_path]
        self.navigator = ImageNavigator(self.image_paths, current_index)
        self.image_path = self.navigator.get_current_image()
        self.annotation_manager = annotation_manager
        self.window = None
        self.canvas = None
        self.annotations = []
        self.active_tool = "select"
        self.start_x = 0
        self.start_y = 0
        self.current_item = None
        self.temp_item = None
        self.color = ANNOTATION_COLOR  # Usar a configuração salva
        
        # Configurações de fonte
        self.font_family = ANNOTATION_FONT_FAMILY  # Usar a configuração salva
        self.font_size = ANNOTATION_FONT_SIZE  # Usar a configuração salva
        
        # Fator de zoom - definir para 48% por padrão
        self.zoom_factor = 0.48
        
        # Histórico de operações para desfazer/refazer (ctrl+z)
        self.history = []
        self.current_history_index = -1
        self.max_history = 20  # Limite do histórico para não consumir muita memória
        
        # Carregar anotações existentes
        self._load_annotations()
        
    def show(self):
        """Mostra a janela de edição de imagem."""
        if self.window:
            self.window.destroy()
        
        self.window = tk.Toplevel(self.parent)
        self.window.title(f"Editor de Imagem - {os.path.basename(self.image_path)}")
        
        # Permitir fechar, maximizar e minimizar - configurar como janela independente
        self.window.resizable(True, True)
        
        # Calcular o tamanho apropriado da janela (80% da tela)
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        
        # Redimensionar janela para ser proporcional à imagem, mas não maior que 80% da tela
        try:
            # Carregar a imagem para obter suas dimensões
            img = Image.open(self.image_path)
            img_width, img_height = img.size
            
            # Aplicar o zoom inicial de 48%
            img_width_zoomed = int(img_width * self.zoom_factor)
            img_height_zoomed = int(img_height * self.zoom_factor)
            
            # Adicionar espaço para controles
            window_width = min(int(screen_width * 0.8), img_width_zoomed + 100)
            window_height = min(int(screen_height * 0.8), img_height_zoomed + 150)
            
            # Definir tamanho da janela
            self.window.geometry(f"{window_width}x{window_height}")
            
            # Centralizar na tela
            x = (screen_width - window_width) // 2
            y = (screen_height - window_height) // 2
            self.window.geometry(f"+{x}+{y}")
            
        except Exception as e:
            # Usar tamanho padrão em caso de erro (80% da tela)
            window_width = int(screen_width * 0.8)
            window_height = int(screen_height * 0.8)
            self.window.geometry(f"{window_width}x{window_height}+{screen_width//10}+{screen_height//10}")
            print(f"Erro ao dimensionar janela: {e}")
        
        self.window.minsize(window_width, window_height)
        icon_path = ICON
        if getattr(sys, 'frozen', False):
            icon_path = os.path.join(sys._MEIPASS, ICON)
        self.window.iconbitmap(icon_path)
        
        # Layout principal
        main_frame = ttk.Frame(self.window)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Reorganizar a barra de ferramentas em categorias
        toolbar_frame = ttk.LabelFrame(main_frame, text="Ferramentas")
        toolbar_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Grid para organizar as ferramentas em categorias
        tools_grid = ttk.Frame(toolbar_frame)
        tools_grid.pack(fill=tk.X, padx=5, pady=5)
        
        # 1. Grupo de Seleção
        selection_frame = ttk.LabelFrame(tools_grid, text="Seleção")
        selection_frame.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        
        self.select_btn = tk.Button(selection_frame, text="Selecionar", width=10,
                            command=lambda: self._set_tool("select"), bg="SystemButtonFace")
        self.select_btn.pack(side=tk.LEFT, padx=2, pady=2)
        
        self.delete_btn = ttk.Button(selection_frame, text="Excluir", width=10,
                                   command=self._delete_selected)
        self.delete_btn.pack(side=tk.LEFT, padx=2, pady=2)
        
        # 2. Grupo de Formas
        shapes_frame = ttk.LabelFrame(tools_grid, text="Formas")
        shapes_frame.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        
        self.line_btn = tk.Button(shapes_frame, text="Linha", width=7,
                                 command=lambda: self._set_tool("line"), bg="SystemButtonFace")
        self.line_btn.pack(side=tk.LEFT, padx=2, pady=2)
        
        self.arrow_btn = tk.Button(shapes_frame, text="Seta", width=7,
                                  command=lambda: self._set_tool("arrow"), bg="SystemButtonFace")
        self.arrow_btn.pack(side=tk.LEFT, padx=2, pady=2)
        
        self.rect_btn = tk.Button(shapes_frame, text="Retângulo", width=11,
                                 command=lambda: self._set_tool("rect"), bg="SystemButtonFace")
        self.rect_btn.pack(side=tk.LEFT, padx=2, pady=2)
        
        # 3. Grupo de Texto
        text_frame = ttk.LabelFrame(tools_grid, text="Texto")
        text_frame.grid(row=0, column=2, padx=5, pady=5, sticky="w")
        
        self.text_btn = tk.Button(text_frame, text="Adicionar", width=11,
                                 command=lambda: self._set_tool("text"), bg="SystemButtonFace")
        self.text_btn.pack(side=tk.LEFT, padx=2, pady=2)
        
        self.font_btn = ttk.Button(text_frame, text="Fonte", width=7,
                                 command=self._choose_font)
        self.font_btn.pack(side=tk.LEFT, padx=2, pady=2)
        
        # 4. Grupo de Cores
        color_frame = ttk.LabelFrame(tools_grid, text="Cor")
        color_frame.grid(row=0, column=3, padx=5, pady=5, sticky="w")
        
        self.color_btn = ttk.Button(color_frame, text="Escolher", width=10,
                                  command=self._choose_color)
        self.color_btn.pack(side=tk.LEFT, padx=2, pady=2)
        
        # Amostra de cor atual
        self.color_sample = tk.Canvas(color_frame, width=20, height=20, bg=self.color)
        self.color_sample.pack(side=tk.LEFT, padx=2, pady=2)
        
        # 5. Grupo de Zoom
        zoom_frame = ttk.LabelFrame(tools_grid, text="Zoom")
        zoom_frame.grid(row=0, column=4, padx=5, pady=5, sticky="w")
        
        self.zoom_in_btn = ttk.Button(zoom_frame, text="Ampliar", width=8,
                                    command=self._zoom_in)
        self.zoom_in_btn.pack(side=tk.LEFT, padx=2, pady=2)
        
        self.zoom_out_btn = ttk.Button(zoom_frame, text="Reduzir", width=8,
                                     command=self._zoom_out)
        self.zoom_out_btn.pack(side=tk.LEFT, padx=2, pady=2)
        
        self.zoom_reset_btn = ttk.Button(zoom_frame, text="1:1", width=4,
                                       command=self._zoom_reset)
        self.zoom_reset_btn.pack(side=tk.LEFT, padx=2, pady=2)
        
        # Label para exibir o zoom atual
        self.zoom_label = ttk.Label(zoom_frame, text="48%")
        self.zoom_label.pack(side=tk.LEFT, padx=2, pady=2)
        
        # 6. Grupo de Histórico
        history_frame = ttk.LabelFrame(tools_grid, text="Histórico")
        history_frame.grid(row=0, column=5, padx=5, pady=5, sticky="w")
        
        self.undo_btn = ttk.Button(history_frame, text="Desfazer", width=8,
                                  command=self._undo)
        self.undo_btn.pack(side=tk.LEFT, padx=2, pady=2)
        
        self.redo_btn = ttk.Button(history_frame, text="Refazer", width=8,
                                  command=self._redo)
        self.redo_btn.pack(side=tk.LEFT, padx=2, pady=2)
        
        # Canvas para a imagem e anotações (com scrollbars)
        canvas_frame = ttk.Frame(main_frame)
        canvas_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Adicionar scrollbars
        h_scrollbar = ttk.Scrollbar(canvas_frame, orient=tk.HORIZONTAL)
        h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        
        v_scrollbar = ttk.Scrollbar(canvas_frame, orient=tk.VERTICAL)
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Canvas
        self.canvas = tk.Canvas(canvas_frame, bg="lightgray",
                              xscrollcommand=h_scrollbar.set,
                              yscrollcommand=v_scrollbar.set)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        h_scrollbar.config(command=self.canvas.xview)
        v_scrollbar.config(command=self.canvas.yview)
        
        # Carregar imagem no canvas
        self._load_image()
        
        # Configurar eventos do canvas
        self.canvas.bind("<ButtonPress-1>", self._on_press)
        self.canvas.bind("<B1-Motion>", self._on_drag)
        self.canvas.bind("<ButtonRelease-1>", self._on_release)
        
        # Adicionar evento de clique duplo para edição de texto
        self.canvas.bind("<Double-Button-1>", self._on_double_click)
        
        # Adicionar suporte a zoom com roda do mouse
        self.canvas.bind("<MouseWheel>", self._on_mousewheel)
        
        # Adicionar suporte a Ctrl+Z e Ctrl+Y
        self.window.bind("<Control-z>", lambda e: self._undo())
        self.window.bind("<Control-y>", lambda e: self._redo())
        
        # Botões de ação
        action_frame = ttk.Frame(main_frame)
        action_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(action_frame, text="Cancelar", 
                 command=self._on_cancel).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(action_frame, text="Limpar Anotações", 
                 command=self._clear_annotations).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(action_frame, text="Salvar", 
                 command=self._on_save).pack(side=tk.RIGHT, padx=5)
        
        # Adicionar rótulo de indicador de imagem
        self.image_index_label = ttk.Label(action_frame, text="")
        self.image_index_label.pack(side=tk.LEFT, padx=5)
        self._update_image_index_label()

        # Botões para avançar e retroceder imagem
        ttk.Button(
            action_frame,
            text="← Anterior",
            command=self._on_prev_image
        ).pack(side=tk.LEFT, padx=5)

        ttk.Button(
            action_frame,
            text="Próxima →",
            command=self._on_next_image
        ).pack(side=tk.LEFT, padx=5)

        # Destacar o botão da ferramenta ativa
        self._update_tool_buttons()
        
        # Renderizar anotações existentes
        self._render_annotations()
        
        # Salvar o estado inicial no histórico
        self._add_to_history()
        
        # Configurar um protocolo para quando a janela for fechada
        self.window.protocol("WM_DELETE_WINDOW", self._on_cancel)
        
        # Configuração modal que mantém os botões de controle da janela
        self.window.grab_set()  # Captura todos os eventos, impedindo interação com a janela pai
        
        # Não usar transient() para manter os botões de controle
        # self.window.transient(self.parent)  # Define a janela pai
    
        # Esperar que a janela seja fechada
        self.parent.wait_window(self.window)
    
    def _zoom_in(self):
        """Aumentar o zoom."""
        new_zoom = min(3.0, self.zoom_factor * 1.2)  # Limite máximo de zoom 300%
        self._apply_zoom(new_zoom)
    
    def _zoom_out(self):
        """Reduzir o zoom."""
        new_zoom = max(0.2, self.zoom_factor / 1.2)  # Limite mínimo de zoom 20%
        self._apply_zoom(new_zoom)
    
    def _zoom_reset(self):
        """Resetar o zoom para 100%."""
        self._apply_zoom(1.0)
    
    def _apply_zoom(self, new_zoom):
        """Aplica o novo fator de zoom."""
        if new_zoom == self.zoom_factor:
            return
        
        old_zoom = self.zoom_factor
        self.zoom_factor = new_zoom
        
        # Atualizar o label de zoom
        zoom_percent = int(self.zoom_factor * 100)
        self.zoom_label.config(text=f"{zoom_percent}%")
        
        # Ajustar as dimensões do canvas e recarregar a imagem
        if self.pil_image:
            # Salvar posição de rolagem atual
            current_x = self.canvas.canvasx(0)
            current_y = self.canvas.canvasy(0)
            
            # Calcular o novo centro de visualização
            view_width = self.canvas.winfo_width()
            view_height = self.canvas.winfo_height()
            view_center_x = current_x + view_width / 2
            view_center_y = current_y + view_height / 2
            
            # Aplicar novo zoom
            new_width = int(self.image_width * self.zoom_factor)
            new_height = int(self.image_height * self.zoom_factor)
            
            # Recriar a imagem com o novo zoom
            img_resized = self.pil_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
            self.tk_image = ImageTk.PhotoImage(img_resized)
            
            # Atualizar a região de rolagem do canvas
            self.canvas.config(scrollregion=(0, 0, new_width, new_height))
            
            # Atualizar a imagem no canvas
            self.canvas.delete(self.image_item)
            self.image_item = self.canvas.create_image(0, 0, anchor=tk.NW, image=self.tk_image)
            
            # Redesenhar as anotações com o novo zoom
            self._redraw_annotations_with_zoom()
            
            # Centralizar na mesma posição relativa após o zoom
            new_center_x = view_center_x * (new_zoom / old_zoom)
            new_center_y = view_center_y * (new_zoom / old_zoom)
            
            # Calcular as novas coordenadas para centralizar a visualização
            new_x = new_center_x - view_width / 2
            new_y = new_center_y - view_height / 2
            
            # Aplicar a nova posição de rolagem
            self.canvas.xview_moveto(new_x / new_width)
            self.canvas.yview_moveto(new_y / new_height)
    
    def _on_mousewheel(self, event):
        """Manipula o evento da roda do mouse para zoom."""
        if event.state & 0x4:  # Ctrl pressionado
            # Determinar direção do zoom
            if event.delta > 0:
                self._zoom_in()
            else:
                self._zoom_out()
            return "break"
    
    def _on_double_click(self, event):
        """Manipula o evento de clique duplo para edição de texto."""
        # Verificar se estamos no modo de seleção
        if self.active_tool != "select":
            return
            
        # Converter coordenadas do canvas
        canvas_x = self.canvas.canvasx(event.x)
        canvas_y = self.canvas.canvasy(event.y)
        
        # Verificar se clicou em algum item
        tolerance = 5 / self.zoom_factor
        items = self.canvas.find_overlapping(
            canvas_x-tolerance, canvas_y-tolerance, 
            canvas_x+tolerance, canvas_y+tolerance
        )
        
        # Filtrar para não selecionar a imagem de fundo
        filtered_items = [item for item in items if item != self.image_item]
        
        if filtered_items:
            item_id = filtered_items[0]
            # Verificar se é um texto
            annotation = self._get_annotation_by_item_id(item_id)
            if annotation and annotation.type == "text":
                # Editar o texto
                self._edit_text_annotation(annotation)
    
    def _redraw_annotations_with_zoom(self):
        """Redesenha todas as anotações com o zoom atual."""
        # Remover anotações atuais do canvas
        for annotation in self.annotations:
            if annotation.item_id:
                self.canvas.delete(annotation.item_id)
                annotation.item_id = None
        
        # Redesenhar todas as anotações
        for annotation in self.annotations:
            item_id = self._create_annotation_item(annotation)
            annotation.item_id = item_id
    
    def _add_to_history(self):
        """Adiciona o estado atual das anotações ao histórico."""
        # Limitar o tamanho do histórico
        if self.current_history_index < len(self.history) - 1:
            # Se estamos em um ponto intermediário do histórico, descarte estados posteriores
            self.history = self.history[:self.current_history_index + 1]
        
        # Criar uma cópia profunda das anotações atuais
        current_state = []
        for annotation in self.annotations:
            current_state.append({
                'type': annotation.type,
                'properties': annotation.properties.copy()
            })
        
        # Adicionar ao histórico
        self.history.append(current_state)
        self.current_history_index = len(self.history) - 1
        
        # Limitar o tamanho do histórico
        if len(self.history) > self.max_history:
            self.history = self.history[-self.max_history:]
            self.current_history_index = len(self.history) - 1
        
        # Atualizar estado dos botões
        self._update_history_buttons()
    
    def _update_history_buttons(self):
        """Atualiza o estado dos botões de desfazer/refazer."""
        # Habilitar/desabilitar o botão de desfazer
        if self.current_history_index > 0:
            self.undo_btn.config(state=tk.NORMAL)
        else:
            self.undo_btn.config(state=tk.DISABLED)
        
        # Habilitar/desabilitar o botão de refazer
        if self.current_history_index < len(self.history) - 1:
            self.redo_btn.config(state=tk.NORMAL)
        else:
            self.redo_btn.config(state=tk.DISABLED)
    
    def _undo(self):
        """Desfaz a última operação."""
        if self.current_history_index > 0:
            self.current_history_index -= 1
            self._restore_history_state()
    
    def _redo(self):
        """Refaz a última operação desfeita."""
        if self.current_history_index < len(self.history) - 1:
            self.current_history_index += 1
            self._restore_history_state()
    
    def _restore_history_state(self):
        """Restaura o estado das anotações a partir do histórico."""
        if 0 <= self.current_history_index < len(self.history):
            # Limpar anotações atuais
            for annotation in self.annotations:
                if annotation.item_id:
                    self.canvas.delete(annotation.item_id)
            
            # Carregar do histórico
            state = self.history[self.current_history_index]
            self.annotations = []
            
            for item_data in state:
                self.annotations.append(AnnotationElement.from_dict(item_data))
            
            # Renderizar as anotações
            self._render_annotations()
            
            # Atualizar os botões
            self._update_history_buttons()
    
    def _load_image(self):
        """Carrega a imagem no canvas."""
        try:
            # Carregar a imagem com PIL
            self.pil_image = Image.open(self.image_path)
            self.image_width, self.image_height = self.pil_image.size
            
            # Aplicar zoom
            new_width = int(self.image_width * self.zoom_factor)
            new_height = int(self.image_height * self.zoom_factor)
            
            # Redimensionar a imagem conforme o zoom
            img_resized = self.pil_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
            self.tk_image = ImageTk.PhotoImage(img_resized)
            
            # Configurar o tamanho do canvas
            self.canvas.config(scrollregion=(0, 0, new_width, new_height))
            
            # Adicionar a imagem ao canvas
            self.image_item = self.canvas.create_image(0, 0, anchor=tk.NW, image=self.tk_image)
            
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao carregar imagem: {str(e)}")
            if self.window:
                self.window.destroy()
    
    def _load_annotations(self):
        """Carrega anotações existentes para a imagem."""
        self.annotations = []
        
        # Verificar se existem anotações para esta imagem
        if not self.annotation_manager.has_annotations(self.image_path):
            return
        
        # Carregar anotações
        annotations_data = self.annotation_manager.load_annotations(self.image_path)
        
        for item_data in annotations_data:
            # Criar objetos de anotação sem ID por enquanto
            self.annotations.append(AnnotationElement.from_dict(item_data))
    
    def _render_annotations(self):
        """Renderiza as anotações no canvas."""
        if not self.canvas:
            return
            
        # Limpar IDs antigos
        for annotation in self.annotations:
            annotation.item_id = None
            
        # Renderizar cada anotação
        for annotation in self.annotations:
            item_id = self._create_annotation_item(annotation)
            annotation.item_id = item_id
    
    def _create_annotation_item(self, annotation):
        """Cria um item de anotação no canvas com base no tipo."""
        if annotation.type == "text":
            props = annotation.properties
            # Converter coordenadas originais para coordenadas de canvas
            canvas_x = props['x'] * self.zoom_factor
            canvas_y = props['y'] * self.zoom_factor
            
            # Ajustar tamanho da fonte para o zoom
            font_size = int(props.get('font_size', self.font_size) * self.zoom_factor)
            
            # Criar caixa de texto com suporte a quebra de linha
            return self.canvas.create_text(
                canvas_x, canvas_y,
                text=props['text'],
                fill=props['color'],
                font=(props.get('font_family', self.font_family), font_size),
                anchor=props.get('anchor', tk.NW),
                width=props.get('width', 300) * self.zoom_factor  # Adicionar largura máxima para quebra de texto
            )
            
        elif annotation.type == "arrow":
            props = annotation.properties
            # Converter coordenadas originais para coordenadas de canvas
            x1 = props['x1'] * self.zoom_factor
            y1 = props['y1'] * self.zoom_factor
            x2 = props['x2'] * self.zoom_factor
            y2 = props['y2'] * self.zoom_factor
            
            # Ajustar largura da linha para o zoom
            width = props.get('width', 2)
            
            # Criar seta
            return self.canvas.create_line(
                x1, y1, x2, y2,
                fill=props['color'],
                width=width,
                arrow=tk.LAST
            )
            
        elif annotation.type == "rect":
            props = annotation.properties
            # Converter coordenadas originais para coordenadas de canvas
            x1 = props['x1'] * self.zoom_factor
            y1 = props['y1'] * self.zoom_factor
            x2 = props['x2'] * self.zoom_factor
            y2 = props['y2'] * self.zoom_factor
            
            # Ajustar largura da linha para o zoom
            width = props.get('width', 2)
            
            # Criar retângulo
            return self.canvas.create_rectangle(
                x1, y1, x2, y2,
                outline=props['color'],
                width=width
            )
            
        elif annotation.type == "line":
            props = annotation.properties
            # Converter coordenadas originais para coordenadas de canvas
            x1 = props['x1'] * self.zoom_factor
            y1 = props['y1'] * self.zoom_factor
            x2 = props['x2'] * self.zoom_factor
            y2 = props['y2'] * self.zoom_factor
            
            # Ajustar largura da linha para o zoom
            width = props.get('width', 2)
            
            # Criar linha
            return self.canvas.create_line(
                x1, y1, x2, y2,
                fill=props['color'],
                width=width
            )
            
        return None
    
    def _set_tool(self, tool):
        """Define a ferramenta ativa."""
        self.active_tool = tool
        self._update_tool_buttons()
    
    def _update_tool_buttons(self):
        """Atualiza o estado visual dos botões de ferramentas."""
        # Cores para os botões
        normal_color = "SystemButtonFace"  # Cor padrão de botões
        active_color = "#ADD8E6"  # Azul claro
        
        # Resetar todos os botões para a cor normal
        for btn in [self.select_btn, self.text_btn, self.arrow_btn, 
                   self.rect_btn, self.line_btn]:
            btn.config(bg=normal_color)
        
        # Destacar o botão da ferramenta ativa com a cor de destaque
        if self.active_tool == "select":
            self.select_btn.config(bg=active_color)
        elif self.active_tool == "text":
            self.text_btn.config(bg=active_color)
        elif self.active_tool == "arrow":
            self.arrow_btn.config(bg=active_color)
        elif self.active_tool == "rect":
            self.rect_btn.config(bg=active_color)
        elif self.active_tool == "line":
            self.line_btn.config(bg=active_color)

        # Para garantir que a mudança seja visível, atualizar a UI
        self.window.update_idletasks()
    
    def _choose_color(self):
        """Abre o seletor de cor."""
        # Não há necessidade de desabilitar a janela do editor
        color = colorchooser.askcolor(initialcolor=self.color, parent=self.window)
        if color[1]:
            self.color = color[1]
            # Atualizar a amostra de cor
            self.color_sample.config(bg=self.color)
            
            # Atualizar e salvar a configuração global
            from src.config.config import ANNOTATION_COLOR, save_config
            # Atualizar variável global diretamente no módulo config
            import src.config.config as config_module
            config_module.ANNOTATION_COLOR = self.color
            
            print(f"Nova cor selecionada: {self.color}")
            save_config()
        
        # Garantir que o foco retorne para a janela do editor
        self.window.focus_force()
    
    def _choose_font(self):
        """Abre o diálogo de configuração de fonte."""
        # Lista de fontes disponíveis
        font_families = ["Arial", "Helvetica", "Times", "Courier", "Verdana"]
        
        # Criar uma janela de diálogo personalizada
        font_dialog = tk.Toplevel(self.window)
        font_dialog.title("Configurações de Fonte")
        font_dialog.geometry("250x150")
        font_dialog.transient(self.window)  # Vincula a janela de diálogo à janela principal
        font_dialog.grab_set()  # Torna o diálogo modal

        # Adicionar ícone
        icon_path = ICON
        if getattr(sys, 'frozen', False):
            icon_path = os.path.join(sys._MEIPASS, ICON)
        font_dialog.iconbitmap(icon_path)
        
        # Centralizar o diálogo em relação à janela principal
        font_dialog.update_idletasks()  # Atualiza o tamanho da janela
        dialog_width = font_dialog.winfo_width()
        dialog_height = font_dialog.winfo_height()
        
        # Obter a posição e o tamanho da janela principal
        parent_x = self.window.winfo_rootx()
        parent_y = self.window.winfo_rooty()
        parent_width = self.window.winfo_width()
        parent_height = self.window.winfo_height()
        
        # Calcular a posição centralizada
        x = parent_x + (parent_width - dialog_width) // 2
        y = parent_y + (parent_height - dialog_height) // 2
        
        # Aplicar a posição centralizada
        font_dialog.geometry(f"+{x}+{y}")
        
        # Frame principal
        frame = ttk.Frame(font_dialog, padding=10)
        frame.pack(fill=tk.BOTH, expand=True)
        
        # Família da fonte
        ttk.Label(frame, text="Família:").grid(row=0, column=0, sticky=tk.W, pady=5)
        family_var = tk.StringVar(value=self.font_family)
        family_combo = ttk.Combobox(frame, textvariable=family_var, values=font_families)
        family_combo.grid(row=0, column=1, sticky=tk.W, pady=5)
        
        # Tamanho da fonte
        ttk.Label(frame, text="Tamanho:").grid(row=1, column=0, sticky=tk.W, pady=5)
        size_var = tk.IntVar(value=self.font_size)
        size_spinbox = ttk.Spinbox(frame, from_=8, to=256, textvariable=size_var, width=5)
        size_spinbox.grid(row=1, column=1, sticky=tk.W, pady=5)
        
        # Botões
        btn_frame = ttk.Frame(frame)
        btn_frame.grid(row=2, column=0, columnspan=2, pady=10)
        
        ttk.Button(btn_frame, text="Cancelar", 
                 command=font_dialog.destroy).pack(side=tk.LEFT, padx=5)
        
        def apply_font():
            self.font_family = family_var.get()
            self.font_size = size_var.get()
            font_dialog.destroy()
            
            # Atualizar variáveis globais diretamente no módulo config
            import src.config.config as config_module
            config_module.ANNOTATION_FONT_FAMILY = self.font_family
            config_module.ANNOTATION_FONT_SIZE = self.font_size
            
            print(f"Nova fonte selecionada: {self.font_family}, tamanho: {self.font_size}")
            from src.config.config import save_config
            save_config()
            
        ttk.Button(btn_frame, text="Aplicar", 
                 command=apply_font).pack(side=tk.RIGHT, padx=5)
        
        # Esperar que o diálogo seja fechado
        self.window.wait_window(font_dialog)
    
    def _delete_selected(self):
        """Remove a anotação selecionada."""
        if not self.current_item:
            return
            
        # Encontrar a anotação correspondente ao item atual
        for i, annotation in enumerate(self.annotations):
            if annotation.item_id == self.current_item:
                # Remover do canvas
                self.canvas.delete(self.current_item)
                # Remover da lista
                self.annotations.pop(i)
                # Resetar o item atual
                self.current_item = None
                return
    
    def _clear_annotations(self):
        """Remove todas as anotações."""
        if not self.annotations:
            return
            
        # Manter a referência da posição atual da janela
        window_x = self.window.winfo_x()
        window_y = self.window.winfo_y()
        
        # Exibir a caixa de diálogo com parent
        if messagebox.askyesno("Confirmar", "Tem certeza que deseja remover todas as anotações?", parent=self.window):
            # Remover do canvas
            for annotation in self.annotations:
                if annotation.item_id:
                    self.canvas.delete(annotation.item_id)
            
            # Limpar a lista
            self.annotations = []
            self.current_item = None
            
            # Adicionar ao histórico após limpar
            self._add_to_history()
        
        # Forçar a janela de volta para o primeiro plano após a caixa de diálogo
        self.window.lift()
        self.window.focus_force()
        
        # Reposicionar a janela se necessário
        if window_x and window_y:
            self.window.geometry(f"+{window_x}+{window_y}")

    def _on_press(self, event):
        """Manipula o evento de pressionar o botão do mouse."""
        # Converter coordenadas do canvas
        canvas_x = self.canvas.canvasx(event.x)
        canvas_y = self.canvas.canvasy(event.y)
        
        # Converter para coordenadas da imagem original
        x = canvas_x / self.zoom_factor
        y = canvas_y / self.zoom_factor
        
        # Salvar posição inicial
        self.start_x = x
        self.start_y = y
        
        if self.active_tool == "select":
            # Verificar se clicou em algum item
            # Ajustar a área de tolerância de clique baseado no zoom
            tolerance = 5 / self.zoom_factor
            items = self.canvas.find_overlapping(
                canvas_x-tolerance, canvas_y-tolerance, 
                canvas_x+tolerance, canvas_y+tolerance
            )
            if items:
                # Filtrar para não selecionar a imagem de fundo
                filtered_items = [item for item in items if item != self.image_item]
                if filtered_items:
                    self.current_item = filtered_items[0]
                    # Destacar o item selecionado
                    self._highlight_item(self.current_item)
                    
                    # Removida a chamada direta para edição de texto aqui
                    # para permitir movimentação do texto
                else:
                    self.current_item = None
            else:
                self.current_item = None
        
        elif self.active_tool == "text":
            # Desabilitar todos os widgets da janela antes de abrir o diálogo
            for widget in self.window.winfo_children():
                if isinstance(widget, ttk.Frame):
                    for child in widget.winfo_children():
                        if isinstance(child, (ttk.Button, ttk.Entry)):
                            child.configure(state='disabled')
        
            # Usar nossa caixa de diálogo personalizada com texto inicial vazio
            text_dialog = TextInputDialog(self.window, "Adicionar Texto", initial_text="")
            text = text_dialog.result
            
            # Reabilitar todos os widgets da janela após fechar o diálogo
            for widget in self.window.winfo_children():
                if isinstance(widget, ttk.Frame):
                    for child in widget.winfo_children():
                        if isinstance(child, (ttk.Button, ttk.Entry)):
                            child.configure(state='normal')
        
            if text:
                # Criar uma nova anotação de texto com coordenadas originais
                properties = {
                    'x': x,
                    'y': y,
                    'text': text,
                    'color': self.color,
                    'font_family': self.font_family,
                    'font_size': self.font_size,
                    'anchor': tk.NW
                }
                
                # Criar o item no canvas (usando coordenadas de canvas)
                font_size_zoomed = int(self.font_size * self.zoom_factor)
                item_id = self.canvas.create_text(
                    canvas_x, canvas_y, 
                    text=text, 
                    fill=self.color,
                    font=(self.font_family, font_size_zoomed),
                    anchor=tk.NW
                )
                
                # Adicionar à lista de anotações (com coordenadas originais)
                self.annotations.append(AnnotationElement("text", properties, item_id))
                
                # Adicionar ao histórico após criar texto
                self._add_to_history()
                
        elif self.active_tool in ["arrow", "rect", "line"]:
            # Criar um item temporário (usando coordenadas de canvas)
            if self.active_tool == "arrow":
                self.temp_item = self.canvas.create_line(
                    canvas_x, canvas_y, canvas_x, canvas_y, 
                    fill=self.color, 
                    width=2,
                    arrow=tk.LAST
                )
            elif self.active_tool == "rect":
                self.temp_item = self.canvas.create_rectangle(
                    canvas_x, canvas_y, canvas_x, canvas_y, 
                    outline=self.color, 
                    width=2
                )
            elif self.active_tool == "line":
                self.temp_item = self.canvas.create_line(
                    canvas_x, canvas_y, canvas_x, canvas_y, 
                    fill=self.color, 
                    width=2
                )
    
    def _on_drag(self, event):
        """Manipula o evento de arrastar o mouse."""
        # Converter coordenadas do canvas
        canvas_x = self.canvas.canvasx(event.x)
        canvas_y = self.canvas.canvasy(event.y)
        
        # Converter para coordenadas da imagem original
        x = canvas_x / self.zoom_factor
        y = canvas_y / self.zoom_factor
        
        if self.active_tool == "select" and self.current_item:
            # Mover o item selecionado
            dx = (x - self.start_x) * self.zoom_factor
            dy = (y - self.start_y) * self.zoom_factor
            
            self.canvas.move(self.current_item, dx, dy)
            
            # Atualizar a posição inicial para o próximo movimento
            self.start_x = x
            self.start_y = y
            
            # Atualizar as propriedades da anotação (usando coordenadas originais)
            self._update_annotation_position(self.current_item, dx/self.zoom_factor, dy/self.zoom_factor)
            
        elif self.active_tool in ["arrow", "rect", "line"] and self.temp_item:
            # Calcular as coordenadas de início em canvas
            start_canvas_x = self.start_x * self.zoom_factor
            start_canvas_y = self.start_y * self.zoom_factor
            
            # Atualizar o item temporário (usando coordenadas de canvas)
            if self.active_tool == "arrow" or self.active_tool == "line":
                self.canvas.coords(self.temp_item, start_canvas_x, start_canvas_y, canvas_x, canvas_y)
            elif self.active_tool == "rect":
                self.canvas.coords(self.temp_item, start_canvas_x, start_canvas_y, canvas_x, canvas_y)
    
    def _on_release(self, event):
        """Manipula o evento de soltar o botão do mouse."""
        # Converter coordenadas do canvas
        canvas_x = self.canvas.canvasx(event.x)
        canvas_y = self.canvas.canvasy(event.y)
        
        # Converter para coordenadas da imagem original
        x = canvas_x / self.zoom_factor
        y = canvas_y / self.zoom_factor
        
        if self.active_tool in ["arrow", "rect", "line"] and self.temp_item:
            # Finalizar o item temporário usando coordenadas originais
            if self.active_tool == "arrow":
                properties = {
                    'x1': self.start_x,
                    'y1': self.start_y,
                    'x2': x,
                    'y2': y,
                    'color': self.color,
                    'width': 2
                }
                self.annotations.append(AnnotationElement("arrow", properties, self.temp_item))
                
            elif self.active_tool == "rect":
                properties = {
                    'x1': self.start_x,
                    'y1': self.start_y,
                    'x2': x,
                    'y2': y,
                    'color': self.color,
                    'width': 2
                }
                self.annotations.append(AnnotationElement("rect", properties, self.temp_item))
                
            elif self.active_tool == "line":
                properties = {
                    'x1': self.start_x,
                    'y1': self.start_y,
                    'x2': x,
                    'y2': y,
                    'color': self.color,
                    'width': 2
                }
                self.annotations.append(AnnotationElement("line", properties, self.temp_item))
            
            # Resetar o item temporário
            self.temp_item = None
            
            # Adicionar ao histórico após cada operação
            self._add_to_history()
    
    def _update_annotation_position(self, item_id, dx, dy):
        """Atualiza a posição da anotação na lista após ser movida."""
        for annotation in self.annotations:
            if annotation.item_id == item_id:
                if annotation.type == "text":
                    annotation.properties['x'] += dx
                    annotation.properties['y'] += dy
                elif annotation.type in ["arrow", "rect", "line"]:
                    annotation.properties['x1'] += dx
                    annotation.properties['y1'] += dy
                    annotation.properties['x2'] += dx
                    annotation.properties['y2'] += dy
                break
    
    def _highlight_item(self, item_id):
        """Destaca o item selecionado."""
        # Implementação básica de destaque (pode ser melhorada)
        # Verifique se é um texto para mostrar uma dica visual de que pode ser editado
        annotation = self._get_annotation_by_item_id(item_id)
        if annotation and annotation.type == "text":
            # Mostrar uma dica na barra de status ou em um tooltip
            # Você pode adicionar uma mensagem como "Clique duplo para editar"
            pass
    
    def _on_cancel(self):
        """Cancela a edição e fecha a janela."""
        self.window.destroy()
    
    def _on_save(self):
        """Salva as anotações e mantém a janela aberta."""
        try:
            # Preparar dados para salvar
            annotations_data = []
            
            # Converter todas as anotações para coordenadas absolutas (sem zoom)
            for annotation in self.annotations:
                # Criar uma cópia das propriedades para não modificar o original
                annotation_data = annotation.to_dict()
                
                # Garantir que estamos salvando coordenadas absolutas
                annotations_data.append(annotation_data)
            
            # Salvar as anotações
            self.annotation_manager.save_annotations(self.image_path, annotations_data)
            
            # Mostrar confirmação temporária sem fechar a janela
            messagebox.showinfo("Sucesso", "Anotações salvas com sucesso!", parent=self.window)
            self.window.lift()
            
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao salvar anotações: {str(e)}")
    
    def _on_next_image(self):
        """Navega para a próxima imagem se disponível."""
        if self.navigator.has_next():
            self.navigator.next_image()
            self._reload_with_new_image()

    def _on_prev_image(self):
        """Navega para a imagem anterior se disponível."""
        if self.navigator.has_prev():
            self.navigator.prev_image()
            self._reload_with_new_image()

    def _reload_with_new_image(self):
        """
        Recarrega o editor de imagem com base no novo índice,
        mantendo a mesma janela aberta.
        """
        self.image_path = self.navigator.get_current_image()
        self._clear_state_and_reload()
        self._update_image_index_label()

    def _clear_state_and_reload(self):
        if self.canvas:
            self.canvas.delete("all")
        self.annotations = []
        self._load_annotations()
        self._load_image()
        self._render_annotations()
        self._add_to_history()
        self._add_to_history()

    def _update_image_index_label(self):
        """Atualiza o texto que mostra o índice atual da imagem."""
        current = self.navigator.current_index + 1
        total = self.navigator.get_image_count()
        self.image_index_label.config(text=f"Imagem {current} / {total}")

    def update_image_list(self, image_paths, current_index=None):
        """Atualiza a lista de imagens e o índice atual dinamicamente."""
        self.image_paths = image_paths
        self.navigator.image_paths = image_paths
        if current_index is not None:
            self.navigator.current_index = current_index
        # Atualiza o label de índice, se necessário
        if hasattr(self, 'image_index_label'):
            self._update_image_index_label()

    def _get_annotation_by_item_id(self, item_id):
        """Retorna a anotação correspondente ao ID do item."""
        for annotation in self.annotations:
            if annotation.item_id == item_id:
                return annotation
        return None

    def _edit_text_annotation(self, annotation):
        """Abre um diálogo para editar o texto de uma anotação existente."""
        if annotation.type != "text":
            return
            
        # Desabilitar temporariamente a janela do editor para manter a modalidade
        self.window.attributes('-disabled', True)
        
        try:
            # Guardar uma referência à janela atual para garantir foco correto depois
            current_window = self.window
            
            # Abrir diálogo de edição com o texto atual
            text_dialog = TextInputDialog(
                self.window, 
                "Editar Texto", 
                initial_text=annotation.properties['text']
            )
            
            # Obter o novo texto
            edited_text = text_dialog.result
            
            if edited_text is not None and edited_text != annotation.properties['text']:
                # Atualizar o texto na anotação
                annotation.properties['text'] = edited_text
                
                # Se o texto não tiver uma largura definida, definir uma padrão para quebra de linha
                if 'width' not in annotation.properties:
                    annotation.properties['width'] = 300  # Largura padrão em pixels
                
                # Atualizar o texto no canvas
                canvas_x = annotation.properties['x'] * self.zoom_factor
                canvas_y = annotation.properties['y'] * self.zoom_factor
                font_size_zoomed = int(annotation.properties.get('font_size', self.font_size) * self.zoom_factor)
                
                # Remover o item antigo
                self.canvas.delete(annotation.item_id)
                
                # Criar o novo item com o texto atualizado
                new_item_id = self.canvas.create_text(
                    canvas_x, canvas_y,
                    text=edited_text,
                    fill=annotation.properties['color'],
                    font=(annotation.properties.get('font_family', self.font_family), font_size_zoomed),
                    anchor=annotation.properties.get('anchor', tk.NW),
                    width=annotation.properties['width'] * self.zoom_factor  # Aplicar largura para quebra de linha
                )
                
                # Atualizar o ID do item na anotação
                annotation.item_id = new_item_id
                
                # Adicionar ao histórico após editar texto
                self._add_to_history()
        finally:
            # Reabilitar a janela do editor após o diálogo ser fechado
            self.window.attributes('-disabled', False)
            
            # Corrigir o problema de foco da janela usando after para dar tempo ao sistema
            self.window.after(100, lambda: self._restore_window_focus())
    
    def _restore_window_focus(self):
        """Restaura o foco na janela principal corretamente."""
        # Trazer a janela do editor para a frente novamente
        self.window.lift()
        # Garantir que o foco retorne para a janela do editor
        self.window.focus_force()
        
        # Em alguns sistemas, a janela precisa ser destacada antes de receber foco novamente
        self.window.attributes('-topmost', True)
        self.window.update()
        self.window.attributes('-topmost', False)
