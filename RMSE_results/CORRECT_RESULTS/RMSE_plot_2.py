import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# Dimensioni del cilindro e bordi
#D = [10, 12.8, 15.9, 19, 22.3, 25.6]
#NU = [6, 8, 12, 17]

d = 10
NU = [6, 8, 12, 17]

lamda = 3e8/2e9
# 1. Lista per accumulare i dataframe mediati di ogni NU
lista_df = []
    
for nu in NU:
    df = pd.read_csv(f"./RESULTS_{nu}_{d}.csv")

    df["cylinder_dimension"] = d
    df["nu"] = nu
    print(f"NU: {nu}") 
    print(df)
    # Accumulo nella lista esterna
    lista_df.append(df)

# 4. Creazione del DataFrame finale unico
df_finale = pd.concat(lista_df, ignore_index=True)

print("--- DATAFRAME FINALE ACCUMULATO ---")

# =====================================================================
# 5. GRAFICO CON SEABORN (X: distanza, Y: RMSE, Linee separate per NU)
# =====================================================================
plt.figure(figsize=(10, 6))

# Usiamo 'hue' per creare una linea di colore diverso per ogni 'nu'
# 'marker="o"' aggiunge i pallini sui punti dati per renderlo più leggibile
sns.lineplot(
    data=df_finale, 
    x="distance_in_lamda", 
    y="RMSE", 
    hue="nu", 
    marker="o", 
    palette="Set1"
)

# Personalizzazione del grafico
plt.title(f"Cylinder radius = {d} $\lambda$", fontsize=14, fontweight='bold')
plt.title(f"Cylinder radius = {d} $\lambda$", fontsize=14, fontweight='bold')
plt.xlabel("Distanza dal cilindro [lambda]", fontsize=12)
plt.ylabel("RMSE Mediato sulle Dimensioni [dB]", fontsize=12)
plt.grid(True, linestyle="--", alpha=0.6)
plt.legend(title="Valori di NU")
D_meter = d*lamda
plt.axvline(x=2*((2*D_meter)**2/lamda))
# Mostra e salva il grafico
plt.tight_layout()
plt.savefig(f"RMSE_D_{d}.png", dpi=300)

plt.xlim([0, 100])
plt.savefig(f"near_RMSE_D_{d}.png", dpi=300)

exit()
