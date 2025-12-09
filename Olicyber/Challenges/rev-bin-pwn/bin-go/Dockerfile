FROM ubuntu:18.04

RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y socat
RUN apt-get install -y libssl-dev python3

RUN useradd -ms /bin/sh pwn

WORKDIR /home/pwn

ENV FLAG=ptm{REDACTED}
COPY ./bingo ./

RUN chown -R root:pwn /home/pwn && chmod 750 /home/pwn && chmod 550 /home/pwn/bingo

EXPOSE 1907

CMD ["socat", "-T60", "TCP-LISTEN:1907,reuseaddr,fork,su=pwn", "EXEC:/home/pwn/bingo,pty,raw,echo=0"]
