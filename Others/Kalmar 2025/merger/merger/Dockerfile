FROM ubuntu:24.04@sha256:80dd3c3b9c6cecb9f1667e9290b3bc61b78c2678c02cbdae5f0fea92cc6734ab

RUN apt update && apt install -y socat

RUN mkdir /app
RUN useradd ctf

COPY merger /app/merger
RUN echo "kalmar{redacted}" > /flag-$(cat /dev/urandom | tr -cd 'a-f0-9' | head -c 32).txt

USER ctf

EXPOSE 1337

CMD socat tcp-l:1337,reuseaddr,fork exec:/app/merger,pty,echo=0,raw,iexten=0
