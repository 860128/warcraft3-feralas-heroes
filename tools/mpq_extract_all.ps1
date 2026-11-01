param([string]$MapPath, [string]$OutDir)
$ErrorActionPreference = 'Stop'
$here = Split-Path -Parent $MyInvocation.MyCommand.Path
[Reflection.Assembly]::LoadFrom((Join-Path $here 'StormLibSharp.dll')) | Out-Null
New-Item -ItemType Directory -Force -Path $OutDir | Out-Null
$mpq = New-Object StormLibSharp.MpqArchive($MapPath, [System.IO.FileAccess]::Read)
$lf = Join-Path $OutDir '(listfile)'
$names = @()
if ($mpq.HasFile('(listfile)')) {
  $mpq.ExtractFile('(listfile)', $lf)
  $names = Get-Content -LiteralPath $lf | Where-Object { $_ -ne '' }
}
$extra = @('war3map.w3a','war3map.w3u','war3map.w3t','war3map.w3q','war3map.w3b','war3map.w3h','war3map.w3d','war3mapMisc.txt','war3mapSkin.txt','war3mapExtra.txt','war3map.wts','war3map.j','war3map.lua','war3map.imp')
$all = @($names) + $extra | Select-Object -Unique
foreach ($n in $all) {
  if (-not $mpq.HasFile($n)) { continue }
  $dest = Join-Path $OutDir $n
  New-Item -ItemType Directory -Force -Path (Split-Path -Parent $dest) | Out-Null
  $mpq.ExtractFile($n, $dest)
  if (Test-Path -LiteralPath $dest) { "{0}`t{1}" -f $n, (Get-Item -LiteralPath $dest).Length } else { "NULLFILE`t$n" }
}
$mpq.Dispose()
