<#
.SYNOPSIS
List all properties and values of the Win32_BIOS class in WMI's root/cimv2 namespace

.DESCRIPTION
This PowerShell 7 script was generated using WMIGen (formerly known as WMI Code Generator), Version 10.0.15.0 and then trimmed manually.
WMIGen's PowerShell template script was updated to PowerShell 7 by Thierry Montané.
It queries WMI to list all properties and values of the Win32_BIOS class in the root/cimv2 namepace, for the local or a remote computer.

.PARAMETER Computer
The optional name of a remote computer to be queried.
If not specified, the local computer will be queried.

.LINK
WMIGen multi-language code generator by Rob van der Woude
https://www.robvanderwoude.com/wmigen.php
#>

param( [string]$Computer = "." )

if ( $computer -eq "." ) {
	$instances = Get-CimInstance -ClassName "Win32_BIOS" -Namespace "root/cimv2"
} else {
	$instances = Get-CimInstance -ClassName "Win32_BIOS" -Namespace "root/cimv2" -ComputerName "$Computer"
}

$count = ( $instances | Measure-Object ).Count
if ( $count -eq 1 ) {
	Write-Host "1 instance:"
} else {
	Write-Host "$count instances:"
}
Write-Host

foreach ($objItem in $instances) {
	write-host "Name                           :" $objItem.Name
	write-host "Version                        :" $objItem.Version
	write-host "Manufacturer                   :" $objItem.Manufacturer
	write-host "SMBIOSBIOS Version             :" $objItem.SMBIOSBIOSVersion
	write-host
}
