Set-Location "C:\Users\wyh\.gemini\antigravity\scratch\feralas_hero"
Copy-Item feralas_orig.w3x rebuild_feralas.w3x -Force

$files = @('war3map.w3a', 'war3map.w3u', 'war3map.j', 'war3map.wts')
Get-ChildItem "payload\_Locales" -Recurse -Filter "war3map.wts" | ForEach-Object {
    $rel = $_.FullName.Substring((Resolve-Path "payload").Path.Length + 1)
    $files += $rel
}
$fileListStr = $files -join ','

Write-Host "Files to inject:" $fileListStr
& "C:\Windows\SysWOW64\WindowsPowerShell\v1.0\powershell.exe" -ExecutionPolicy Bypass -File tools/mpq_write.ps1 rebuild_feralas.w3x payload $fileListStr
