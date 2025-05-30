import os
import sys
import pyautogui
import time
from datetime import datetime
from typing import Optional
from src.config.config import IMAGES_DIR

class ScreenshotManager:
    def __init__(self, images_dir: str = IMAGES_DIR):
        # Determinar o caminho base da aplicação
        if getattr(sys, 'frozen', False):
            # Se estiver executando como um executável compilado
            application_path = os.path.dirname(sys.executable)
        else:
            # Se estiver executando do código-fonte
            application_path = os.path.dirname(os.path.abspath(__file__))
            # Voltar dois níveis (de src/core para a raiz do projeto)
            application_path = os.path.dirname(os.path.dirname(application_path))
        
        # Criar diretório de imagens em relação ao caminho base
        self.images_dir = os.path.join(application_path, 'images')
        os.makedirs(self.images_dir, exist_ok=True)
        
    def take_screenshot(self) -> Optional[str]:
        """Captura uma screenshot e salva no diretório de imagens."""
        try:
            filename = datetime.now().strftime("%Y%m%d_%H%M%S") + ".png"
            path = os.path.join(self.images_dir, filename)
            screenshot = pyautogui.screenshot()
            screenshot.save(path)
            
            # Verifica se o arquivo foi salvo corretamente
            if os.path.exists(path) and os.path.getsize(path) > 0:
                time.sleep(0.1)  # Pausa para garantir que o arquivo foi escrito
                return path
            return None
        except Exception as e:
            print(f"Erro ao salvar screenshot: {e}")
            return None
    
    def get_image_paths(self) -> list[str]:
        """Retorna lista de caminhos das imagens ordenadas."""
        try:
            files = [
                os.path.join(self.images_dir, f) 
                for f in os.listdir(self.images_dir) 
                if f.lower().endswith('.png')
            ]
            files.sort()
            return files
        except Exception as e:
            print(f"Erro ao listar imagens: {e}")
            return []
