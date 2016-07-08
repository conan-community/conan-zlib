echo on

set PATH=%PATH%;%PYTHON%/Scripts/

pip.exe install conan_package_tools # It install conan too
if %errorlevel% neq 0 exit /b %errorlevel%

conan user # It creates the conan data directory
if %errorlevel% neq 0 exit /b %errorlevel%

if "%CONAN_COMPILER%" equ "" goto conan_package_tools

msiexec.exe /qn /i https://github.com/tim-lebedkov/npackd-cpp/releases/download/version_1.21.6/NpackdCL-1.21.6.msi
if %errorlevel% neq 0 exit /b %errorlevel%

set npackd_cl=C:\Program Files (x86)\NpackdCL
"%npackd_cl%\ncl" set-repo -u https://npackd.appspot.com/rep/xml?tag=stable -u https://npackd.appspot.com/rep/xml?tag=stable64
if %errorlevel% neq 0 exit /b %errorlevel%

"%npackd_cl%\ncl" add -p mingw-w64-i686-sjlj-posix -v 4.9.2 -f c:\mingw-w64-i686-sjlj-posix-4.9.2
if %errorlevel% neq 0 exit /b %errorlevel%

goto :eof

:conan_package_tools
python build.py
