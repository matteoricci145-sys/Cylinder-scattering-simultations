import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# Dimensioni del cilindro e bordi
D = [10, 12.8, 15.9, 19, 22.3, 25.6]
NU = [17]
fc = 2e9
lamda = 3e8/fc
# 1. Lista per accumulare i dataframe mediati di ogni NU
lista = []
    
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
    #df_dimension = df_all.groupby("distance_in_lamda")["RMSE"].mean().reset_index()
    
    # 3. Aggiungo la colonna 'nu' così sappiamo a quale ciclo appartengono i dati
    df_all["nu"] = nu
    
    # Accumulo nella lista esterna
    lista.append(df_all)

# 4. Creazione del DataFrame finale unico
df_finale = pd.concat(lista, ignore_index=False)
print(df_finale)

# Riordino le colonne come richiesto per pulizia
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
    hue="cylinder_dimension", 
    marker="o", 
    palette="Set1"
)

# Personalizzazione del grafico
plt.title("RMSE in funzione della Distanza", fontsize=14, fontweight='bold')
plt.xlabel("Distanza dal cilindro [lambda]", fontsize=12)
plt.ylabel("RMSE Mediato sulle Dimensioni [dB]", fontsize=12)
plt.grid(True, linestyle="--", alpha=0.6)
plt.legend(title="Valori di dimensioni del cilindro")
for d in D:
    plt.axvline(x=2 * (2*d*lamda)**2/ lamda, linestyle='--', label="Far field")

# Mostra e salva il grafico
plt.tight_layout()
plt.savefig("confronto_RMSE_nu.png", dpi=300)
plt.show()

exit()
# =====================================================================
# GRAFICO AGGIORNATO (Asse Y invertito e Linea a X=10)
# =====================================================================
plt.figure(figsize=(10, 6))

# Creiamo il grafico a linee
sns.lineplot(
    data=df_finale, 
    x="distance_in_lamda", 
    y="RMSE", 
    hue="nu", 
    marker="o", 
    palette="Set1"
)

# 1. INVERTIRE L'ASSE Y (L'RMSE più basso va in alto)
plt.gca().invert_yaxis()

# 2. TRACCIARE LA LINEA VERTICALE A DISTANZA = 10
# ls="--" la fa tratteggiata, color="red" la rende visibile, alpha ne regola la trasparenza
plt.axvline(x=10, color="red", linestyle="--", linewidth=1.5, alpha=0.8, label="Distanza = 10 $\lambda$")

# Personalizzazione del grafico
plt.title("Andamento dell'RMSE Medio (Valori migliori in alto)", fontsize=14, fontweight='bold')
plt.xlabel("Distanza dal cilindro [lambda]", fontsize=12)
plt.ylabel("RMSE Mediato (Scala Invertita)", fontsize=12)
plt.grid(True, linestyle="--", alpha=0.5)

# Aggiorniamo la legenda per includere anche la linea verticale appena aggiunta
plt.legend(title="Legenda")

# Mostra e salva il grafico
plt.tight_layout()
plt.savefig("confronto_RMSE_nu_invertito.png", dpi=300)
plt.show()
