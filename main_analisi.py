import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from utils import classifica_corsa

#task 5 
#generazione dati
np.random.seed(14)
os.makedirs("output", exist_ok=True) #creazione cartella output se non esiste
# 500 valori interi (media 28, std 12) clippati a >= 1
durate = np.random.normal(28,12, size=500).astype(int)
durate = np.clip(durate, 1, None) #per evitare di avere durate<=0
# km basati sulla durata con fattore di conversione casuale, arrotondati a 2 decimali
km = durate * np.random.uniform(0.15, 0.25, size=500)
km = np.round(km, 2)   
     
velocita = km / (durate / 60)
    
print("DURATE -> Shape:", durate.shape, "| Dtype:", durate.dtype)
print(f"  Min: {durate.min()} | Max: {durate.max()} | Media: {durate.mean():.2f} | Std: {durate.std():.2f}\n")
    
print("KM -> Shape:", km.shape, "| Dtype:", km.dtype)
print(f"  Min: {km.min():.2f} | Max: {km.max():.2f} | Media: {km.mean():.2f} | Std: {km.std():.2f}\n")
    
print("VELOCITA -> Shape:", velocita.shape, "| Dtype:", velocita.dtype)
print(f"  Min: {velocita.min()} | Max: {velocita.max()} | Media: {velocita.mean():.2f} | Std: {velocita.std():.2f}\n")
    
    #slicing e selezione
print(f"Prime 10 corse: {durate[:10]}")
print(f"Ultine 10 corse: {durate[-10:]}")

indici_fancy= [0, 42, 99, 150, 200, 350, 499]
print("Estrazione con fancy indexing: ", durate[indici_fancy])
    
    #maschere booleane per corse>45 minuti
filtro_lunghe = durate > 45
print(f"Numero corse più lunghe di 45 min: {np.sum(filtro_lunghe)}")
print(f"Distanza media corse lunghe: {km[filtro_lunghe].mean():.2f} km")
    
print(f"Corsa più veloce: indice {np.argmax(velocita)} ({velocita.max():.2f} km/h)")
print(f"Corsa più lenta: indice {np.argmin(velocita)} ({velocita.min():.2f} km/h)\n")
    
    #statistiche e normalizzazioni
percentili = np.percentile(durate, [25, 50, 75, 90])
print("Percentili durate [25°, 50°, 75°, 90°]: ", percentili)
    
    #normalizzazione min-max durate
durate_norm = (durate - durate.min()) / (durate.max() - durate.min())
print(f"Verifica range normalizzato -> Min: {durate_norm.min()} | Max: {durate_norm.max()}")
    
    #correlazione lineare tra durata e km
r_pearson = np.corrcoef(durate, km)[0, 1]
print(f"Correlazione di Pearson: {r_pearson:.4f}")
    # commento sul risultato: c'è un legame lineare positivo fortissimo, all'aumentare dei minuti aumentano proporzionalmente i km percorsi
    
    #genero 30 giorni di volume corse
corse_30gg = np.random.randint(80, 200, size=30)
    
    #media mobile a 7 giorni
media_mobile_7gg = np.convolve(corse_30gg, np.ones(7)/7, mode='valid')
print(f"Giorno con picco massimo: Giorno {np.argmax(corse_30gg) + 1} ({corse_30gg.max()} corse)")
print(f"Giorno con picco minimo: Giorno {np.argmin(corse_30gg) + 1} ({corse_30gg.min()} corse)\n")
    
print(f"{'Giorno':<8} | {'Corse':<6} | {'Media Mobile (7g)':<18}")
print("-" * 38)
for i in range(30):
    if i >= 6 and (i - 6) < len(media_mobile_7gg):
        val_mm = f"{media_mobile_7gg[i - 6]:.2f}"
    else:
        val_mm = "N/D"        
    print(f"Giorno {i+1:<2} | {corse_30gg[i]:<6} | {val_mm:<18}")
print("\n" + "="*50 + "\n")
    
#task 6
citta = ["Milano", "Roma", "Torino"]
date = ["2026-05-10", "2026-05-11", "2026-05-12"]
fasce_orarie = ["Mattina", "Pomeriggio", "Sera", "Notte"]

# df_corse — almeno 80 righe:
df_corse = pd.DataFrame({
    "id_corsa": [f"CRS_{i:03d}" for i in range(80)],
    "id_bici": [f"BC_{np.random.randint(1, 21):03d}" for _ in range(80)],
    "id_utente": [f"UT_{np.random.randint(1, 26):03d}" for _ in range(80)],
    "citta": [np.random.choice(citta) for _ in range(80)],
    "data_corsa": [np.random.choice(date) for _ in range(80)],
    "durata_minuti": [float(np.random.randint(5, 60)) for _ in range(80)],
    "km_percorsi": [round(np.random.uniform(1.2, 14.5), 2) for _ in range(80)],
    "fascia_oraria": [np.random.choice(fasce_orarie) for _ in range(80)]
})

# inserisco i 5 duplicati espliciti e gli 8 NaN sparsi
df_corse = pd.concat([df_corse, df_corse.iloc[:5]], ignore_index=True)
df_corse.loc[[5, 18, 33, 50], "durata_minuti"] = np.nan
df_corse.loc[[12, 27, 41, 64], "km_percorsi"] = np.nan

#  df_bici (20 righe)
df_bici = pd.DataFrame({
    "id_bici": [f"BC_{i:03d}" for i in range(1, 21)],
    "tipo": [np.random.choice(["classica", "elettrica"]) for _ in range(20)],
    "citta": [np.random.choice(citta) for _ in range(20)],
    "anno_acquisto": [np.random.randint(2022, 2026) for _ in range(20)],
    "costo_acquisto": [round(np.random.uniform(500, 1200), 2) for _ in range(20)]
})

# df_utenti (25 righe)
df_utenti = pd.DataFrame({
    "id_utente": [f"UT_{i:03d}" for i in range(1, 26)],
    "nome": [f"Utente_{i}" for i in range(1, 26)],
    "citta": [np.random.choice(citta) for _ in range(25)],
    "tipo_abbonamento": [np.random.choice(["Standard", "Premium"]) for _ in range(25)],
    "data_iscrizione": ["2025-04-01" for _ in range(25)]
})


print("STATO PRIMA DELLA PULIZIA: ")
df_corse.info()

# rimozione duplicati
df_corse = df_corse.drop_duplicates().reset_index(drop=True)

# imputazione dei NaN: mediana per città per le durate, formula basata su velocità media per i km
df_corse["durata_minuti"] = df_corse.groupby("citta")["durata_minuti"].transform(lambda x: x.fillna(x.median()))
df_corse["km_percorsi"] = df_corse["km_percorsi"].fillna(df_corse["durata_minuti"] * 0.18)

# gestione date ed estrazione features temporali
df_corse["data_corsa"] = pd.to_datetime(df_corse["data_corsa"])
df_corse["mese"] = df_corse["data_corsa"].dt.month
df_corse["giorno_settimana"] = df_corse["data_corsa"].dt.day_name()

print("\nSTATO DOPO LA PULIZIA")
df_corse.info()
print("\n STATISTICHE DESCRITTIVE DEL DATAFRAME PULITO")
print(df_corse.describe())


# applico la funzione custom importata da utility
df_corse["tipo_corsa"] = df_corse["durata_minuti"].apply(classifica_corsa)

# calcolo velocità media della singola corsa
df_corse["velocita_media"] = df_corse["km_percorsi"] / (df_corse["durata_minuti"] / 60)

# funzione per calcolare le tariffe basata sulla traccia
def calcola_tariffa(minuti):
    if minuti < 15:
        return 1.50
    elif 15 <= minuti <= 45:
        return 2.50 + 0.10 * (minuti - 15)
    else:
        return 5.00 + 0.08 * (minuti - 45)

df_corse["costo_stimato"] = df_corse["durata_minuti"].apply(calcola_tariffa)

#aggregazione e merge
print("Aggregazione per Città:")
print(df_corse.groupby("citta").agg(
    numero_corse=("id_corsa", "count"),
    durata_media=("durata_minuti", "mean"),
    km_totali=("km_percorsi", "sum"),
    costo_totale=("costo_stimato", "sum")
))

print("\nAggregazione per Fascia Oraria:")
print(df_corse.groupby("fascia_oraria").agg(
    numero_corse=("id_corsa", "count"),
    velocita_media=("velocita_media", "mean")
))

print("\nPivot Table (Città / Tipo Corsa):")
print(df_corse.pivot_table(index="citta", columns="tipo_corsa", values="id_corsa", aggfunc="count", fill_value=0))

#rinomino la colonna 'citta' in ogni dataframe prima del merge per non fare confusione coi suffissi
df_corse_rinominato = df_corse.rename(columns={"citta": "citta_corsa"})
df_bici_rinominato = df_bici.rename(columns={"citta": "citta_bici"})
df_utenti_rinominato = df_utenti.rename(columns={"citta": "citta_utente"})

#adesso il merge è pulito, lineare e non sovrascrive nulla in modo strano
df_unito = df_corse_rinominato.merge(df_bici_rinominato, on="id_bici")
df_unito = df_unito.merge(df_utenti_rinominato, on="id_utente")

print("\nPrime 5 righe del dataset unito:")
print(df_unito.head(5))
print("\nColonne disponibili dopo il merge:", df_unito.columns.tolist())

#classifiche top-n richieste
print("\ntop 5 Bici più usate:")
print(df_unito["id_bici"].value_counts().head(5))

print("\ntop 3 Utenti Premium per spesa totale:")
df_premium = df_unito[df_unito["tipo_abbonamento"] == "Premium"]
classifica_utenti = df_premium.groupby(["id_utente", "nome"])["costo_stimato"].sum().reset_index()
print(classifica_utenti.sort_values(by="costo_stimato", ascending=False).head(3))
print("\n" + "="*50 + "\n")

#task 7

# imposto alcuni stili globali standard
plt.rcParams["font.size"] = 10
plt.rcParams["figure.figsize"] = (9, 4.5)
sns.set_theme(style="whitegrid")

# grafico  1
plt.figure()
df_unito.groupby(["data_corsa", "citta_corsa"]).size().unstack(fill_value=0).plot(marker='o', linewidth=2)
#domanda di business: quali sono i volumi di utilizzo giornalieri e le differenze di trend tra le varie città?
plt.title("Andamento giornaliero delle corse per singola città")
plt.xlabel("Data")
plt.ylabel("Numero di noleggi")
plt.legend(title="Città")
plt.tight_layout()
plt.savefig("output/01_serie_temporale.png")
plt.close()

# grafico 2
plt.figure()
#domanda di business: qual è la durata tipica di un noleggio e come varia la distribuzione dei tempi tra i diversi comuni?
sns.histplot(data=df_unito, x="durata_minuti", hue="citta_corsa", kde=True, element="step", palette="muted")
plt.title("Distribuzione dei minuti di utilizzo per città")
plt.xlabel("Minuti corsa")
plt.ylabel("Frequenza")
plt.savefig("output/02_distribuzione_durate.png")
plt.close()

#grafico 3
plt.figure()
#domanda di business: in quali fasce orarie c'è una maggiore richiesta di bici elettriche rispetto alle classiche?
df_orari = df_unito.groupby(["fascia_oraria", "tipo"]).size().reset_index(name="conteggio")
sns.barplot(data=df_orari, x="fascia_oraria", y="conteggio", hue="tipo", palette="Set2")
plt.title("Utilizzo delle tipologie di bici per fascia oraria")
plt.xlabel("Fascia Oraria")
plt.ylabel("N. Corse")
plt.legend(title="Tipo Mezzo")
plt.savefig("output/03_fasce_orarie.png")
plt.close()

#grafico 4
plt.figure()
#domanda di business: le corse più lunghe tendono ad avere velocità medie inferiori (es. utilizzo ricreativo vs pendolarismo)?
colori_citta = {"Milano": "teal", "Roma": "crimson", "Torino": "gold"}
for nome_citta, gruppo in df_unito.groupby("citta_corsa"):
    plt.scatter(gruppo["durata_minuti"], gruppo["velocita_media"], label=nome_citta, color=colori_citta[nome_citta], alpha=0.6)

#linea di tendenza
coeff = np.polyfit(df_unito["durata_minuti"], df_unito["velocita_media"], 1)
policod = np.poly1d(coeff)
plt.plot(df_unito["durata_minuti"], policod(df_unito["durata_minuti"]), color="darkred", linestyle="--", label="Trend")
plt.title("Relazione tra durata della corsa e velocità media")
plt.xlabel("Durata (minuti)")
plt.ylabel("Velocità media (km/h)")
plt.legend()
plt.savefig("output/04_scatter_durata_velocita.png")
plt.close()

#grafico 5 
#domanda di business: qual è la panoramica complessiva dei principali KPI di performance per il management?
fig, axs = plt.subplots(2, 2, figsize=(13, 9))
fig.suptitle("Dashboard Riepilogativa Servizio VeloCittà", fontsize=14, fontweight="bold")

# alto SX: conteggio corse
conteggio_c = df_unito["citta_corsa"].value_counts()
axs[0, 0].bar(conteggio_c.index, conteggio_c.values, color=["cadetblue", "indianred", "yellowgreen"])
axs[0, 0].set_title("Totale corse per città")
axs[0, 0].set_ylabel("Numero corse")

# alto DX: tipi abbonamento
counts_abb = df_unito["tipo_abbonamento"].value_counts()
axs[0, 1].pie(counts_abb.values, labels=counts_abb.index, autopct='%1.1f%%', colors=["#4f5d75", "#ef8354"])
axs[0, 1].set_title("Ripartizione abbonamenti utenti")

# basso SX: costo totale per città
ricavi_citta = df_unito.groupby("citta_corsa")["costo_stimato"].sum()
axs[1, 0].bar(ricavi_citta.index, ricavi_citta.values, color="peru")
axs[1, 0].set_title("Ricavi totali per città (€)")
axs[1, 0].set_ylabel("Euro (€)")

# basso DX: boxplot durate
sns.boxplot(data=df_unito, x="tipo_corsa", y="durata_minuti", ax=axs[1, 1], palette="Pastel2")
axs[1, 1].set_title("Distribuzione durate per tipo corsa")
axs[1, 1].set_xlabel("Categoria")
axs[1, 1].set_ylabel("Minuti")

plt.tight_layout()
plt.savefig("output/05_dashboard.png")
plt.close()

print("Tutti i grafici richiesti sono stati correttamente salvati nella cartella 'output/'.")


