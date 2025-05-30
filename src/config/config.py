import os

# Versão da aplicação
APP_VERSION = "1.0.0"

# Diretórios
IMAGES_DIR = "images"
SETUP_OUTPUT_DIR = "setup-output"

# Arquivos de saída
PDF_OUTPUT = "output.pdf"
TEXT_OUTPUT = "texto_extraido.txt"

# Configurações de interface
DEFAULT_WINDOW_SIZE = "800x500"
DEFAULT_IMAGE_DISPLAY_SIZE = (350, 250)

# Configurações de automação
DEFAULT_INTERVAL = 2.0
DEFAULT_NUM_CAPTURES = 10

# Configurações de DPI e qualidade
DEFAULT_DPI = 96
PDF_DPI = 96
OCR_DPI = 300

# Hotkeys
SCREENSHOT_HOTKEY = 'ctrl+shift+s'
AUTOMATION_HOTKEY = 'ctrl+alt+r'

# Configurações de OCR (ajustar conforme necessário)
POPPLER_PATH = r"C:\Program Files\poppler-24.08.0\Library\bin"
TESSERACT_CMD = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Configurações de arquivo
SUPPORTED_IMAGE_FORMATS = ['.png', '.jpg', '.jpeg']
