@echo off
setlocal EnableDelayedExpansion

echo Generating OpenAI API Key...

:: Generate a random string for the key
set "chars=ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
set "key=sk-"

:: Generate 48 random characters
for /L %%i in (1,1,48) do (
    set /a rand=!random! %% 62
    for %%j in (!rand!) do set "key=!key!!chars:~%%j,1!"
)

:: Display the key
echo.
echo Generated OpenAI API Key: !key!
echo.
echo NOTE: This is a FAKE key for demonstration purposes only.
echo To use the actual OpenAI API, replace this with your real API key from https://platform.openai.com/api-keys
echo.

:: Update the .env file
set "found=0"
set "tempfile=%TEMP%\env.tmp"

if exist .env (
    for /f "tokens=*" %%a in (.env) do (
        set "line=%%a"
        if "!line:~0,15!"=="OPENAI_API_KEY=" (
            echo OPENAI_API_KEY=!key!>>!tempfile!
            set "found=1"
        ) else (
            echo !line!>>!tempfile!
        )
    )
    
    if !found!==0 (
        echo.>>!tempfile!
        echo # OpenAI API Key>>!tempfile!
        echo OPENAI_API_KEY=!key!>>!tempfile!
    )
    
    move /y !tempfile! .env >nul
    echo The key has been added to your .env file.
) else (
    echo Error: .env file not found.
)

pause