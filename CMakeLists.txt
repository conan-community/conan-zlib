cmake_minimum_required(VERSION 3.1.2)
project(conanzlib C)

include(conanbuildinfo.cmake)
conan_basic_setup(TARGETS)

# BUILD_SHARED_LIBS is a standard CMake variable, but we declare it here to
# make it prominent in the GUI.
# NOTE: unfortunately this is not respected by the zlib CMakeLists.txt file yet! CK
option(BUILD_SHARED_LIBS "Build shared libraries(DLLs)." OFF)

# disable unwanted debug postfix 'd'
set(CMAKE_DEBUG_POSTFIX "" CACHE STRING "Not useful with conan, should be empty!" FORCE)

# The zlib CMakeFile.txt is a nightmare! CK
set(CMAKE_LEGACY_CYGWIN_WIN32 0) # Remove when CMake >= 2.8.4 is required

include_directories(${CMAKE_SOURCE_DIR}/zlib-1.2.11)
add_subdirectory("./zlib-1.2.11")
