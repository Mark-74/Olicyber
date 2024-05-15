import zipfile
import os

def bruteForce(zippedDir):
    wordList = open('rockyou.txt', 'rb')
    
    with zipfile.ZipFile(zippedDir,'r') as file: 
        
        for line in wordList:
            for word in line.split():            
                try:
                    file.extractall(pwd = word)
                    print("found {i} with password: " + word.decode())
                    return
                except:
                    continue
    
    wordList.close()

for i in range(100, 0, -1):
    print(i)
    zippedDir = (f"{i}.zip")
    
    bruteForce(zippedDir)
    
    if(i != 100):
        os.remove(f"{i}.zip")
    