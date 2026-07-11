import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("RESULTS_12_12.8.csv")
df2 = pd.read_csv("LEN_cylinder_RESULTS_12_12.8.csv")

df["RMSE_basic"] = df2["RMSE"]

df.index=df["distance_in_lamda"]
df = df.drop("distance_in_lamda", axis=1)
print(df)

plt.figure()
plt.plot(df)
plt.legend(["Short cylinder", "Long cylinder"])
plt.xlabel("Distance from cylinder [lambda]")
plt.ylabel("RMSE [dB]")
plt.title("Comparison between differnt cylinders lengths")
plt.show()
