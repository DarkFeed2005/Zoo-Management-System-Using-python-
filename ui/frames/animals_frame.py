import customtkinter as ctk
from services.animals import list_animals, update_health

class AnimalsFrame(ctk.CTkFrame):
    def __init__(self, master, session):
        super().__init__(master)
        self.session = session
        ctk.CTkLabel(self, text="Animals").pack(anchor="w", padx=12, pady=8)
        self.table = ctk.CTkTextbox(self, width=800, height=400)
        self.table.pack(padx=12, pady=8, fill="both", expand=True)
        self._load()

        control = ctk.CTkFrame(self)
        control.pack(fill="x", padx=12, pady=8)
        ctk.CTkLabel(control, text="Animal ID").pack(side="left", padx=6)
        self.animal_id = ctk.CTkEntry(control, width=120)
        self.animal_id.pack(side="left")
        ctk.CTkLabel(control, text="New health").pack(side="left", padx=6)
        self.health = ctk.CTkEntry(control, width=160)
        self.health.pack(side="left")
        ctk.CTkButton(control, text="Update", command=self._update).pack(side="left", padx=8)

    def _load(self):
        rows = list_animals()
        self.table.delete("1.0", "end")
        for r in rows:
            self.table.insert("end", f"#{r['id']} {r['name']} [{r['species']}] - {r['health_status']} - Enclosure: {r.get('enclosure_name')}\n")

    def _update(self):
        try:
            aid = int(self.animal_id.get())
        except ValueError:
            return
        update_health(self.session["id"], aid, self.health.get())
        self._load()