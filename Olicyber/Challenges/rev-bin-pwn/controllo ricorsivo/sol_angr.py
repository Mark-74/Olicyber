import angr
from pwn import remote
proj = angr.Project(
    "./controllo_ricorsivo_circa", 
    load_options={"auto_load_libs":False},
    main_opts={"base_addr":0})

init_state = proj.factory.entry_state()
simulation = proj.factory.simulation_manager(init_state)

sol = simulation.explore(find=0x13B7, avoid=0x13C5)
res = sol.found[0].posix.dumps(0)

r = remote('crc.challs.olicyber.it', 12201)
print(res)

r.sendlineafter(b'password:', res)
r.interactive()