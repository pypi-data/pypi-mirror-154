@echo off

set failure=0

set module_dir=%1
set script_dir=%2

set "module_file=%module_dir%\harfang.dll"
if not exist %module_file% (
    echo missing harfang lua module 1>&2
    exit /b 1
)

set "test_script=%script_dir%\dummy.lua"
if not exist %test_script% (
    echo missing test script 1>&2
    exit /b 1
)

set "work_dir=%temp%\lua_module_test"
mkdir %work_dir%

xcopy /s "%module_dir%" "%work_dir%" /y
xcopy "%test_script%" "%work_dir%" /y

pushd "%work_dir%"

lua dummy.lua
if %ERRORLEVEL% EQU 0 goto end
    echo test script failed 1>&2
    set failure=1
:end

popd
rmdir %work_dir% /s /q

if %failure% == 1 (
    exit /b 1
)