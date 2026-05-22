from utils import calcola_durata_minuti, classifica_corsa, riepilogo_corse
from bicicletta import BiciclettaClassica, BiciclettaElettrica
from flotta import FlottaBici

def stampa_flotta_polimorfica(biciclette: list) -> None:
    print(f"{'ID':<10} | {'Dettagli generali e specifici':<60}")
    print("-"*75)
    for bici in biciclette:
        print(bici)
        
def main():
    print("----- ESECUTORE OOP -----")
    
    print("TEST FUNZIONI UTILS: ")
    durata = calcola_durata_minuti("08:15", "09:45")
    print(f"Minuti trascorsi (08:15 -> 09:45): {durata}")   
    ora_ini, ora_fin = "14:30", "13:15"
    h_ini, m_ini = [int(x) for x in ora_ini.split(":")]
    h_fin, m_fin = [int(x) for x in ora_fin.split(":")]
    if (h_fin * 60 + m_fin) < (h_ini * 60 + m_ini):
        print(f"Blocco preventivo: {ora_fin} viene prima di {ora_ini}") 
    print(f"Corsa di 30 min classificata come: {classifica_corsa(30)}")
    durate_esempio = [12, 35, 7, 50, 22, 90]
    report = riepilogo_corse(durate_esempio)
    print(f"Statistiche corse di prova: {report}\n")
    
    print("INIZIALIZZAZIONE DELLA FLOTTA: ")
    dati_input_esame = [
        {"id": "MI-001", "tipo": "classica", "stazione": "Cadorna", "km": 45.2, "taglia": "M"},
        {"id": "MI-002", "tipo": "elettrica", "stazione": "Duomo", "km": 120.8, "batteria": 85},
        {"id": "MI-003", "tipo": "elettrica", "stazione": "Centrale", "km": 340.5, "batteria": 15},
        {"id": "MI-004", "tipo": "classica", "stazione": "Garibaldi", "km": 12.0, "taglia": "L"}
    ]
    flotta_milano = FlottaBici.da_lista("Milano", dati_input_esame)
    print(f"Flotta creata correttamente per la città di: {flotta_milano.citta}")
    print(f"Numero totale di biciclette caricate: {len(flotta_milano)}\n")
    
    print("Stampa polimorfica: \n")
    stampa_flotta_polimorfica(flotta_milano.biciclette)
    print()
    
    #controllo metodi della classe Bicicletta
    bici_scelta = flotta_milano.cerca_per_id("MI-002")
    print(f"Stato iniziale: {bici_scelta}")
    #noleggia solo se disponibile
    if bici_scelta.disponibile:
        messaggio = bici_scelta.noleggia("Utente_Rossi")
        print(f"Noleggio: {messaggio}")
        print(f"Stato attuale: {bici_scelta}")
    #restituzione 
    print("Azione: Consegna a San Babila e aggiunta di 8.5 km")    
    bici_scelta.restituisci("San Babila", 8.5)
    print(f"Stato finale: {bici_scelta}\n")
    
    #controlli validazione
    bici_occupata = flotta_milano.cerca_per_id("MI-001")
    bici_occupata.noleggia("Primo_Utente") 
    if not bici_occupata.disponibile:
        print("Blocco: MI-001 non è disponibile per un secondo noleggio.")
    else:
        bici_occupata.noleggia("Secondo_Utente")
        
    bici_scarica = flotta_milano.cerca_per_id("MI-003")
    if bici_scarica.batteria_percentuale < 20:
        print(f"Blocco: Batteria al {bici_scarica.batteria_percentuale}%, ricaricare il mezzo.")
    else:
        bici_scarica.noleggia("Utente_Green")
        
    id_da_cercare = "MI-999"
    esiste = False
    for b in flotta_milano.biciclette:
        if b.id_bici == id_da_cercare:
            esiste = True    
    if not esiste:
        print(f"Blocco: L'ID {id_da_cercare} non è presente nella lista.")
    else:
        flotta_milano.cerca_per_id(id_da_cercare)
        
    km_da_aggiungere = -15.0
    if km_da_aggiungere <= 0:
        print(f"Blocco: Impossibile aggiungere {km_da_aggiungere} km. Valore non valido.")
    else:
        bici_occupata.aggiungi_km(km_da_aggiungere)
    print()
    
    print("STATISTICHE FINALI: ")
    print(f"Batteria MI-003 prima della ricarica: {bici_scarica.batteria_percentuale}%")
    bici_scarica.ricarica(50)
    print(f"Batteria post ricarica parziale (+50%): {bici_scarica.batteria_percentuale}%")
    bici_scarica.ricarica(60)
    print(f"Batteria post ricarica totale (limite 100%): {bici_scarica.batteria_percentuale}%")
    
    stats = flotta_milano.statistiche()
    print("\nResoconto finale flotta:")
    for k, v in stats.items():
        print(f" - {k}: {v}")

if __name__ == "__main__":
    main()