#include <stdlib.h>
#include <stdio.h>

char* generate() {
    char* str = malloc(0x21);
    srandom(0x539);
	int i;
    for (i = 0; i < 0x20; i++) {
            int tmp = rand() % 0x5e;
            str[i] = tmp + 0x21;
    }
    str[0x20] = 0;
    return str;
}

int main() {
	printf("%s", generate());
	return 0;
}