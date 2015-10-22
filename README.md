# conan-zlib

(https://conan.io)[Conan.io] package for ZLIB library

The packages generated with this **conanfile** can be found in (https://conan.io/source/zlib/1.2.8/lasote/stable)[conan.io].

## Build packages

    $ python build.py
    
## Upload packages to server

    $ conan upload zlib/1.2.8@lasote/stable --all
    
## Reuse the packages

### Basic setup

    $ conan install zlib/1.2.8@lasote/stable
    
### Project setup

If you handle multiple dependencies in your project is better to add a *conanfile.txt*
    
    [requires]
    zlib/1.2.8@lasote/stable

    [options]
    zlib:shared=true # false
    
    [generators]
    txt
    cmake

Complete the installation of requirements for your project running:</small></span>

    conan install . -s compiler=gcc -s compiler.version=4.9 ... 

Project setup installs the library (and all his dependencies) and generates the files *conanbuildinfo.txt* and *conanbuildinfo.cmake* with all the paths and variables that you need to link with your dependencies.

### Advanced setup

If you feel confortable with conan, you can create a *conanfile.py* and compile your project with conan's help!
This is exactly what **build.py** and **test/conanfile.py** does.

