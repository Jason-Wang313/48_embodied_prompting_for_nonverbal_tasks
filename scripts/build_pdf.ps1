$ErrorActionPreference = "Stop"

$Root = Resolve-Path (Join-Path $PSScriptRoot "..")
$PaperDir = Join-Path $Root "paper"
$DataDir = Join-Path $Root "data"
$CanonicalPdf = "C:\Users\wangz\Downloads\48.pdf"

New-Item -ItemType Directory -Force -Path $DataDir | Out-Null

Push-Location $PaperDir
try {
    pdflatex -interaction=nonstopmode -halt-on-error main.tex
    pdflatex -interaction=nonstopmode -halt-on-error main.tex
    pdflatex -interaction=nonstopmode -halt-on-error main.tex
}
finally {
    Pop-Location
}

$BuiltPdf = Join-Path $PaperDir "main.pdf"
if (-not (Test-Path $BuiltPdf)) {
    throw "Expected PDF was not produced: $BuiltPdf"
}

Copy-Item -Force -Path $BuiltPdf -Destination $CanonicalPdf
Remove-Item -Force -LiteralPath $BuiltPdf

$status = [ordered]@{
    paper = 48
    decision = "workshop-only"
    canonical_pdf = $CanonicalPdf
    local_pdf_removed = -not (Test-Path $BuiltPdf)
    built_at = Get-Date -Format "yyyy-MM-dd HH:mm:ss zzz"
}
$status | ConvertTo-Json | Set-Content -Encoding UTF8 (Join-Path $DataDir "build_status.json")
