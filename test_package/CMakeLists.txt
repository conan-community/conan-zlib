cmake_minimum_required(VERSION 3.1.2)
project(TestPackage C)

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
# conan is a buggy, prevent find_library() errors on MSYS! CK
# -- Conan: Compiler GCC>=5, checking major version 6.4
# -- Conan: Checking correct version: 6.4
# -- Conan: Using cmake targets configuration
# -- Library zlib not found in package, might be system one
if(${CMAKE_SYSTEM_NAME} MATCHES "Windows")
    conan_basic_setup()
else()
    conan_basic_setup(TARGETS)
endif()

add_executable(enough enough.c)
conan_target_link_libraries(enough)
