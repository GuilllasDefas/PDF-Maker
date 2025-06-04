# PDF Maker

PDF Maker é um aplicativo desktop para Windows que permite capturar screenshots de forma manual ou automática, organizá-las e gerar arquivos PDF a partir dessas imagens. Ele oferece recursos como presets de automação, atalhos de teclado configuráveis e gerenciamento de sessões de captura.

## Funcionalidades

- Captura de screenshots (manual ou automática)
- Organização de imagens por sessões (pastas)
- Geração de PDF a partir das imagens capturadas
- Presets de automação personalizáveis
- Atalhos de teclado configuráveis
- Interface gráfica amigável (Tkinter)
- Verificação automática de atualizações

## Requisitos

- Python 3.8 ou superior (Foi utilizado Python 3.12)
- Windows (recomendado)
- Dependências listadas em `requirements.txt`

## Instalação

1. Clone este repositório:

   ```bash
   git clone https://github.com/GuilllasDefas/PDF-Maker.git
   cd PDF_Maker
   ```

2. Instale as dependências:

   ```bash
   pip install -r requirements.txt
   ```

## Como usar

1. Execute o aplicativo:

   ```bash
   python main.py
   ```

2. Na interface:
   - Selecione um diretório para salvar as imagens e PDFs.
   - Use os botões ou atalhos para capturar screenshots.
   - Configure e inicie automações conforme necessário.
   - Gere o PDF a partir das imagens capturadas.

## Atalhos padrão

- Tirar Screenshot: `Ctrl+Shift+S`
- Iniciar Automação: `Ctrl+Shift+A`

(Os atalhos podem ser alterados nas configurações do aplicativo.)

## Observações

- As imagens e PDFs são salvos no diretório selecionado pelo usuário.
- O aplicativo cria subpastas para cada sessão de captura.
- Para compilar um executável, utilize o arquivo `main.spec` com o PyInstaller.

## Licença

Este projeto é distribuído sob a licença MIT.
