import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# Dimensioni del cilindro e bordi
D = [10, 12.8, 15.9, 19, 22.3, 25.6]
NU = [6, 8, 12, 17]

# 1. Lista per accumulare i dataframe mediati di ogni NU
lista_mediati = []
    
for nu in NU:
    data_frames = []
    for d in D:
        # Lettura dati
        df = pd.read_csv(f"./RESULTS_{nu}_{d}.csv")
        df["cylinder_dimension"] = d 
        data_frames.append(df)
        
    df_all = pd.concat(data_frames, ignore_index=True)
    df_all['distance_in_lamda'] = df_all['distance_in_lamda'].round(2)

    # 2. Calcolo la media dell'RMSE raggruppato per distanza
    df_dimension = df_all.groupby("distance_in_lamda")["RMSE"].mean().reset_index()
    
    # 3. Aggiungo la colonna 'nu' così sappiamo a quale ciclo appartengono i dati
    df_dimension["nu"] = nu
    
    # Accumulo nella lista esterna
    lista_mediati.append(df_dimension)

# 4. Creazione del DataFrame finale unico
df_finale = pd.concat(lista_mediati, ignore_index=True)

# Riordino le colonne come richiesto per pulizia
df_finale = df_finale[["nu", "distance_in_lamda", "RMSE"]]
print("--- DATAFRAME FINALE ACCUMULATO ---")
print(df_finale.head(10)) # Mostra le prime 10 righe


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
plt.title("RMSE in funzione della distanza per diverse discretizzazioni", fontsize=14, fontweight='bold')
plt.xlabel(f"Distanza dal cilindro [$\lambda$]", fontsize=12)
plt.ylabel("RMSE Mediato sulle Dimensioni [dB]", fontsize=12)
plt.grid(True, linestyle="--", alpha=0.6)
plt.legend(title="Numero di facce")

# Mostra e salva il grafico
plt.tight_layout()
plt.savefig("confronto_RMSE_nu.png", dpi=300)


plt.xlim([0, 100])
plt.savefig("confronto_near_RMSE_nu.png", dpi=300)


