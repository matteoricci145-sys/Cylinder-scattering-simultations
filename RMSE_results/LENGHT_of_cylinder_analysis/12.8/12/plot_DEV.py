import pandas as pd
import matplotlib.pyplot as plt

df0 = pd.read_csv("./LONG_LONG_RESULTS_12_12.8.csv")
df1 = pd.read_csv("./DEV3_RESULTS_12_12.8.csv")

df = pd.DataFrame()
df["Classic"] = df0["RMSE"]
df["Fixed"] = df1["RMSE"]
df.index = df0["distance_in_lamda"]

plt.plot(df)
plt.title(r"Bug fixing validation mobile $\epsilon$")
plt.xlabel("Distance [lambda]")
plt.ylabel("RMSE [dB]")
plt.legend(df.columns)
plt.savefig("bug_fixed3.png")
plt.show()
