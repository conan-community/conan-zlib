echo on
where cmake
where conan

if "%CONAN_COMPILER%" equ "" goto conan_package_tools
conan export lasote/ci
set path=C:\Python27\Scripts;C:\Program Files (x86)\CMake\bin;c:\c:\mingw-w64-i686-sjlj-posix-4.9.2\bin&&conan test_package -s os="Windows" -s arch="x86" -s build_type="Release" -s compiler=gcc -s compiler.libcxx=libstdc++ -s compiler.version="4.9" -o zlib:shared="True"
goto :eof

:conan_package_tools
python build.py
