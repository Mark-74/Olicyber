FROM ubuntu@sha256:8feb4d8ca5354def3d8fce243717141ce31e2c428701f6682bd2fafe15388214

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    libseccomp-dev \
    libseccomp2 \
    socat \
    && rm -rf /var/lib/apt/lists/*

RUN useradd -m -u 1000 pwn
WORKDIR /home/pwn

COPY safenote ./
COPY flag.txt ./

RUN chown root:root safenote flag.txt && \
    chmod 755 safenote && \
    chmod 444 flag.txt

USER pwn

EXPOSE 9088

ENTRYPOINT ["socat"]
CMD ["TCP-LISTEN:9088,reuseaddr,fork", "EXEC:./safenote,stderr,pty,raw,echo=0"]
