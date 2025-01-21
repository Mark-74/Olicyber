#!/usr/bin/python3
import time, random, string
regdate = 1694103917.3166134
random.seed(regdate)

print("".join(random.choices(string.ascii_letters + string.digits, k=16)))