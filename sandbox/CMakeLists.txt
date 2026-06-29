cmake_minimum_required(VERSION 3.13)

set(CMAKE_TRY_COMPILE_TARGET_TYPE "STATIC_LIBRARY")
set(CMAKE_C_COMPILER "arm-none-eabi-gcc")
set(CMAKE_ASM_COMPILER "arm-none-eabi-gcc")
set(CMAKE_OBJCOPY "arm-none-eabi-objcopy")
set(RUNTIME_OUTPUT_DIRECTORY "${CMAKE_CURRENT_SOURCE_DIR}/../bin")
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

project(ExampleGBA C ASM)
 
add_subdirectory(
    "${CMAKE_CURRENT_SOURCE_DIR}/../libs" 
    "${CMAKE_CURRENT_BINARY_DIR}/libs_build"
)

set(SOURCES
    src/bootstrap.S
    src/main.c
)

add_executable(${PROJECT_NAME} ${SOURCES})
set_target_properties(${PROJECT_NAME} PROPERTIES
    SUFFIX ".elf"
    RUNTIME_OUTPUT_DIRECTORY "${CMAKE_CURRENT_SOURCE_DIR}/../build"
)

target_compile_options(${PROJECT_NAME} PRIVATE
    -mcpu=arm7tdmi
    -mlittle-endian
)

target_link_libraries(${PROJECT_NAME} PRIVATE GbaLib)

target_include_directories(${PROJECT_NAME} PRIVATE
    "${CMAKE_CURRENT_SOURCE_DIR}/include"
    "${CMAKE_CURRENT_SOURCE_DIR}/../libs/include"
)

target_link_options(${PROJECT_NAME} PRIVATE
    -T "${CMAKE_CURRENT_SOURCE_DIR}/linker/gba.ld"
    -nostartfiles
    -specs=nano.specs
    -specs=nosys.specs
)

add_custom_command(TARGET ${PROJECT_NAME} POST_BUILD
    COMMAND ${CMAKE_OBJCOPY} -O binary "${CMAKE_CURRENT_SOURCE_DIR}/../build/${PROJECT_NAME}.elf" "${RUNTIME_OUTPUT_DIRECTORY}/${PROJECT_NAME}.bin"
    COMMENT "Extracting raw binary to bin/${PROJECT_NAME}.bin"
)