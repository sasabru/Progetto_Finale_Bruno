from bicicletta import Bicicletta, BiciclettaClassica, BiciclettaElettrica

class FlottaBici:
    def __init__(self,citta: str):
        self.citta = citta
        self.biciclette = []
        
    def aggiungi(self, bici: Bicicletta) -> None:
        self.biciclette.append(bici)
        
    def cerca_per_id(self, id_bici: str) ->Bicicletta: 
        for b in self.biciclette:
            if b.id_bici == id_bici:
                return b
        raise KeyError(f"Bicicletta {id_bici} non trovata")
    
    def rimuovi(self, id_bici: str) -> None:
        bici = self.cerca_per_id(id_bici)
        self.biciclette.remove(bici)
        
    def disponibili(self) -> list:
        return [b for b in self.biciclette if b.disponibile]
    
    def statistiche(self) -> dict:
        totale = len(self.biciclette)
        if totale == 0:
            return {"totale": 0, "disponibili": 0, "in_uso": 0, "km_totali_flotta": 0, "km_medi_per_bici": 0}
        disp = len(self.disponibili())
        km_tot = sum(b.km_percorsi for b in self.biciclette)
        return {
            "totale": totale,
            "disponibili": disp,
            "in_uso": totale - disp,
            "km_totali_flotta": round(km_tot, 2),
            "km_medi_per_bici": round(km_tot / totale, 2)
        }
        
    def __len__(self) -> int:
        return len(self.biciclette)
    
    @classmethod
    def da_lista(cls, citta: str, dati: list) -> "FlottaBici":
        flotta = cls(citta)
        for d in dati:
            tipo = d.get("tipo", "classica")
            if tipo == "classica":
                b = BiciclettaClassica(d["id"], d["stazione"], d["km"], d.get("taglia", "M"))
            elif tipo == "elettrica":
                b = BiciclettaElettrica(d["id"], d["stazione"], d["km"], d.get("batteria", 100))
            else: 
                b = Bicicletta(d["id"], d["tipo"], d["stazione"], d["km"])
            flotta.aggiungi(b)
        return flotta

                