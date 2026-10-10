# Grava os cliques no site Brasíndice com Playwright codegen.
# Uso: .\tools\start_capture_brasicinde.ps1 [URL]
# Se a URL não for passada, usa config/settings.json.

param([string]$Url = "")

$PSScriptRoot = Split-Path -Parent $MyInvocation.MyCommand.Path

if (-not $Url) {
    $settings = Get-Content "$PSScriptRoot\..\config\settings.json" -Raw | ConvertFrom-Json
    $Url = $settings.brasicinde.site_url
}

if (-not $Url) {
    Write-Error "Preencha brasicinde.site_url em config/settings.json ou passe a URL como argumento."
    exit 1
}

$out = "$PSScriptRoot\captures\brasicinde_codegen.py"
$storage = "$PSScriptRoot\captures\auth_state.json"

Write-Host "Gravando cliques em: $Url"
Write-Host "Saída: $out"
Write-Host ""
Write-Host "IMPORTANTE: digite sua senha APENAS se ela não for gravada no script."
Write-Host "Recomendado: ao terminar, remova a senha do script gerado (ela vai para .env)."
Write-Host ""

python -m playwright codegen --target python --save-storage $storage -o $out $Url
