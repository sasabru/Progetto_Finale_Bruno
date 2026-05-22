class Bicicletta: 
    def __init__(self, id_bici: str, tipo: str, stazione_corrente: str, km_percorsi: float, disponibile: bool = True):
        self.id_bici = id_bici
        self.tipo = tipo
        self.stazione_corrente = stazione_corrente
        self.km_percorsi = float(km_percorsi)
        self.disponibile = disponibile
    
    @property
    def km_percorsi(self) -> float:
        return self._km_percorsi
    
    def aggiungi_km(self, km: float) -> None:
        if km<=0:
            raise ValueError("I km aggiunti devono essere maggiori di zero")
        self._km_percorsi += km
    
    def noleggia(self, utente: str) -> str:
        if not self.disponibile:
            raise ValueError(f"La bicicletta {self.id_bici} è già in uso")
        self.disponibile = False
        return f"Bici {self.id_bici} noleggiata dall'utente {utente}"
    
    def restituisci(self, stazione : str, km_aggiunta: float) -> None:
        self.stazione_corrente = stazione
        self.aggiungi_km(km_aggiunta)
        self.disponibile = True
    
    def __str__(self) -> str:
        if self.disponibile:
            stato = "DISPONIBILE"
        else: 
            stato = "IN USO"
        return f"[{self.id_bici}] {self.tipo} | {self.stazione_corrente} | {self._km_percorsi:.1f} km | {stato}"
    
    def __repr__(self) -> str:
        return f"Bicicletta('{self.id_bici}', '{self.tipo}', '{self.stazione_corrente}', '{self._km_percorsi}, {self.disponibile})"
    
    

class BiciclettaClassica(Bicicletta):
    def __init__(self, id_bici: str, stazione_corrente: str, km_percorsi: float, taglia: str = "M", disponibile: bool = True):
        super().__init__(id_bici, "classica", stazione_corrente, km_percorsi, disponibile)
        self.taglia = taglia
        
    def __str__(self) -> str:
        base = super().__str__()
        return f"{base} | Taglia: {self.taglia}"
    

class BiciclettaElettrica(Bicicletta):
    def __init__(self, id_bici: str, stazione_corrente: str, km_percorsi: float, batteria_percentuale: int = 100, disponibile: bool = True):
        super().__init__(id_bici, "elettrica", stazione_corrente, km_percorsi, disponibile)
        self.batteria_percentuale = batteria_percentuale
        
    def ricarica(self, percentuale: int) -> None:
        self.batteria_percentuale = min(100, self.batteria_percentuale + percentuale)
        
    def noleggia(self, utente: str) -> str:
        if self.batteria_percentuale < 20:
            raise ValueError(f"Batteria troppo bassa ({self.batteria_percentuale}%), non disponibile per il noleggio")
        return super().noleggia(utente)
    
    def __str__(self) -> str:
        base = super().__str__()
        return f"{base} | Batteria: {self.batteria_percentuale}%"