import pandas as pd
import matplotlib.pyplot as plt

df0 = pd.read_csv("./12/LONG_LONG_RESULTS_12_12.8.csv")
df1 = pd.read_csv("./8/LONG_LONG_RESULTS_8_12.8.csv")

df = pd.DataFrame()
df["12"] = df0["RMSE"]
df["8"] = df1["RMSE"]
df.index = df0["distance_in_lamda"]

plt.plot(df)
plt.title(r"Comparison different discretizazion, radius 12.8$\lambda$")
plt.xlabel("Distance [lambda]")
plt.ylabel("RMSE [dB]")
plt.legend(df.columns)
plt.show()
