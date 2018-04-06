cmake_minimum_required(VERSION 3.1.2)
project(TestPackage C)

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup(TARGETS)

add_executable(enough enough.c)
conan_target_link_libraries(enough)
