#!/usr/bin/env python3.8

from waitress import serve
from flask import Flask, request, make_response

import os
import hmac
import time
import hashlib
from datetime import datetime
import random
import string

flag = os.getenv("FLAG")

app = Flask(__name__)

def get_random_string(length):
  letters = string.ascii_lowercase
  result_str = ''.join(random.choice(letters) for i in range(length))
  return result_str

uptime = time.time()
seed = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
print(f"Seed: {seed}")
random.seed(seed)
SUPER_SECRET_KEY = get_random_string(32)
print(f"SUPER_SECRET_KEY: {SUPER_SECRET_KEY}")

def sign(text, key):
  textAsBytes = bytes(text, encoding='ascii')
  keyAsBytes  = bytes(key, encoding='ascii')
  signature = hmac.new(keyAsBytes, textAsBytes, hashlib.sha256)
  return signature.hexdigest()

def verify(text, signature, key):
  expected_signature = sign(text, key)
  return hmac.compare_digest(expected_signature, signature)

@app.route('/admin')
def admin():
  cookie = request.cookies.get('user')
  signature = request.cookies.get('signature')

  is_cookie_valid = verify(cookie, signature, SUPER_SECRET_KEY)

  if is_cookie_valid == False:
    return "HACKER DETECTED, ABORTING"

  if cookie == "admin":
    return f'Flag: {flag}'
  
  return "Hey, come va? Non c'è niente qui"

@app.route('/')
def index():
  default_user_name = "not_admin"

  resp = make_response(f"Ciao {default_user_name}!")

  resp.headers['X-Uptime'] = str(int(time.time()-uptime))

  resp.set_cookie("user", value=default_user_name)
  resp.set_cookie("signature", value=sign(default_user_name, SUPER_SECRET_KEY))

  return resp
