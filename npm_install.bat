CALL :INSTALL_INDEX
CALL :CHECK_FAIL
CALL :INSTALL_AUTH
CALL :CHECK_FAIL
CALL :INSTALL_AUTH_GOOGLE
CALL :CHECK_FAIL
CALL :INSTALL_QUEST_EDITOR
CALL :CHECK_FAIL
pause

:: /// check if the app has failed
:CHECK_FAIL
if NOT ["%errorlevel%"]==["0"] (
    pause
)

:INSTALL_INDEX
CD %~dp0\web\static
CALL npm install

:INSTALL_AUTH
CD %~dp0\web\auth\static
CALL npm install

:INSTALL_AUTH_GOOGLE
CD %~dp0\web\auth\google\static
CALL npm install

:INSTALL_QUEST_EDITOR
CD %~dp0\web\quest_editor\static
CALL npm install