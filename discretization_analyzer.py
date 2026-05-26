import numpy as np

# Number of EDGE
nu = 8  

fc = 2e9  # Se cambio la frequenza il cylinder radio diventa 12.8 / 2 per lamda giusto ??????
lamda = 3e8 / fc

cylinder_radius_lamda = 12.8*2
cylinder_radius = cylinder_radius_lamda * lamda

#=============================== DISCRETIZATION and PARAMETERS ==============================================#

E_wav = np.sqrt(2 * (1 - np.cos(2*np.pi/nu))) * (cylinder_radius / lamda)  # edge size in wavelengths
S_wav = cylinder_radius * (1 - np.cos(np.pi / nu)) / lamda  # in wavelengths
E2divR_wav = E_wav**2 * lamda / cylinder_radius

print("\n=== DISCRETIZATION PARAMETERS ===")
print(f"Number of edge = {nu}")
print(f"Cylinder radius = {cylinder_radius_lamda*lamda}")
print(f"E = {E_wav} * lambda")
print(f"S = {S_wav} * lambda")
print(f"E^2/R = {E2divR_wav} * lambda")
