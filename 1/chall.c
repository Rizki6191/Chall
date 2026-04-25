#include <stdio.h>
#include <unistd.h>

void helper() {
  char buf[0x10];

  printf("Plase give me some advice!\n");
  printf("> ");

  read(0, buf, sizeof(buf) - 1);

  printf("So you tell me to ");
  printf(buf);
}


int main() {
  char buf[0x50];

  helper();

  printf("Please input for the last time!\n");
  printf("> ");

  scanf("%[^\n]", buf);
}

__attribute__((constructor)) void setup(){
  setvbuf(stdin, NULL, 2, 0);
  setvbuf(stdout, NULL, 2, 0);
  setvbuf(stderr, NULL, 2, 0);
}
