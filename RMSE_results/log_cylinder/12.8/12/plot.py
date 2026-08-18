import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("RESULTS_12_12.8.csv")
df2 = pd.read_csv("LONG_RESULTS_12_12.8.csv")
df3 = pd.read_csv("LONG_LONG_RESULTS_12_12.8.csv")

df["RMSE_LONG"] = df2["RMSE"]
df["RMSE_LONG_LONG"] = df3["RMSE"]

df.index=df["distance_in_lamda"]
df = df.drop("distance_in_lamda", axis=1)
print(df)

plt.figure()
plt.plot(df)
plt.legend(["Short cylinder", "Long cylinder", "Long long cylinder"])
plt.xlabel("Distance from cylinder [lambda]")
plt.ylabel("RMSE [dB]")
plt.title("Comparison between differnt cylinders lengths")
plt.show()

df = pd.read_csv("FAR_LONG_LONG_RESULTS_12_12.8.csv")
df.index=df["distance_in_lamda"]
df = df.drop("distance_in_lamda", axis=1)

plt.figure()
plt.plot(df)
plt.xlabel("Distance from cylinder [lambda]")
plt.ylabel("RMSE [dB]")
plt.title("Long long cylinder in far distances")
plt.show()
