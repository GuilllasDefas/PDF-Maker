# Versão da aplicação
APP_VERSION = "0.3.6"

# Diretórios
IMAGES_DIR = "images"
SETUP_OUTPUT_DIR = "setup-output"

# Arquivos de saída
PDF_OUTPUT = "output.pdf"
TEXT_OUTPUT = "texto_extraido.txt"

# Configurações de interface

## Tamanho da janela principal
MAIN_WINDOW_SIZE = (60, 55)
MIN_MAIN_WINDOW_SIZE = (20, 20)
DEFAULT_IMAGE_DISPLAY_SIZE = (350, 250)
DIALOG_WINDOW_SIZE = (20, 15)

## Tamanho da janela de configurar preset

PRESET_WINDOW_SIZE = (31, 55)
MIN_PRESET_WINDOW_SIZE = (20, 20)  # 20%

## Tamanho da janela do editor de sessão

SESSION_WINDOW_SIZE = (70, 60)
MIN_SESSION_WINDOW_SIZE = (20, 20)
THUMBNAIL_SIZE = (13, 18)

## Tamanho da janela de editor de imagens

IMAGE_EDITOR_DIALOG_WINDOW_SIZE = (21, 23)

## Tamanho da janela configuração de atalho

HOTKEY_WINDOW_SIZE = (30, 22)


ICON = "assets/PDF-Maker.ico"

# Configurações de automação
DEFAULT_INTERVAL = 2.0
DEFAULT_NUM_CAPTURES = 10

# Configurações de DPI e qualidade
DEFAULT_DPI = 96
PDF_DPI = 96
OCR_DPI = 300

# Hotkeys padrão
DEFAULT_SCREENSHOT_HOTKEY = 'ctrl+shift+s'
DEFAULT_AUTOMATION_HOTKEY = 'ctrl+alt+r'

# Hotkeys atuais (inicialmente são os padrões, podem ser sobrescritos)
SCREENSHOT_HOTKEY = DEFAULT_SCREENSHOT_HOTKEY
AUTOMATION_HOTKEY = DEFAULT_AUTOMATION_HOTKEY

# Configurações de OCR (ajustar conforme necessário)
POPPLER_PATH = r"C:\Program Files\poppler-24.08.0\Library\bin"
TESSERACT_CMD = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Configurações de arquivo
SUPPORTED_IMAGE_FORMATS = ['.png', '.jpg', '.jpeg']

# Configurações de anotação padrão
DEFAULT_ANNOTATION_COLOR = "#FF0000"  # Vermelho
DEFAULT_ANNOTATION_FONT_FAMILY = "Arial"
DEFAULT_ANNOTATION_FONT_SIZE = 36

# Variáveis para armazenar as configurações atuais (inicialmente são os padrões)
ANNOTATION_COLOR = DEFAULT_ANNOTATION_COLOR
ANNOTATION_FONT_FAMILY = DEFAULT_ANNOTATION_FONT_FAMILY
ANNOTATION_FONT_SIZE = DEFAULT_ANNOTATION_FONT_SIZE

# Tenta carregar configurações personalizadas de arquivo
try:
    import os
    import json
    
    config_path = os.path.join(os.path.expanduser("~"), ".pdf_maker_config.json")
    
    if os.path.exists(config_path):
        with open(config_path, 'r') as f:
            config_data = json.load(f)
            
        # Atualizar hotkeys se estiverem na configuração
        if 'screenshot_hotkey' in config_data:
            SCREENSHOT_HOTKEY = config_data['screenshot_hotkey']
        if 'automation_hotkey' in config_data:
            AUTOMATION_HOTKEY = config_data['automation_hotkey']
            
        # Carregar configurações de anotação
        if 'annotation_color' in config_data:
            ANNOTATION_COLOR = config_data['annotation_color']
        if 'annotation_font_family' in config_data:
            ANNOTATION_FONT_FAMILY = config_data['annotation_font_family']
        if 'annotation_font_size' in config_data:
            ANNOTATION_FONT_SIZE = config_data['annotation_font_size']
except:
    # Em caso de erro, manter os valores padrão
    pass

# Função para salvar configurações
def save_config():
    try:
        config_path = os.path.join(os.path.expanduser("~"), ".pdf_maker_config.json")
        
        # Carregar configurações existentes ou criar um novo dicionário
        if os.path.exists(config_path):
            with open(config_path, 'r') as f:
                config_data = json.load(f)
        else:
            config_data = {}
        
        # Atualizar com as configurações atuais
        config_data.update({
            'screenshot_hotkey': SCREENSHOT_HOTKEY,
            'automation_hotkey': AUTOMATION_HOTKEY,
            'annotation_color': ANNOTATION_COLOR,
            'annotation_font_family': ANNOTATION_FONT_FAMILY,
            'annotation_font_size': ANNOTATION_FONT_SIZE
        })
        
        # Salvar no arquivo
        with open(config_path, 'w') as f:
            json.dump(config_data, f, indent=2)
            
        return True
    except Exception as e:
        print(f"Erro ao salvar configurações: {e}")
        return False


