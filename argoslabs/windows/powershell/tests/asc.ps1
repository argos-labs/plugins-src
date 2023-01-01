function Syntax {
    Write-Host
    Write-Host "Asc.ps1,  Version 1.00"
    Write-Host "Returns the numeric ASCII value for the specified character"
    Write-Host
    Write-Host "Usage:   " -NoNewline
    Write-Host "ASC.PS1  char" -ForegroundColor White
    Write-Host
    Write-Host "Returns: Numeric ASCII value of " -NoNewline
    Write-Host "char" -ForegroundColor White
    Write-Host
    Write-Host "Notes:   The ASCII value is written to Standard Output (usually the screen)"
    Write-Host "         as well as returned as `"errorlevel`""
    Write-Host "         If more than 1 character is passed on the command line, only the first"
    Write-Host "         character will be used, the remainder of the string will be ignored."
    Write-Host "         The `"errorlevel`" will equal the ASCII value, or 0 if no parameter"
    Write-Host "         was passed, or -1 in case of errors or for this help"
    Write-Host
    Write-Host "Credits: Code to pass exit code as `"errorlevel`" to the calling batch file"
    Write-Host "         or PowerShell script by Serge van den Oever:"
    Write-Host "         weblogs.asp.net/soever/returning-an-exit-code-from-a-powershell-script" -ForegroundColor DarkGray
    Write-Host
    Write-Host "Written by Rob van der Woude"
    Write-Host "http://www.robvanderwoude.com"

    $Host.SetShouldExit( -1 )
    Exit
}

if ( $args.Length -eq 1 ) {
    if ( $args[0] -eq "/?" ) {
        Syntax
    } else {
        $input = $args[0]
    }
} else {
    Syntax
}

if ( $input -eq "" ) { $input = [string][char]0 }

[char]$char = $input[0]

Write-Host ([byte]$char) -NoNewline

# Pass exit code to calling batch or PowerShell script, by Serge van den Oever
# https://weblogs.asp.net/soever/returning-an-exit-code-from-a-powershell-script
$Host.SetShouldExit( [byte]$char )
# Exit
