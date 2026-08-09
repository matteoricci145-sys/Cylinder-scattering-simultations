import pandas as pd
import matplotlib.pyplot as plt

df0 = pd.read_csv("./LONG_LONG_RESULTS_12_12.8.csv")
df1 = pd.read_csv("./DEV2_RESULTS_12_12.8.csv")

df = pd.DataFrame()
df["Classic"] = df0["RMSE"]
df["Standard"] = df1["RMSE"]
df.index = df0["distance_in_lamda"]

plt.plot(df)
plt.title(r"Bug fixing validation")
plt.xlabel("Distance [lambda]")
plt.ylabel("RMSE [dB]")
plt.legend(df.columns)
plt.savefig("bug_fixed2.png")
plt.show()
