@echo off

:: It's more convenient to test the generated wheel using bash scripts because
:: venv and pip are not really designed to be used like standard Python modules.
:: Especially venv and its activation scripts.

set failure=0

set python_bin=%1
set whl_dir=%2
set script_dir=%3

if not exist %python_bin% (
    echo missing python binary 1>&2
    exit /b 1
)

for %%F in (%whl_dir%\harfang-*.whl) do (
 set whl_file=%%F
 goto ok
)
:ok
if not exist %whl_file% (
    echo missing wheel file 1>&2
    exit /b 1
)

set "test_script=%script_dir%\dummy.py"
if not exist %test_script% (
    echo missing test script 1>&2
    exit /b 1
)

set "work_dir=%temp%\harfang_wheel_test"
mkdir %work_dir%

%python_bin% -m venv %work_dir% --copies --clear
xcopy "%test_script%" "%work_dir%" /y

pushd "%work_dir%"

call Scripts\activate 
python -m pip install %whl_file% --upgrade
if %ERRORLEVEL% EQU 0 goto run_dummy
    echo wheel installation failed 1>&2
    set failure=1
    goto end
:run_dummy

python dummy.py
if %ERRORLEVEL% EQU 0 goto end
    echo test script failed 1>&2
    set failure=1
:end

call deactivate

popd
rmdir %work_dir% /s /q

if %failure% == 1 (
    exit /b 1
)