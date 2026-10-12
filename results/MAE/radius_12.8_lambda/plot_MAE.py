import glob
import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams.update({"font.size": 20})

nus = [6, 8, 12, 17]
radius = 12.8

fig, ax = plt.subplots(figsize=(16, 10))

for nu in nus:
    files = glob.glob(f"MAE_{nu}_{12.8}*.csv")
    if not files:
        print(f"Nessun file trovato per nu = {nu}")
        continue

    df = pd.read_csv(files[0])
    df = df.sort_values("distance_in_lamda")

    ax.plot(df["distance_in_lamda"], df["MAE"],
            linewidth=1.8, label=rf"{nu}", marker="o", markersize=5)

ax.set_xlabel(r"Distance [$\lambda$]")
ax.set_ylabel("MAE [dB]")
ax.set_title("MAE versus distance for different discretization levels")
ax.grid(True, which="both", alpha=0.3)
ax.legend(title="Discretization level")
ax.axvline(x=10, color="k", linestyle="--", linewidth=1.2, label=r"$d = 10\lambda$")
ax.text(10, ax.get_ylim()[1], r" $10\lambda$", va="top", ha="left")

fig.tight_layout()
fig.savefig("MAE_vs_distance.png", dpi=300)
plt.show()
