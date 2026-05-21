import matplotlib.pyplot as plt

fig, ax = plt.subplots()
ax.plot([0, 1, 2], [0, 1, 4], label="Dati")

# Testo informativo aggiuntivo
info_text = "Nota: Dati aggiornati al 2026\nMedia: 1.66\nTarget: Raggiunto"

# Aggiunta del box di testo
ax.text(0.05, 0.95, info_text, 
        transform=ax.transAxes, 
        fontsize=10,
        verticalalignment='top',
        bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

plt.title("Titolo Principale del Grafico")
plt.show()
