import customtkinter as ctk
from core.auth import login

class LoginWindow(ctk.CTk):
    def __init__(self, on_success):
        super().__init__()
        self.title("Zoo Manager - Login")
        self.geometry("400x280")
        ctk.CTkLabel(self, text="Username").pack(pady=5)
        self.username = ctk.CTkEntry(self)
        self.username.pack(pady=5)
        ctk.CTkLabel(self, text="Password").pack(pady=5)
        self.password = ctk.CTkEntry(self, show="*")
        self.password.pack(pady=5)
        self.msg = ctk.CTkLabel(self, text="")
        self.msg.pack(pady=5)
        ctk.CTkButton(self, text="Login", command=self._do_login).pack(pady=10)
        self.on_success = on_success

    def _do_login(self):
        user = login(self.username.get(), self.password.get())
        if user:
            self.on_success(user)
            self.destroy()
        else:
            self.msg.configure(text="Invalid credentials", text_color="red")