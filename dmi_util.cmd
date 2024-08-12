@echo off
setlocal

:: Check for the first argument
if "%~1"=="" (
    echo Usage: dmi_util build, run, test, peek
    exit /b 1
)

:: Execute commands based on the argument
if "%~1"=="build" (
    echo Building Docker image...
    docker build -t dmi_gribcatcher .
) else if "%~1"=="remove" (
    echo Removing Docker image...
    docker rmi dmi_gribcatcher -f
) else if "%~1"=="run" (
    echo Running Docker container...
    docker run dmi_gribcatcher
) else if "%~1"=="test" (
    echo Building and running Docker container...
    call dmi_util build
    call dmi_util run
) else if "%~1"=="peek" (
    echo Running Docker container interactively...
    docker run -it dmi_gribcatcher bash
) else (
    echo Invalid argument: %~1
    echo Usage: dmi_util build, run, test, peek
    exit /b 1
)

endlocal
