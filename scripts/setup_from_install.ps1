# Prepares this source checkout to run Rose on patch 16.19.
# Copies user-provided files from the local Rose and LTK Manager installs
# (nothing is downloaded or redistributed), creates .venv and installs deps.
$ErrorActionPreference = 'Stop'
$repo = Split-Path -Parent $PSScriptRoot
$tools = Join-Path $repo 'injection\tools'
$pengu = Join-Path $repo 'Pengu Loader'

function Fail($msg) {
    Write-Host ""
    Write-Host "ERRO: $msg" -ForegroundColor Red
    exit 1
}

function Find-File($name, $roots) {
    foreach ($root in $roots) {
        if (-not $root -or -not (Test-Path $root)) { continue }
        $hit = Get-ChildItem $root -Recurse -Depth 4 -Filter $name -ErrorAction SilentlyContinue |
            Select-Object -First 1
        if ($hit) { return $hit.FullName }
    }
    return $null
}

Write-Host "== Python"
$pyExe = $null; $pyArgs = @()
foreach ($cand in @('py', 'python')) {
    if (-not (Get-Command $cand -ErrorAction SilentlyContinue)) { continue }
    $candArgs = @()
    if ($cand -eq 'py') { $candArgs = @('-3') }
    try {
        $ok = & $cand @candArgs -c "import sys; print(sys.version_info >= (3, 11))" 2>$null
        if ($ok -eq 'True') { $pyExe = $cand; $pyArgs = $candArgs; break }
    } catch {}
}
if (-not $pyExe) { Fail "Python 3.11 ou mais novo nao encontrado. Instale em https://www.python.org/downloads/ (marque 'Add python.exe to PATH')." }

Write-Host "== Arquivos do Rose instalado"
$roseInstall = Join-Path $env:ProgramFiles 'Rose\_internal'
if (-not (Test-Path $roseInstall)) { Fail "Rose instalado nao encontrado em '$roseInstall'. Instale o Rose oficial primeiro." }
$copies = @(
    @{ From = "$roseInstall\injection\tools\cslol-dll.dll"; To = $tools },
    @{ From = "$roseInstall\Pengu Loader\Pengu Loader.exe"; To = $pengu },
    @{ From = "$roseInstall\Pengu Loader\Pengu Loader.exe.config"; To = $pengu }
)
foreach ($c in $copies) {
    if (-not (Test-Path $c.From)) { Fail "Arquivo nao encontrado: $($c.From)" }
    Copy-Item $c.From $c.To -Force
}
$hashes = "$roseInstall\injection\tools\hashes.game.txt"
if (Test-Path $hashes) { Copy-Item $hashes $tools -Force }

Write-Host "== Injetor do LTK Manager"
$ltkRoots = @("$env:LOCALAPPDATA\LTK Manager", "$env:ProgramFiles\LTK Manager", "$env:LOCALAPPDATA\Programs", $env:ProgramFiles)
$host_ = Find-File 'ltk_patcher_host.exe' $ltkRoots
if (-not $host_) { Fail "LTK Manager nao encontrado. Instale a versao mais recente em https://github.com/LeagueToolkit/ltk-manager/releases e rode este script de novo." }
$dll = Join-Path (Split-Path $host_) 'ltk_patcher_dll.dll'
if (-not (Test-Path $dll)) { Fail "ltk_patcher_dll.dll nao encontrado ao lado de $host_" }
Copy-Item $host_, $dll $tools -Force
Write-Host "   $host_"

Write-Host "== Ambiente Python (.venv)"
$venvPy = Join-Path $repo '.venv\Scripts\python.exe'
if (-not (Test-Path $venvPy)) { & $pyExe @pyArgs -m venv (Join-Path $repo '.venv') }
if (-not (Test-Path $venvPy)) { Fail "Nao foi possivel criar o .venv" }
$reqs = Get-Content (Join-Path $repo 'requirements.txt') | Where-Object { $_ -match '^[A-Za-z]' -and $_ -notmatch '^pyinstaller' }
& $venvPy -m pip install -q --disable-pip-version-check @reqs
if ($LASTEXITCODE -ne 0) { Fail "Falha ao instalar dependencias" }

Write-Host ""
Write-Host "Pronto." -ForegroundColor Green
