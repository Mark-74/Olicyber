import angr
proj = angr.Project(
    "./md6", 
    load_options={"auto_load_libs":False},
    main_opts={"base_addr":0})

init_state = proj.factory.entry_state()
simulation = proj.factory.simulation_manager(init_state)

sol = simulation.explore(find=0x12F2, avoid=0x1303)
print(sol.found[0].posix.dumps(0).decode() + '}')