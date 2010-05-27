netsh firewall set portopening protocol=UDP port=137 name=se3_137 mode=ENABLE scope=CUSTOM addresses=%se3ip%/255.255.255.255
netsh firewall set portopening protocol=TCP port=139 name=se3_139 mode=ENABLE scope=CUSTOM addresses=%se3ip%/255.255.255.255
netsh firewall set portopening protocol=UDP port=138 name=se3_138 mode=ENABLE scope=CUSTOM addresses=%se3ip%/255.255.255.255
netsh firewall set portopening protocol=TCP port=445 name=se3_445 mode=ENABLE scope=CUSTOM addresses=%se3ip%/255.255.255.255
%sharecmd%
mkdir %SYSTEMROOT%\System32\GroupPolicy
mkdir %SYSTEMROOT%\System32\GroupPolicy\Machine
mkdir %SYSTEMROOT%\System32\GroupPolicy\Machine\Scripts
mkdir %SYSTEMROOT%\System32\GroupPolicy\Machine\Scripts\Startup
mkdir %SYSTEMROOT%\System32\GroupPolicy\User
mkdir %SYSTEMROOT%\System32\GroupPolicy\User\Scripts
mkdir %SYSTEMROOT%\System32\GroupPolicy\User\Scripts\logon

cacls.exe "%SYSTEMROOT%\System32\GroupPolicy" /E /T /G "BUILTIN\Administrateurs":F /C >NUL

del %SYSTEMROOT%\System32\GroupPolicy\User\registry.pol
del %SYSTEMROOT%\System32\GroupPolicy\gpt.ini
del %SYSTEMROOT%\System32\GroupPolicy\User\Scripts\scripts.ini
del %SYSTEMROOT%\System32\GroupPolicy\Machine\Scripts\scripts.ini

copy \\%se3ip%\netlogon\machine\%machine%\user.pol %SYSTEMROOT%\System32\GroupPolicy\User\registry.pol
copy \\%se3ip%\netlogon\machine\%machine%\printers.vbs %SYSTEMROOT%\printers.vbs
copy \\%se3ip%\netlogon\machine\%machine%\machine.pol %SYSTEMROOT%\System32\GroupPolicy\Machine\registry.pol
copy \\%se3ip%\netlogon\machine\%machine%\startup.bat %SYSTEMROOT%\System32\GroupPolicy\Machine\Scripts\Startup\startup.bat
copy \\%se3ip%\netlogon\machine\%machine%\gpt.ini %SYSTEMROOT%\System32\GroupPolicy\gpt.ini

cacls %SYSTEMROOT%\System32\GroupPolicy\User\registry.pol /E /R Administrateur
cacls %SYSTEMROOT%\System32\GroupPolicy\User\registry.pol /E /R "Utilisateurs avec pouvoir"
cacls %SYSTEMROOT%\System32\GroupPolicy\User\registry.pol /E /R "Utilisateurs"
cacls %SYSTEMROOT%\System32\GroupPolicy\User\registry.pol /E /R Administrateurs
cacls %SYSTEMROOT%\System32\GroupPolicy\gpt.ini /E /R Administrateur
cacls %SYSTEMROOT%\System32\GroupPolicy\gpt.ini /E /R "Utilisateurs avec pouvoir"
cacls %SYSTEMROOT%\System32\GroupPolicy\gpt.ini /E /R "Utilisateurs"
cacls %SYSTEMROOT%\System32\GroupPolicy\gpt.ini /E /R Administrateurs


cacls %SYSTEMROOT%\System32\GroupPolicy\User\registry.pol /E /G adminse3:F
cacls %SYSTEMROOT%\System32\GroupPolicy\User\registry.pol /E /G system:F
cacls %SYSTEMROOT%\System32\GroupPolicy\User\registry.pol /E /G %domain%\%user%:R
cacls %SYSTEMROOT%\System32\GroupPolicy\gpt.ini /E /G adminse3:F
cacls %SYSTEMROOT%\System32\GroupPolicy\gpt.ini /E /G system:F
cacls %SYSTEMROOT%\System32\GroupPolicy\gpt.ini /E /G %domain%\%user%:R

gpupdate /force
