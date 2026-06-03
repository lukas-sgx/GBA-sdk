CC = arm-none-eabi-gcc
FLAGS = -mcpu=arm7tdmi -mlittle-endian -nostdlib
LINKER = -T gba.ld
SRC = bootstrap.S
NAME = test.gba


all: $(NAME)

$(NAME): $(SRC)
	$(CC) $(FLAGS) -o test.elf $(SRC)
	mkdir -p bin
	arm-none-eabi-objcopy -O binary test.elf bin/test.bin
	python ../cartridge.py hdr gen -o bin/test.gba -b bin/test.bin