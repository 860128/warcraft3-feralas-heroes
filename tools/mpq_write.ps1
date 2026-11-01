param([string]$MapPath, [string]$PayloadDir, [string]$FileList)
$ErrorActionPreference = 'Stop'
$here = Split-Path -Parent $MyInvocation.MyCommand.Path
$asm = [Reflection.Assembly]::LoadFrom((Join-Path $here 'StormLibSharp.dll'))
$nm = $asm.GetType('StormLibSharp.Native.NativeMethods')
$removeMethod = $nm.GetMethod('SFileRemoveFile')
$flushMethod = $nm.GetMethod('SFileFlushArchive')
$mpq = New-Object StormLibSharp.MpqArchive($MapPath, [System.IO.FileAccess]::ReadWrite)
$handle = $mpq.GetType().GetField('_handle', [Reflection.BindingFlags]'NonPublic,Instance').GetValue($mpq)
foreach ($f in ($FileList -split ',')) {
  $f = $f.Trim(); if (-not $f) { continue }
  $local = Join-Path $PayloadDir $f
  if (-not (Test-Path -LiteralPath $local)) { "SKIP $f"; continue }
  if ($mpq.HasFile($f)) {
    $arr = New-Object 'object[]' 3; $arr[0] = $handle; $arr[1] = [string]$f; $arr[2] = [uint32]0
    $r = $removeMethod.Invoke($null, $arr); "REMOVE $f -> $r"
  }
  $mpq.AddFileFromDisk($local, $f)
  "ADD $f size=$((Get-Item -LiteralPath $local).Length) ok=$($mpq.HasFile($f))"
}
$farr = New-Object 'object[]' 1; $farr[0] = $handle
$flushMethod.Invoke($null, $farr) | Out-Null
$mpq.Dispose()
"size(after)=" + (Get-Item -LiteralPath $MapPath).Length
