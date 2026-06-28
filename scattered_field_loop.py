#===================================  IMP LIBRARIES =====================================#

import os
#os.environ['DRJIT_LIBLLVM_PATH'] = "/home/aizi0357/environments/sionna_v0/lib/libLLVM-20.so"
#os.environ["LD_LIBRARY_PATH"] = "$LD_LIBRARY_PATH:/home/aizi0357/environments/sionna_v0/lib/"

gpu_num = "" # Use "" to use the CPU
os.environ["CUDA_VISIBLE_DEVICES"] = f"{gpu_num}"
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

import sionna

resolution = [480,320] # increase for higher quality of renderings

# Allows to exit cell execution in Jupyter
class ExitCell(Exception):
    def _render_traceback_(self):
        pass

import tensorflow as tf
gpus = tf.config.list_physical_devices('GPU')
print("gpus:", gpus)
print(f"Using GPU {gpu_num}")
if gpu_num and gpus:
    try:
        tf.config.experimental.set_memory_growth(gpus[0], True)
    except RuntimeError as e:
        print(e)

tf.get_logger().setLevel('ERROR')

tf.random.set_seed(1) # Set global random seed for reproducibility

#%matplotlib inline
import matplotlib.pyplot as plt
import numpy as np
import time

# Import Sionna RT components
from sionna.rt import load_scene, Transmitter, Receiver, PlanarArray, Camera

#===================================  SETTING THE SCENE =====================================#

dtype = tf.complex128
rdtype = tf.float64


fc = 2e9  # Se cambio la frequenza il cylinder radio diventa 12.8 / 2 per lamda giusto ??????
lamda = 3e8 / fc

print("\n==== SIMULATION PARAMETERS ===")
print(f"fc: {fc}")
print(f"lamda: {lamda}")

cylinder_radius_lamda = 12.8
nu = 8

cylinder_radius = cylinder_radius_lamda * lamda
print(f"cylinder_radius: {cylinder_radius}")

scene = load_scene(f"./cylinder_{cylinder_radius_lamda}_lamda/cylinder_{nu}/cylinder_{nu}.xml", dtype)

scene.frequency = fc
scene.synthetic_array = True


#================================ SETTING RX and TX =========================================#

pol = 'HH'   

scene.tx_array = PlanarArray(num_rows=1,
                             num_cols=1,
                             vertical_spacing=0.5,
                             horizontal_spacing=0.5,
                             pattern="iso",
                             polarization=pol[0],
                             dtype=dtype)

scene.rx_array = PlanarArray(num_rows=1,
                             num_cols=1,
                             vertical_spacing=0.5,
                             horizontal_spacing=0.5,
                             pattern="iso",
                             polarization=pol[1],
                             dtype=dtype)


# =============================== PLACING TX ================================================== #

# Calcola a desnità di onda incidente e il modulo del campo incidente.
# Metti il TX che rispetti fronhoufer ma la potenza va normalizzta con la potenza incidente. 
# Questo per vedere come varia il campo scatterato al varire della distanza di osservazione.
# Cambia la potenza del trasmettitore in modo che il campo indidente sia sempre 1 V/m.

# Per la simulzione CST allunga il cilindro 

# Valuta il campo a distanza maggiori di 20 lamda per vedere se alte dicretizzazioni sono quele ottime 

D = cylinder_radius
tx_dist = 2*(D**2)/lamda + D # TX must be in Frahofer zone

source_point = np.array([tx_dist, 0.0, 0.0])

scene.remove("tx")

tx = Transmitter(name="tx", position=source_point, dtype=dtype)
scene.add(tx)

coef = (4 * np.pi * tx_dist)




#================================ IMP DOUBLE EDGE DIFRACTION =========================================#

from sionna.rt.objects_geometry import ObjectsGeometry

obj_names = list(scene.objects.keys())

obj_geom = ObjectsGeometry(scene._solver_paths)
obj_geom.is_table_gfi = True
obj_geom.is_vertex_diffraction = True
obj_geom.is_double_diffraction = True
obj_geom.init_objects(obj_names, [None])

scene._solver_paths.vertex_diffraction.set_objects_geometry(obj_geom)
scene._solver_paths.double_diffraction.set_objects_geometry(obj_geom)

# tf.math.reduce_mean(scene._solver_paths._wedges_length) / lamda

#=============================== DISCRETIZATION and PARAMETERS ==============================================#

E_wav = np.sqrt(2 * (1 - np.cos(2*np.pi/nu))) * (cylinder_radius / lamda)  # edge size in wavelengths
S_wav = cylinder_radius * (1 - np.cos(np.pi / nu)) / lamda  # in wavelengths
E2divR_wav = E_wav**2 * lamda / cylinder_radius

print("\n=== DISCRETIZATION PARAMETERS ===")
print(f"E = {E_wav} * lambda")
print(f"S = {S_wav} * lambda")
print(f"E^2/R = {E2divR_wav} * lambda")

RMSE_result = []

#=========================================== SIMULATION =====================================================#

#circle_radius = np.concatenate([cylinder_radius + lamda*np.arange(0.1, 1, 0.1), 
#                                cylinder_radius + lamda*np.arange(1, 20, 2)]) #np.array([0.1, 0.3, 0.5, 0.7, 0.9, 1.1, 1.3])

circle_radius = cylinder_radius + np.array([0.5, 10, 50])*lamda

i_loop = 1

for circle_radius_i in circle_radius:

    """ THIS IS USELESS !!!
    # ====== PLACING RX TO HAVE THE SAME RECIEVED POWER ===== #

    link_distance = tx_dist - cylinder_radius

    # Link budget formula 
    pt = link_distance**2/30

     
    scene.remove("tx")

    tx = Transmitter(name="tx", position=source_point, dtype=dtype, power_dbm=10*np.log10(pt*1e3))
    scene.add(tx)

    print(f"Trasmitter distance: {link_distance}")
    print(f"Power in mW: {pt*1e3}")
    """
    
    r = circle_radius_i-cylinder_radius
 
    # ============================== PLACING RX ==================================================== #
    num_points = 720

    theta_arr = np.linspace(0.0, 2*np.pi, num_points, endpoint=False)

    def get_circle_points(theta_arr, p1, p2):
        res = np.zeros((len(theta_arr), 3))
        res[:, 0] = p1[0] * np.cos(theta_arr) + p2[0] * np.sin(theta_arr)
        res[:, 1] = p1[1] * np.cos(theta_arr) + p2[1] * np.sin(theta_arr)
        res[:, 2] = p1[2] * np.cos(theta_arr) + p2[2] * np.sin(theta_arr)

        return res

    circle_p1 = np.array([1, 0, 0]) * circle_radius_i
    circle_p2 = np.array([0, 1, 0])  * circle_radius_i
    receive_points = get_circle_points(theta_arr, circle_p1, circle_p2)


    for i in range(len(receive_points)):
        scene.remove(f"rx_{i}")
        rx = Receiver(name=f"rx_{i}", position=receive_points[i], dtype=dtype)
        scene.add(rx)

    #========================================= SCATTERED FILED =================================================#


    def get_field_los_full(tx_pos, rx_poses):
        # This fuction returns the field wich there would be without any obstacle

        dist = np.linalg.norm(tx_pos - rx_poses, axis=1)
        field = 1.0 / dist / (4 * 3.141592653589793) * lamda 
        return field

    field_los_full = get_field_los_full(source_point, receive_points)

    
    #== Calculating the SHADOW REGION
    paths = scene.compute_paths(max_depth=1,
                                method="exhaustive",
                                num_samples=1e6,
                                los = True,
                                reflection = False,
                                diffraction = False,
                                vertex_diffraction = False)

    a, tau = paths.cir()
    path_amplitudes = a[0,:,0,0,0,:,0]
    receiver_amplitudes_los = np.abs(np.sum(path_amplitudes, axis=1)) #/ lamda

    los_line_idx = np.where(receiver_amplitudes_los <= 1e-6)[0][0], np.where(receiver_amplitudes_los <= 1e-6)[0][-1] #first and last index of the shadow region
    field_los_full = np.where(receiver_amplitudes_los <= 0.0, field_los_full, receiver_amplitudes_los) + 1e-6
    if pol == 'VV':
        field_los_full = -field_los_full
        
    from scipy.constants import c as speed_of_light
    dist = np.linalg.norm(source_point - receive_points, axis=1)
    field_los_full2 = field_los_full * np.exp(-1j * 2 * np.pi * fc * dist/speed_of_light)


    
    #== Calculating the ANALYTIC SCATTERED FILED (Plane wave incidence)
    
    from sionna.rt.analytical_equations import cylinder_te_inc_scat_total, cylinder_tm_inc_scat_total
    	
    if pol == 'HH':
    	u_inc, an_scattering, an_total = cylinder_te_inc_scat_total(theta_arr, cylinder_radius, circle_radius_i, 2*np.pi / lamda, terms=512)
    elif pol == 'VV':
    	u_inc, an_scattering, an_total = cylinder_tm_inc_scat_total(theta_arr, cylinder_radius, circle_radius_i, 2*np.pi / lamda, terms=512)


    # ======================================== SCATTERED FIELD =============================================#

    paths = scene.compute_paths(max_depth=1,
                                method="exhaustive",
                                num_samples=1e6,
                                los = True,
                                reflection = True,
                                diffraction = True,
                                vertex_diffraction = False,
                                double_diffraction = True,)
    
    paths.normalize_delays = False
    
    a, tau = paths.cir()
    #a.shape   # [batch_size, num_rx, num_rx_ant, num_tx, num_tx_ant, max_num_paths, num_time_steps]
    
    nans_bool = tf.math.is_nan(tf.math.real(a)) 
    a = tf.where(nans_bool, tf.zeros_like(a), a)
    
    path_amplitudes = a[0,:,0,0,0,:,0]
    tmp1 = np.sum(path_amplitudes, axis=1) + field_los_full2
    receiver_amplitudes = np.abs(tmp1) / lamda

    plt.subplot(3,1,i_loop)
    i_loop = i_loop + 1
    #plt.plot(20*np.log10(coef*receiver_amplitudes_[:num_points//2 + 10]), label='RT', linestyle='--')
    plt.plot(57.3*theta_arr, 20*np.log10(np.abs(an_scattering)), label='Equation')
    plt.plot(57.3*theta_arr, 20*np.log10(coef*receiver_amplitudes), label='RT+EE')
    plt.axvline(x=57.3*theta_arr[los_line_idx[0]], color='r', linestyle='--', label='LOS/NLOS')
    plt.axvline(x=57.3*theta_arr[los_line_idx[1]], color='r', linestyle='--')
    plt.title(f'Scattered field, rx_dist = {r/lamda} $\lambda$')
    plt.xlabel("Degree [°]")
    plt.ylabel("|E_scattered|")
    plt.grid()
    plt.legend()
    
plt.tight_layout() # Fondamentale per evitare che i titoli si sovrappongan
plt.savefig(f"./plots/scattered_field_{nu}_rx_{r/lamda}.png")

"""
# Save result in csv file
import pandas as pd
df = pd.DataFrame([20*np.log10(np.abs(an_scattering)),20*np.log10(coef*receiver_amplitudes)],columns=theta_arr*57.3,index=["Equation","Ray-Tracing"])
df.to_csv("./near_field_validation/sionna_results2.csv",index=True)
print(df)
"""
    
#df.to_csv(f"./RMSE_results/risultati_full_{nu}_{cylinder_radius_lamda}.csv", index=False)
#print("Results of RMSE correctly exported")
