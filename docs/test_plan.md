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
- [ ] Testar comportamento da interface em diferentes resoluções

### 3. TESTES DE CAPTURA DE TELA

- [x] Capturar screenshot único
- [x] Capturar múltiplos screenshots em sequência
- [x] Verificar se as imagens são salvas corretamente na pasta de destino
- [ ] Testar captura em múltiplos monitores (se aplicável)
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
- [ ] Verificar se as predefinições são salvas entre sessões

### 8. TESTES DE SESSÃO

- [x] Iniciar nova sessão (botão "Nova Sessão")
- [x] Verificar se uma nova pasta é criada para os prints
- [x] Resetar e recomeçar sessão atual
- [x] Verificar se os arquivos da sessão anterior são preservados

### 9. TESTES DE GERENCIAMENTO DE ARQUIVOS

- [x] Verificar se as imagens são salvas no diretório correto
- [x] Verificar se o PDF é salvo no local esperado
- [x] Testar a abertura do PDF após geração
- [ ] Verificar comportamento quando não há espaço em disco suficiente

### 10. TESTES DE ROBUSTEZ

- [x] Testar comportamento quando há muitas imagens
- [ ] Testar com imagens de tamanhos muito grandes
- [ ] Verificar comportamento quando há erros de permissão de arquivos
- [ ] Testar recuperação após fechamento inesperado
- [ ] Verificar uso de memória durante operações intensivas

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
