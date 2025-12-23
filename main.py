from customtkinter import *
from tkinter import messagebox
import sys
import subprocess
import mysql.connector


# ---------- Main Window ----------
app = CTk()
app.title("Zoo Management System")
app.geometry("1200x700+300+100")
app.resizable(True, True)

# ---------- Top Bar ----------
topbar = CTkFrame(app, height=50, fg_color="#eeeeee")
topbar.pack(side="top", fill="x")

# Role and username passed from login.py
role = sys.argv[1] if len(sys.argv) > 1 else "guest"
username = sys.argv[2] if len(sys.argv) > 2 else "Unknown User"

# Show username in top-right corner
user_label = CTkLabel(topbar, text=f"👤 {username} ({role.title()})",
                      font=("Arial Bold", 14), text_color="#333333")
user_label.pack(side="right", padx=20, pady=10)

# ---------- Logout Button ----------
def logout():
    app.destroy()
    subprocess.Popen([sys.executable, "login.py"])

logout_btn = CTkButton(topbar, text="Logout", fg_color="#E44982",
                       text_color="white", width=80, command=logout)
logout_btn.pack(side="right", padx=10, pady=10)

# ---------- Theme Toggle ----------
def toggle_theme():
    current = get_appearance_mode()
    if current == "Light":
        set_appearance_mode("Dark")
    else:
        set_appearance_mode("Light")

theme_btn = CTkButton(topbar, text="Toggle Theme", fg_color="#601E88",
                      text_color="white", width=120, command=toggle_theme)
theme_btn.pack(side="right", padx=10, pady=10)

# ---------- Sidebar ----------
sidebar = CTkFrame(app, width=220, fg_color="#601E88")
sidebar.pack(side="left", fill="y")

CTkLabel(sidebar, text="Zoo System", text_color="white",
         font=("Arial Bold", 22)).pack(pady=25)

# ---------- Content Frame ----------
content = CTkFrame(app, fg_color="#f5f5f5")
content.pack(side="right", expand=True, fill="both")

# ---------- Utility ----------
def clear_content():
    for widget in content.winfo_children():
        widget.destroy()

# ---------- Module Functions ----------
def show_dashboard():
    clear_content()
    CTkLabel(content, text=f"📊 {role.title()} Dashboard",
             font=("Arial Bold", 26), text_color="#333333").pack(pady=30)

    if role == "admin":
        CTkLabel(content, text="Manage users, view audit logs, oversee operations",
                 font=("Arial", 14)).pack(pady=10)
    elif role == "zookeeper":
        CTkLabel(content, text="Track animals, feeding schedules, and health records",
                 font=("Arial", 14)).pack(pady=10)
    elif role == "ticketing":
        CTkLabel(content, text="Sell tickets, view sales, and manage pricing",
                 font=("Arial", 14)).pack(pady=10)
    else:
        CTkLabel(content, text="No role assigned", font=("Arial", 14)).pack(pady=10)

        # ---------- DB Connection ----------
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",   
        database="zoo"
    )


# ---------- User Management ----------
def show_users():
    clear_content()
    CTkLabel(content, text="👥 User Management", font=("Arial Bold", 22),
             text_color="#333333").pack(pady=20)

    # Only Admins can see this
    if role != "admin":
        CTkLabel(content, text="Access denied. Only Admins can view users.",
                 font=("Arial", 14), text_color="red").pack(pady=10)
        return

    # Frame for table
    table_frame = CTkScrollableFrame(content, fg_color="#A8EE8A")
    table_frame.pack(fill="both", expand=True, padx=20, pady=10)

    # Table header
    header = CTkFrame(table_frame, fg_color="#020202")
    header.pack(fill="x")
    for i, h in enumerate(["ID", "Username", "Email", "Role", "Active", "Last Login"]):
        CTkLabel(header, text=h, font=("Arial Bold", 12)).grid(row=0, column=i, padx=8, pady=6, sticky="w")

    # Fetch users from DB
    try:
        conn = get_db_connection()
        cur = conn.cursor(dictionary=True)
        cur.execute("SELECT id, username, email, role, is_active, last_login FROM users ORDER BY created_at DESC")
        rows = cur.fetchall()

        for r in rows:
            rowf = CTkFrame(table_frame, fg_color="#4ED988")
            rowf.pack(fill="x", padx=2, pady=2)

            CTkLabel(rowf, text=str(r["id"])).grid(row=0, column=0, padx=8, pady=6, sticky="w")
            CTkLabel(rowf, text=r["username"]).grid(row=0, column=1, padx=8, pady=6, sticky="w")
            CTkLabel(rowf, text=r.get("email") or "-").grid(row=0, column=2, padx=8, pady=6, sticky="w")
            CTkLabel(rowf, text=r["role"]).grid(row=0, column=3, padx=8, pady=6, sticky="w")
            CTkLabel(rowf, text="Yes" if r["is_active"] else "No").grid(row=0, column=4, padx=8, pady=6, sticky="w")
            CTkLabel(rowf, text=str(r["last_login"]) if r["last_login"] else "-").grid(row=0, column=5, padx=8, pady=6, sticky="w")

        cur.close()
        conn.close()

    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")


def show_animals():
    clear_content()
    CTkLabel(content, text="🦁 Animals Management", font=("Arial Bold", 22),
             text_color="#333333").pack(pady=20)

def show_enclosures():
    clear_content()
    CTkLabel(content, text="🏛️ Enclosures Management", font=("Arial Bold", 22),
             text_color="#333333").pack(pady=20)

def show_feeding():
    clear_content()
    CTkLabel(content, text="🍖 Feeding Schedules", font=("Arial Bold", 22),
             text_color="#333333").pack(pady=20)

def show_tickets():
    clear_content()
    CTkLabel(content, text="🎫 Ticket Sales", font=("Arial Bold", 22),
             text_color="#333333").pack(pady=20)

# ---------- Role-based Sidebar ----------
if role == "admin":
    CTkButton(sidebar, text="Dashboard", command=show_dashboard).pack(pady=10, fill="x")
    CTkButton(sidebar, text="Users", command=show_users).pack(pady=10, fill="x")
    CTkButton(sidebar, text="Animals", command=show_animals).pack(pady=10, fill="x")
    CTkButton(sidebar, text="Enclosures", command=show_enclosures).pack(pady=10, fill="x")
    CTkButton(sidebar, text="Feeding", command=show_feeding).pack(pady=10, fill="x")
    CTkButton(sidebar, text="Tickets", command=show_tickets).pack(pady=10, fill="x")

elif role == "zookeeper":
    CTkButton(sidebar, text="Dashboard", command=show_dashboard).pack(pady=10, fill="x")
    CTkButton(sidebar, text="Animals", command=show_animals).pack(pady=10, fill="x")
    CTkButton(sidebar, text="Feeding", command=show_feeding).pack(pady=10, fill="x")

elif role == "ticketing":
    CTkButton(sidebar, text="Dashboard", command=show_dashboard).pack(pady=10, fill="x")
    CTkButton(sidebar, text="Tickets", command=show_tickets).pack(pady=10, fill="x")

else:
    CTkLabel(sidebar, text="No role assigned", text_color="white").pack(pady=20)

# ---------- Auto-load Dashboard ----------
show_dashboard()

# ---------- Run App ----------
app.mainloop()