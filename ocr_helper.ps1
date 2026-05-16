# Windows Built-in OCR Helper for BoltPDF
# Uses Windows.Media.Ocr (available on Windows 10/11) — zero installs needed.
# Outputs word-level bounding boxes grouped by line for precise text selection.
param([string]$ImagePath)

# Load WinRT assemblies
Add-Type -AssemblyName System.Runtime.WindowsRuntime
$null = [Windows.Media.Ocr.OcrEngine, Windows.Foundation.UniversalApiContract, ContentType = WindowsRuntime]
$null = [Windows.Storage.StorageFile, Windows.Storage, ContentType = WindowsRuntime]
$null = [Windows.Graphics.Imaging.BitmapDecoder, Windows.Graphics, ContentType = WindowsRuntime]

# Helper: await WinRT async operations from PowerShell
function Invoke-Await {
    param($AsyncOp, [Type]$ResultType)
    $methods = [System.WindowsRuntimeSystemExtensions].GetMethods() |
        Where-Object { $_.Name -eq 'AsTask' -and $_.IsGenericMethod -and $_.GetParameters().Count -eq 1 }
    foreach ($m in $methods) {
        try {
            $task = $m.MakeGenericMethod($ResultType).Invoke($null, @($AsyncOp))
            $task.Wait(-1) | Out-Null
            return $task.Result
        } catch [System.ArgumentException] { continue }
    }
    throw "Failed to await async operation for type $ResultType"
}

try {
    # Create OCR engine from user's language preferences
    $engine = [Windows.Media.Ocr.OcrEngine]::TryCreateFromUserProfileLanguages()
    if ($null -eq $engine) {
        Write-Output '{"error":"No OCR language packs available.","lines":[]}'
        exit 1
    }

    # Resolve to absolute path
    $absPath = (Resolve-Path $ImagePath).Path

    # Load image
    $file = Invoke-Await ([Windows.Storage.StorageFile]::GetFileFromPathAsync($absPath)) ([Windows.Storage.StorageFile])
    $stream = Invoke-Await ($file.OpenAsync([Windows.Storage.FileAccessMode]::Read)) ([Windows.Storage.Streams.IRandomAccessStream])
    $decoder = Invoke-Await ([Windows.Graphics.Imaging.BitmapDecoder]::CreateAsync($stream)) ([Windows.Graphics.Imaging.BitmapDecoder])
    $bitmap = Invoke-Await ($decoder.GetSoftwareBitmapAsync()) ([Windows.Graphics.Imaging.SoftwareBitmap])

    # Run OCR
    $result = Invoke-Await ($engine.RecognizeAsync($bitmap)) ([Windows.Media.Ocr.OcrResult])

    # Build word-level output grouped by line
    $lines = @()
    foreach ($line in $result.Lines) {
        if ($line.Words.Count -eq 0) { continue }

        $words = @()
        foreach ($word in $line.Words) {
            $r = $word.BoundingRect
            # Sanitize text: strip control characters
            $cleanText = ($word.Text -replace '[\x00-\x1f\x7f]', '').Trim()
            if ($cleanText.Length -eq 0) { continue }

            $words += @{
                text = $cleanText
                x    = [int][math]::Floor($r.X)
                y    = [int][math]::Floor($r.Y)
                w    = [int][math]::Ceiling($r.Width)
                h    = [int][math]::Ceiling($r.Height)
            }
        }

        if ($words.Count -gt 0) {
            $lines += @{ words = $words }
        }
    }

    # Output JSON
    $output = @{ lines = $lines; error = $null }
    $output | ConvertTo-Json -Depth 4 -Compress

    # Cleanup
    $stream.Dispose()

} catch {
    $errMsg = $_.Exception.Message -replace '"', '\"'
    Write-Output "{`"error`":`"$errMsg`",`"lines`":[]}"
    exit 1
}
