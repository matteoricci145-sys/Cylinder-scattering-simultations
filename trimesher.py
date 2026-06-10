import trimesh

cylinder_radius_lamda_list = [10, 12.8, 15.9, 19, 22.3, 25.6]
nu = 6

for cylinder_radius_lamda in cylinder_radius_lamda_list:
    mesh = trimesh.load(f"./cylinder_{cylinder_radius_lamda}_stl_files/cylinders_{nu}.stl")

    if 'stl' in mesh.metadata:
        del mesh.metadata['stl']

    mesh.export(f"./cylinder_{cylinder_radius_lamda}_lamda/cylinder_{nu}.ply")
