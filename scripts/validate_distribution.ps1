$ErrorActionPreference = 'Stop'
$errors = @()
$skills = @(Get-ChildItem (Split-Path $PSScriptRoot -Parent) -Recurse -Filter SKILL.md -File | Where-Object { $_.FullName -notmatch '[\\/]_canonical[\\/]' })
foreach ($skill in $skills) {
  $content = Get-Content -Raw -Encoding UTF8 $skill.FullName
  if ($content -notmatch '(?s)\A---\r?\n.*?name:\s*[a-z0-9-]+.*?description:\s*.+?\r?\n---') { $errors += "Invalid Skill: $($skill.FullName)" }
  if ($content -notmatch '(?is)designed.{0,100}integrated.{0,100}(independently\s+)?refactored.{0,100}(continuously\s+)?maintained.{0,60}TIKAZ') { $errors += "Missing TIKAZ contribution: $($skill.FullName)" }
  if ($content -match '(?i)[A-Z]:\\Users\\|[A-Z]:\\CodexTools') { $errors += "Machine-specific path: $($skill.FullName)" }
}
if (-not (Test-Path (Join-Path (Split-Path $PSScriptRoot -Parent) 'DISTRIBUTION.yml'))) { $errors += 'Missing distribution metadata' }
if ($errors.Count) { $errors | ForEach-Object { Write-Error $_ }; exit 1 }
Write-Output "PASS: validated $($skills.Count) Skills in this distribution."
