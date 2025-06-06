import os
import json
from typing import Dict, List, Any, Optional
import shutil
from PIL import Image, ImageDraw, ImageFont

class AnnotationManager:
    """Gerencia anotações para imagens sem modificar os arquivos originais."""
    def __init__(self, session_dir: str):
        self.session_dir = session_dir
        
        # Criar diretório para anotações se não existir
        self.annotations_dir = os.path.join(session_dir, ".annotations")
        os.makedirs(self.annotations_dir, exist_ok=True)
        
        # Diretório para as imagens anotadas renderizadas
        self.rendered_dir = os.path.join(session_dir, ".rendered")
        os.makedirs(self.rendered_dir, exist_ok=True)
    
    def get_annotation_file_path(self, image_path: str) -> str:
        """Retorna o caminho para o arquivo de anotações correspondente à imagem."""
        # Usar o nome da imagem como base para o arquivo de anotações
        image_name = os.path.basename(image_path)
        annotation_file = f"{image_name}.annotations.json"
        return os.path.join(self.annotations_dir, annotation_file)
    
    def get_rendered_image_path(self, image_path: str) -> str:
        """Retorna o caminho para a imagem renderizada com anotações."""
        image_name = os.path.basename(image_path)
        rendered_file = f"{image_name}.rendered.png"
        return os.path.join(self.rendered_dir, rendered_file)
    
    def has_annotations(self, image_path: str) -> bool:
        """Verifica se uma imagem possui anotações."""
        annotation_file = self.get_annotation_file_path(image_path)
        return os.path.exists(annotation_file)
    
    def save_annotations(self, image_path: str, annotations: List[Dict[str, Any]]) -> bool:
        """Salva as anotações para uma imagem."""
        try:
            annotation_file = self.get_annotation_file_path(image_path)
            
            with open(annotation_file, 'w') as f:
                json.dump(annotations, f, indent=2)
            
            # Renderizar a imagem com anotações
            self.render_annotated_image(image_path, annotations)
            
            return True
        except Exception as e:
            print(f"Erro ao salvar anotações: {e}")
            return False
    
    def load_annotations(self, image_path: str) -> List[Dict[str, Any]]:
        """Carrega as anotações para uma imagem."""
        annotation_file = self.get_annotation_file_path(image_path)
        
        if not os.path.exists(annotation_file):
            return []
        
        try:
            with open(annotation_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Erro ao carregar anotações: {e}")
            return []
    
    def remove_annotations(self, image_path: str) -> bool:
        """Remove as anotações de uma imagem."""
        try:
            annotation_file = self.get_annotation_file_path(image_path)
            rendered_file = self.get_rendered_image_path(image_path)
            
            # Remover arquivos se existirem
            if os.path.exists(annotation_file):
                os.remove(annotation_file)
                
            if os.path.exists(rendered_file):
                os.remove(rendered_file)
                
            return True
        except Exception as e:
            print(f"Erro ao remover anotações: {e}")
            return False
    
    def render_annotated_image(self, image_path: str, annotations: List[Dict[str, Any]]) -> str:
        """Renderiza uma imagem com suas anotações."""
        try:
            # Carregar a imagem original
            with Image.open(image_path) as img:
                # Criar uma cópia para não modificar a original
                annotated_img = img.copy().convert("RGBA")
                
                # Obter dimensões originais da imagem para escala
                img_width, img_height = annotated_img.size
                
                # Criar uma camada para as anotações
                draw = ImageDraw.Draw(annotated_img)
                
                # Desenhar cada anotação
                for annotation in annotations:
                    self._draw_annotation(draw, annotation, (img_width, img_height))
                
                # Salvar a imagem renderizada
                output_path = self.get_rendered_image_path(image_path)
                annotated_img.save(output_path)
                
                return output_path
        except Exception as e:
            print(f"Erro ao renderizar imagem anotada: {e}")
            return ""
    
    def _draw_annotation(self, draw: ImageDraw.Draw, annotation: Dict[str, Any], image_size: tuple):
        """Desenha uma anotação específica na imagem."""
        annotation_type = annotation.get('type')
        props = annotation.get('properties', {})
        
        # Obter dimensões da imagem para possíveis ajustes de escala
        img_width, img_height = image_size
        
        if annotation_type == "text":
            try:
                # Carregar a fonte
                font_family = props.get('font_family', 'Arial')
                font_size = props.get('font_size', 12)
                
                # Tentar carregar a fonte
                try:
                    # Usar uma lista de fontes confiáveis para fallback
                    for font_try in [font_family, 'Arial', 'DejaVuSans.ttf', 'FreeSans.ttf', 'LiberationSans-Regular.ttf']:
                        try:
                            font = ImageFont.truetype(font_try, int(font_size))
                            break
                        except:
                            continue
                    else:
                        # Se nenhuma fonte específica funcionar, usar a fonte padrão com tamanho ajustado
                        default_font = ImageFont.load_default()
                        # Ajustar o tamanho para aproximar da fonte truetype solicitada
                        # Aplicar um fator de escala para aproximar do tamanho desejado
                        scale_factor = int(font_size) / 12  # Assumindo que a fonte padrão é ~12pt
                        font = default_font.font_variant(size=int(10 * scale_factor))
                except Exception as font_error:
                    print(f"Erro ao carregar fontes: {font_error}")
                    # Último recurso - fonte padrão sem ajuste
                    font = ImageFont.load_default()
                
                # Desenhar o texto usando as coordenadas armazenadas
                draw.text(
                    (props.get('x', 0), props.get('y', 0)),
                    props.get('text', ''),
                    fill=props.get('color', 'red'),
                    font=font
                )
            except Exception as e:
                print(f"Erro ao desenhar texto: {e}")
                
        elif annotation_type == "arrow":
            # Desenhar uma linha com seta usando coordenadas absolutas
            draw.line(
                [
                    props.get('x1', 0), props.get('y1', 0),
                    props.get('x2', 0), props.get('y2', 0)
                ],
                fill=props.get('color', 'red'),
                width=props.get('width', 2)
            )
            
            # Adicionar a ponta da seta
            self._draw_arrow_head(
                draw,
                (props.get('x1', 0), props.get('y1', 0)),
                (props.get('x2', 0), props.get('y2', 0)),
                props.get('color', 'red'),
                props.get('width', 2)
            )
            
        elif annotation_type == "rect":
            # Desenhar um retângulo usando coordenadas absolutas
            draw.rectangle(
                [
                    props.get('x1', 0), props.get('y1', 0),
                    props.get('x2', 0), props.get('y2', 0)
                ],
                outline=props.get('color', 'red'),
                width=props.get('width', 2)
            )
            
        elif annotation_type == "line":
            # Desenhar uma linha usando coordenadas absolutas
            draw.line(
                [
                    props.get('x1', 0), props.get('y1', 0),
                    props.get('x2', 0), props.get('y2', 0)
                ],
                fill=props.get('color', 'red'),
                width=props.get('width', 2)
            )
    
    def _draw_arrow_head(self, draw: ImageDraw.Draw, start_point, end_point, color, width=2):
        """Desenha a ponta da seta."""
        import math
        
        # Calcular o ângulo da linha
        x1, y1 = start_point
        x2, y2 = end_point
        
        angle = math.atan2(y2 - y1, x2 - x1)
        
        # Tamanho da ponta da seta
        arrow_size = width * 4
        
        # Calcular os pontos da ponta da seta
        arrow_point1 = (
            x2 - arrow_size * math.cos(angle - math.pi/6),
            y2 - arrow_size * math.sin(angle - math.pi/6)
        )
        
        arrow_point2 = (
            x2 - arrow_size * math.cos(angle + math.pi/6),
            y2 - arrow_size * math.sin(angle + math.pi/6)
        )
        
        # Desenhar a ponta da seta
        draw.polygon([end_point, arrow_point1, arrow_point2], fill=color)
    
    def get_image_for_pdf(self, image_path: str) -> str:
        """Retorna o caminho da imagem a ser usada no PDF (original ou anotada)."""
        # Se a imagem tem anotações, usar a versão renderizada
        if self.has_annotations(image_path):
            rendered_path = self.get_rendered_image_path(image_path)
            if os.path.exists(rendered_path):
                return rendered_path
        
        # Caso contrário, usar a imagem original
        return image_path
