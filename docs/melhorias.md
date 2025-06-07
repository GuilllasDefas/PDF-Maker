# Melhorias e Funcionalidades para PDF Maker

## Correções

- **Geral**

  - Ao salvar uma sessão pela primeira vez, a próxima vez que tenta salvar, ele pede novamente o nome da sessão, mesmo que já tenha sido salvo anteriormente.
  
  - Ao tirar prints, salvar sessão, tirar mais prints e fechar sem salvar, o programa não pergunta se deseja salvar as alterações. E ao abrir novemente ele reconhece os prints anteriores mas mostra a quantidade de prints antes de salvar a sessão.

  - Está sendo possível abrir mais de uma instância da janela Editar Sessão, o que não deveria ser possível, pois deveria ser uma janela única.

---

## Funcionalidades a Adicionar (Prioridade)

- **Capturas de Tela**
  - Permitir capturas básicas de tela: opção para capturar tela inteira ou janela específica.

- **Editor de Sessão**
  - Ao redimensionar a janela, as miniaturas continuam mostrando apenas 4 imagens por coluna, mesmo que haja espaço para mais.
    Deve ajustar o número de colunas dinamicamente com base no tamanho da janela.
  - Ao renomear uma sessão aparecem duas sessões pra carregar, a anterior e a renomeada, mas a anterior não deveria existir mais, apenas a renomeada.

- **Editor de Imagem**
  - Ao editar ordem, não há opção de Salvar a ordem, apenas de Gerar PDF, dessa forma se sair e voltar, a versão original volta.
  - Ao editar uma imagem e tentar fechar sem salvar, o programa deve perguntar se deseja salvar as alterações.
  - Destacar o botão apertado para feedback visual.
  - Em "Texto" adicionar opção de cabeçalho e rodapé a marge da imagem na edição.
  - Adicionar opção de Recortar Imagem (ex: cortar para manter apenas a área selecionada).
  - Ferramenta de Seleção, ao selecionar, deve fazer um retângulo ao redor da área selecionada para feedback visual.
  - Aumentar espessura das Formas

- **Indicador de Tempo**
  - Incluir indicador de tempo (para eventos com duração).

- **Barra de Progresso**
  - Adicionar barra de progresso (para mostrar progresso em tarefas).

- **Melhorias de UX**
  - Adicionar feedback visual ao tirar screenshot (ex: flash ou som).
  - Permitir visualização em miniatura de todas as imagens da sessão.

- **Configurações**
  - Permitir salvar e carregar configurações do usuário (ex: último preset, preferências de janela).
  - Adicionar opção de idioma (internacionalização).

- **Automação**
  - Permitir múltiplas ações entre capturas (ex: pressionar sequência de teclas).
  - Adicionar logs detalhados das automações realizadas.

---

## Observações

- Manter este documento atualizado conforme as tarefas forem concluídas ou novas demandas surgirem.
