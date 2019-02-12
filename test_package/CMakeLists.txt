cmake_minimum_required(VERSION 3.8)
project(test_package C)

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()

find_package(ZLIB REQUIRED)

add_executable(test test.c)
target_link_libraries(test ZLIB::zlib)

if(WITH_MINIZIP)
  add_executable(test_minizip test_minizip.c)
  target_link_libraries(test_minizip ZLIB::zlib)
endif()
