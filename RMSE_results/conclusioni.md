# Scelta della Discretizzazione di un Cilindro per l'Analisi Ray Tracing Sionna con Implementazione Double Edge

## 1. Simulazione e Specifiche Tecniche

Le analisi sono state condotte utilizzando il simulatore Ray Tracing **Sionna**, integrando un'implementazione a doppia lamina (*double edge*) per la gestione dei fenomeni diffrattivi.

Le simulazioni sono state eseguite configurando i seguenti parametri geometrici e di scenario:
* **Frequenza di lavoro ($f_c$):** $2.0 \text{ GHz}$
* **Lunghezza d'onda ($\lambda$):** $0.15 \text{ m}$
* **Raggio del cilindro ($R$):** Variato progressivamente tra $10\lambda$ e $25.6\lambda$.
* **Distanza di osservazione ($r$):** Variata in un intervallo compreso tra $2\lambda$ e $20\lambda$.
* **Livelli di discretizzazione poligonale:** Il cilindro è stato approssimato valutando configurazioni a 8, 12 e 17 facce.

A seconda della distanza di osservazione $r$ rispetto alle dimensioni della struttura (diametro $D$) e alla lunghezza d'onda $\lambda$, le regioni di spazio analizzate sono state classificate secondo i seguenti criteri fisici:
* **Campo di Fresnel:** Condizione in cui $r \gg \lambda$, ma la distanza non soddisfa ancora il criterio di campo lontano ($r < \frac{2D^2}{\lambda}$).
* **Campo vicino radiativo:** Condizione di prossimità alla struttura, definita genericamente per $r > \lambda$.

---

## 2. Risultati Ottenuti

L'accuratezza dei modelli è stata valutata calcolando l'errore quadratico medio (**RMSE** - *Root Mean Square Error*) del campo elettromagnetico all'interno della **zona d'ombra**, regione in cui il contributo della diffrazione è predominante.

I risultati dell'RMSE in funzione della distanza di osservazione per le diverse discretizzazioni sono illustrati nei seguenti grafici:

![Grafico 1: Andamento dell'RMSE con discretizzazione a 8 facce](RMSE_8.png)
![Grafico 2: Andamento dell'RMSE con discretizzazione a 12 facce](RMSE_12.png)
![Grafico 3: Andamento dell'RMSE con discretizzazione a 17 facce](RMSE_17.png)

Un'osservazione fondamentale emersa dalle simulazioni indica che **la scelta della discretizzazione ottima risulta indipendente dal raggio del cilindro ($R$)**, legando la precisione del modello quasi esclusivamente alla distanza di osservazione e alla regione di campo.

---

## 3. Conclusioni e Linee Guida

Dall'analisi comparativa dei dati emergono criteri di scelta netti e differenziati a seconda dello scenario di ricezione:

### 3.1 Scenario in Campo di Fresnel ($r \gg \lambda$)
In questa regione, la configurazione che minimizza l'RMSE garantendo il miglior compromesso tra accuratezza numerica e costo computazionale è la **discretizzazione a 12 facce**. Questo livello di dettaglio permette al solutore *double edge* di approssimare correttamente i punti di distacco dell'onda geometrica e i relativi contributi diffrattivi.

### 3.2 Scenario in Campo Vicino Radiativo ($r > \lambda$)
In condizioni di forte prossimità alla struttura, la **discretizzazione a 8 facce** si è rivelata l'unica opzione applicabile. All'aumentare del dettaglio geometrico (discretizzazioni a 12 e 17 facce), l'algoritmo di Ray Tracing manifesta instabilità numeriche critiche, fallendo completamente nel calcolo e nella convergenza del campo.

---

## 4. Fattore della Curvatura Ottima

Utilizzzando lo stesso fattore di cruvatura utilizzato  nell'articolo preso in esame si possono ricavare le relaizoni del fattore di curvatora megliore dei due casi.  

### Campo di Fresnel
$$
\frac{E^2}{R} \approx 0.585 \cdot \lambda \cdot \frac{D}{10}
$$

### Campo Vicino Radiativo
$$
\frac{E^2}{R} \approx 0.267 \cdot \lambda \cdot \frac{D}{10}
$$

Queste formule permettono di scalare il livello di discretizzazione geometrica ($E$) in funzione della frequenza operativa ($\lambda$) e delle dimensioni del cilindro, assicurando la stabilità del solutore elettromagnetico di Sionna.
$$



