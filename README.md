# PDF Maker

PDF Maker é um aplicativo desktop para Windows que permite capturar screenshots de forma manual ou automática, adicionar anotações, organizar imagens em sessões e gerar arquivos PDF. Ideal para documentação, tutoriais e relatórios.

## Funcionalidades

### Captura de Screenshots

- Captura manual com atalho de teclado configurável
- Automação de capturas com intervalo configurável (milissegundos, segundos ou minutos)
- Captura de tela inteira, janela específica ou área selecionada
- Ações automatizadas entre capturas (simulação de teclas)

### Gerenciamento de Sessões

- Organização de imagens em sessões (pastas)
- Salvar sessões com nomes personalizados
- Carregar sessões anteriores
- Restauração automática da última sessão usada
- Editor de sessão para reorganizar imagens

### Anotações e Edição

- Editor de imagem integrado
- Adicionar texto com fontes e tamanhos personalizáveis
- Desenhar setas, linhas e retângulos
- Seleção de cores para anotações
- Zoom para edição precisa
- Ferramenta de seleção para mover e excluir anotações

### Geração de PDF

- Geração de PDF com todas as imagens da sessão
- Preservação de anotações no PDF final
- Tamanho de página adaptado às dimensões das imagens
- Controle da ordem das imagens no PDF

### Configurações Avançadas

- Presets de automação personalizáveis e reutilizáveis
- Atalhos de teclado configuráveis
- Condições de parada automática (tempo ou tecla)
- Opções de intervalo entre capturas

### Interface

- Interface gráfica intuitiva
- Visualização das imagens capturadas em tempo real
- Indicadores de status de automação
- Verificação automática de atualizações

## Requisitos

- Python 3.8 ou superior (Foi utilizado Python 3.12)
- Windows (recomendado)
- Dependências listadas em `requirements.txt`

## Instalação

### Instalação do executável (recomendado)

1. Baixe o instalador da [página de releases](https://github.com/GuilllasDefas/PDF-Maker/releases)
2. Execute o instalador e siga as instruções

### Instalação a partir do código-fonte

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

### Uso básico

1. Selecione um diretório para salvar as imagens e PDFs
2. Use o atalho `Ctrl+Shift+S` para capturar screenshots
3. Edite as imagens usando o botão "Editar Sessão"
4. Gere o PDF clicando no botão "Gerar PDF"

### Automação

1. Configure as opções de automação em "Ferramentas > Configurar Automação"
2. Inicie a automação com o atalho `Ctrl+Shift+A` ou pelo menu
3. A aplicação capturará screenshots automaticamente no intervalo definido

### Anotações

1. Abra o editor de sessão clicando em "Editar Sessão"
2. Selecione uma imagem e clique em "Editar"
3. Use as ferramentas disponíveis para adicionar texto, setas, linhas ou retângulos
4. Ajuste a cor, fonte e tamanho conforme necessário
5. Salve as anotações para incluí-las no PDF final

### Gerenciamento de Sessão

1. Salve a sessão atual em "Arquivo > Salvar Sessão Atual"
2. Carregue sessões salvas em "Arquivo > Carregar Sessão"
3. Inicie uma nova sessão em "Arquivo > Nova Sessão"

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
