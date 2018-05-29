[![Build Status](https://travis-ci.org/lasote/conan-zlib.svg)](https://travis-ci.org/lasote/conan-zlib)
[![Build Status](https://ci.appveyor.com/api/projects/status/github/lasote/conan-zlib)](https://ci.appveyor.com/project/lasote/conan-zlib)


# conan-zlib


[Conan](https://bintray.com/conan-community/conan/zlib%3Aconan) package for ZLIB library. Thanks to Tim Lebedkov for the MinGW integration help! :)


## Basic setup

    $ conan install zlib/1.2.11@conan/stable
    
## Project setup

If you handle multiple dependencies in your project is better to add a *conanfile.txt*
    
    [requires]
    zlib/1.2.11@conan/stable

    [options]
    zlib:shared=True # False
    
    [generators]
    cmake

Complete the installation of requirements for your project running:</small></span>

    conan install . 

Project setup installs the library (and all his dependencies) and generates the files *conanbuildinfo.cmake* with all the 
paths and variables that you need to link with your dependencies.
