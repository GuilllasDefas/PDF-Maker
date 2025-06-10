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
- [x] Gerar PDF e confirmar se as anotações aparecem corretamente

### 3. FLUXO DE AUTOMAÇÃO E PRESETS

**Objetivo:** Verificar a criação e uso de presets de automação.

- [x] Abrir as configurações de automação
- [x] Criar um novo preset configurando:
  - Nome personalizado
  - 5 capturas
  - Intervalo de 2 segundos
  - Começar após 3 segundos
  - Capturar área específica (selecionar área da tela)
  - Parar após pressionar uma tecla específica
- [x] Salvar o preset e verificar se aparece na lista
- [x] Aplicar o preset e iniciar a automação
- [x] Verificar se a contagem regressiva funciona
- [x] Verificar se as capturas ocorrem no intervalo configurado
- [x] Interromper usando a tecla configurada
- [x] Verificar se todas as imagens foram capturadas corretamente
- [x] Reabrir configurações e editar o preset existente
- [x] Aplicar as mudanças e testar novamente
- [x] Excluir o preset e confirmar que foi removido da lista

### 4. FLUXO DE SESSÕES E PERSISTÊNCIA

**Objetivo:** Testar o gerenciamento de sessões e recuperação entre execuções.

- [x] Iniciar nova sessão
- [x] Capturar 3 screenshots
- [x] Salvar a sessão com nome personalizado
- [x] Criar nova sessão e capturar 2 screenshots diferentes
- [x] Verificar se a nova sessão tem imagens diferentes
- [x] Usar o menu para carregar a sessão salva anteriormente
- [x] Verificar se as imagens originais foram restauradas
- [x] Editar uma imagem e adicionar anotações
- [x] Fechar o aplicativo sem salvar explicitamente
- [x] Reabrir o aplicativo e verificar se a última sessão é carregada
- [x] Confirmar que as anotações foram preservadas

### 5. FLUXO DE TESTES DE ROBUSTEZ

**Objetivo:** Verificar o comportamento em condições adversas.

- [x] Tentar salvar em um diretório sem permissões de escrita
- [x] Capturar e editar uma imagem muito grande (>10MB)
- [x] Adicionar muitas anotações a uma única imagem (>20)
- [x] Tentar criar um PDF com 30+ imagens
- [x] Realizar operações rápidas em sequência (alternar entre sessões rapidamente)
- [x] Simular falta de espaço em disco durante salvamento
- [x] Tentar abrir uma sessão com imagens que foram excluídas externamente
- [x] Testar atalhos personalizados após alterá-los nas configurações

### 6. FLUXO DE TESTES DAS CORREÇÕES RECENTES

**Objetivo:** Verificar especificamente as correções implementadas recentemente.

#### Teste do Redimensionamento Dinâmico de Miniaturas

- [x] Abrir o editor de sessão com 15+ imagens
- [x] Redimensionar a janela horizontalmente (aumentar largura)
- [x] Verificar se o número de miniaturas por linha aumenta
- [x] Redimensionar para uma janela estreita
- [x] Verificar se o número de miniaturas diminui adequadamente
- [x] Maximizar a janela e confirmar distribuição adequada
- [x] Realizar redimensionamentos rápidos e repetidos para testar estabilidade

#### Teste do Comportamento Modal

- [x] Abrir o editor de sessão
- [x] Tentar interagir com a janela principal (deve estar bloqueada)
- [x] Abrir o editor de imagem a partir do editor de sessão
- [x] Fazer alguma anotação e salvar
- [x] Verificar se, ao fechar o editor de imagem, o editor de sessão ainda bloqueia a janela principal
- [x] Repetir o processo várias vezes, alternando entre salvar e cancelar no editor de imagem

## Testes de Integração Rápida

### Teste de Integridade Básica

- [x] Iniciar aplicativo, capturar screenshot, gerar PDF, fechar aplicativo (deve levar <1 minuto)
- [x] Verificar redimensionamento dinâmico das miniaturas no editor de sessão (aumentar/diminuir janela)
- [x] Testar comportamento modal após editar uma imagem (deve manter bloqueio da janela principal)
- [x] Verificar remoção automática de pastas vazias ao sair

### Teste de Regressão Visual

- [ ] Verificar se a interface principal é exibida corretamente
- [ ] Confirmar que miniaturas são exibidas adequadamente no editor de sessão
- [ ] Verificar se anotações são exibidas corretamente no editor de imagem
- [ ] Confirmar que a barra de ferramentas do editor de imagem está completa e funcional

## Automatização de Testes

Para testes futuros, recomenda-se criar scripts de automação para os seguintes cenários:

1. Instalação e configuração inicial
2. Captura básica e geração de PDF
3. Teste de comportamento modal entre janelas
4. Verificação de redimensionamento adaptativo de miniaturas

Estes scripts podem economizar tempo significativo em testes de regressão e garantir consistência entre as execuções de teste.
