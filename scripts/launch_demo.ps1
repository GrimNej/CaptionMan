param(
    [ValidateSet("mock", "fireworks_direct")]
    [string]$Provider = "fireworks_direct",
    [int]$ApiPort = 8000,
    [int]$WebPort = 3000,
    [switch]$Restart,
    [switch]$LiveDoctor,
    [switch]$SkipOpen
)

$ErrorActionPreference = "Stop"
trap {
    Write-Error $_
    exit 1
}

$RepoRoot = Split-Path -Parent $PSScriptRoot
$ApiDir = Join-Path $RepoRoot "apps\api"
$WebDir = Join-Path $RepoRoot "apps\web"
$ApiLogDir = Join-Path $ApiDir ".data"
$WebLogDir = Join-Path $WebDir ".next"
$ApiOut = Join-Path $ApiLogDir "api-live.log"
$ApiErr = Join-Path $ApiLogDir "api-live.err.log"
$WebOut = Join-Path $WebLogDir "web-live.log"
$WebErr = Join-Path $WebLogDir "web-live.err.log"

function Get-ListenerProcessId {
    param([int]$Port)

    $listener = Get-NetTCPConnection -LocalPort $Port -State Listen -ErrorAction SilentlyContinue |
        Select-Object -First 1
    if ($null -eq $listener) {
        return $null
    }
    return $listener.OwningProcess
}

function Stop-PortListener {
    param([int]$Port)

    $processId = Get-ListenerProcessId -Port $Port
    if ($null -ne $processId) {
        Stop-Process -Id $processId -Force
        Start-Sleep -Seconds 1
    }
}

function Assert-Command {
    param([string]$Name)

    $command = Get-Command $Name -ErrorAction SilentlyContinue
    if ($null -eq $command) {
        throw "Required command '$Name' was not found on PATH."
    }

    if ($command.Source -match "\.ps1$") {
        $cmdShim = [System.IO.Path]::ChangeExtension($command.Source, ".cmd")
        if (Test-Path $cmdShim) {
            return $cmdShim
        }
    }

    if ($command.Source -notmatch "\.(cmd|exe|bat)$") {
        $nativeCommand = Get-Command $Name -All |
            Where-Object { $_.Source -match "\.(cmd|exe|bat)$" } |
            Select-Object -First 1
        if ($null -ne $nativeCommand) {
            return $nativeCommand.Source
        }
    }

    return $command.Source
}

function Wait-HttpOk {
    param(
        [string]$Uri,
        [int]$TimeoutSeconds = 45,
        [switch]$Json
    )

    $deadline = (Get-Date).AddSeconds($TimeoutSeconds)
    $lastError = $null
    while ((Get-Date) -lt $deadline) {
        try {
            if ($Json) {
                return Invoke-RestMethod -Uri $Uri -TimeoutSec 5
            }
            $response = Invoke-WebRequest -Uri $Uri -TimeoutSec 5
            if ($response.StatusCode -ge 200 -and $response.StatusCode -lt 400) {
                return $response
            }
        }
        catch {
            $lastError = $_.Exception.Message
            Start-Sleep -Seconds 2
        }
    }

    throw "Timed out waiting for $Uri. Last error: $lastError"
}

function Start-ServiceProcess {
    param(
        [string]$FilePath,
        [string[]]$Arguments,
        [string]$WorkingDirectory,
        [string]$StdOutPath,
        [string]$StdErrPath
    )

    $process = Start-Process `
        -FilePath $FilePath `
        -ArgumentList $Arguments `
        -WorkingDirectory $WorkingDirectory `
        -RedirectStandardOutput $StdOutPath `
        -RedirectStandardError $StdErrPath `
        -WindowStyle Hidden `
        -PassThru

    return $process.Id
}

New-Item -ItemType Directory -Force -Path $ApiLogDir | Out-Null
New-Item -ItemType Directory -Force -Path $WebLogDir | Out-Null

$uv = Assert-Command "uv"
$pnpm = Assert-Command "pnpm"

if ($Restart) {
    Stop-PortListener -Port $ApiPort
    Stop-PortListener -Port $WebPort
}

$apiPid = Get-ListenerProcessId -Port $ApiPort
$webPid = Get-ListenerProcessId -Port $WebPort

if ($null -eq $apiPid) {
    $env:OFFICIAL_MODE = "true"
    $env:AI_PROVIDER = $Provider
    $env:MODEL_ROUTING_MODE = "champion"
    $env:CHAMPION_ROUTE = "fireworks_qwen37_glm"
    $env:VISION_MODEL = "accounts/fireworks/models/qwen3p7-plus"
    $env:VISION_FALLBACK_MODEL = "accounts/fireworks/models/kimi-k2p7-code"
    $env:GEMMA_USAGE_MODE = "off"
    $env:CAPTION_CANDIDATES_PER_STYLE = "1"
    $env:MAX_MODEL_CALLS_PER_VIDEO = "8"
    $env:MAX_EVIDENCE_ATTEMPTS = "2"
    $env:MAX_CAPTION_RECOVERY_CALLS = "3"
    $env:NUM_FRAMES = "12"
    $env:MIN_FRAMES = "10"
    $env:MAX_FRAMES = "14"
    $env:CORS_ORIGINS = "http://localhost:$WebPort,http://127.0.0.1:$WebPort"

    $apiPid = Start-ServiceProcess `
        -FilePath $uv `
        -Arguments @("run", "uvicorn", "app.server.main:api", "--host", "127.0.0.1", "--port", "$ApiPort") `
        -WorkingDirectory $ApiDir `
        -StdOutPath $ApiOut `
        -StdErrPath $ApiErr
}

if ($null -eq $webPid) {
    $env:NEXT_PUBLIC_API_BASE_URL = "http://127.0.0.1:$ApiPort"

    $webPid = Start-ServiceProcess `
        -FilePath $pnpm `
        -Arguments @("exec", "next", "start", "-H", "127.0.0.1", "-p", "$WebPort") `
        -WorkingDirectory $WebDir `
        -StdOutPath $WebOut `
        -StdErrPath $WebErr
}

$health = Wait-HttpOk -Uri "http://127.0.0.1:$ApiPort/api/health" -Json -TimeoutSeconds 45
if ($true -ne $health.ok) {
    throw "API health check returned an unhealthy response."
}

$doctorUri = "http://127.0.0.1:$ApiPort/api/doctor?live=$($LiveDoctor.IsPresent.ToString().ToLowerInvariant())"
$doctor = Wait-HttpOk -Uri $doctorUri -Json -TimeoutSeconds 90
if ($true -ne $doctor.ok) {
    throw "API doctor check failed. See $ApiErr"
}

Wait-HttpOk -Uri "http://127.0.0.1:$WebPort/studio" -TimeoutSeconds 60 | Out-Null

if (-not $SkipOpen) {
    Start-Process "http://127.0.0.1:$WebPort/studio"
}

Write-Output "CaptionMan Studio is ready: http://127.0.0.1:$WebPort/studio"
Write-Output "API is ready: http://127.0.0.1:$ApiPort/api/health"
Write-Output "Provider mode: $Provider"
Write-Output "API PID: $apiPid"
Write-Output "Web PID: $webPid"
Write-Output "API logs: $ApiOut"
Write-Output "Web logs: $WebOut"
