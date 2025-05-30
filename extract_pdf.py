import fitz
from pdf2image import convert_from_path
import pytesseract
import os

# Configurar caminhos (AJUSTE ESTES VALORES!)
POPPLER_PATH = r"C:\Program Files\poppler-24.08.0\Library\bin"
TESSERACT_CMD = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def pdf_para_texto_com_ocr(caminho_pdf, saida_txt="texto_extraido.txt"):
    # Converter PDF para imagens
    imagens = convert_from_path(
        caminho_pdf, 
        dpi=300,
        poppler_path=POPPLER_PATH
    )
    
    # Configurar Tesseract
    pytesseract.pytesseract.tesseract_cmd = TESSERACT_CMD
    
    with open(saida_txt, "w", encoding="utf-8") as f:
        for i, img in enumerate(imagens):
            texto = pytesseract.image_to_string(img, lang='por')
            f.write(f"--- PÁGINA {i+1} ---\n{texto}\n\n")
            print(f"Página {i+1} processada")
    
    return f"Texto salvo em {saida_txt}"


def reconhecer_pdf(caminho):
    doc = fitz.open(caminho)
    if doc.page_count == 0:
        doc.close()
        return False
    
    try:
        pagina = doc.load_page(0)
        texto = pagina.get_text().strip()
        return bool(texto)
    finally:
        doc.close()

if __name__ == "__main__":
    caminho_pdf = "output.pdf"
    
    if reconhecer_pdf(caminho_pdf):
        print("PDF contém texto extraível - usando extração direta")
        # Adicione aqui sua lógica de extração textual
    else:
        print("PDF é imagem - usando OCR")
        pdf_para_texto_com_ocr(caminho_pdf)