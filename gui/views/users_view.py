"""
Users management view (Admin only)
"""

import customtkinter as ctk
from tkinter import messagebox
from config.database import Database
from services.auth_service import AuthService

class UsersView(ctk.CTkFrame):
    def __init__(self, parent, user):
        super().__init__(parent, fg_color="transparent")
        self.user = user
        self.db = Database()
        self.auth_service = AuthService()
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        self.create_ui()
        self.load_users()
    
    def create_ui(self):
        """Create UI"""
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.grid(row=0, column=0, sticky="ew", pady=(0, 20))
        header_frame.grid_columnconfigure(1, weight=1)
        
        title = ctk.CTkLabel(
            header_frame,
            text="👥 Users Management",
            font=ctk.CTkFont(size=28, weight="bold")
        )
        title.grid(row=0, column=0, sticky="w")
        
        add_btn = ctk.CTkButton(
            header_frame,
            text="➕ Add User",
            command=self.show_add_dialog,
            width=130,
            height=35
        )
        add_btn.grid(row=0, column=2, padx=5)
        
        refresh_btn = ctk.CTkButton(
            header_frame,
            text="🔄 Refresh",
            command=self.load_users,
            width=120,
            height=35,
            fg_color="gray40",
            hover_color="gray30"
        )
        refresh_btn.grid(row=0, column=3, padx=5)
        
        self.content_frame = ctk.CTkScrollableFrame(self)
        self.content_frame.grid(row=1, column=0, sticky="nsew")
        self.content_frame.grid_columnconfigure(0, weight=1)
    
    def load_users(self):
        """Load users"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        try:
            query = """
                SELECT u.*, r.name as role_name
                FROM users u
                JOIN roles r ON u.role_id = r.id
                ORDER BY u.id
            """
            users = self.db.execute_query(query, fetch=True)
            
            if not users:
                no_data = ctk.CTkLabel(
                    self.content_frame,
                    text="No users found.",
                    font=ctk.CTkFont(size=16),
                    text_color="gray"
                )
                no_data.grid(row=0, column=0, pady=50)
                return
            
            for idx, user_data in enumerate(users):
                self.create_user_card(user_data, idx)
        
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load users: {e}")
    
    def create_user_card(self, user_data, idx):
        """Create user card"""
        card = ctk.CTkFrame(self.content_frame)
        card.grid(row=idx, column=0, sticky="ew", pady=10, padx=10)
        card.grid_columnconfigure(1, weight=1)
        
        icon_label = ctk.CTkLabel(
            card,
            text="👤",
            font=ctk.CTkFont(size=40)
        )
        icon_label.grid(row=0, column=0, rowspan=2, padx=20, pady=20)
        
        info_frame = ctk.CTkFrame(card, fg_color="transparent")
        info_frame.grid(row=0, column=1, sticky="w", padx=10, pady=10)
        
        username_label = ctk.CTkLabel(
            info_frame,
            text=user_data['username'],
            font=ctk.CTkFont(size=16, weight="bold")
        )
        username_label.pack(anchor="w")
        
        role_label = ctk.CTkLabel(
            info_frame,
            text=f"Role: {user_data['role_name'].capitalize()}",
            font=ctk.CTkFont(size=13),
            text_color="gray"
        )
        role_label.pack(anchor="w")
        
        status = "Active" if user_data['is_active'] else "Inactive"
        status_color = "#2ecc71" if user_data['is_active'] else "#e74c3c"
        status_label = ctk.CTkLabel(
            info_frame,
            text=f"Status: {status}",
            font=ctk.CTkFont(size=13),
            text_color=status_color
        )
        status_label.pack(anchor="w")
        
        button_frame = ctk.CTkFrame(card, fg_color="transparent")
        button_frame.grid(row=0, column=2, padx=10, pady=10)
        
        edit_btn = ctk.CTkButton(
            button_frame,
            text="✏️ Edit",
            command=lambda u=user_data: self.show_edit_dialog(u),
            width=80,
            height=30
        )
        edit_btn.pack(side="left", padx=2)
        
        if user_data['id'] != self.user['id']:  # Can't delete yourself
            delete_btn = ctk.CTkButton(
                button_frame,
                text="🗑️",
                command=lambda u=user_data: self.delete_user(u),
                width=40,
                height=30,
                fg_color="#e74c3c",
                hover_color="#c0392b"
            )
            delete_btn.pack(side="left", padx=2)
    
    def show_add_dialog(self):
        """Show add dialog"""
        self.show_user_dialog(None)
    
    def show_edit_dialog(self, user_data):
        """Show edit dialog"""
        self.show_user_dialog(user_data)
    
    def show_user_dialog(self, user_data=None):
        """Show add/edit user dialog"""
        is_edit = user_data is not None
        
        dialog = ctk.CTkToplevel(self)
        dialog.title(f"{'Edit' if is_edit else 'Add'} User")
        dialog.geometry("450x500")
        dialog.transient(self)
        dialog.grab_set()
        
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (450 // 2)
        y = (dialog.winfo_screenheight() // 2) - (500 // 2)
        dialog.geometry(f"450x500+{x}+{y}")
        
        form = ctk.CTkFrame(dialog)
        form.pack(fill="both", expand=True, padx=20, pady=20)
        
        entries = {}
        
        # Username
        ctk.CTkLabel(
            form,
            text="Username",
            font=ctk.CTkFont(size=13, weight="bold")
        ).pack(anchor="w", pady=(10, 5))
        
        username_entry = ctk.CTkEntry(form, height=35)
        if user_data:
            username_entry.insert(0, user_data['username'])
            username_entry.configure(state="disabled")  # Can't change username
        username_entry.pack(fill="x", pady=(0, 15))
        entries['username'] = username_entry
        
        # Password (only for new users or if changing)
        if not is_edit:
            ctk.CTkLabel(
                form,
                text="Password",
                font=ctk.CTkFont(size=13, weight="bold")
            ).pack(anchor="w", pady=(0, 5))
            
            password_entry = ctk.CTkEntry(form, height=35, show="●")
            password_entry.pack(fill="x", pady=(0, 15))
            entries['password'] = password_entry
        else:
            ctk.CTkLabel(
                form,
                text="New Password (leave empty to keep current)",
                font=ctk.CTkFont(size=13, weight="bold")
            ).pack(anchor="w", pady=(0, 5))
            
            password_entry = ctk.CTkEntry(form, height=35, show="●")
            password_entry.pack(fill="x", pady=(0, 15))
            entries['password'] = password_entry
        
        # Role
        ctk.CTkLabel(
            form,
            text="Role",
            font=ctk.CTkFont(size=13, weight="bold")
        ).pack(anchor="w", pady=(0, 5))
        
        roles = self.db.execute_query("SELECT * FROM roles ORDER BY name", fetch=True)
        role_options = [r['name'] for r in roles]
        role_map = {r['name']: r['id'] for r in roles}
        
        role_menu = ctk.CTkOptionMenu(form, values=role_options, height=35)
        if user_data:
            role_menu.set(user_data['role_name'])
        role_menu.pack(fill="x", pady=(0, 15))
        entries['role'] = (role_menu, role_map)
        
        # Active status
        ctk.CTkLabel(
            form,
            text="Status",
            font=ctk.CTkFont(size=13, weight="bold")
        ).pack(anchor="w", pady=(0, 5))
        
        active_var = ctk.StringVar(value="Active" if not user_data or user_data['is_active'] else "Inactive")
        active_menu = ctk.CTkOptionMenu(form, variable=active_var, values=["Active", "Inactive"], height=35)
        active_menu.pack(fill="x", pady=(0, 15))
        entries['active'] = active_var
        
        # Buttons
        button_frame = ctk.CTkFrame(form, fg_color="transparent")
        button_frame.pack(fill="x", pady=(20, 0))
        
        cancel_btn = ctk.CTkButton(
            button_frame,
            text="Cancel",
            command=dialog.destroy,
            fg_color="gray40",
            hover_color="gray30",
            width=120
        )
        cancel_btn.pack(side="right", padx=5)
        
        save_btn = ctk.CTkButton(
            button_frame,
            text="Save",
            command=lambda: self.save_user(entries, user_data, dialog),
            width=120
        )
        save_btn.pack(side="right", padx=5)
    
    def save_user(self, entries, user_data, dialog):
        """Save user"""
        try:
            username = entries['username'].get().strip()
            password = entries['password'].get()
            role_menu, role_map = entries['role']
            role_name = role_menu.get()
            role_id = role_map[role_name]
            is_active = 1 if entries['active'].get() == "Active" else 0
            
            if not username:
                messagebox.showerror("Error", "Username is required")
                return
            
            if user_data:  # Update
                if password:  # If password provided, update it
                    password_hash = self.auth_service.hash_password(password)
                    query = """
                        UPDATE users SET role_id = %s, is_active = %s, password_hash = %s
                        WHERE id = %s
                    """
                    params = (role_id, is_active, password_hash, user_data['id'])
                else:  # Keep existing password
                    query = """
                        UPDATE users SET role_id = %s, is_active = %s
                        WHERE id = %s
                    """
                    params = (role_id, is_active, user_data['id'])
            else:  # Insert
                if not password:
                    messagebox.showerror("Error", "Password is required for new users")
                    return
                
                password_hash = self.auth_service.hash_password(password)
                query = """
                    INSERT INTO users (username, password_hash, role_id, is_active)
                    VALUES (%s, %s, %s, %s)
                """
                params = (username, password_hash, role_id, is_active)
            
            self.db.execute_query(query, params)
            
            messagebox.showinfo("Success", f"User {'updated' if user_data else 'added'} successfully")
            dialog.destroy()
            self.load_users()
        
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save user: {e}")
    
    def delete_user(self, user_data):
        """Delete user"""
        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete user '{user_data['username']}'?"):
            try:
                self.db.execute_query("DELETE FROM users WHERE id = %s", (user_data['id'],))
                messagebox.showinfo("Success", "User deleted successfully")
                self.load_users()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete user: {e}")