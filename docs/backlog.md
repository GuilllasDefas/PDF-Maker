# Melhorias e Funcionalidades para PDF Maker

# Correções

## Editor de Imagens

- Gerar PDF com textos com acentos acaba gerando um caractere estranho

---

## Funcionalidades a Adicionar

- **Capturas de Tela**
  - Permitir capturas básicas de tela: opção para capturar tela inteira ou janela específica.
  - Em automações, deveria haver uma label (invisível para a captura) que mostra:
    - Tempo para iniciar a captura
    - Quantidade de capturas restantes
    - Tempo para começar a automação (Se for maior que 0)
    - Tempo total para concluir a automação (Se houver, e for maior que 0)
    - Qual Ação entre as capturas (Se houver alguma ação)

- **Editor de Sessão**
  - No Teste do Redimensionamento Dinâmico de Miniaturas, ocorre um delay de 1 segundo para atualizar o número de miniaturas por linha.

- **Editor de Imagem**
  - Ao adicionar um texto, a Janela de texto não permite quebra de linha (Seria melhor adicionar o texto na própria imagem, ao invés de usar Janela).
  - Ao editar ordem, não há opção de Salvar a ordem, apenas de Gerar PDF, dessa forma se sair e voltar, a versão original volta.
  - A configuração de texto deve ser feita abaixo na própria Janela do texto para uma melhor experiência e o mesmo para as demais anotações
  - Em "Texto" adicionar opção de cabeçalho e rodapé a marge da imagem na edição.
  - Adicionar opção de Recortar Imagem (ex: cortar para manter apenas a área selecionada).
  - Ferramenta de Seleção, ao selecionar, deve fazer um retângulo ao redor da área selecionada para feedback visual.
  - Aumentar espessura das Formas
  - Pode haver na Janela o próprio número da ordem da imagem para facilitar a modificação da ordem se o usuário quiser.
  - Editar itens e anotações, ou seja, rotacionar, redimensionar, mudar cor e etc.

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

- **Sobre**
  - Integrar Melhorias e correções no botão sobre

---

## Observações

- Manter este documento atualizado conforme as tarefas forem concluídas ou novas demandas surgirem.
