import os
import sys
import pyautogui
import time
import tkinter as tk
from tkinter import filedialog
from datetime import datetime
from typing import Optional, Tuple
from src.config.config import IMAGES_DIR

class ScreenshotManager:
    def __init__(self, images_dir: str = IMAGES_DIR):
        self.base_dir = None
        self.images_dir = None
        self.capture_area = None  # Para captura de área específica (x1, y1, x2, y2)
        
    def set_directory(self, base_dir: Optional[str] = None):
        """Define o diretório base para salvar arquivos."""
        if base_dir is None:
            base_dir = self._ask_user_for_directory()
        
        if base_dir:
            self.base_dir = base_dir
            # Se o diretório passado já é uma pasta de sessão, use diretamente
            # Só cria subpasta se for o diretório padrão global
            if base_dir == IMAGES_DIR:
                timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                self.images_dir = os.path.join(base_dir, f"Screenshots_{timestamp}")
            else:
                self.images_dir = base_dir
            self._ensure_directory_exists()
            return True
        return False
    
    def set_capture_area(self, area: Optional[Tuple[int, int, int, int]]):
        """Define a área de captura (x1, y1, x2, y2)"""
        self.capture_area = area
    
    def _ask_user_for_directory(self) -> str:
        """Pergunta ao usuário onde salvar as capturas de tela."""
        root = tk.Tk()
        root.withdraw()  # Esconder janela
        
        selected_folder = filedialog.askdirectory(
            title="Escolha onde salvar as capturas de tela"
        )
        
        root.destroy()
        
        if selected_folder:
            return os.path.join(selected_folder, "PDF_Maker")
        else:
            # Se cancelou, usar fallback
            import tempfile
            return os.path.join(tempfile.gettempdir(), "PDF_Maker")
        
    def _ensure_directory_exists(self):
        """Garante que o diretório de imagens existe."""
        try:
            os.makedirs(self.images_dir, exist_ok=True)
            print(f"Diretório criado/verificado: {self.images_dir}")
        except PermissionError as e:
            print(f"Erro ao criar diretório {self.images_dir}: {e}")
            # Fallback para pasta temporária
            import tempfile
            self.base_dir = os.path.join(tempfile.gettempdir(), "PDF_Maker")
            self.images_dir = os.path.join(self.base_dir, "Images")
            try:
                os.makedirs(self.images_dir, exist_ok=True)
                print(f"Usando diretório temporário: {self.images_dir}")
            except Exception as fallback_error:
                print(f"Erro crítico: não foi possível criar nenhum diretório: {fallback_error}")
                raise
        except Exception as e:
            print(f"Erro inesperado ao criar diretório: {e}")
            raise
        
    def take_screenshot(self) -> Optional[str]:
        """Captura uma screenshot e salva no diretório de imagens."""
        try:
            # Gerar timestamp para o nome do arquivo
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

            # Verificar se o diretório ainda existe antes de salvar
            if not self.images_dir or not os.path.exists(self.images_dir):
                print(f"Diretório de screenshots não definido ou não existe. Criando diretório da sessão...")
                if self.images_dir:
                    os.makedirs(self.images_dir, exist_ok=True)
                else:
                    # fallback para temporário
                    import tempfile
                    temp_base = os.path.join(tempfile.gettempdir(), "PDF_Maker")
                    self.base_dir = temp_base
                    self.images_dir = temp_base
                    os.makedirs(self.images_dir, exist_ok=True)

            # Criar o nome do arquivo com timestamp
            filename = f"screenshot_{timestamp}.png"
            path = os.path.join(self.images_dir, filename)

            # Capturar tela completa ou área específica
            if self.capture_area:
                x1, y1, x2, y2 = self.capture_area
                screenshot = pyautogui.screenshot(region=(x1, y1, x2-x1, y2-y1))
            else:
                screenshot = pyautogui.screenshot()
                
            screenshot.save(path)

            # Verifica se o arquivo foi salvo corretamente
            if os.path.exists(path) and os.path.getsize(path) > 0:
                time.sleep(0.1)  # Pausa para garantir que o arquivo foi escrito
                print(f"Screenshot salva com sucesso: {path}")
                return path
            else:
                print(f"Falha ao verificar arquivo salvo: {path}")
                return None
        except Exception as e:
            print(f"Erro ao salvar screenshot: {e}")
            return None
    
    def get_image_paths(self) -> list[str]:
        """Retorna lista de caminhos das imagens ordenadas."""
        try:
            # Verificar se o diretório existe antes de listar
            if not self.images_dir or not os.path.exists(self.images_dir):
                print(f"Diretório de imagens não definido ou não existe")
                return []
            
            files = [
                os.path.join(self.images_dir, f) 
                for f in os.listdir(self.images_dir) 
                if f.lower().endswith('.png')
            ]
            files.sort()
            print(f"Encontradas {len(files)} imagens em {self.images_dir}")
            return files
        except Exception as e:
            print(f"Erro ao listar imagens: {e}")
            return []
            
    def get_base_dir(self) -> Optional[str]:
        """Retorna o diretório base onde o PDF deve ser salvo."""
        return self.base_dir
    
    def is_temp_dir(self) -> bool:
        """Verifica se o diretório atual é temporário."""
        if not self.base_dir:
            return False
        import tempfile
        temp_dir = tempfile.gettempdir()
        return self.base_dir.startswith(temp_dir)
    
    def cleanup_temp_images(self) -> bool:
        """Limpa imagens temporárias se estiver usando diretório temporário."""
        try:
            if not self.is_temp_dir() or not self.images_dir or not os.path.exists(self.images_dir):
                return False
                
            print(f"Limpando imagens temporárias em: {self.images_dir}")
            count = 0
            
            for f in os.listdir(self.images_dir):
                if f.lower().endswith(('.png', '.jpg', '.jpeg')):
                    file_path = os.path.join(self.images_dir, f)
                    try:
                        os.remove(file_path)
                        count += 1
                    except Exception as e:
                        print(f"Erro ao remover {file_path}: {e}")
            
            print(f"Removidas {count} imagens temporárias")
            return True
        except Exception as e:
            print(f"Erro ao limpar imagens temporárias: {e}")
            return False
    
    def get_images_dir(self) -> Optional[str]:
        """Retorna o diretório onde as imagens estão armazenadas."""
        return self.images_dir
