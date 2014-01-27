#include <unistd.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>

#define STACK 64
#define HEAP 64
#define FLAG "./flag"

/* gcc -masm=intel -z norelro -fno-stack-protector -o chall_heap chall_heap.c */

const char *malloc_error = "Memory allocation failed!\n";
const char *file_error = "Opening flag failed!\n";
const char *pwn = "Good Enough? Pwn Me!\n";

void main(int argc, char **argv) {
    char *flag;
    int fd;
    char user[STACK];
    flag = malloc(HEAP);

    if (flag == NULL) {
	write(1, malloc_error, strlen(malloc_error));
	exit(1);
    }

    fd = open(FLAG ,O_RDONLY);
    if (fd < 0){
        write(1, file_error, strlen(file_error));
	exit(1);
    }

    if(setresuid(getuid(), getuid(), getuid()) < 0){
	exit(1);	
    } 

    read(fd, flag, HEAP-1);
    close(fd);

    write(1, pwn, strlen(pwn));
    
    read(0, user, 0x800);

   asm (".intel_syntax noprefix;"
   "xor eax, eax;"
   "xor ebx, ebx;"
   "xor ecx, ecx;"
   "xor esi, esi;"
   "xor edi, edi;"
       ); 

}
