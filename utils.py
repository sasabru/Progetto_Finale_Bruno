def calcola_durata_minuti(ora_inizio: str, ora_fine: str) -> int: #con -> indichiamo il tipo del valore di ritorno
    h_ini, m_ini = [int(x) for x in ora_inizio.split(":")]
    h_fin, m_fin = [int(x) for x in ora_fine.split(":")]
    
    minuti_inizio = h_ini*60 + m_ini
    minuti_fine = h_fin*60 + m_fin
    
    if minuti_fine < minuti_inizio:
        raise ValueError("ERRORE: l'ora di fine non può essere precedente all'ora di inizio")
    return minuti_fine - minuti_inizio

def classifica_corsa(durata_minuti: int) -> str:
    if durata_minuti < 15:
        return "breve"
    elif 15<= durata_minuti <= 45:
        return "media"
    else: 
        return "lunga"
    
def riepilogo_corse(lista_durate: list) -> dict:
    if not lista_durate:
        return {
            "totale": 0, "media": 0.0, "max": 0, "min": 0, "brevi": 0, "medie": 0, "lunghe": 0
        }
        
    totale = len(lista_durate)
    massimo = max(lista_durate)
    minimo = min(lista_durate)
    media = sum(lista_durate) / totale
    brevi = 0
    medie = 0
    lunghe = 0
    
    for durata in lista_durate:
        categoria = classifica_corsa(durata)
        if categoria == "breve":
            brevi += 1
        elif categoria == "media":
            medie += 1
        elif categoria == "lunga":
            lunghe += 1
    
    return {
        "totale": totale,
        "media": round(media,2), #arrotondiamo la media a due decimali per una questione di pulizia visiva
        "max": massimo,
        "min": minimo,
        "brevi": brevi,
        "medie": medie,
        "lunghe": lunghe
    }

    
