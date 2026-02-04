$ErrorActionPreference = "Stop"

$RepoRoot = Split-Path -Parent $PSScriptRoot
$ScriptPath = Join-Path $PSScriptRoot "generate_project.py"

$PythonExe = $null
$PyCmd = Get-Command py -ErrorAction SilentlyContinue
if ($PyCmd) {
    $PythonExe = $PyCmd.Source
    $PythonArgs = "-3 `"$ScriptPath`""
} else {
    $PyCmd = Get-Command python -ErrorAction SilentlyContinue
    if ($PyCmd) {
        $PythonExe = $PyCmd.Source
        $PythonArgs = "`"$ScriptPath`""
    }
}

if (-not $PythonExe) {
    throw "Python executable not found. Install Python or add it to PATH."
}

$Action = New-ScheduledTaskAction -Execute $PythonExe -Argument $PythonArgs -WorkingDirectory $RepoRoot
$Trigger1 = New-ScheduledTaskTrigger -Daily -At 00:00
$Trigger1.RandomDelay = New-TimeSpan -Hours 12
$Trigger2 = New-ScheduledTaskTrigger -Daily -At 12:00
$Trigger2.RandomDelay = New-TimeSpan -Hours 12

$Settings = New-ScheduledTaskSettingsSet -StartWhenAvailable -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -MultipleInstances IgnoreNew

$TaskName = "AIProjects-Generator"
if (Get-ScheduledTask -TaskName $TaskName -ErrorAction SilentlyContinue) {
    Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false
}

Register-ScheduledTask -TaskName $TaskName -Action $Action -Trigger @($Trigger1, $Trigger2) -Settings $Settings | Out-Null
Write-Host "Scheduled task '$TaskName' created with two random daily runs."
