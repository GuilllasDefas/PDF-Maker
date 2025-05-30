import os
import pyautogui
import time
from datetime import datetime
from PIL import Image, ImageFile
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

# Permite carregar imagens truncadas
ImageFile.LOAD_TRUNCATED_IMAGES = True

def save_screenshot(images_dir):
    try:
        os.makedirs(images_dir, exist_ok=True)
        filename = datetime.now().strftime("%Y%m%d_%H%M%S") + ".png"
        path = os.path.join(images_dir, filename)
        screenshot = pyautogui.screenshot()
        screenshot.save(path)
        
        # Verifica se o arquivo foi salvo corretamente
        if os.path.exists(path):
            file_size = os.path.getsize(path)
            if file_size > 0:
                # Pequena pausa para garantir que o sistema de arquivos finalizou a escrita
                time.sleep(0.1)
                return path
        return None
    except Exception as e:
        print(f"Erro ao salvar screenshot: {e}")
        return None

def get_image_paths(images_dir):
    files = [os.path.join(images_dir, f) for f in os.listdir(images_dir) if f.lower().endswith('.png')]
    files.sort()
    return files

def generate_pdf(image_paths, output_pdf):
    """
    Gera um PDF com as imagens, respeitando as dimensões originais de cada imagem.
    Cada página do PDF terá o tamanho da imagem correspondente.
    """
    from reportlab.lib.units import inch, mm
    
    # Cria o canvas sem definir um tamanho fixo de página
    c = canvas.Canvas(output_pdf)
    
    for img_path in image_paths:
        try:
            with open(img_path, 'rb') as f:
                img = Image.open(f)
                img.load()  # Carrega a imagem completamente
                
                # Obtém dimensões em pixels
                img_width_px, img_height_px = img.size
                
                # Converte pixels para pontos (1/72 de polegada, unidade padrão do ReportLab)
                # Considerando uma resolução padrão de 96 DPI para tela
                dpi = 96
                img_width_pt = img_width_px * 72.0 / dpi
                img_height_pt = img_height_px * 72.0 / dpi
                
                # Adiciona uma pequena margem para segurança (5mm em cada lado)
                margin = 5 * mm
                page_width = img_width_pt + 2 * margin
                page_height = img_height_pt + 2 * margin
                
                # Define o tamanho da página para esta imagem específica
                c.setPageSize((page_width, page_height))
                
                # Desenha a imagem na página, centralizada
                x = (page_width - img_width_pt) / 2
                y = (page_height - img_height_pt) / 2
                c.drawImage(img_path, x, y, width=img_width_pt, height=img_height_pt)
                
                # Finaliza a página
                c.showPage()
                
        except Exception as e:
            print(f"Erro ao processar imagem {img_path} para PDF: {e}")
            # Continua para a próxima imagem
    
    # Salva o PDF
    c.save()
