[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [string]$Vault,

    [string]$Record = "05_MEMORY/pending/2026-08-26-kpa-v30-conclusion.json",

    [switch]$Apply
)

$ErrorActionPreference = "Stop"
$RepoRoot = Split-Path -Parent $PSScriptRoot
$PythonScript = Join-Path $PSScriptRoot "write_obsidian_memory.py"
$RecordPath = if ([System.IO.Path]::IsPathRooted($Record)) {
    $Record
} else {
    Join-Path $RepoRoot $Record
}

if (-not (Test-Path -LiteralPath $PythonScript -PathType Leaf)) {
    throw "Script Python não encontrado: $PythonScript"
}
if (-not (Test-Path -LiteralPath $RecordPath -PathType Leaf)) {
    throw "Registro não encontrado: $RecordPath"
}
if (-not (Test-Path -LiteralPath $Vault -PathType Container)) {
    throw "Vault não encontrado: $Vault"
}
if (-not (Test-Path -LiteralPath (Join-Path $Vault ".obsidian") -PathType Container)) {
    Write-Warning "A pasta informada não contém .obsidian. Confirme se é a raiz do vault."
}

$Python = Get-Command py -ErrorAction SilentlyContinue
if ($null -eq $Python) {
    $Python = Get-Command python -ErrorAction SilentlyContinue
}
if ($null -eq $Python) {
    throw "Python não encontrado. Instale Python 3 e habilite a opção Add Python to PATH."
}

$Arguments = @($PythonScript, $RecordPath, "--vault", $Vault)
if ($Apply) {
    $Arguments += "--apply"
}

Write-Host "Repositório: $RepoRoot"
Write-Host "Registro: $RecordPath"
Write-Host "Vault: $Vault"
if (-not $Apply) {
    Write-Host "Modo: dry-run (use -Apply para gravar)"
}

& $Python.Source @Arguments
exit $LASTEXITCODE
