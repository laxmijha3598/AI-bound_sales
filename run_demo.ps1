$ErrorActionPreference = "Stop"

if (!(Test-Path -LiteralPath "config.toml")) {
  Copy-Item -LiteralPath "config.example.toml" -Destination "config.toml"
}

$env:PYTHONDONTWRITEBYTECODE = "1"
python -m sales_agent.cli run --config config.toml --leads data/starter_leads.csv --limit 10 --log out/outreach_log.csv

Write-Host ""
Write-Host "Demo artifacts generated:"
Write-Host " - out/outreach_log.csv"
Write-Host " - out/linkedin_queue.csv"

