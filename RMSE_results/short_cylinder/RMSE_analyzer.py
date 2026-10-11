import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# Cylinders dimension
D = [10, 12.8, 15.9, 19, 22.3, 25.6]
#NU = [6, 8, 12, 17]
NU = [12]
    
for nu in NU:
    data_frames = []
    for d in D:
        # Reading data
        df = pd.read_csv(f"./RESULTS_{nu}_{d}.csv")
        
        # Adding a coloum with D value in the starting csv
        df["cylinder_dimension"] = d 
    
        data_frames.append(df)


    df_all = pd.concat(data_frames, ignore_index=True)

    df_all['distance_in_lamda'] = df_all['distance_in_lamda'].round(2)

    # Extract data frame for near and far field
    df_reactive = df_all[df_all["distance_in_lamda"]<=1]
    
    df_radiant = df_all[df_all["distance_in_lamda"]>=1]
    df_radiant = df_radiant[df_radiant["distance_in_lamda"]<= 100]
    df_radiant = df_radiant[df_radiant.index % 2 == 0]
    
    df_pivot_RMSE = df_reactive.pivot(index="distance_in_lamda", columns="cylinder_dimension", values="RMSE")

    df_pivot_RMSE = df_pivot_RMSE.replace(np.inf, np.nan)

    
    plt.figure()
    sns.heatmap(df_pivot_RMSE, annot=True, cmap="YlGnBu",
            cbar_kws={"label": "RMSE [dB]"})
    plt.title(f"RMSE with {nu}-EDGES cylinder")
    plt.xlabel("Cylinder dimension [lambda]")
    plt.ylabel("Distance from cylinder [lambda]")
    plt.savefig(f"RMSE_reactive_{nu}")
    plt.close()

    df_pivot_RMSE = df_radiant.pivot(index="distance_in_lamda", columns="cylinder_dimension", values="RMSE")
    df_pivot_RMSE = df_pivot_RMSE.replace(np.inf, np.nan)
    
    plt.figure()
    sns.heatmap(df_pivot_RMSE, annot=True, cmap="YlGnBu",
                cbar_kws={"label": "RMSE [dB]"})
    plt.title(f"Cylinder discretized {nu}")
    plt.xlabel(f"Radius of cylinder [$\lambda$]")
    plt.ylabel(f"Distance from cylinder [$\lambda$]")
    plt.savefig(f"RMSE_radiant_{nu}", dpi=400, bbox_inches='tight')
    plt.show()
    plt.close()
        


