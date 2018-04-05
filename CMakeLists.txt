cmake_minimum_required(VERSION 3.1.2)
project(conanzlib C)

include(conanbuildinfo.cmake)
conan_basic_setup(TARGETS)

# BUILD_SHARED_LIBS is a standard CMake variable, but we declare it here to
# make it prominent in the GUI.
option(BUILD_SHARED_LIBS "Build shared libraries(DLLs)." OFF)

# set debug postfix a la gtest
### set(CMAKE_DEBUG_POSTFIX "d")

include_directories(${CMAKE_SOURCE_DIR}/zlib-1.2.11)
add_subdirectory("./zlib-1.2.11")
