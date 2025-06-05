# Plano de Testes PDF Maker

## Objetivo

Este documento descreve o plano de testes para verificar a funcionalidade do aplicativo PDF Maker após a compilação.

## Escopo

Os testes abrangem todas as funcionalidades da aplicação, desde a instalação até recursos avançados.

## Plano de Testes

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
- [ ] Testar captura em múltiplos monitores (se aplicável)
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
- [ ] Verificar comportamento quando não há espaço em disco suficiente

### 10. TESTES DE ROBUSTEZ

- [ ] Testar comportamento quando há muitas imagens
- [ ] Testar com imagens de tamanhos muito grandes
- [ ] Verificar comportamento quando há erros de permissão de arquivos
- [ ] Testar recuperação após fechamento inesperado
- [ ] Verificar uso de memória durante operações intensivas

## Testes de Novas Funcionalidades de Edição

### 11. TESTES DE COMPORTAMENTO MODAL DAS JANELAS

- [ ] Abrir a janela principal e tentar interagir com ela enquanto a janela "Editar Sessão de Imagens" está aberta
- [ ] Verificar se a janela "Editar Sessão de Imagens" bloqueia corretamente a interação com a janela principal
- [ ] Abrir a janela "Editar Sessão de Imagens" e depois abrir o "Editor de Imagem", verificar se a janela "Editar Sessão" fica bloqueada
- [ ] Verificar se os botões de maximizar, minimizar e fechar funcionam corretamente em cada janela
- [ ] Testar a redimensionamento das janelas secundárias
- [ ] No "Editor de Imagem", testar a caixa de diálogo "Adicionar Texto" e verificar se ela bloqueia a interação com o editor
- [ ] Verificar se a ordem de foco é restaurada corretamente quando janelas secundárias são fechadas

### 12. TESTES DE EDIÇÃO DE SESSÃO

- [ ] Abrir uma sessão existente e verificar se todas as imagens são carregadas corretamente
- [ ] Testar a reordenação de imagens por arrastar e soltar
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
- [ ] Verificar se o indicador visual de anotações (borda verde) aparece corretamente na miniatura da imagem
- [ ] Verificar se o texto do botão muda de "Editar" para "Ver/Editar" quando há anotações
- [ ] Testar a geração de PDF com imagens anotadas
- [ ] Verificar a qualidade das anotações no PDF final

### 16. TESTES DE FLUXO COMPLETO DE EDIÇÃO

1. [ ] Capturar 5 screenshots
2. [ ] Clicar em "Editar Sessão"
3. [ ] Reordenar as imagens 
4. [ ] Excluir uma das imagens
5. [ ] Editar uma imagem adicionando texto e formas
6. [ ] Salvar as edições
7. [ ] Voltar à tela de edição de sessão
8. [ ] Gerar PDF diretamente da tela de edição
9. [ ] Verificar se o PDF contém as imagens na ordem correta com as anotações

### 17. TESTES DE ROBUSTEZ DA EDIÇÃO

- [ ] Testar o comportamento quando se tenta editar uma imagem corrompida
- [ ] Verificar a resposta ao tentar adicionar textos muito longos
- [ ] Testar o comportamento quando há muitas anotações em uma imagem
- [ ] Verificar o comportamento de desfazer/refazer (Ctrl+Z/Ctrl+Y) com múltiplas operações
- [ ] Testar o comportamento quando falta espaço em disco para salvar anotações

## Casos de Teste Específicos

### Teste Básico

1. [ ] Tirar Prints
2. [ ] Gerar PDF

### Teste Básico 2

1. [ ] Tirar Prints
2. [ ] Gerar PDF
3. [ ] Resetar e Recomeçar

### Teste Completo

1. [ ] Iniciar nova sessão
2. [ ] Capturar 5 screenshots
3. [ ] Gerar PDF
4. [ ] Verificar PDF gerado
5. [ ] Iniciar nova sessão
6. [ ] Capturar 3 screenshots
7. [ ] Gerar novo PDF
8. [ ] Verificar que ambos PDFs existem e estão corretos
