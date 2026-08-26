# Obsidian no Windows — execução sem caminho fictício

O caminho `C:\caminho\para\KPA-calixto` usado em exemplos é apenas um marcador. Não execute esse texto literalmente.

## 1. Confirmar que o repositório existe no computador

No PowerShell:

```powershell
$candidatos = @(
  "$env:USERPROFILE\Documents\KPA-calixto",
  "$env:USERPROFILE\Desktop\KPA-calixto",
  "$env:USERPROFILE\Downloads\KPA-calixto"
)
$repo = $candidatos | Where-Object { Test-Path "$_\scripts\write-obsidian-memory.ps1" } | Select-Object -First 1
$repo
```

Se nada for exibido, o repositório ainda não está baixado nessa máquina ou está em outro local. Localize a pasta no Explorador e copie seu caminho real.

## 2. Localizar o vault

No Obsidian, use **Abrir pasta no Explorador**. A raiz correta normalmente contém a pasta `.obsidian`.

Exemplo:

```powershell
$vault = "$env:USERPROFILE\Documents\Obsidian\MeuVault"
Test-Path "$vault\.obsidian"
```

O resultado esperado é `True`.

## 3. Executar sem trocar de diretório

Dry-run:

```powershell
& "$repo\scripts\write-obsidian-memory.ps1" -Vault $vault
```

Gravação real:

```powershell
& "$repo\scripts\write-obsidian-memory.ps1" -Vault $vault -Apply
```

O wrapper calcula a raiz do repositório automaticamente. Não é necessário usar `cd`, configurar variável de ambiente ou escrever o caminho do script Python manualmente.

## Erros comuns

- **`Set-Location ... não existe`**: foi usado um caminho de exemplo, não o caminho real.
- **`can't open file C:\Users\...\scripts\...`**: o comando foi executado fora do repositório usando caminho relativo.
- **`Vault não encontrado`**: o caminho não aponta para uma pasta existente.
- **aviso sobre `.obsidian`**: provavelmente foi selecionada uma subpasta dentro do vault, não a raiz.
