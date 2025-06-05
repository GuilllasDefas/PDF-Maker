from PIL import Image, ImageFile
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from typing import List
from src.config.config import DEFAULT_DPI
from tkinter import messagebox
import os

# Permite carregar imagens truncadas
ImageFile.LOAD_TRUNCATED_IMAGES = True

class PDFGenerator:
    def __init__(self, dpi: int = DEFAULT_DPI):
        self.dpi = dpi
    
    def generate_pdf(self, image_paths: List[str], output_pdf: str) -> bool:
        """
        Gera um PDF com as imagens, respeitando as dimensões originais.
        Cada página do PDF terá o tamanho da imagem correspondente.
        """
        try:
            c = canvas.Canvas(output_pdf)
            
            # Verificar se temos um gerenciador de anotações disponível
            from src.core.annotation_manager import AnnotationManager
            
            # Tentar criar um gerenciador de anotações para a pasta da sessão
            annotation_manager = None
            try:
                session_dir = os.path.dirname(image_paths[0]) if image_paths else None
                if session_dir:
                    annotation_manager = AnnotationManager(session_dir)
            except Exception as e:
                print(f"Aviso: Não foi possível criar gerenciador de anotações: {e}")
            
            # Processar cada imagem
            for img_path in image_paths:
                # Se temos um gerenciador de anotações, verificar se há versão anotada
                path_to_use = img_path
                if annotation_manager and annotation_manager.has_annotations(img_path):
                    annotated_path = annotation_manager.get_image_for_pdf(img_path)
                    if annotated_path and os.path.exists(annotated_path):
                        path_to_use = annotated_path
                
                if self._add_image_to_pdf(c, path_to_use):
                    c.showPage()
                else:
                    messagebox.showerror("Erro", f"Falha ao processar imagem: {img_path}")
            
            c.save()
            return True
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao gerar PDF: {e}")
            return False
    
    def _add_image_to_pdf(self, canvas_obj, img_path: str) -> bool:
        """Adiciona uma imagem ao PDF."""
        try:
            with open(img_path, 'rb') as f:
                img = Image.open(f)
                img.load()
                
                # Obtém dimensões em pixels
                img_width_px, img_height_px = img.size
                
                # Converte pixels para pontos
                img_width_pt = img_width_px * 72.0 / self.dpi
                img_height_pt = img_height_px * 72.0 / self.dpi
                
                # Adiciona margem
                margin = 5 * mm
                page_width = img_width_pt + 2 * margin
                page_height = img_height_pt + 2 * margin
                
                # Define o tamanho da página
                canvas_obj.setPageSize((page_width, page_height))
                
                # Desenha a imagem centralizada
                x = (page_width - img_width_pt) / 2
                y = (page_height - img_height_pt) / 2
                canvas_obj.drawImage(img_path, x, y, width=img_width_pt, height=img_height_pt)
                
                return True
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao processar imagem {img_path}: {e}")
            return False
