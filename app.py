import customtkinter as ctk
from ui.login import LoginWindow
from ui.main import MainApp

def run():
    def on_success(session):
        app = MainApp(session)
        app.mainloop()

    login = LoginWindow(on_success)
    login.mainloop()

if __name__ == "__main__":
    ctk.set_appearance_mode("system")
    ctk.set_default_color_theme("blue")
    run()