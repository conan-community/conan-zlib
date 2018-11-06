cmake_minimum_required(VERSION 2.8)
PROJECT(test_package C)

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
CONAN_BASIC_SETUP()

add_executable(test test.c)
target_link_libraries(test ${CONAN_LIBS})
