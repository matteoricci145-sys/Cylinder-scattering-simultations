# Conoverts .stl files in ply files importable in Sionna

import trimesh

cylinder_radius_lamda_list = [10]
nu = 17

for cylinder_radius_lamda in cylinder_radius_lamda_list:
    mesh = trimesh.load(f"./cylinder_{cylinder_radius_lamda}_stl_files/cylinders_{nu}.stl")

    if 'stl' in mesh.metadata:
        del mesh.metadata['stl']

    mesh.export(f"./cylinder_{nu}.ply")
