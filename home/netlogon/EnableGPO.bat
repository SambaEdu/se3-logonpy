netsh firewall reset
netsh firewall set portopening protocol=UDP port=137 name=se3_137 mode=ENABLE scope=CUSTOM addresses=%se3ip%/255.255.255.255
netsh firewall set portopening protocol=TCP port=139 name=se3_139 mode=ENABLE scope=CUSTOM addresses=%se3ip%/255.255.255.255
netsh firewall set portopening protocol=UDP port=138 name=se3_138 mode=ENABLE scope=CUSTOM addresses=%se3ip%/255.255.255.255
netsh firewall set portopening protocol=TCP port=445 name=se3_445 mode=ENABLE scope=CUSTOM addresses=%se3ip%/255.255.255.255
reg delete "HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\LanmanServer\Parameters" /v "AutoShareWks" /f 2>NUL
reg add "HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Lsa" /v "ForceGuest" /t "REG_DWORD" /d "0" /f 2>NUL 
reg add "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\NetCache" /v "Formatdatabase" /t "REG_DWORD" /d "1" /F 2>NUL
reg add "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\NetCache" /v "Enabled" /t "REG_DWORD" /d "0" /F 2>NUL

:: recherche du numero de version gpo et on l'incremente si il existe.
for /f "tokens=2 delims=x" %%a in ('reg query "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Group Policy\State\Machine\GPO-List\0" /v Version ^| findstr REG_DWORD') do set /a VERSION=0x%%a+65537
if "%VERSION%"=="" set VERSION=65537

%sharecmd%
rd /S /Q %SYSTEMROOT%\System32\GroupPolicy
mkdir %SYSTEMROOT%\System32\GroupPolicy
mkdir %SYSTEMROOT%\System32\GroupPolicy\Machine
mkdir %SYSTEMROOT%\System32\GroupPolicy\Machine\Scripts
mkdir %SYSTEMROOT%\System32\GroupPolicy\Machine\Scripts\Startup
mkdir %SYSTEMROOT%\System32\GroupPolicy\Machine\Scripts\Shutdown
mkdir %SYSTEMROOT%\System32\GroupPolicy\User
mkdir %SYSTEMROOT%\System32\GroupPolicy\User\Scripts
mkdir %SYSTEMROOT%\System32\GroupPolicy\User\Scripts\logon
mkdir %SYSTEMROOT%\System32\GroupPolicy\User\Scripts\logoff
:: cacls.exe "%SYSTEMROOT%\System32\GroupPolicy" /E /T /G "BUILTIN\Administrateurs":F /C >NUL
copy \\%se3ip%\netlogon\scriptsC.ini %SYSTEMROOT%\System32\GroupPolicy\Machine\Scripts\scripts.ini
copy \\%se3ip%\netlogon\machine\%machine%\user.pol %SYSTEMROOT%\System32\GroupPolicy\User\registry.pol
copy \\%se3ip%\netlogon\machine\%machine%\printers.vbs %SYSTEMROOT%\printers.vbs
copy \\%se3ip%\netlogon\machine\%machine%\machine.pol %SYSTEMROOT%\System32\GroupPolicy\Machine\registry.pol
copy \\%se3ip%\netlogon\machine\%machine%\startup.cmd %SYSTEMROOT%\System32\GroupPolicy\Machine\Scripts\Startup\startup.cmd
copy \\%se3ip%\netlogon\machine\%machine%\shutdown.cmd %SYSTEMROOT%\System32\GroupPolicy\Machine\Scripts\Shutdown\shutdown.cmd
:: scripts user ?
copy \\%se3ip%\netlogon\scriptsU.ini %SYSTEMROOT%\System32\GroupPolicy\User\Scripts\scripts.ini
copy \\%se3ip%\netlogon\machine\%machine%\shutdown.cmd %SYSTEMROOT%\System32\GroupPolicy\User\Scripts\Logoff\logoff.cmd
del /f /s /q %SYSTEMROOT%\web\wallpaper\se3.bmp
if exist \\%se3ip%\Docs\media\fonds_ecran\%user%.bmp copy \\%se3ip%\Docs\media\fonds_ecran\%user%.bmp %SYSTEMROOT%\web\wallpaper\se3.bmp

:: creation du fichier gpt.ini
echo [general]>%SYSTEMROOT%\System32\GroupPolicy\gpt.ini
echo Version=%VERSION%>>%SYSTEMROOT%\System32\GroupPolicy\gpt.ini
echo gPCUserExtensionNames=[{35378EAC-683F-11D2-A89A-00C04FBBCFA2}{0F6B957E-509E-11D1-A7CC-0000F87571E3}][{42B5FAAE-6536-11D2-AE5A-0000F87571E3}{40B66650-4972-11D1-A7CA-0000F87571E3}]>>%SYSTEMROOT%\System32\GroupPolicy\gpt.ini
echo gPCMachineExtensionNames=[{35378EAC-683F-11D2-A89A-00C04FBBCFA2}{0F6B957D-509E-11D1-A7CC-0000F87571E3}][{42B5FAAE-6536-11D2-AE5A-0000F87571E3}{40B6664F-4972-11D1-A7CA-0000F87571E3}]>>%SYSTEMROOT%\System32\GroupPolicy\gpt.ini
:: inutile, on les DL au logon
:: copy  %SYSTEMROOT%\System32\GroupPolicy\gpt.ini \\%se3ip%\netlogon\machine\%machine%\gpt.ini

cacls %SYSTEMROOT%\System32\GroupPolicy\User\registry.pol /E /G %domain%\%user%:RDX
cacls %SYSTEMROOT%\System32\GroupPolicy\gpt.ini /E /G %domain%\%user%:R
gpupdate /force
echo cpau ok>%SYSTEMROOT%\System32\GroupPolicy\Se3.log
echo %VERSION%>>%SYSTEMROOT%\System32\GroupPolicy\Se3.log
time /T >> %SYSTEMDRIVE%\netinst\logs\domscripts.txt
echo cpau ok>> %SYSTEMDRIVE%\netinst\logs\domscripts.txt
echo %VERSION%>> %SYSTEMDRIVE%\netinst\logs\domscripts.txt
