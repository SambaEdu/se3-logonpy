On Error Resume Next
Set oWsh = CreateObject("WScript.Shell")
Const HKEY_USERS = &H80000003
Const HKEY_LOCAL_MACHINE = &H80000002 

strComputer = "."

Set objRegistry = GetObject("winmgmts:\\" & _
    strComputer & "\root\default:StdRegProv") 

Sub DeleteUserSubkeys(strKeyPath) 
    objRegistry.EnumKey HKEY_USERS, strKeyPath, arrSubkeys 

    If IsArray(arrSubkeys) Then 
        For Each strSubkey In arrSubkeys 
            DeleteUserSubkeys strKeyPath & "\" & strSubkey 
        Next 
    End If 

    objRegistry.DeleteKey HKEY_USERS, strKeyPath 
End Sub

Sub DeleteLocalSubkeys(strKeyPath) 
    objRegistry.EnumKey HKEY_LOCAL_MACHINE, strKeyPath, arrSubkeys 

    If IsArray(arrSubkeys) Then 
        For Each strSubkey In arrSubkeys 
            DeleteLocalSubkeys strKeyPath & "\" & strSubkey 
        Next 
    End If 
    objRegistry.DeleteKey HKEY_LOCAL_MACHINE, strKeyPath 
End Sub
