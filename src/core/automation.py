import time
import threading
import keyboard
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
        
        # Configurações de ações e condições de parada
        self.action_type = "none"
        self.action_key = None
        self.stop_on_key = False
        self.stop_key = None
        self.stop_after_time = False
        self.stop_time_value = 0
        self.start_delay = 0
    
    def set_callbacks(self, 
                     on_screenshot: Optional[Callable[[str], None]] = None,
                     on_status: Optional[Callable[[str], None]] = None,
                     on_finish: Optional[Callable[[], None]] = None):
        """Define callbacks para eventos da automação."""
        self.on_screenshot_callback = on_screenshot
        self.on_status_callback = on_status
        self.on_finish_callback = on_finish
    
    def set_action_between_captures(self, action_type: Optional[str], action_key: Optional[str]):
        """Define a ação a ser executada entre capturas."""
        self.action_type = action_type if action_type else "none"
        self.action_key = action_key
    
    def set_stop_conditions(self, 
                           stop_on_key: bool, 
                           stop_key: Optional[str], 
                           stop_after_time: bool, 
                           stop_time_value: Optional[float]):
        """Define as condições de parada da automação."""
        self.stop_on_key = stop_on_key
        self.stop_key = stop_key
        self.stop_after_time = stop_after_time
        self.stop_time_value = stop_time_value if stop_time_value else 0
    
    def start(self, interval: float, num_captures: int, start_delay: float = 0) -> bool:
        """Inicia a automação de capturas."""
        if self.is_running:
            return False
        
        if interval <= 0 or num_captures <= 0:
            return False
        
        self.is_running = True
        self.start_delay = start_delay
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
            
            # Configurar listener de tecla para parada
            stop_event = threading.Event()
            if self.stop_on_key and self.stop_key:
                self._setup_key_listener(stop_event)
            
            # Tempo de início para verificar limite de tempo
            start_time = time.time()
            
            # Atraso inicial
            if self.start_delay > 0:
                if self.on_status_callback:
                    self.on_status_callback(f"Status: Preparando... {self.start_delay}s")
                time.sleep(self.start_delay)
            
            for i in range(num_captures):
                if not self.is_running:
                    break
                
                # Verificar condição de parada por tempo
                if self.stop_after_time and self.stop_time_value > 0:
                    elapsed = time.time() - start_time
                    if elapsed >= self.stop_time_value:
                        if self.on_status_callback:
                            self.on_status_callback("Status: Tempo limite atingido")
                        break
                
                # Verificar se o botão de parada foi pressionado
                if stop_event.is_set():
                    if self.on_status_callback:
                        self.on_status_callback("Status: Interrompido pelo usuário")
                    break
                
                # Atualiza status
                if self.on_status_callback:
                    self.on_status_callback(f"Status: Capturando {i+1}/{num_captures}")
                
                # Captura screenshot
                img_path = self.screenshot_manager.take_screenshot()
                if img_path and self.on_screenshot_callback:
                    self.on_screenshot_callback(img_path)
                
                # Verifica se é a última captura
                if i < num_captures - 1 and self.is_running:
                    # Executa ação entre capturas
                    if self.action_type == "key" and self.action_key:
                        try:
                            keyboard.press_and_release(self.action_key)
                            time.sleep(0.1)  # Pequena pausa após pressionar tecla
                        except Exception as e:
                            print(f"Erro ao simular tecla {self.action_key}: {e}")
                    
                    # Aguarda intervalo antes da próxima captura
                    time.sleep(interval)
            
            # Finaliza
            if self.on_finish_callback:
                self.on_finish_callback()
                
        except Exception as e:
            print(f"Erro na automação: {e}")
            if self.on_status_callback:
                self.on_status_callback(f"Status: Erro - {str(e)[:30]}")
            if self.on_finish_callback:
                self.on_finish_callback()
        finally:
            self.is_running = False
    
    def _setup_key_listener(self, stop_event: threading.Event):
        """Configura um listener para a tecla de parada."""
        def key_pressed(e):
            if e.name == self.stop_key:
                stop_event.set()
                return False  # Para parar o listener
        
        # Inicia o listener em um thread separado
        listener_thread = threading.Thread(
            target=lambda: keyboard.hook(key_pressed),
            daemon=True
        )
        listener_thread.start()
