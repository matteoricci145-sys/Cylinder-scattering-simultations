import pandas as pd

data_frames = []


# Cylinders dimension
D = [10, 12.8, 15.9, 19, 22.3, 25.6]
nu = 8

for i in D:
    df = pd.read_csv(f"./{i}/risultati_{nu}_{i}.csv")
    df["cylinder_dimension"] = i # Adding a coloum with D value in the starting csv
    data_frames.append(df)

df_all = pd.concat(data_frames, ignore_index=True)

df_all['distance_in_lamda'] = df_all['distance_in_lamda'].round(2)
df_pivot = df_all.pivot(index="distance_in_lamda", columns="cylinder_dimension", values="RMSE")

print(df_pivot) 

import seaborn as sns
import matplotlib.pyplot as plt

sns.heatmap(df_pivot, annot=True, cmap="YlGnBu")
plt.show()

