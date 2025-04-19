import subprocess

def dnsTXTquery(domain):
    result = subprocess.run(['dig', '-t', 'TXT', '-p10500', '@pisani.challs.olicyber.it', domain], capture_output=True, text=True).stdout
    
    if "flag{" in result:
        print(result)
        raise Exception("Flag found")
    
def dnsquery(domain):
    result = subprocess.run(['dig', '-p10500', '@pisani.challs.olicyber.it', domain], capture_output=True, text=True).stdout
    
    if "flag{" in result:
        print(result)
        raise Exception("Flag found")
    
    if result.find("CNAME") == -1:
        print(f"[-] No CNAME found for {domain}")
        return None
    
    result = result[result.index("CNAME")+6:]
    result = result[:result.index("localhost.")+10]
    return result

if __name__ == "__main__":
    visited = []
    queue = []
    
    queue.append("00000000-0000-4000-0000-000000000000.maze.localhost.")
    
    while len(queue) > 0:
        current = queue.pop(0)
        visited.append(current)
        
        for i in ["left", "right", "up", "down"]:
            response = dnsquery(f"{i}.{current}")
            if response is not None and response not in visited and response not in queue:
                queue.append(response)
                print(f"[+] Found new domain: {i}.{current} -> {response}")
                dnsTXTquery(response)
                