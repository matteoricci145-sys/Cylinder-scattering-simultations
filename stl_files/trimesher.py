# Conoverts .stl files in ply files importable in Sionna

import trimesh

cylinder_radius_lamda_list = [25.6]
nu = 12

for cylinder_radius_lamda in cylinder_radius_lamda_list:
    mesh = trimesh.load(f"./cylinder_{cylinder_radius_lamda}_stl_files/long/cylinders_{nu}.stl")

    if 'stl' in mesh.metadata:
        del mesh.metadata['stl']

    mesh.export(f"./cylinder_{nu}.ply")
