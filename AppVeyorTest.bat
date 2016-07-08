echo on

if "%CONAN_COMPILER%" equ "" goto conan_package_tools

conan export lasote/ci
if %errorlevel% neq 0 exit /b %errorlevel%

set path=C:\Python27\Scripts;C:\Program Files (x86)\CMake\bin;c:\mingw-w64-i686-sjlj-posix-4.9.2\bin&&conan test_package -s os="Windows" -s arch="x86" -s build_type="Release" -s compiler=gcc -s compiler.libcxx=libstdc++ -s compiler.version="4.9" -o zlib:shared="True"
if %errorlevel% neq 0 exit /b %errorlevel%

set path=C:\Python27\Scripts;C:\Program Files (x86)\CMake\bin;c:\mingw-w64-i686-sjlj-posix-4.9.2\bin&&conan test_package -s os="Windows" -s arch="x86" -s build_type="Debug" -s compiler=gcc -s compiler.libcxx=libstdc++ -s compiler.version="4.9" -o zlib:shared="True"
if %errorlevel% neq 0 exit /b %errorlevel%

set path=C:\Python27\Scripts;C:\Program Files (x86)\CMake\bin;c:\mingw-w64-i686-sjlj-posix-4.9.2\bin&&conan test_package -s os="Windows" -s arch="x86" -s build_type="Release" -s compiler=gcc -s compiler.libcxx=libstdc++ -s compiler.version="4.9" -o zlib:shared="False"
if %errorlevel% neq 0 exit /b %errorlevel%

set path=C:\Python27\Scripts;C:\Program Files (x86)\CMake\bin;c:\mingw-w64-i686-sjlj-posix-4.9.2\bin&&conan test_package -s os="Windows" -s arch="x86" -s build_type="Debug" -s compiler=gcc -s compiler.libcxx=libstdc++ -s compiler.version="4.9" -o zlib:shared="False"
if %errorlevel% neq 0 exit /b %errorlevel%

set path=C:\Python27\Scripts;C:\Program Files (x86)\CMake\bin;c:\mingw-w64-x86_64-seh-posix-4.9.2\bin&&conan test_package -s os="Windows" -s arch="x86_64" -s build_type="Release" -s compiler=gcc -s compiler.libcxx=libstdc++ -s compiler.version="4.9" -o zlib:shared="True"
if %errorlevel% neq 0 exit /b %errorlevel%

set path=C:\Python27\Scripts;C:\Program Files (x86)\CMake\bin;c:\mingw-w64-x86_64-seh-posix-4.9.2\bin&&conan test_package -s os="Windows" -s arch="x86_64" -s build_type="Debug" -s compiler=gcc -s compiler.libcxx=libstdc++ -s compiler.version="4.9" -o zlib:shared="True"
if %errorlevel% neq 0 exit /b %errorlevel%

set path=C:\Python27\Scripts;C:\Program Files (x86)\CMake\bin;c:\mingw-w64-x86_64-seh-posix-4.9.2\bin&&conan test_package -s os="Windows" -s arch="x86_64" -s build_type="Release" -s compiler=gcc -s compiler.libcxx=libstdc++ -s compiler.version="4.9" -o zlib:shared="False"
if %errorlevel% neq 0 exit /b %errorlevel%

set path=C:\Python27\Scripts;C:\Program Files (x86)\CMake\bin;c:\mingw-w64-x86_64-seh-posix-4.9.2\bin&&conan test_package -s os="Windows" -s arch="x86_64" -s build_type="Debug" -s compiler=gcc -s compiler.libcxx=libstdc++ -s compiler.version="4.9" -o zlib:shared="False"
if %errorlevel% neq 0 exit /b %errorlevel%

goto :eof

:conan_package_tools
python build.py
