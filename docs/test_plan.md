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
- [x] Testar captura em múltiplos monitores (se aplicável)
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
- [x] Verificar comportamento quando não há espaço em disco suficiente

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
- [Errado] Testar a reordenação de imagens por arrastar e soltar
- [Errado] Verificar se a mudança de ordem é refletida no PDF gerado
- [x] Testar a exclusão de imagens da sessão
- [x] Verificar se as imagens excluídas não aparecem no PDF final
- [x] Testar o botão "Cancelar" para garantir que nenhuma alteração seja aplicada
- [x] Testar o botão "Gerar PDF" diretamente da interface de edição de sessão

### 13. TESTES DE EDIÇÃO DE IMAGEM E ANOTAÇÕES

- [x] Testar a adição de texto às imagens
- [Errado] Verificar o redimensionamento do texto conforme o zoom
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
- [Errado] Verificar se as anotações escalam corretamente com o zoom
- [x] Testar a navegação pelas barras de rolagem horizontais e verticais
- [x] Verificar se a posição de visualização é mantida ao aplicar zoom

### 15. TESTES DE PERSISTÊNCIA DE ANOTAÇÕES

- [x] Adicionar anotações e salvar
- [x] Fechar a imagem e reabri-la para verificar se as anotações foram salvas
- [x] Verificar se o texto do botão muda de "Editar" para "Ver/Editar" quando há anotações
- [x] Testar a geração de PDF com imagens anotadas
- [x] Verificar a qualidade das anotações no PDF final

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

### 18. TESTES DE GERENCIAMENTO DE SESSÕES

- [x] Salvar uma sessão atual com um nome personalizado
- [x] Verificar se a janela de diálogo para salvar sessão exibe corretamente o ícone e título
- [x] Verificar se a sessão salva aparece no menu "Carregar Sessão"
- [ ] Renomear uma sessão existente e verificar se o novo nome é aplicado
- [ ] Testar o carregamento de uma sessão salva anteriormente
- [ ] Verificar se ao carregar uma sessão, todas as imagens são restauradas corretamente
- [ ] Verificar se o contador de imagens é restaurado corretamente ao carregar uma sessão
- [ ] Verificar se o título da janela é atualizado com o nome da sessão ao carregar uma sessão
- [ ] Testar o salvamento automático da sessão ao fechar a aplicação
- [ ] Verificar se a última sessão é carregada automaticamente ao iniciar a aplicação
- [ ] Testar a criação de uma nova sessão após carregar uma sessão salva
- [ ] Verificar se múltiplas sessões podem ser salvas e carregadas corretamente

## Casos de Teste Específicos

### Teste Básico

- [ ] Instalar o aplicativo
- [ ] Abrir o aplicativo
- [ ] Capturar uma tela
- [ ] Gerar um PDF
- [ ] Salvar o PDF
- [ ] Fechar o aplicativo
- [ ] Reabrir o aplicativo
- [ ] Verificar se o PDF gerado pode ser aberto
- [ ] Enviar o PDF gerado por e-mail (opcional)
- [ ] Excluir o PDF gerado
- [ ] Verificar se o PDF foi excluído com sucesso
