cmake_minimum_required(VERSION 3.13)
project(GbaLib C)

set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

add_library(${PROJECT_NAME} STATIC 
    src/driver/graphical.c
    src/autogenerate/font.c
)

target_compile_options(${PROJECT_NAME} PRIVATE -mcpu=arm7tdmi -mlittle-endian -nostdlib)
target_include_directories(${PROJECT_NAME} PUBLIC 
    "${CMAKE_CURRENT_SOURCE_DIR}/include"
)