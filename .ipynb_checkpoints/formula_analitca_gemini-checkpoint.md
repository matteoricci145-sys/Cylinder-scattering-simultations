# Validità della formula analitica per il calcolo del campo 

## ME 
u_inc, an_scattering, an_total = cylinder_te_inc_scat_total(theta_arr, cylinder_radius, circle_radius_i, 2*np.pi / lamda, terms=512)
Cosa fa questa funzione del simulatore Ray-Tracing Sionna?



## GEMINI
Questa funzione non esegue il ray-tracing vero e proprio, ma calcola la soluzione analitica esatta (spesso chiamata "ground truth") dello scattering elettromagnetico causato da un cilindro colpito da un'onda piana, considerando una polarizzazione TE (Trasversale Elettrica).

In contesti legati al simulatore NVIDIA Sionna, funzioni come questa (spesso incluse nei tutorial, nei notebook di validazione o scritte ad hoc) sono fondamentali per verificare l'accuratezza del Ray-Tracer. Poiché il ray-tracing si basa su approssimazioni geometriche e asintotiche (Ottica Geometrica e UTD), confrontare i risultati simulati da Sionna con la soluzione esatta prodotta da questa funzione permette di valutare quanto bene il simulatore gestisca ostacoli curvi e diffrazioni.

Ecco il dettaglio di come funziona e cosa calcola.
Parametri di Input

La funzione utilizza il metodo matematico dell'espansione in onde cilindriche (che sfrutta le funzioni di Bessel e Hankel) per risolvere le equazioni di Maxwell.
Parametro	Descrizione
theta_arr	Array contenente gli angoli di osservazione in cui misurare il campo.
cylinder_radius	Raggio fisico del cilindro che fa da ostacolo (scatteratore).
circle_radius_i	Raggio della circonferenza di osservazione (la distanza dei "ricevitori" dal centro del cilindro).
2*np.pi / lamda	Il numero d'onda k=λ2π​ del segnale incidente.
terms=512	Numero di termini della serie matematica infinita da calcolare per ottenere una precisione elevata.
Valori Restituiti

La funzione restituisce tre array contenenti i valori complessi del campo elettromagnetico valutati nei punti specificati da theta_arr e circle_radius_i:
Variabile	Descrizione
u_inc	Campo incidente: L'onda originaria non perturbata, calcolata come se il cilindro non esistesse.
an_scattering	Campo diffuso (Scattered): Le onde riflesse e diffratte generate esclusivamente dall'impatto con il cilindro.
an_total	Campo totale: La somma complessa dei primi due (u_inc + an_scattering), ovvero il campo reale che verrebbe misurato dai ricevitori.

Il legame con Sionna: Tipicamente, dopo aver eseguito questa funzione, lo script istruisce il Ray-Tracer di Sionna a simulare la stessa scena (un trasmettitore lontano, un cilindro e dei ricevitori disposti in cerchio). Alla fine, l'output totale di Sionna viene sovrapposto graficamente al vettore an_total per dimostrare l'accuratezza del motore di rendering elettromagnetico.



## ME
Questa funzione è utilizzzabile solo per valutare il campo in zona lontana oppure anche in zona vicina?



## GEMINI
Questa funzione è utilizzabile in entrambe le zone, sia in campo vicino (near-field) che in campo lontano (far-field).

La sua forza e la sua utilità derivano proprio da questo. Ecco perché:

È una soluzione matematica esatta: A differenza delle formule approssimate per le antenne o per l'ottica (che assumono r→∞), questa funzione calcola l'espansione esatta in serie di onde cilindriche (spesso basata sulla teoria dello scattering di Mie applicata ai cilindri). La matematica sottostante utilizza le funzioni di Bessel e le funzioni di Hankel.

Nessun limite di distanza: Le funzioni di Hankel descrivono correttamente l'andamento del campo per qualsiasi distanza radiale r passata alla funzione (il tuo circle_radius_i), a patto che sia maggiore o uguale alla superficie dell'ostacolo (r≥cylinder_radius).

Inclusione dei campi reattivi: Se imposti un circle_radius_i vicinissimo al cilindro, i termini matematici della serie terranno conto in modo naturale dell'energia reattiva, delle onde superficiali e delle oscillazioni tipiche del campo vicino di Fresnel o reattivo.

Perché è fondamentale per valutare il Ray-Tracer?

I motori di Ray-Tracing come quello di Sionna si basano su approcci asintotici (Ottica Geometrica e Teoria Uniforme della Diffrazione - UTD). L'UTD assume, per definizione, che l'onda diffratta si comporti come un raggio in campo lontano rispetto al punto di diffrazione.

Essendo questa funzione analitica valida ovunque, ti permette di fare uno "stress test" sui limiti fisici di Sionna:

Se imposti un cerchio di ricevitori in campo lontano (r≫λ), vedrai che i risultati di Sionna e an_total coincideranno quasi perfettamente.

Se avvicini progressivamente circle_radius_i alla superficie del cilindro (entrando in campo vicino), vedrai il raggio-tracing di Sionna iniziare a perdere precisione e a discostarsi dal risultato esatto di questa funzione, permettendoti di capire fino a che distanza le simulazioni del Ray-Tracer sono affidabili.
