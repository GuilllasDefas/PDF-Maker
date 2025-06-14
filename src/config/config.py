# Versão da aplicação
APP_VERSION = "0.3.4"

# Diretórios
IMAGES_DIR = "images"
SETUP_OUTPUT_DIR = "setup-output"

# Arquivos de saída
PDF_OUTPUT = "output.pdf"
TEXT_OUTPUT = "texto_extraido.txt"

# Configurações de interface
DEFAULT_WINDOW_SIZE = "1200x700"
DEFAULT_IMAGE_DISPLAY_SIZE = (350, 250)
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

# Tenta carregar hotkeys personalizados de arquivo
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
except:
    # Em caso de erro, manter os valores padrão
    pass

# Configurações de OCR (ajustar conforme necessário)
POPPLER_PATH = r"C:\Program Files\poppler-24.08.0\Library\bin"
TESSERACT_CMD = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Configurações de arquivo
SUPPORTED_IMAGE_FORMATS = ['.png', '.jpg', '.jpeg']
