if "%CONAN_COMPILER%" equ "" goto conan_package_tools
set cc=c:\mingw32\bin\gcc.exe
conan export lasote/testing
conan test_package
goto :eof

:conan_package_tools
python build.py
