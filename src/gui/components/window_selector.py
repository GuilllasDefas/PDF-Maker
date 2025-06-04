import os
import sys
import tkinter as tk
from tkinter import messagebox
import threading
import time
from typing import Dict, Any, Optional
import queue

# Importação para gerenciar janelas
try:
    import pygetwindow as gw
    import pyautogui
except ImportError:
    import subprocess
    messagebox.showinfo("Instalando dependência", "Instalando bibliotecas necessárias...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pygetwindow", "pyautogui"])
    import pygetwindow as gw
    import pyautogui

class WindowSelector:
    """Classe para seleção direta de janela por mouse hover"""
    def __init__(self, parent=None):
        self.parent = parent
        self.result = None
        self.running = False
        self.command_queue = queue.Queue()  # Para comunicação entre threads
        
    def select_window(self) -> Optional[Dict[str, Any]]:
        """Inicia o processo de seleção direta por mouse"""
        # Encontrar e minimizar a janela principal do aplicativo
        main_app_window = None
        for window in gw.getWindowsWithTitle("PDF Maker"):
            if "PDF Maker" in window.title:
                main_app_window = window
                # Guarde o estado para restaurar depois
                main_app_visible = window.visible
                if main_app_visible:
                    window.minimize()
                break
        
        # Criar uma pequena janela de instrução
        instrucao = tk.Toplevel()
        instrucao.title("Selecionar Janela")
        instrucao.geometry("400x80")
        instrucao.attributes("-topmost", True)
        instrucao.configure(bg="#333333")
        
        # Armazenar IDs das nossas próprias janelas para ignorá-las
        self.own_windows = set()
        self.own_windows.add(instrucao.winfo_id())
        
        # Armazenar também o título da nossa aplicação principal para ignorar
        self.main_app_title = "PDF Maker"
        
        # Mensagem de instrução
        tk.Label(
            instrucao, 
            text="Mova o mouse sobre a janela desejada e clique para selecionar\nPressione ESC para cancelar",
            font=("Arial", 10, "bold"),
            fg="white",
            bg="#333333"
        ).pack(pady=10)
        
        # Centralizar na tela
        instrucao.update_idletasks()
        x = (instrucao.winfo_screenwidth() - 400) // 2
        y = 30  # Posicionar no topo da tela
        instrucao.geometry(f"+{x}+{y}")
        
        # Criar destaque e tooltip no thread principal (evita erros de Tkinter)
        destaque = tk.Toplevel()
        destaque.overrideredirect(True)
        destaque.attributes("-topmost", True)
        destaque.attributes("-alpha", 0.8)
        destaque.configure(bg="red")
        
        # Adicionar à lista de janelas próprias
        self.own_windows.add(destaque.winfo_id())
        
        # Frame interno sem padding fixo
        frame_interno = tk.Frame(destaque, bg="#f0f0f0")
        frame_interno.pack(fill=tk.BOTH, expand=True, padx=3, pady=3)
        
        # Esconder inicialmente
        destaque.withdraw()
        
        # Tooltip
        tooltip = tk.Toplevel()
        tooltip.overrideredirect(True)
        tooltip.attributes("-topmost", True)
        tooltip.configure(bg="black")
        
        # Adicionar à lista de janelas próprias
        self.own_windows.add(tooltip.winfo_id())
        
        label_tooltip = tk.Label(
            tooltip, 
            text="", 
            fg="white", 
            bg="black",
            font=("Arial", 10),
            padx=8, pady=4
        )
        label_tooltip.pack()
        
        # Esconder inicialmente
        tooltip.withdraw()
        
        # Função para processar comandos da thread
        def check_queue():
            try:
                while not self.command_queue.empty():
                    cmd, *args = self.command_queue.get_nowait()
                    
                    if cmd == "update_highlight":
                        # Atualizar destaque
                        left, top, width, height = args
                        borda = 3
                        destaque.geometry(f"{width+borda*2}x{height+borda*2}+{left-borda}+{top-borda}")
                        destaque.deiconify()
                        
                    elif cmd == "update_tooltip":
                        # Atualizar tooltip
                        text, x, y = args
                        label_tooltip.config(text=text)
                        
                        # Ajustar posição
                        screen_width = tooltip.winfo_screenwidth()
                        tooltip_width = len(text) * 7
                        tooltip_x = x + 15
                        
                        if tooltip_x + tooltip_width > screen_width:
                            tooltip_x = screen_width - tooltip_width - 20
                            
                        tooltip.geometry(f"+{tooltip_x}+{y+15}")
                        tooltip.deiconify()
                        
                    elif cmd == "hide_all":
                        # Esconder ambos
                        destaque.withdraw()
                        tooltip.withdraw()
                        
                    elif cmd == "finish":
                        # Encerrar
                        self.running = False
                        instrucao.destroy()
                        destaque.destroy()
                        tooltip.destroy()
                        return  # Parar de verificar a fila
            except Exception as e:
                print(f"Erro ao processar comandos: {e}")
                
            # Continuar verificando enquanto estiver rodando
            if self.running:
                instrucao.after(50, check_queue)
        
        # Função para cancelar a seleção
        def cancelar(event=None):
            print("Cancelando seleção de janela...")
            self.result = None
            self.running = False
            # Limpar e fechar
            if instrucao.winfo_exists():
                instrucao.destroy()
            if destaque.winfo_exists():
                destaque.destroy()
            if tooltip.winfo_exists():
                tooltip.destroy()
        
        # Associar tecla ESC para cancelar - melhorado para funcionar em todas as janelas
        instrucao.bind("<Escape>", cancelar)
        destaque.bind("<Escape>", cancelar)
        tooltip.bind("<Escape>", cancelar)
        
        # Também associar o ESC globalmente durante a seleção
        keyboard_hook = None
        try:
            import keyboard
            # Função para verificar se ESC foi pressionado globalmente
            def global_esc_handler(e):
                if e.name == 'escape':
                    print("ESC pressionado globalmente")
                    if self.running:
                        self.command_queue.put(("finish",))
                        self.running = False
                        self.result = None
                        return False  # Parar propagação do evento
            
            # Registrar o hook
            keyboard_hook = keyboard.hook(global_esc_handler)
        except ImportError:
            print("Biblioteca keyboard não disponível para ESC global")
        
        # Iniciar thread de detecção
        self.running = True
        thread = threading.Thread(target=self._monitorar_mouse, daemon=True)
        thread.start()
        
        # Iniciar processamento de comandos
        check_queue()
        
        try:
            # Aguardar até que a janela seja fechada
            instrucao.wait_window(instrucao)
        finally:
            # Garantir que o hook do teclado seja removido
            if keyboard_hook:
                try:
                    keyboard.unhook(keyboard_hook)
                except:
                    pass
        
        # Restaurar a janela principal
        if main_app_window and main_app_visible:
            try:
                main_app_window.restore()
            except:
                pass  # Ignorar erros ao tentar restaurar
                
        return self.result
    
    def _monitorar_mouse(self):
        """Monitora o mouse para detectar janelas e cliques"""
        # Desativar failsafe do pyautogui
        original_failsafe = pyautogui.FAILSAFE
        pyautogui.FAILSAFE = False
        
        last_window = None
        try:
            # Monitorar enquanto estiver ativo
            while self.running:
                try:
                    # Verificar ESC diretamente
                    try:
                        import keyboard
                        if keyboard.is_pressed('escape'):
                            print("ESC detectado durante monitoramento")
                            self.result = None
                            self.running = False
                            self.command_queue.put(("finish",))
                            break
                    except:
                        pass
                    
                    # Obter posição do mouse
                    x, y = pyautogui.position()
                    
                    # Detectar janela sob o cursor
                    window = self._obter_janela_na_posicao(x, y)
                    
                    if window:
                        # Se for diferente da última
                        if not last_window or window['handle'] != last_window['handle']:
                            # Atualizar destaque
                            self.command_queue.put((
                                "update_highlight", 
                                window['left'], window['top'], 
                                window['width'], window['height']
                            ))
                            
                            # Atualizar tooltip
                            self.command_queue.put((
                                "update_tooltip",
                                window['title'], x, y
                            ))
                            
                            last_window = window
                    else:
                        # Esconder quando não há janela
                        if last_window:
                            self.command_queue.put(("hide_all",))
                            last_window = None
                    
                    # Verificar clique (só processa quando temos uma janela)
                    if last_window and self._verificar_clique_mouse():
                        # Usuário selecionou a janela
                        self.result = last_window
                        self.command_queue.put(("finish",))
                        break
                        
                    # Pequena pausa para não sobrecarregar
                    time.sleep(0.05)
                    
                except Exception as e:
                    print(f"Erro durante monitoramento: {e}")
                    time.sleep(0.1)
        
        except Exception as e:
            print(f"Erro geral no monitoramento: {e}")
        finally:
            # Restaurar configuração
            pyautogui.FAILSAFE = original_failsafe
    
    def _verificar_clique_mouse(self) -> bool:
        """Verifica se o usuário clicou com o mouse"""
        try:
            # No Windows, usar win32api para detecção mais confiável
            if sys.platform == 'win32':
                try:
                    # Tentar primeiro com win32api (mais confiável)
                    import win32api
                    state_left = win32api.GetKeyState(0x01)
                    clicked = state_left < 0  # Pressionado se negativo
                    
                    if clicked:
                        # Confirmar com pequeno delay para evitar falsos positivos
                        time.sleep(0.05)
                        state_left = win32api.GetKeyState(0x01)
                        return state_left < 0
                    return False
                    
                except ImportError:
                    # Fallback para pyautogui se win32api não estiver disponível
                    clicked = pyautogui.mouseDown()
                    if clicked:
                        time.sleep(0.05)  # Pequeno delay
                        return pyautogui.mouseDown()  # Confirmar que ainda está pressionado
                    return False

        except Exception as e:
            print(f"Erro ao verificar clique: {e}")
            return False
    
    def _obter_janela_na_posicao(self, x, y) -> Optional[Dict[str, Any]]:
        """Obtém a janela na posição do cursor"""
        try:
            # Obter todas as janelas visíveis
            windows = gw.getAllWindows()
            
            # Filtrar janelas válidas e ordenar por z-order (primeiras são mais visíveis)
            janelas_candidatas = []
            
            for window in windows:
                # Verificar se é uma janela válida e está sob o cursor
                if (window.visible and 
                    window.title and window.title.strip() and
                    window.left <= x <= window.left + window.width and
                    window.top <= y <= window.top + window.height):
                    
                    # Ignorar nossas próprias janelas de seleção
                    if hasattr(self, 'own_windows') and window._hWnd in self.own_windows:
                        continue
                    
                    # Ignorar a aplicação principal do PDF Maker
                    if hasattr(self, 'main_app_title') and self.main_app_title in window.title:
                        continue
                        
                    # Ignorar janelas do tkinter com títulos padrão
                    if window.title in ["tk", "toplevel"]:
                        continue
                    
                    # Adicionar à lista de candidatas
                    janelas_candidatas.append({
                        'title': window.title,
                        'handle': window._hWnd,
                        'left': window.left,
                        'top': window.top,
                        'width': window.width,
                        'height': window.height,
                        'visible': window.visible
                    })
            
            # Debug - mostrar todas as janelas encontradas
            if janelas_candidatas:
                print(f"Janelas sob o cursor ({x},{y}) - Excluindo 'PDF Maker':")
                for i, j in enumerate(janelas_candidatas):
                    print(f"  {i+1}. {j['title']}")
            else:
                # Se não encontrou janelas, mostrar todas as disponíveis para debug
                print(f"Nenhuma janela encontrada sob o cursor. Janelas disponíveis:")
                for i, window in enumerate(windows):
                    if window.title and window.title.strip():
                        print(f"  {i+1}. {window.title} - Visível: {window.visible}, Posição: {window.left},{window.top} até {window.left+window.width},{window.top+window.height}")
            
            # Retornar a primeira janela (mais visível devido à ordem Z)
            return janelas_candidatas[0] if janelas_candidatas else None
            
        except Exception as e:
            print(f"Erro ao verificar janela: {e}")
            return None
