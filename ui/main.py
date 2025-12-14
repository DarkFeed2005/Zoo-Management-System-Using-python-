import customtkinter as ctk
from core.rbac import can
from ui.frames.animals_frame import AnimalsFrame
from ui.frames.ticket_frame import TicketsFrame
from ui.frames.enclosures_frame import EnclosuresFrame
from ui.frames.users_frame import UsersFrame


class MainApp(ctk.CTk):
    def __init__(self, session):
        super().__init__()
        self.session = session
        self.title(f"Zoo Manager - {session['username']} ({session['role']})")
        self.geometry("1100x700")
        # Sidebar
        sidebar = ctk.CTkFrame(self, width=200)
        sidebar.pack(side="left", fill="y")
        self.content = ctk.CTkFrame(self)
        self.content.pack(side="right", fill="both", expand=True)

        def add_btn(text, frame_cls, perm=None):
            if perm and not can(session["role"], perm):
                return
            btn = ctk.CTkButton(sidebar, text=text, command=lambda: self._load(frame_cls))
            btn.pack(padx=10, pady=6, fill="x")

        add_btn("Animals", AnimalsFrame, "animals:view")
        add_btn("Enclosures", EnclosuresFrame, "enclosures:view")
        add_btn("Tickets", TicketsFrame, "tickets:*")
        add_btn("Users", UsersFrame, "*")  # admin only by RBAC map

        self._load(AnimalsFrame)

    def _load(self, frame_cls):
        for w in self.content.winfo_children():
            w.destroy()
        frame = frame_cls(self.content, self.session)
        frame.pack(fill="both", expand=True)