
$From = $args[0]
$To = $args[1]
$Subject = $args[2]
$Body = [IO.File]::ReadAllText("body.html")
$Attachment = "Email_Send-1.png"
$SMTPServer = "smtp.office365.com"
$SMTPPort = "587"

Send-MailMessage `
    -From $From `
    -to $To `
    -Subject $Subject `
    -Body $Body `
    -BodyAsHtml `
    -SmtpServer $SMTPServer `
    -Port $SMTPPort `
    -UseSsl `
    -Credential (Get-Credential) `
    -Attachments $Attachment
