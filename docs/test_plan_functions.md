# Plano de Testes PDF Maker

## Objetivo

Este documento descreve o plano de testes para verificar a funcionalidade e estabilidade do aplicativo PDF Maker após a implementação de correções.

## Escopo

Os testes abrangem todas as funcionalidades da aplicação, com ênfase em estabilidade, gerenciamento de recursos e correções recentes.

## Plano de Testes Funcionais

### 1. TESTES DE INSTALAÇÃO

- [ ] Instalação via setup.exe em Windows 11
- [ ] Verificar ícones no menu iniciar
- [ ] Verificar ícone na área de trabalho (se opção selecionada)
- [ ] Verificar primeira execução após instalação
- [ ] Teste de desinstalação completa

### 2. TESTES DE INTERFACE

- [ ] Verificar se a janela principal abre corretamente
- [ ] Verificar se todos os botões estão visíveis e clicáveis
- [ ] Verificar se os textos estão legíveis e sem sobreposição
- [ ] Testar redimensionamento da janela
- [ ] Verificar se o ícone da aplicação aparece corretamente
- [ ] Testar comportamento da interface em diferentes resoluções

### 3. TESTES DE CAPTURA DE TELA

- [ ] Capturar screenshot único
- [ ] Capturar múltiplos screenshots em sequência
- [ ] Verificar se as imagens são salvas corretamente na pasta de destino
- [ ] Verificar qualidade e tamanho das imagens capturadas
- [ ] Testar atalhos de teclado para captura

### 4. TESTES DE GERAÇÃO DE PDF

- [ ] Gerar PDF com uma única imagem
- [ ] Gerar PDF com múltiplas imagens
- [ ] Verificar qualidade do PDF gerado
- [ ] Verificar se todas as imagens foram incluídas no PDF
- [ ] Testar diferentes opções de formato/tamanho de página

### 5. TESTES DE AUTOMAÇÃO

- [ ] Testar recursos de automação disponíveis
- [ ] Verificar se sequências automáticas funcionam conforme esperado
- [ ] Testar interação com outras aplicações
- [ ] Verificar comportamento com diferentes intervalos de tempo

### 6. TESTES DE ATUALIZAÇÃO

- [ ] Verificar se o verificador de atualizações está funcionando
- [ ] Testar notificação de nova versão disponível
- [ ] Testar redirecionamento para download da nova versão

### 7. TESTES DE PREDEFINIÇÕES

- [ ] Criar novas predefinições
- [ ] Carregar predefinições existentes
- [ ] Editar predefinições
- [ ] Excluir predefinições
- [ ] Verificar se as predefinições são salvas entre sessões

### 8. TESTES DE SESSÃO

- [ ] Iniciar nova sessão (botão "Nova Sessão")
- [ ] Verificar se uma nova pasta é criada para os prints
- [ ] Resetar e recomeçar sessão atual
- [ ] Verificar se os arquivos da sessão anterior são preservados

### 9. TESTES DE GERENCIAMENTO DE ARQUIVOS

- [ ] Verificar se as imagens são salvas no diretório correto
- [ ] Verificar se o PDF é salvo no local esperado
- [ ] Testar a abertura do PDF após geração

### 10. TESTES DE ROBUSTEZ

- [ ] Testar comportamento quando há muitas imagens
- [ ] Testar com imagens de tamanhos muito grandes
- [ ] Verificar comportamento quando há erros de permissão de arquivos
- [ ] Testar recuperação após fechamento inesperado
- [ ] Verificar uso de memória durante operações intensivas

## Testes de Funcionalidades Específicas

### 11. TESTES DE COMPORTAMENTO MODAL DAS JANELAS

- [ ] Abrir a janela principal e tentar interagir com ela enquanto a janela "Editar Sessão de Imagens" está aberta
- [ ] Verificar se a janela "Editar Sessão de Imagens" bloqueia corretamente a interação com a janela principal
- [ ] Abrir a janela "Editar Sessão de Imagens" e depois abrir o "Editor de Imagem", verificar se a janela "Editar Sessão" fica bloqueada
- [ ] Verificar se os botões de maximizar, minimizar e fechar funcionam corretamente em cada janela
- [ ] Testar a redimensionamento das janelas secundárias
- [ ] No "Editor de Imagem", testar a caixa de diálogo "Adicionar Texto" e verificar se ela bloqueia a interação com o editor
- [ ] Verificar se a ordem de foco é restaurada corretamente quando janelas secundárias são fechadas
- [ ] Testar diálogos modais em diferentes configurações de monitor
- [ ] Verificar comportamento modal durante operações de longa duração

### 12. TESTES DE EDIÇÃO DE SESSÃO

- [ ] Abrir uma sessão existente e verificar se todas as imagens são carregadas corretamente
- [ ] Testar a reordenação de imagens
- [ ] Verificar se a mudança de ordem é refletida no PDF gerado
- [ ] Testar a exclusão de imagens da sessão
- [ ] Verificar se as imagens excluídas não aparecem no PDF final
- [ ] Testar o botão "Cancelar" para garantir que nenhuma alteração seja aplicada
- [ ] Testar o botão "Gerar PDF" diretamente da interface de edição de sessão

### 13. TESTES DE EDIÇÃO DE IMAGEM E ANOTAÇÕES

- [ ] Testar a adição de texto às imagens
- [ ] Verificar o redimensionamento do texto conforme o zoom
- [ ] Testar a adição de linhas às imagens
- [ ] Testar a adição de setas às imagens
- [ ] Testar a adição de retângulos às imagens
- [ ] Verificar se todas as anotações aparecem corretamente no PDF final
- [ ] Testar a seleção e movimentação de elementos já adicionados
- [ ] Testar a exclusão de elementos individuais
- [ ] Testar o botão "Limpar Anotações" para remover todas as anotações
- [ ] Verificar se as configurações de cor funcionam para todos os tipos de anotação
- [ ] Testar as opções de fonte (família e tamanho) para anotações de texto

### 14. TESTES DE ZOOM E NAVEGAÇÃO

- [ ] Testar o zoom in/out no editor de imagem
- [ ] Verificar se o zoom de 48% é aplicado por padrão ao abrir imagens
- [ ] Testar o zoom usando Ctrl+Roda do mouse
- [ ] Verificar se as anotações escalam corretamente com o zoom
- [ ] Testar a navegação pelas barras de rolagem horizontais e verticais
- [ ] Verificar se a posição de visualização é mantida ao aplicar zoom

### 15. TESTES DE PERSISTÊNCIA DE ANOTAÇÕES

- [ ] Adicionar anotações e salvar
- [ ] Fechar a imagem e reabri-la para verificar se as anotações foram salvas
- [ ] Verificar se o texto do botão muda de "Editar" para "Ver/Editar" quando há anotações
- [ ] Testar a geração de PDF com imagens anotadas
- [ ] Verificar a qualidade das anotações no PDF final

### 16. TESTES DE FLUXO COMPLETO DE EDIÇÃO

- [ ] Capturar 5 screenshots
- [ ] Clicar em "Editar Sessão"
- [ ] Reordenar as imagens
- [ ] Excluir uma das imagens
- [ ] Editar uma imagem adicionando texto e formas
- [ ] Salvar as edições
- [ ] Voltar à tela de edição de sessão
- [ ] Gerar PDF diretamente da tela de edição
- [ ] Verificar se o PDF contém as imagens na ordem correta com as anotações

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
- [ ] Renomear uma sessão existente e verificar se o novo nome é aplicado
- [ ] Testar o carregamento de uma sessão salva anteriormente
- [ ] Verificar se ao carregar uma sessão, todas as imagens são restauradas corretamente
- [ ] Verificar se o contador de imagens é restaurado corretamente ao carregar uma sessão
- [ ] Verificar se o título da janela é atualizado com o nome da sessão ao carregar uma sessão

### 19. TESTES DE LIMPEZA DE PASTAS VAZIAS

- [ ] Iniciar o aplicativo, criar uma nova sessão, fechar sem fazer nada e verificar se a pasta vazia foi removida
- [ ] Criar várias sessões sequenciais sem tirar screenshots e verificar se todas as pastas vazias são removidas ao sair
- [ ] Criar uma sessão, tirar um screenshot, excluir a imagem e verificar se a pasta vazia é removida ao sair
- [ ] Testar em sessão com imagens: criar sessão, tirar screenshots, fechar e verificar se a pasta NÃO é removida

### 20. TESTES DE OVERLAY DE AUTOMAÇÃO

- [ ] Verificar se o overlay aparece corretamente durante automação
- [ ] Testar se o overlay permanece visível o tempo todo para o usuário
- [ ] Confirmar que o overlay nunca aparece nas imagens capturadas
- [ ] Verificar se as informações exibidas no overlay são atualizadas corretamente
- [ ] Testar a visibilidade do overlay em diferentes configurações de monitor
- [ ] Verificar se o overlay pode ser arrastado e reposicionado durante a automação
- [ ] Testar o botão de fechamento do overlay
- [ ] Verificar se o overlay é fechado automaticamente quando a automação termina

### 21. TESTES DE ESTABILIDADE E DESEMPENHO

- [ ] Executar o aplicativo por um período prolongado (>1 hora) e verificar estabilidade
- [ ] Criar e gerenciar múltiplas sessões em sequência (>10) e verificar desempenho
- [ ] Testar com um grande número de imagens (>50) em uma única sessão
- [ ] Verificar uso de memória durante operações intensivas (monitorar com Gerenciador de Tarefas)
- [ ] Realizar operações repetidas de criação/edição/exclusão de sessões para detectar vazamentos de memória

### 22. TESTES DE RECUPERAÇÃO DE ERROS

- [ ] Tentar acessar uma pasta de sessão que foi removida externamente
- [ ] Tentar gerar PDF quando a pasta de destino não tem permissão de escrita
- [ ] Testar o comportamento quando uma imagem referenciada foi excluída ou movida externamente
- [ ] Verificar recuperação após erros de leitura/escrita em arquivos
- [ ] Tentar abrir imagens corrompidas ou com formatos não suportados
