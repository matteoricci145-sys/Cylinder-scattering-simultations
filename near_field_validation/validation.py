import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

sionna = pd.read_csv("sionna_results.csv")

print("\n=== SIONNA df ===")
sionna = sionna.T
sionna.rename(columns={ 0 : "Equation", 1 : "Sionna-RT"}, inplace=True)
print(sionna)


# Nel file ci sono i risltati di cst con theta=90 
cst = pd.read_csv("far_filed_2m.txt", sep=r'\s+')
print("\n=== CST df ===")
cst = cst["Abs(E)[dB(V/m)]"]
print(cst)

print("\n === SIONA_FILTERED df ===")
sionna_filtered = sionna[sionna.index.astype(str).str.contains(r'\.0\d')]

print(sionna_filtered)

print("\n === RESULTS ====")

df = sionna_filtered
df.index = df.index.astype(float).round(0).astype(int)
df["cst"] = cst
df['cst'] = np.roll(df['cst'], shift=1)
print(df)

plt.title("Scatteref field comparison")
plt.plot(df)
plt.xlabel("Degree [°]")
plt.ylabel("Abs(E) [dB]")
plt.legend(df.columns)
plt.savefig("near_field_validation.png")
plt.show()




