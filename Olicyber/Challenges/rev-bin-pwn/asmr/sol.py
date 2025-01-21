import angr
proj = angr.Project(
    "./asmr", 
    load_options={"auto_load_libs":False},
    main_opts={"base_addr":0x8049000})

init_state = proj.factory.entry_state()
simulation = proj.factory.simulation_manager(init_state)

sol = simulation.explore(find=0x08049429, avoid=0x08049478)
print('f' + sol.found[0].posix.dumps(0).decode())