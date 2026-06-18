cmake_minimum_required(VERSION 3.13)
project(MiniGBA C ASM)

set(CMAKE_C_COMPILER "arm-none-eabi-gcc")
set(CMAKE_ASM_COMPILER "arm-none-eabi-gcc")
set(CMAKE_OBJCOPY "arm-none-eabi-objcopy")
set(RUNTIME_OUTPUT_DIRECTORY "${CMAKE_CURRENT_SOURCE_DIR}/../../bin")

set(SOURCES
    main.c
    driver/graphical.c
    bootstrap.S
)

add_executable(${PROJECT_NAME} ${SOURCES})
set_target_properties(${PROJECT_NAME} PROPERTIES SUFFIX ".elf")

target_compile_options(${PROJECT_NAME} PRIVATE
    -mcpu=arm7tdmi
    -mlittle-endian
    -nostdlib
)

target_link_options(${PROJECT_NAME} PRIVATE
    -T "${CMAKE_CURRENT_SOURCE_DIR}/../linker/gba.ld"
    -nostdlib
)

add_custom_command(TARGET ${PROJECT_NAME} POST_BUILD
    COMMAND ${CMAKE_OBJCOPY} -O binary "${CMAKE_CURRENT_SOURCE_DIR}/${PROJECT_NAME}.elf" "${RUNTIME_OUTPUT_DIRECTORY}/${PROJECT_NAME}.bin"
    COMMENT "Extracting raw binary to bin/${PROJECT_NAME}.bin"
)