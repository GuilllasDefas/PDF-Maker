# Como gerar o executável com PyInstaller, UPX, optimize e hidden imports

1. **Instale o PyInstaller e o UPX**  
   ```bash
   pip install pyinstaller
   # Baixe o UPX em https://upx.github.io/ e extraia o executável na sua máquina
   ```

2. **Comando para gerar o executável (PowerShell):**
   > No PowerShell, use a barra invertida (`\`) para quebra de linha, ou coloque tudo em uma linha só.
   ```powershell
   pyinstaller main.py `
     --onefile `
     --noconsole `
     --upx-dir="E:\UPX" `
     --optimize=2 `
     --hidden-import=keyboard `
     --hidden-import=pyautogui `
     --hidden-import=PIL `
     --hidden-import=reportlab
   ```
   > Ou, em uma linha só:
   ```powershell
   pyinstaller main.py --onefile --noconsole --upx-dir="CAMINHO_PARA_UPX" --optimize=2 --hidden-import=keyboard --hidden-import=pyautogui --hidden-import=PIL --hidden-import=reportlab
   ```
   > Substitua `CAMINHO_PARA_UPX` pelo caminho onde está o executável do UPX.

3. **Notas:**
   - O parâmetro `--onefile` gera um único executável.
   - `--noconsole` oculta o terminal (útil para apps GUI).
   - `--upx-dir` ativa compressão UPX.
   - `--optimize=2` ativa otimização máxima do bytecode.
   - `--hidden-import` garante que dependências dinâmicas sejam incluídas.

4. **Exemplo de caminho para UPX no Windows:**
   ```
   --upx-dir="C:\Ferramentas\upx-4.2.1-win64"
   ```

5. **Após a execução, o executável estará em `dist\main.exe`.**
