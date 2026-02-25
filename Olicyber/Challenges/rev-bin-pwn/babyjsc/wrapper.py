#!/usr/bin/env python3
from base64 import b64decode
import tempfile, subprocess
import os

os.environ["PYTHONUNBUFFERED"] = "1"

data = input("Send me your js exploit b64-encoded followed by a newline\n")
data = b64decode(data)

tempf = tempfile.NamedTemporaryFile()
tempf.write(data)
tempf.flush()

ENV = os.environ.copy()
ENV["LD_LIBRARY_PATH"] = "./libs"
res = subprocess.run(["./jsc", tempf.name], env=ENV, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
out = res.stdout.decode()
print(out)

tempf.close()
