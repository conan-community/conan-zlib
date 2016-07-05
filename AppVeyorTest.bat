if "%CONAN_COMPILER%" equ "" goto conan_package_tools
set cc=c:\mingw\bin\gcc.exe
conan export lasote/testing
conan test_package . -s arch="x86" -s build_type="Release" -s compiler=gcc -s compiler.version="4.8" -o zlib:shared="False"
goto :eof

:conan_package_tools
python build.py
