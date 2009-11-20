On Error Resume Next
Const HKEY_CURRENT_USER = &H80000001
strComputer = "."

Set objNetwork = CreateObject("WScript.Network")

Set objRegistry = GetObject("winmgmts:\\" & _
    strComputer & "\root\default:StdRegProv") 

Sub DeleteUserSubkeys(strKeyPath) 
    objRegistry.EnumKey HKEY_CURRENT_USER, strKeyPath, arrSubkeys 

    If IsArray(arrSubkeys) Then 
        For Each strSubkey In arrSubkeys 
            DeleteUserSubkeys strKeyPath & "\" & strSubkey 
        Next 
    End If 

    objRegistry.DeleteKey HKEY_CURRENT_USER, strKeyPath 
End Sub

Sub DeleteUserPrintersDevice(server)
    Set objPrinter = objNetwork.EnumPrinterConnections
    For intDrive = 0 To (objPrinter.Count -1) Step 2
        intNetLetter = IntNetLetter +1
        If (InStr(objPrinter.Item(intDrive+1), server)> 0) Then
            objNetwork.RemovePrinterConnection objPrinter.Item(intDrive+1)
        End If
    Next
    DeleteUserSubkeys "Printers\Connections"
End Sub

Sub AddUserPrinterDevice(server, printer)
    objNetwork.AddWindowsPrinterConnection "\\" & server & "\" & printer
End Sub

Sub SetUserDefaultPrinterDevice (server, printer)
    objNetwork.SetDefaultPrinter "\\" & server & "\" & printer
End Sub
