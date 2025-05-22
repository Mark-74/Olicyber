FROM ubuntu:16.04

RUN dpkg --add-architecture i386 && \
    apt update && \
    apt install -y gcc-multilib libc6:i386 lib32stdc++6 lib32z1 gdb file net-tools

RUN apt-get install -y perl

RUN useradd -u 1089 -m memcpy_pwn

COPY memcpy.c /home/memcpy_pwn/memcpy.c
COPY super.pl /home/memcpy_pwn/super.pl

RUN chown root:memcpy_pwn /home/memcpy_pwn/memcpy.c /home/memcpy_pwn/super.pl
WORKDIR /home/memcpy_pwn
RUN gcc -o memcpy memcpy.c -m32 -lm
RUN chown root:memcpy_pwn /home/memcpy_pwn/memcpy
RUN chmod 550 /home/memcpy_pwn/memcpy
RUN chmod 550 /home/memcpy_pwn/super.pl


WORKDIR /home
CMD ["perl", "/home/memcpy_pwn/super.pl"]
