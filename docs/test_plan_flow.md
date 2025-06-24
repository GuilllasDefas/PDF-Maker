# Plano de Testes Otimizado - PDF Maker

## Fluxos de Trabalho Integrados

Os seguintes fluxos de trabalho combinam múltiplos casos de teste em sequências que exercitam funcionalidades relacionadas simultaneamente, economizando tempo de teste.

### 1. FLUXO BÁSICO DE CAPTURA E GERAÇÃO DE PDF

**Objetivo:** Verificar o fluxo completo desde a instalação até a geração de PDF com configurações padrão.

- [x] Instalar o aplicativo e verificar ícones no menu iniciar/desktop
- [x] Abrir o aplicativo e confirmar que a interface carrega corretamente
- [x] Selecionar um diretório para salvar capturas
- [x] Capturar 3 screenshots usando o atalho padrão
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
- [x] Salvar as edições e verificar se salva
- [x] Gerar PDF e confirmar se as anotações aparecem corretamente
- [x] Testar desfazer/refazer durante edição de imagem
- [x] Testar mudança de cor para diferentes tipos de anotação

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
- [x] Fechar completamente o aplicativo e reabri-lo
- [x] Verificar se o último preset aplicado é carregado automaticamente
- [x] Iniciar a automação sem fazer nenhuma configuração adicional
- [x] Confirmar que as configurações do preset persistiram corretamente
- [x] Reabrir configurações e editar o preset existente
- [x] Aplicar as mudanças e testar novamente
- [x] Excluir o preset e confirmar que foi removido da lista
- [x] Testar preset com captura de janela específica em vez de área
- [x] Testar automação com diferentes condições de parada

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

### 7. FLUXO DE PERSISTÊNCIA DE CONFIGURAÇÕES

**Objetivo:** Verificar se o aplicativo salva e restaura corretamente as configurações do usuário.

- [ ] Configurar um preset personalizado com características específicas
- [ ] Aplicar o preset (sem salvar explicitamente) e verificar se funciona
- [ ] Fechar o aplicativo completamente
- [ ] Reabrir o aplicativo e verificar se o último preset aplicado é carregado automaticamente
- [ ] Iniciar a automação para confirmar que as configurações persistiram
- [ ] Aplicar um preset diferente e repetir o processo de fechamento/abertura
- [ ] Verificar se o segundo preset agora é carregado automaticamente
- [ ] Excluir o preset que estava sendo usado e fechar o aplicativo
- [ ] Reabrir o aplicativo e verificar o comportamento quando o último preset não existe mais
- [ ] Testar a persistência após uma atualização de versão

### 8. FLUXO DE NOVOS RECURSOS E CASOS ESPECÍFICOS

#### Navegação entre Imagens no Editor

- [x] Abrir o editor de imagem com múltiplas imagens carregadas
- [x] Usar os botões "← Anterior" e "Próxima →" para navegar entre imagens
- [x] Fazer anotações em uma imagem, navegar para outra e voltar para verificar persistência
- [x] Testar navegação enquanto edita (verificar se alterações são salvas)
- [x] Navegar até os limites (primeira/última imagem) e verificar o comportamento dos botões

#### Personalização de Fonte e Cor

- [x] Abrir o diálogo de configuração de fonte e testar todas as opções disponíveis
- [x] Verificar se o botão da ferramenta ativa é destacado visualmente (fundo colorido)
- [x] Testar a persistência das configurações de fonte entre sessões
- [x] Testar fontes com caracteres especiais ou não-latinos
- [x] Verificar se a amostra de cor atual é atualizada corretamente após escolher uma nova cor

#### Manipulação de Diálogos

- [ ] Verificar se o diálogo de configuração de fonte permanece centralizado em relação à janela principal
- [ ] Testar se o diálogo de limpar anotações mantém a janela principal visível e em primeiro plano
- [ ] Confirmar que o foco retorna à janela correta após fechar diálogos
- [ ] Testar escape ou clique fora para fechar diálogos quando apropriado

#### Recursos do Editor de Imagem

- [x] Testar o recurso desfazer/refazer para cada tipo de anotação
- [x] Verificar limites de desfazer (número máximo de operações armazenadas)
- [x] Editar texto existente através de clique duplo
- [x] Verificar a precisão do posicionamento de anotações em diferentes níveis de zoom

#### Desempenho e Capacidade

- [ ] Testar edição de imagens de resolução muito alta (4K ou superior)
- [ ] Verificar desempenho com dezenas de anotações em uma única imagem
- [ ] Testar o tempo de carregamento do editor de sessão com 50+ imagens
- [ ] Verificar consumo de memória durante operações intensivas
- [ ] Testar com imagens de diferentes formatos (PNG, JPG, BMP) e transparência

#### Configurações com Múltiplos Monitores

- [ ] Capturar screenshots em configurações com vários monitores
- [ ] Testar a seleção de área abrangendo múltiplos monitores
- [ ] Verificar posicionamento correto de janelas ao mover entre monitores
- [ ] Testar captura de janela específica em monitor secundário
- [ ] Verificar comportamento da automação em múltiplos monitores
