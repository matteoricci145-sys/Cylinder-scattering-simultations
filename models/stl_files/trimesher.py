# Conoverts .stl files in ply files importable in Sionna

import trimesh

mesh = trimesh.load(f"./cylinder_12.8_stl_files/cylinders_17.stl")    

if 'stl' in mesh.metadata:
    del mesh.metadata['stl']

mesh.export(f"./cylinder_17.ply")
