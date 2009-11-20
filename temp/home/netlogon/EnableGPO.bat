netsh firewall set portopening protocol=UDP port=137 name=se3_137 mode=ENABLE scope=CUSTOM addresses=%se3ip%/255.255.255.255
netsh firewall set portopening protocol=TCP port=139 name=se3_139 mode=ENABLE scope=CUSTOM addresses=%se3ip%/255.255.255.255
netsh firewall set portopening protocol=UDP port=138 name=se3_138 mode=ENABLE scope=CUSTOM addresses=%se3ip%/255.255.255.255
netsh firewall set portopening protocol=TCP port=445 name=se3_445 mode=ENABLE scope=CUSTOM addresses=%se3ip%/255.255.255.255
%sharecmd%
mkdir %SYSTEMDRIVE%\Windows\System32\GroupPolicy
mkdir %SYSTEMDRIVE%\Windows\System32\GroupPolicy\Machine
mkdir %SYSTEMDRIVE%\Windows\System32\GroupPolicy\Machine\Scripts
mkdir %SYSTEMDRIVE%\Windows\System32\GroupPolicy\Machine\Scripts\Startup
mkdir %SYSTEMDRIVE%\Windows\System32\GroupPolicy\User
mkdir %SYSTEMDRIVE%\Windows\System32\GroupPolicy\User\Scripts
mkdir %SYSTEMDRIVE%\Windows\System32\GroupPolicy\User\Scripts\logon

del %SYSTEMDRIVE%\Windows\System32\GroupPolicy\User\registry.pol
del %SYSTEMDRIVE%\Windows\System32\GroupPolicy\gpt.ini
del %SYSTEMDRIVE%\Windows\System32\GroupPolicy\User\Scripts\scripts.ini
del %SYSTEMDRIVE%\Windows\System32\GroupPolicy\Machine\Scripts\scripts.ini

copy \\%se3ip%\netlogon\machine\%machine%\user.pol %SYSTEMDRIVE%\Windows\System32\GroupPolicy\User\registry.pol
copy \\%se3ip%\netlogon\machine\%machine%\printers.vbs %SYSTEMDRIVE%\Windows\printers.vbs
copy \\%se3ip%\netlogon\machine\%machine%\machine.pol %SYSTEMDRIVE%\Windows\System32\GroupPolicy\Machine\registry.pol
copy \\%se3ip%\netlogon\machine\%machine%\startup.bat %SYSTEMDRIVE%\Windows\System32\GroupPolicy\Machine\Scripts\Startup\startup.bat
copy \\%se3ip%\netlogon\machine\%machine%\gpt.ini %SYSTEMDRIVE%\Windows\System32\GroupPolicy\gpt.ini

cacls %SYSTEMDRIVE%\Windows\System32\GroupPolicy\User\registry.pol /E /R Administrateur
cacls %SYSTEMDRIVE%\Windows\System32\GroupPolicy\User\registry.pol /E /R "Utilisateurs avec pouvoir"
cacls %SYSTEMDRIVE%\Windows\System32\GroupPolicy\User\registry.pol /E /R "Utilisateurs"
cacls %SYSTEMDRIVE%\Windows\System32\GroupPolicy\User\registry.pol /E /R Administrateurs
cacls %SYSTEMDRIVE%\Windows\System32\GroupPolicy\gpt.ini /E /R Administrateur
cacls %SYSTEMDRIVE%\Windows\System32\GroupPolicy\gpt.ini /E /R "Utilisateurs avec pouvoir"
cacls %SYSTEMDRIVE%\Windows\System32\GroupPolicy\gpt.ini /E /R "Utilisateurs"
cacls %SYSTEMDRIVE%\Windows\System32\GroupPolicy\gpt.ini /E /R Administrateurs


cacls %SYSTEMDRIVE%\Windows\System32\GroupPolicy\User\registry.pol /E /G adminse3:F
cacls %SYSTEMDRIVE%\Windows\System32\GroupPolicy\User\registry.pol /E /G system:F
cacls %SYSTEMDRIVE%\Windows\System32\GroupPolicy\User\registry.pol /E /G %domain%\%user%:R
cacls %SYSTEMDRIVE%\Windows\System32\GroupPolicy\gpt.ini /E /G adminse3:F
cacls %SYSTEMDRIVE%\Windows\System32\GroupPolicy\gpt.ini /E /G system:F
cacls %SYSTEMDRIVE%\Windows\System32\GroupPolicy\gpt.ini /E /G %domain%\%user%:R

gpupdate /force
