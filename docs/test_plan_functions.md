# Plano de Testes PDF Maker

## Objetivo

Este documento descreve o plano de testes para verificar a funcionalidade e estabilidade do aplicativo PDF Maker após a implementação de correções.

## Escopo

Os testes abrangem todas as funcionalidades da aplicação, com ênfase em estabilidade, gerenciamento de recursos e correções recentes.

## Plano de Testes

### 1. TESTES DE INSTALAÇÃO

- [x] Instalação via setup.exe em Windows 11
- [x] Verificar ícones no menu iniciar
- [x] Verificar ícone na área de trabalho (se opção selecionada)
- [x] Verificar primeira execução após instalação
- [x] Teste de desinstalação completa

### 2. TESTES DE INTERFACE

- [x] Verificar se a janela principal abre corretamente
- [x] Verificar se todos os botões estão visíveis e clicáveis
- [x] Verificar se os textos estão legíveis e sem sobreposição
- [x] Testar redimensionamento da janela
- [x] Verificar se o ícone da aplicação aparece corretamente
- [x] Testar comportamento da interface em diferentes resoluções

### 3. TESTES DE CAPTURA DE TELA

- [x] Capturar screenshot único
- [x] Capturar múltiplos screenshots em sequência
- [x] Verificar se as imagens são salvas corretamente na pasta de destino
- [x] Verificar qualidade e tamanho das imagens capturadas
- [x] Testar atalhos de teclado para captura

### 4. TESTES DE GERAÇÃO DE PDF

- [x] Gerar PDF com uma única imagem
- [x] Gerar PDF com múltiplas imagens
- [x] Verificar qualidade do PDF gerado
- [x] Verificar se todas as imagens foram incluídas no PDF
- [x] Testar diferentes opções de formato/tamanho de página

### 5. TESTES DE AUTOMAÇÃO

- [x] Testar recursos de automação disponíveis
- [x] Verificar se sequências automáticas funcionam conforme esperado
- [x] Testar interação com outras aplicações
- [x] Verificar comportamento com diferentes intervalos de tempo

### 6. TESTES DE ATUALIZAÇÃO

- [x] Verificar se o verificador de atualizações está funcionando
- [x] Testar notificação de nova versão disponível
- [x] Testar redirecionamento para download da nova versão

### 7. TESTES DE PREDEFINIÇÕES

- [x] Criar novas predefinições
- [x] Carregar predefinições existentes
- [x] Editar predefinições
- [x] Excluir predefinições
- [x] Verificar se as predefinições são salvas entre sessões

### 8. TESTES DE SESSÃO

- [x] Iniciar nova sessão (botão "Nova Sessão")
- [x] Verificar se uma nova pasta é criada para os prints
- [x] Resetar e recomeçar sessão atual
- [x] Verificar se os arquivos da sessão anterior são preservados

### 9. TESTES DE GERENCIAMENTO DE ARQUIVOS

- [x] Verificar se as imagens são salvas no diretório correto
- [x] Verificar se o PDF é salvo no local esperado
- [x] Testar a abertura do PDF após geração

### 10. TESTES DE ROBUSTEZ

- [x] Testar comportamento quando há muitas imagens
- [x] Testar com imagens de tamanhos muito grandes
- [x] Verificar comportamento quando há erros de permissão de arquivos
- [x] Testar recuperação após fechamento inesperado
- [x] Verificar uso de memória durante operações intensivas

## Testes de Novas Funcionalidades de Edição

### 11. TESTES DE COMPORTAMENTO MODAL DAS JANELAS

- [x] Abrir a janela principal e tentar interagir com ela enquanto a janela "Editar Sessão de Imagens" está aberta
- [x] Verificar se a janela "Editar Sessão de Imagens" bloqueia corretamente a interação com a janela principal
- [x] Abrir a janela "Editar Sessão de Imagens" e depois abrir o "Editor de Imagem", verificar se a janela "Editar Sessão" fica bloqueada
- [x] Verificar se os botões de maximizar, minimizar e fechar funcionam corretamente em cada janela
- [x] Testar a redimensionamento das janelas secundárias
- [x] No "Editor de Imagem", testar a caixa de diálogo "Adicionar Texto" e verificar se ela bloqueia a interação com o editor
- [x] Verificar se a ordem de foco é restaurada corretamente quando janelas secundárias são fechadas

### 12. TESTES DE EDIÇÃO DE SESSÃO

- [x] Abrir uma sessão existente e verificar se todas as imagens são carregadas corretamente
- [x] Testar a reordenação de imagens
- [x] Verificar se a mudança de ordem é refletida no PDF gerado
- [x] Testar a exclusão de imagens da sessão
- [x] Verificar se as imagens excluídas não aparecem no PDF final
- [x] Testar o botão "Cancelar" para garantir que nenhuma alteração seja aplicada
- [x] Testar o botão "Gerar PDF" diretamente da interface de edição de sessão

### 13. TESTES DE EDIÇÃO DE IMAGEM E ANOTAÇÕES

- [x] Testar a adição de texto às imagens
- [x] Verificar o redimensionamento do texto conforme o zoom
- [x] Testar a adição de linhas às imagens
- [x] Testar a adição de setas às imagens
- [x] Testar a adição de retângulos às imagens
- [x] Verificar se todas as anotações aparecem corretamente no PDF final
- [x] Testar a seleção e movimentação de elementos já adicionados
- [x] Testar a exclusão de elementos individuais
- [x] Testar o botão "Limpar Anotações" para remover todas as anotações
- [x] Verificar se as configurações de cor funcionam para todos os tipos de anotação
- [x] Testar as opções de fonte (família e tamanho) para anotações de texto

### 14. TESTES DE ZOOM E NAVEGAÇÃO

- [x] Testar o zoom in/out no editor de imagem
- [x] Verificar se o zoom de 48% é aplicado por padrão ao abrir imagens
- [x] Testar o zoom usando Ctrl+Roda do mouse
- [x] Verificar se as anotações escalam corretamente com o zoom
- [x] Testar a navegação pelas barras de rolagem horizontais e verticais
- [x] Verificar se a posição de visualização é mantida ao aplicar zoom

### 15. TESTES DE PERSISTÊNCIA DE ANOTAÇÕES

- [x] Adicionar anotações e salvar
- [x] Fechar a imagem e reabri-la para verificar se as anotações foram salvas
- [x] Verificar se o texto do botão muda de "Editar" para "Ver/Editar" quando há anotações
- [x] Testar a geração de PDF com imagens anotadas
- [x] Verificar a qualidade das anotações no PDF final

### 16. TESTES DE FLUXO COMPLETO DE EDIÇÃO

- [ ] Capturar 5 screenshots
- [ ] Clicar em "Editar Sessão"
- [ ] Reordenar as imagens
- [ ] Excluir uma das imagens
- [ ] Editar uma imagem adicionando texto e formas
- [ ] Salvar as edições
- [ ] Voltar à tela de edição de sessão
- [ ] Gerar PDF diretamente da tela de edição
- [ ] Verificar se o PDF contém as imagens na ordem correta com as anotaçõe- ### 17. TESTES DE ROBUSTEZ DA EDIÇÃO

### 17. TESTES DE ROBUSTEZ DA EDIÇÃO

- [ ] Testar o comportamento quando se tenta editar uma imagem corrompida
- [ ] Verificar a resposta ao tentar adicionar textos muito longos
- [ ] Testar o comportamento quando há muitas anotações em uma imagem
- [ ] Verificar o comportamento de desfazer/refazer (Ctrl+Z/Ctrl+Y) com múltiplas operações
- [ ] Testar o comportamento quando falta espaço em disco para salvar anotações
- [ ] Testar a edição de imagens muito grandes (>10MB) e verificar desempenho
- [ ] Verificar o comportamento ao tentar arrastar ou redimensionar anotações para fora dos limites da imagem

### 18. TESTES DE GERENCIAMENTO DE SESSÕES

- [ ] Salvar uma sessão atual com um nome personalizado
- [ ] Verificar se a janela de diálogo para salvar sessão exibe corretamente o ícone e título
- [ ] Verificar se a sessão salva aparece no menu "Carregar Sessão"
- [ ] Renomear uma sessão existente e verificar se o novo nome é aplicado (OBS: Ao renomear parece que cria uma nova sessão ao invés de renomear a existente)
- [ ] Testar o carregamento de uma sessão salva anteriormente
- [ ] Verificar se ao carregar uma sessão, todas as imagens são restauradas corretamente
- [ ] Verificar se o contador de imagens é restaurado corretamente ao carregar uma sessão
- [ ] Verificar se o título da janela é atualizado com o nome da sessão ao carregar uma sessão
- [ ] Testar o salvamento automático da sessão ao fechar a aplicação
- [ ] Verificar se a última sessão é carregada automaticamente ao iniciar a aplicação
- [ ] Testar a criação de uma nova sessão após carregar uma sessão salva
- [ ] Verificar se múltiplas sessões podem ser salvas e carregadas corretamente

### 19. TESTES DE LIMPEZA DE PASTAS VAZIAS

- [ ] Iniciar o aplicativo, criar uma nova sessão, fechar sem fazer nada e verificar se a pasta vazia foi removida
- [ ] Criar várias sessões sequenciais sem tirar screenshots e verificar se todas as pastas vazias são removidas ao sair
- [ ] Criar uma sessão, tirar um screenshot, excluir a imagem e verificar se a pasta vazia é removida ao sair
- [ ] Testar em sessão com imagens: criar sessão, tirar screenshots, fechar e verificar se a pasta NÃO é removida
- [ ] Verificar se sessões vazias em diretórios externos referenciados em sessões antigas são limpas corretamente
- [ ] Confirmar que apenas pastas de sessão (`sessao_prints_*`) são afetadas pelo processo de limpeza

### 20. TESTES DE PROCESSO DE SAÍDA E CONFIRMAÇÃO

- [ ] Verificar se a caixa de diálogo de confirmação é exibida ao tentar fechar o aplicativo
- [ ] Testar "Cancelar" na caixa de confirmação e verificar se o aplicativo continua em execução
- [ ] Verificar se a confirmação de saída funciona corretamente usando o botão "Sair" do menu
- [ ] Verificar se a confirmação de saída funciona corretamente usando o "X" da janela
- [ ] Testar a confirmação de saída após operações intensivas (muitas imagens, edições)
- [ ] Verificar se o aplicativo salva a sessão atual antes de sair quando há alterações não salvas
- [ ] Testar o comportamento quando o aplicativo é fechado pelo gerenciador de tarefas (Alt+F4)

### 21. TESTES DE ESTABILIDADE E DESEMPENHO

- [ ] Executar o aplicativo por um período prolongado (>1 hora) e verificar estabilidade
- [ ] Criar e gerenciar múltiplas sessões em sequência (>10) e verificar desempenho
- [ ] Testar com um grande número de imagens (>50) em uma única sessão
- [ ] Verificar uso de memória durante operações intensivas (monitorar com Gerenciador de Tarefas)
- [ ] Realizar operações repetidas de criação/edição/exclusão de sessões para detectar vazamentos de memória
- [ ] Testar recuperação após fechamento forçado (simular crash) durante edição de imagem
- [ ] Verificar desempenho ao alternar rapidamente entre diferentes funcionalidades (captura, edição, PDF)

### 22. TESTES DE CASOS DE ERRO E RECUPERAÇÃO

- [ ] Tentar acessar uma pasta de sessão que foi removida externamente
- [ ] Tentar gerar PDF quando a pasta de destino não tem permissão de escrita
- [ ] Testar o comportamento quando uma imagem referenciada foi excluída ou movida externamente
- [ ] Verificar recuperação após erros de leitura/escrita em arquivos
- [ ] Tentar abrir imagens corrompidas ou com formatos não suportados
- [ ] Testar o comportamento quando o arquivo de configuração está corrompido
- [ ] Verificar recuperação quando arquivos de sessão JSON estão mal-formados ou corrompidos

## Casos de Teste Específicos

### Teste Básico

- [ ] Instalar o aplicativo
- [ ] Abrir o aplicativo
- [ ] Selecionar um diretório para salvar capturas
- [ ] Capturar uma tela
- [ ] Gerar um PDF
- [ ] Fechar o aplicativo (confirmar a saída)
- [ ] Verificar se pastas vazias foram removidas
- [ ] Reabrir o aplicativo
- [ ] Verificar se a última sessão é carregada corretamente
- [ ] Verificar se o PDF gerado pode ser aberto
- [ ] Verificar se o contador de screenshots está correto

### Teste de Estabilidade Após Correções

- [ ] Criar múltiplas sessões vazias em sequência (5+)
- [ ] Fechar o aplicativo e verificar se todas as pastas vazias foram removidas
- [ ] Criar uma sessão com screenshots e uma vazia
- [ ] Fechar o aplicativo e verificar se apenas a pasta vazia foi removida
- [ ] Abrir várias janelas do aplicativo e verificar se cada instância gerencia corretamente suas sessões
- [ ] Desligar o computador com o aplicativo aberto e verificar o comportamento ao reiniciar

### 23. TESTES DAS CORREÇÕES RECENTES

- [ ] **Teste de Redimensionamento Dinâmico de Miniaturas**
  - [ ] Abrir a janela "Editar Sessão de Imagens" com múltiplas imagens
  - [ ] Verificar se inicialmente o número de miniaturas por linha é adequado ao tamanho da janela
  - [ ] Aumentar a largura da janela e verificar se o número de miniaturas por linha aumenta
  - [ ] Diminuir a largura da janela e verificar se o número de miniaturas por linha diminui
  - [ ] Testar com diferentes quantidades de imagens (poucas e muitas)
  - [ ] Verificar se o layout permanece consistente durante o redimensionamento
  - [ ] Maximizar a janela e verificar se as miniaturas se distribuem adequadamente

- [ ] **Teste de Comportamento Modal após Edição de Imagem**
  - [ ] Abrir a janela "Editar Sessão de Imagens"
  - [ ] Selecionar uma imagem para editar (duplo clique ou botão "Editar")
  - [ ] Fazer alguma anotação na imagem e salvar
  - [ ] Verificar se, após fechar o Editor de Imagem, a janela de Sessão permanece modal
  - [ ] Tentar interagir com a janela principal enquanto a janela de Sessão está aberta
  - [ ] Repetir este processo várias vezes para garantir que a modalidade é mantida consistentemente
  - [ ] Testar o mesmo processo, mas cancelando a edição de imagem em vez de salvar

- [ ] **Teste de Estabilidade do Redimensionamento de Miniaturas**
  - [ ] Realizar redimensionamentos rápidos e repetidos da janela de Sessão
  - [ ] Verificar se não ocorrem problemas visuais ou travamentos durante redimensionamentos
  - [ ] Alternar entre tamanho máximo e mínimo várias vezes
  - [ ] Testar em diferentes resoluções de tela
  - [ ] Verificar se o desempenho permanece bom mesmo com muitas imagens na sessão

### Teste Completo de Fluxo com Correções

- [ ] Iniciar o aplicativo e criar uma nova sessão
- [ ] Capturar pelo menos 15 imagens para testar bem o layout de miniaturas
- [ ] Abrir a janela "Editar Sessão de Imagens"
- [ ] Redimensionar a janela várias vezes e verificar o comportamento das miniaturas
- [ ] Editar uma imagem, adicionar anotações e salvar
- [ ] Verificar se a janela de Sessão ainda está bloqueando a janela principal
- [ ] Reordenar algumas imagens e excluir outras
- [ ] Testar novamente o redimensionamento após as alterações
- [ ] Gerar um PDF a partir da janela de Sessão
- [ ] Verificar se o PDF contém as imagens na ordem correta com as anotações
- [ ] Fechar o aplicativo e verificar se tudo foi salvo corretamente
