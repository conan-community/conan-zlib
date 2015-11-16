PROJECT(MyHello)
cmake_minimum_required(VERSION 2.8)

include(conanbuildinfo.cmake)
CONAN_BASIC_SETUP()

ADD_EXECUTABLE(enough enough.c)
TARGET_LINK_LIBRARIES(enough ${CONAN_LIBS})
