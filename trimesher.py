import trimesh

cylinder_radius_lamda = 25.6
nu = 8

mesh = trimesh.load(f"./cylinder_{cylinder_radius_lamda}_stl_files/cylinders_{nu}.stl")

if 'stl' in mesh.metadata:
    del mesh.metadata['stl']

mesh.export(f"cylinder_{nu}.ply")
