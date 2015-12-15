PROJECT(MyHello)
cmake_minimum_required(VERSION 2.8)

include(conanbuildinfo.cmake)
CONAN_BASIC_SETUP()

find_package("ZLIB")

IF(ZLIB_FOUND)
    ADD_EXECUTABLE(enough enough.c)
    include_directories(${ZLIB_INCLUDE_DIRS})
    TARGET_LINK_LIBRARIES(enough ${ZLIB_LIBRARIES})
ELSE()
    MESSAGE(FATAL_ERROR "Zlib not found")
ENDIF()
