import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 1. Carica i dataset
df_dev = pd.read_csv("amplitudes_dev.csv")
df_str = pd.read_csv("amplitudes_str.csv")
df_an = pd.read_csv("analytical.csv")

# 2. Converti esplicitamente tutti i valori in float (evita che rimangano stringhe)
df_dev = df_dev.astype(float)
df_str = df_str.astype(float)
df_an = df_an.astype(float)

# 3. Converti le colonne (Angoli) in numeri float per l'asse X
angles = pd.to_numeric(df_dev.columns, errors='coerce')

# 4. Calcola l'array delle distanze senza alterare l'indice dei DataFrame
distances = df_an.index / 0.15

# 5. Ciclo di plot usando gli indici posizionali (.iloc)
for idx in range(len(df_an)):
    dist = distances[idx]
    
    plt.figure()  # Crea una nuova figura pulita per ogni ciclo
    
    # Se i nomi delle colonne sono angoli validi li usiamo sull'asse X
    if not np.isnan(angles).any():
        plt.plot(angles, df_dev.iloc[idx], label="Developed")
        plt.plot(angles, df_str.iloc[idx], label="Classic")
        plt.plot(angles, df_an.iloc[idx], label="Equation")
    else:
        plt.plot(df_dev.iloc[idx], label="Developed")
        plt.plot(df_str.iloc[idx], label="Classic")
        plt.plot(df_an.iloc[idx], label="Equation")
    
    plt.title(rf"Comparison at distance {dist:.2f}$\lambda$")
    plt.xlabel("Angle (°)")
    plt.ylabel("Amplitude (dB)")
    plt.grid(True)  # Aggiunge la griglia per verificare visivamente i dati
    plt.legend()
    
    plt.show()
