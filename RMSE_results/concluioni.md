# Scelta della discretizzazione di un cilindro per l'analisi Ray Tracing Sionna con implementazione double edge

## Simualzione e specifiche

Si sono esseguite diverse simulazioni variando la discretizzazione del cilindro tra 8, 12, 17; varinado la distanza di osservazione tra 2 a 20 lambda.
Varinado il raggio del cilindro tra 10 e 25.6 lamda.

La frequenza è fc = 2e9 quindi la lunghezza d'onda è 0.15m 

A seconda della distanza di osservazione ci si trova:
in campo di Fresnel, cioè r >> lamda ma non r > 2 D^2 / lamda
in campo vicino radiativo cioè r > lamda.

## Risultati ottenuti 

I risultati degli RMSE nella zona d'ombra a seconda della distanza alle diverse discretizzazioni sono

![Grafico 1](RMSE_8.png)
![Grafico 2](RMSE_12.png)
![Grafico 3](RMSE_17.png)

## Conclusioni

Per la distanza r >> lamda la discretizzazione ottima è 12.
Per la distanza r > lamda la discretizzazione ottima è 8, per le altre discretizzazione il Ray tracing non riesce neanche  aclaolcare il campo.

Inoltre la scelta della discerizzazione ottima non dipende dal raggio del cilindro. 

Volendo rappresentare la curvatura con il parametro di crucatura si ha che:

### Campo di Fresnel 
$$
	E^2/R \approx 5.85 * \lamda *D / 10 
$$

### Campo vicino radiativo 
$$
	E^2/R \approx 2.67 * \lamda *D / 10 
$$



