echo on
where cmake
where conan

if "%CONAN_COMPILER%" equ "" goto conan_package_tools
conan export lasote/testing
set path=C:\Program Files (x86)\CMake\bin;c:\mingw\bin&&conan test_package . -s arch="x86" -s build_type="Release" -s compiler=gcc -s compiler.libcxx=libstdc++ -s compiler.version="4.8" -o zlib:shared="False"
goto :eof

:conan_package_tools
python build.py
