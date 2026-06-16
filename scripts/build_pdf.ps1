$ErrorActionPreference = "Stop"

$Root = Resolve-Path (Join-Path $PSScriptRoot "..")
$PaperDir = Join-Path $Root "paper"
$DataDir = Join-Path $Root "data"
$CanonicalPdf = "C:\Users\wangz\Downloads\48.pdf"

New-Item -ItemType Directory -Force -Path $DataDir | Out-Null

Push-Location $PaperDir
try {
    pdflatex -interaction=nonstopmode -halt-on-error main.tex | Out-Null
    if ($LASTEXITCODE -ne 0) { throw "pdflatex pass 1 failed with exit code $LASTEXITCODE" }
    pdflatex -interaction=nonstopmode -halt-on-error main.tex | Out-Null
    if ($LASTEXITCODE -ne 0) { throw "pdflatex pass 2 failed with exit code $LASTEXITCODE" }
    pdflatex -interaction=nonstopmode -halt-on-error main.tex | Out-Null
    if ($LASTEXITCODE -ne 0) { throw "pdflatex pass 3 failed with exit code $LASTEXITCODE" }
}
finally {
    Pop-Location
}

$BuiltPdf = Join-Path $PaperDir "main.pdf"
if (-not (Test-Path $BuiltPdf)) {
    throw "Expected PDF was not produced: $BuiltPdf"
}

Copy-Item -Force -Path $BuiltPdf -Destination $CanonicalPdf
$Hash = Get-FileHash -LiteralPath $CanonicalPdf -Algorithm SHA256
Remove-Item -Force -LiteralPath $BuiltPdf

$status = [ordered]@{
    paper = 48
    status = "final_v3_full_scale"
    canonical_pdf = $CanonicalPdf
    canonical_sha256 = $Hash.Hash
    local_pdf_removed = -not (Test-Path $BuiltPdf)
    built_at = Get-Date -Format "yyyy-MM-dd HH:mm:ss zzz"
}
$status | ConvertTo-Json | Set-Content -Encoding UTF8 (Join-Path $DataDir "build_status.json")
