cmake_minimum_required(VERSION 3.14)

set(CMAKE_CXX_STANDARD 17)

set(PACKAGE_NAME "rle")

# set(CMAKE_CXX_FLAGS "-pthread")

project(${PACKAGE_NAME})

file(GLOB LIB_FILES
	"src/compression/*.h"
	"src/compression/*.cpp"
	"src/utils/*.h"
	"src/utils/*.cpp"
	"src/*.h"
	"src/*.cpp"
)

set(LIB_SRC ${LIB_FILES})

add_executable(${PACKAGE_NAME} ${LIB_SRC} "main.cpp")
