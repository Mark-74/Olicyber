#!/bin/bash

gcc chall.c -o fsop -fPIE -pie -Wl,-z,relro,-z,now

