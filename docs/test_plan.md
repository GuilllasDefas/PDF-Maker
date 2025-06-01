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
- [ ] Verificar metadados do PDF gerado

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

### 11. TESTES DE COMPATIBILIDADE
- [ ] Testar em Windows 10 (várias versões)
- [ ] Testar em Windows 11
- [ ] Testar em diferentes configurações de hardware
- [ ] Verificar comportamento com diferentes DPIs de tela
- [ ] Testar com temas claro/escuro do Windows

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
