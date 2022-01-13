CALL :INSTALL_INDEX
CALL :CHECK_FAIL
CALL :INSTALL_AUTH
CALL :CHECK_FAIL
CALL :INSTALL_AUTH_GOOGLE
CALL :CHECK_FAIL
CALL :INSTALL_QUEST_EDITOR
CALL :CHECK_FAIL
CALL :INSTALL_PROFILE
CALL :CHECK_FAIL
CD %~dp0
pause
exit

:: /// check if the app has failed
:CHECK_FAIL
if NOT ["%errorlevel%"]==["0"] (
    pause
)
EXIT /B 0

:INSTALL_INDEX
CD %~dp0\web\static
echo y|rmdir /s node_modules
CALL npm install
EXIT /B 0

:INSTALL_AUTH
CD %~dp0\web\auth\static
echo y|rmdir /s node_modules
CALL npm install
EXIT /B 0

:INSTALL_AUTH_GOOGLE
CD %~dp0\web\auth\google\static
echo y|rmdir /s node_modules
CALL npm install
EXIT /B 0

:INSTALL_QUEST_EDITOR
CD %~dp0\web\quest_editor\static
echo y|rmdir /s node_modules
CALL npm install
EXIT /B 0

:INSTALL_PROFILE
CD %~dp0\web\profile\static
echo y|rmdir /s node_modules
CALL npm install
EXIT /B 0