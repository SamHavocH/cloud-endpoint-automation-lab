$ErrorActionPreference = "SilentlyContinue"

$firewallEnabled = (Get-NetFirewallProfile | Where-Object { -not $_.Enabled }).Count -eq 0
$bitlockerStatus = "unknown"
$antivirusStatus = "unknown"

if (Get-Command Get-BitLockerVolume -ErrorAction SilentlyContinue) {
    $systemVolume = Get-BitLockerVolume -MountPoint $env:SystemDrive
    $bitlockerStatus = $systemVolume.ProtectionStatus.ToString()
}

if (Get-Command Get-MpComputerStatus -ErrorAction SilentlyContinue) {
    $mpStatus = Get-MpComputerStatus
    $antivirusStatus = if ($mpStatus.AntivirusEnabled) { "enabled" } else { "disabled" }
}

$ipAddress = (Get-NetIPAddress -AddressFamily IPv4 |
    Where-Object { $_.IPAddress -notlike "169.254*" -and $_.IPAddress -ne "127.0.0.1" } |
    Select-Object -First 1 -ExpandProperty IPAddress)

[PSCustomObject]@{
    hostname = $env:COMPUTERNAME
    os_family = "Windows"
    os_version = (Get-CimInstance Win32_OperatingSystem).Caption
    current_user = [System.Security.Principal.WindowsIdentity]::GetCurrent().Name
    ip_address = $ipAddress
    firewall_enabled = $firewallEnabled
    bitlocker_status = $bitlockerStatus
    antivirus_status = $antivirusStatus
    timestamp = (Get-Date).ToUniversalTime().ToString("o")
} | ConvertTo-Json -Depth 3
