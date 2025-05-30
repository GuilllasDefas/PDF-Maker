import time
import threading
from typing import Callable, Optional
from src.core.screenshot import ScreenshotManager

class AutomationManager:
    def __init__(self, screenshot_manager: ScreenshotManager):
        self.screenshot_manager = screenshot_manager
        self.is_running = False
        self.thread: Optional[threading.Thread] = None
        self.on_screenshot_callback: Optional[Callable[[str], None]] = None
        self.on_status_callback: Optional[Callable[[str], None]] = None
        self.on_finish_callback: Optional[Callable[[], None]] = None
    
    def set_callbacks(self, 
                     on_screenshot: Optional[Callable[[str], None]] = None,
                     on_status: Optional[Callable[[str], None]] = None,
                     on_finish: Optional[Callable[[], None]] = None):
        """Define callbacks para eventos da automação."""
        self.on_screenshot_callback = on_screenshot
        self.on_status_callback = on_status
        self.on_finish_callback = on_finish
    
    def start(self, interval: float, num_captures: int) -> bool:
        """Inicia a automação de capturas."""
        if self.is_running:
            return False
        
        if interval <= 0 or num_captures <= 0:
            return False
        
        self.is_running = True
        self.thread = threading.Thread(
            target=self._run_automation,
            args=(interval, num_captures),
            daemon=True
        )
        self.thread.start()
        return True
    
    def stop(self):
        """Para a automação."""
        self.is_running = False
        if self.on_status_callback:
            self.on_status_callback("Status: Parando...")
    
    def _run_automation(self, interval: float, num_captures: int):
        """Executa o loop de automação."""
        try:
            # Verificar se o diretório está configurado
            if not self.screenshot_manager.get_base_dir():
                if not self.screenshot_manager.set_directory():
                    if self.on_status_callback:
                        self.on_status_callback("Status: Falha ao configurar diretório")
                    if self.on_finish_callback:
                        self.on_finish_callback()
                    return
                    
            for i in range(num_captures):
                if not self.is_running:
                    break
                
                # Atualiza status
                if self.on_status_callback:
                    self.on_status_callback(f"Status: Capturando {i+1}/{num_captures}")
                
                # Aguarda intervalo
                time.sleep(interval)
                
                # Captura screenshot
                img_path = self.screenshot_manager.take_screenshot()
                if img_path and self.on_screenshot_callback:
                    self.on_screenshot_callback(img_path)
                
                # Pressiona seta direita (exceto na última iteração)
                #if self.is_running and i < num_captures - 1:
                    #pyautogui.press('right')
            
            # Finaliza
            if self.on_finish_callback:
                self.on_finish_callback()
                
        except Exception as e:
            print(f"Erro na automação: {e}")
            if self.on_finish_callback:
                self.on_finish_callback()
        finally:
            self.is_running = False
