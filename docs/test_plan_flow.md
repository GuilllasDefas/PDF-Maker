# Plano de Testes Otimizado - PDF Maker

## Fluxos de Trabalho Integrados

Os seguintes fluxos de trabalho combinam múltiplos casos de teste em sequências que exercitam funcionalidades relacionadas simultaneamente, economizando tempo de teste.

### 1. FLUXO BÁSICO DE CAPTURA E GERAÇÃO DE PDF

**Objetivo:** Verificar o fluxo completo desde a instalação até a geração de PDF com configurações padrão.

- [x] Instalar o aplicativo e verificar ícones no menu iniciar/desktop
- [x] Abrir o aplicativo e confirmar que a interface carrega corretamente
- [x] Selecionar um diretório para salvar capturas
- [x] Capturar 3 screenshots usando o atalho padrão (Ctrl+Shift+S)
- [x] Verificar se as imagens aparecem corretamente na interface
- [x] Gerar um PDF usando o botão "Gerar PDF"
- [x] Verificar se o PDF é gerado corretamente com todas as imagens
- [x] Fechar o aplicativo e verificar se aparece diálogo de confirmação
- [x] Confirmar saída e verificar se pastas vazias são removidas
- [x] Reabrir o aplicativo e verificar se a última sessão é carregada corretamente

### 2. FLUXO DE EDIÇÃO E ANOTAÇÃO DE IMAGENS

**Objetivo:** Testar a funcionalidade de edição de sessão e imagem com anotações.

- [x] Capturar pelo menos 5 screenshots
- [x] Abrir o editor de sessão (botão "Editar Sessão")
- [x] Verificar se todas as imagens aparecem como miniaturas
- [x] Reordenar as imagens usando os campos de ordem (testar ordem 1→3 e 5→2)
- [x] Selecionar uma imagem e abrir o editor de imagem
- [x] Testar zoom in/out e navegação com barras de rolagem
- [x] Adicionar várias anotações (texto, seta, retângulo e linha)
- [x] Selecionar e mover uma anotação existente
- [x] Excluir uma anotação
- [x] Salvar as edições e verificar se retorna ao editor de sessão
- [x] Verificar se a imagem editada mostra indicador verde de anotações
- [ ] Gerar PDF e confirmar se as anotações aparecem corretamente
- [ ] Testar desfazer/refazer (Ctrl+Z/Ctrl+Y) durante edição de imagem
- [ ] Editar uma imagem com conteúdo complexo (textos e gráficos)
- [ ] Testar mudança de cor para diferentes tipos de anotação

### 3. FLUXO DE AUTOMAÇÃO E PRESETS

**Objetivo:** Verificar a criação e uso de presets de automação.

- [ ] Abrir as configurações de automação
- [ ] Criar um novo preset configurando:
  - Nome personalizado
  - 5 capturas
  - Intervalo de 2 segundos
  - Começar após 3 segundos
  - Capturar área específica (selecionar área da tela)
  - Parar após pressionar uma tecla específica
- [ ] Salvar o preset e verificar se aparece na lista
- [ ] Aplicar o preset e iniciar a automação
- [ ] Verificar se a contagem regressiva funciona
- [ ] Verificar se as capturas ocorrem no intervalo configurado
- [ ] Interromper usando a tecla configurada
- [ ] Verificar se todas as imagens foram capturadas corretamente
- [ ] Reabrir configurações e editar o preset existente
- [ ] Aplicar as mudanças e testar novamente
- [ ] Excluir o preset e confirmar que foi removido da lista
- [ ] Testar preset com captura de janela específica em vez de área
- [ ] Verificar visibilidade do overlay durante automação
- [ ] Testar automação com diferentes condições de parada

### 4. FLUXO DE SESSÕES E PERSISTÊNCIA

**Objetivo:** Testar o gerenciamento de sessões e recuperação entre execuções.

- [ ] Iniciar nova sessão
- [ ] Capturar 3 screenshots
- [ ] Salvar a sessão com nome personalizado
- [ ] Criar nova sessão e capturar 2 screenshots diferentes
- [ ] Verificar se a nova sessão tem imagens diferentes
- [ ] Usar o menu para carregar a sessão salva anteriormente
- [ ] Verificar se as imagens originais foram restauradas
- [ ] Editar uma imagem e adicionar anotações
- [ ] Fechar o aplicativo sem salvar explicitamente
- [ ] Reabrir o aplicativo e verificar se a última sessão é carregada
- [ ] Confirmar que as anotações foram preservadas
- [ ] Renomear uma sessão existente e verificar mudança no título da janela
- [ ] Gerenciar múltiplas sessões simultaneamente
- [ ] Verificar carregamento de sessão com caminhos absolutos e relativos

### 5. FLUXO DE TESTES DE ROBUSTEZ

**Objetivo:** Verificar o comportamento em condições adversas.

- [ ] Tentar salvar em um diretório sem permissões de escrita
- [ ] Capturar e editar uma imagem muito grande (>10MB)
- [ ] Adicionar muitas anotações a uma única imagem (>20)
- [ ] Tentar criar um PDF com 30+ imagens
- [ ] Realizar operações rápidas em sequência (alternar entre sessões rapidamente)
- [ ] Simular falta de espaço em disco durante salvamento
- [ ] Tentar abrir uma sessão com imagens que foram excluídas externamente
- [ ] Testar atalhos personalizados após alterá-los nas configurações
- [ ] Testar edição de imagem corrompida
- [ ] Verificar recuperação após travamento durante edição
- [ ] Simular interrupção de energia durante operação
- [ ] Testar comportamento com caracteres especiais em nomes de arquivo/pasta

### 6. FLUXO DE TESTES DAS CORREÇÕES RECENTES

**Objetivo:** Verificar especificamente as correções implementadas recentemente.

#### Teste do Redimensionamento Dinâmico de Miniaturas

- [ ] Abrir o editor de sessão com 15+ imagens
- [ ] Redimensionar a janela horizontalmente (aumentar largura)
- [ ] Verificar se o número de miniaturas por linha aumenta
- [ ] Redimensionar para uma janela estreita
- [ ] Verificar se o número de miniaturas diminui adequadamente
- [ ] Maximizar a janela e confirmar distribuição adequada
- [ ] Realizar redimensionamentos rápidos e repetidos para testar estabilidade

#### Teste do Comportamento Modal

- [ ] Abrir o editor de sessão
- [ ] Tentar interagir com a janela principal (deve estar bloqueada)
- [ ] Abrir o editor de imagem a partir do editor de sessão
- [ ] Fazer alguma anotação e salvar
- [ ] Verificar se, ao fechar o editor de imagem, o editor de sessão ainda bloqueia a janela principal
- [ ] Repetir o processo várias vezes, alternando entre salvar e cancelar no editor de imagem
- [ ] Testar comportamento modal durante diálogos de configuração aninhados
- [ ] Verificar foco de janela após fechar diálogos modais

#### Teste de Visibilidade do Overlay

- [ ] Iniciar automação com overlay visível
- [ ] Verificar se o overlay está sempre visível para o usuário
- [ ] Confirmar que o overlay não aparece nas capturas de tela
- [ ] Testar visibilidade do overlay em diferentes monitores
- [ ] Verificar interação do overlay com outras janelas durante automação

## Testes de Integração Rápida

### Teste de Integridade Básica

- [ ] Iniciar aplicativo, capturar screenshot, gerar PDF, fechar aplicativo (deve levar <1 minuto)
- [ ] Verificar redimensionamento dinâmico das miniaturas no editor de sessão (aumentar/diminuir janela)
- [ ] Testar comportamento modal após editar uma imagem (deve manter bloqueio da janela principal)
- [ ] Verificar remoção automática de pastas vazias ao sair

### Teste de Regressão Visual

- [ ] Verificar se a interface principal é exibida corretamente
- [ ] Confirmar que miniaturas são exibidas adequadamente no editor de sessão
- [ ] Verificar se anotações são exibidas corretamente no editor de imagem
- [ ] Confirmar que a barra de ferramentas do editor de imagem está completa e funcional
- [ ] Testar a aparência do overlay de automação em diferentes resoluções
- [ ] Verificar adaptação da interface em monitores de alta resolução

## Automatização de Testes

Para testes futuros, recomenda-se criar scripts de automação para os seguintes cenários:

1. Instalação e configuração inicial
2. Captura básica e geração de PDF
3. Teste de comportamento modal entre janelas
4. Verificação de redimensionamento adaptativo de miniaturas
5. Testes de fluxo completo (captura, edição, anotação, PDF)
6. Validação de visibilidade correta do overlay durante automação

Estes scripts podem economizar tempo significativo em testes de regressão e garantir consistência entre as execuções de teste.
