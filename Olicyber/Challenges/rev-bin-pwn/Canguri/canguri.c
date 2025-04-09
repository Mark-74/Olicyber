/**
 * @author Fabio Zoratti <fabio.zoratti96@gmail.com>
 * @file canguri.c
 * Compile with  `gcc -o canguri -fno-pie -fno-stack-protector -znoexecstack -Wl,-z,relro canguri.c -lseccomp`
 */


#include <unistd.h>
#include <stdio.h>
#include <stddef.h>
#include <stdlib.h>
#include <seccomp.h>

#include <linux/seccomp.h>
#include <linux/filter.h>
#include <linux/audit.h>
#include <linux/unistd.h>
#include <sys/mman.h>
#include <sys/ptrace.h>
#include <sys/stat.h>
#include <fcntl.h>



#define BUFFERONE_SIZE 0x50


char bufferone[BUFFERONE_SIZE];

int main(int argc, char** argv, char** envp) {
  char name_buf[40];

  setvbuf(stdin, NULL, _IOLBF, 0);
  setvbuf(stdout, NULL, _IOLBF, 0);
  setvbuf(stderr, NULL, _IOLBF, 0);
  mprotect((void*) ((unsigned long long) bufferone & ~0xfff), BUFFERONE_SIZE, PROT_READ | PROT_WRITE | PROT_EXEC);

  scmp_filter_ctx ctx = seccomp_init(SCMP_ACT_KILL);
  seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(open), 0);
  seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(openat), 0);
  seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(fstat), 0);
  seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(write), 0);
  seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(read), 0);
  seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(close), 0);
  seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(lseek), 0);
  seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(exit_group), 0);
  seccomp_load(ctx);

  puts("Questo programma è assolutamente sicurissimo, con queste protezioni"
       " non riuscirai mai ad avere una shell!");
  puts("E non riuscirai nemmeno a leggere la flag che sta in /home/problemuser/flag.txt");



  puts("Come ti chiami, folle che osi sfidare la potenza dei binari?");
  scanf("%s", name_buf);
  printf("Forza, %s, dimmi come avresti intenzione di rompermi, ora che ci sono queste protezioni.\n", name_buf);
  read(STDIN_FILENO, bufferone, BUFFERONE_SIZE);
  puts("Davvero pensi di riuscirci in questo modo? Buona Fortuna. Hai detto una "
       "boiata così grossa che adesso me la scrivo per ridere più tardi.");

  int fd = open("/tmp/motivazione.txt", O_CREAT | O_WRONLY);
  write(fd, bufferone, BUFFERONE_SIZE);
  puts("Fatto, ora potrò ridere di te anche più tardi.");
  close(fd);

  return 0;
}
