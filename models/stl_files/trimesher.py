# Conoverts .stl files in ply files importable in Sionna

import trimesh

cylinder_radius_lamda_list = [12.8]
nu = 12

for cylinder_radius_lamda in cylinder_radius_lamda_list:
    #mesh = trimesh.load(f"./cylinder_{cylinder_radius_lamda}_stl_files/long long/cylinders_{nu}.stl")
    mesh = trimesh.load(f"./plane.stl")
    

    if 'stl' in mesh.metadata:
        del mesh.metadata['stl']

    mesh.export(f"./plane.ply")
