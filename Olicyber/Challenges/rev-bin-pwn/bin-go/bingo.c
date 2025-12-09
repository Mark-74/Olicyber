#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
void *target;

void initialize(void)
{
    setbuf(stdin, NULL);
    setbuf(stdout, NULL);
    setbuf(stderr, NULL);
}

void setup_challenge(){
  void* chunks[20];
  size_t s = 0x18;
  for(int i=0; i<20; i++){
    chunks[i]=malloc(s);
    if(i%2==1){
      s+=0x10;
    }
  }
  malloc(0x20);
  malloc(0x20);
  target=calloc(0x20, 1);
  for(int i=0; i<20; i++){
    free(chunks[i]);
  }
}

void print_menu(){
  puts("1) Alloc a new chunk");
  puts("2) Free a chunk");
  puts("3) Exit and check");
  printf("> ");
}

int get_int(){
  int input=-1;
  int result=scanf("%d", &input);
  if(result==EOF){
    exit(-1);
  }
  if(result==0){
    exit(-1);
  }
  return input;
}

int is_allowed_size(int size){
  int allowed_sizes[]={0x18, 0x28, 0x38, 0x48, 0x58, 0x68, 0x78, 0x88, 0x98, 0xa8};
  for(int i=0; i<10; i++){
    if(size==allowed_sizes[i]){
      return 1;
    }
  }
  return 0;
}

void* alloc_new_chunk(){

  puts("Which size do you want your chunk to be?");
  printf("> ");
  int size=get_int();
  if(!is_allowed_size(size)){
    puts("Nope.");
    exit(-1);
  }
  void* chunk=malloc(size);
  puts("What do you want to write in your chunk?");
  printf("> ");
  read(STDIN_FILENO, chunk, size+8); //puoi overridare la size e le flag del chunk successivo
  return chunk;
}

void check(){
  if(*(int64_t*)target==0xdeadbeefdeadbeef){
    const char* flag = getenv("FLAG");
    puts("I see you are a master of the secret arts, here is a flag for you:");
    puts(flag);
    exit(0);
  }else{
    puts("You still have many more things to learn my friend....");
    exit(0);
  }
}

void challenge(){
  void* local_chunks[2];
  int allocated_chunks=0;
  puts("Welcome to bin-go, the bin-based heap challenge, without a single line of go!");
  while(1==1){
    print_menu();
    int selection=get_int();
    if(selection==1){
      if(allocated_chunks>=2){
        puts("That's enough chunks for now!");
      }else if(allocated_chunks<0){
        puts("How did you even get here?");
        exit(-1);
      }else{
        local_chunks[allocated_chunks]=alloc_new_chunk();
        allocated_chunks++;
      }
    }else if(selection==2){
      if(allocated_chunks>2){
        puts("How did you even get here?");
        exit(-1);
      }else if(allocated_chunks<=0){
        puts("You have no more chunks to free");
      }else{
        allocated_chunks--;
        free(local_chunks[allocated_chunks]);
        local_chunks[allocated_chunks]=0;

      }
    }else if (selection==3){
      check();
    }else{
      puts("Tell your jokes to someone else.");
    }
  }
}


int main(void) {
  initialize();
  setup_challenge();
  challenge();
}
