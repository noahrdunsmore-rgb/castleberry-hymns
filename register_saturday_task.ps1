<#
    Registers (or updates) a Windows Scheduled Task that runs the Saturday-night
    safety net, so a worship deck is ready before the 11:50 PM CST deadline.

    Usage (normal PowerShell — no admin needed for a per-user task):
        powershell -ExecutionPolicy Bypass -File register_saturday_task.ps1
        powershell -ExecutionPolicy Bypass -File register_saturday_task.ps1 -Time "21:30"
        powershell -ExecutionPolicy Bypass -File register_saturday_task.ps1 -Unregister

    Default run time is 9:00 PM every Saturday, leaving a buffer before 11:50 PM
    so a reminder email can still prompt you to build manually if needed.
    Re-run after moving the project folder to refresh the stored paths.
#>

param(
    [string]$Time = "21:00",
    [switch]$Unregister
)

$TaskName  = "CastleberryServiceDeck"
$ProjDir   = Split-Path -Parent $MyInvocation.MyCommand.Path
$Script    = Join-Path $ProjDir "saturday_build.py"

# Prefer pythonw.exe (no console window) for an unattended task; fall back to python.
$PyW = (Get-Command pythonw.exe -ErrorAction SilentlyContinue).Source
if (-not $PyW) { $PyW = (Get-Command python.exe -ErrorAction SilentlyContinue).Source }
if (-not $PyW) { Write-Error "Could not find python on PATH."; exit 1 }

if ($Unregister) {
    Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false -ErrorAction SilentlyContinue
    Write-Host "Removed scheduled task '$TaskName'."
    exit 0
}

$Action  = New-ScheduledTaskAction -Execute $PyW -Argument "`"$Script`"" -WorkingDirectory $ProjDir
$Trigger = New-ScheduledTaskTrigger -Weekly -DaysOfWeek Saturday -At $Time
$Settings = New-ScheduledTaskSettingsSet -StartWhenAvailable -WakeToRun `
             -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries `
             -RestartCount 3 -RestartInterval (New-TimeSpan -Minutes 10)

Register-ScheduledTask -TaskName $TaskName -Action $Action -Trigger $Trigger `
    -Settings $Settings -Description "Builds the Castleberry worship deck for the upcoming Sunday." `
    -Force | Out-Null

Write-Host "Scheduled task '$TaskName' registered:"
Write-Host "  Runs : every Saturday at $Time"
Write-Host "  Cmd  : $PyW `"$Script`""
Write-Host ""
Write-Host "Test it now with:   Start-ScheduledTask -TaskName $TaskName"
Write-Host "View last result:   Get-ScheduledTaskInfo -TaskName $TaskName"
