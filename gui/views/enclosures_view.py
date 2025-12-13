"""
Enclosures management view
"""

import customtkinter as ctk
from tkinter import messagebox
from config.database import Database
from services.rbac_service import RBACService

class EnclosuresView(ctk.CTkFrame):
    def __init__(self, parent, user):
        super().__init__(parent, fg_color="transparent")
        self.user = user
        self.db = Database()
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        self.can_create = RBACService.has_permission(user['role_name'], 'enclosures', 'create')
        self.can_update = RBACService.has_permission(user['role_name'], 'enclosures', 'update')
        self.can_delete = RBACService.has_permission(user['role_name'], 'enclosures', 'delete')
        
        self.create_ui()
        self.load_enclosures()
    
    def create_ui(self):
        """Create UI"""
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.grid(row=0, column=0, sticky="ew", pady=(0, 20))
        header_frame.grid_columnconfigure(1, weight=1)
        
        title = ctk.CTkLabel(
            header_frame,
            text="🏛️ Enclosures Management",
            font=ctk.CTkFont(size=28, weight="bold")
        )
        title.grid(row=0, column=0, sticky="w")
        
        if self.can_create:
            add_btn = ctk.CTkButton(
                header_frame,
                text="➕ Add Enclosure",
                command=self.show_add_dialog,
                width=150,
                height=35
            )
            add_btn.grid(row=0, column=2, padx=5)
        
        refresh_btn = ctk.CTkButton(
            header_frame,
            text="🔄 Refresh",
            command=self.load_enclosures,
            width=120,
            height=35,
            fg_color="gray40",
            hover_color="gray30"
        )
        refresh_btn.grid(row=0, column=3, padx=5)
        
        self.content_frame = ctk.CTkScrollableFrame(self)
        self.content_frame.grid(row=1, column=0, sticky="nsew")
        self.content_frame.grid_columnconfigure(0, weight=1)
    
    def load_enclosures(self):
        """Load enclosures"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        try:
            query = """
                SELECT e.*, 
                       COUNT(a.id) as animal_count
                FROM enclosures e
                LEFT JOIN animals a ON e.id = a.enclosure_id
                GROUP BY e.id
                ORDER BY e.id DESC
            """
            enclosures = self.db.execute_query(query, fetch=True)
            
            if not enclosures:
                no_data = ctk.CTkLabel(
                    self.content_frame,
                    text="No enclosures found. Add your first enclosure!",
                    font=ctk.CTkFont(size=16),
                    text_color="gray"
                )
                no_data.grid(row=0, column=0, pady=50)
                return
            
            for idx, enclosure in enumerate(enclosures):
                self.create_enclosure_card(enclosure, idx)
        
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load enclosures: {e}")
    
    def create_enclosure_card(self, enclosure, idx):
        """Create enclosure card"""
        card = ctk.CTkFrame(self.content_frame)
        card.grid(row=idx, column=0, sticky="ew", pady=10, padx=10)
        card.grid_columnconfigure(1, weight=1)
        
        icon_label = ctk.CTkLabel(
            card,
            text="🏛️",
            font=ctk.CTkFont(size=48)
        )
        icon_label.grid(row=0, column=0, rowspan=2, padx=20, pady=20)
        
        info_frame = ctk.CTkFrame(card, fg_color="transparent")
        info_frame.grid(row=0, column=1, sticky="w", padx=10, pady=10)
        
        name_label = ctk.CTkLabel(
            info_frame,
            text=enclosure['name'],
            font=ctk.CTkFont(size=18, weight="bold")
        )
        name_label.pack(anchor="w")
        
        details = f"Type: {enclosure['type']} | Capacity: {enclosure['capacity']} | Animals: {enclosure['animal_count']}"
        details_label = ctk.CTkLabel(
            info_frame,
            text=details,
            font=ctk.CTkFont(size=13),
            text_color="gray"
        )
        details_label.pack(anchor="w")
        
        if enclosure['location']:
            location_label = ctk.CTkLabel(
                info_frame,
                text=f"📍 {enclosure['location']}",
                font=ctk.CTkFont(size=13),
                text_color="gray"
            )
            location_label.pack(anchor="w")
        
        button_frame = ctk.CTkFrame(card, fg_color="transparent")
        button_frame.grid(row=0, column=2, padx=10, pady=10)
        
        if self.can_update:
            edit_btn = ctk.CTkButton(
                button_frame,
                text="✏️ Edit",
                command=lambda e=enclosure: self.show_edit_dialog(e),
                width=80,
                height=30
            )
            edit_btn.pack(side="left", padx=2)
        
        if self.can_delete:
            delete_btn = ctk.CTkButton(
                button_frame,
                text="🗑️",
                command=lambda e=enclosure: self.delete_enclosure(e),
                width=40,
                height=30,
                fg_color="#e74c3c",
                hover_color="#c0392b"
            )
            delete_btn.pack(side="left", padx=2)
    
    def show_add_dialog(self):
        """Show add dialog"""
        self.show_enclosure_dialog(None)
    
    def show_edit_dialog(self, enclosure):
        """Show edit dialog"""
        self.show_enclosure_dialog(enclosure)
    
    def show_enclosure_dialog(self, enclosure=None):
        """Show add/edit dialog"""
        is_edit = enclosure is not None
        
        dialog = ctk.CTkToplevel(self)
        dialog.title(f"{'Edit' if is_edit else 'Add'} Enclosure")
        dialog.geometry("500x550")
        dialog.transient(self)
        dialog.grab_set()
        
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (500 // 2)
        y = (dialog.winfo_screenheight() // 2) - (550 // 2)
        dialog.geometry(f"500x550+{x}+{y}")
        
        form = ctk.CTkFrame(dialog)
        form.pack(fill="both", expand=True, padx=20, pady=20)
        
        entries = {}
        fields = [
            ("name", "Name"),
            ("type", "Type"),
            ("capacity", "Capacity"),
            ("location", "Location"),
            ("notes", "Notes")
        ]
        
        for field_name, label in fields:
            ctk.CTkLabel(
                form,
                text=label,
                font=ctk.CTkFont(size=13, weight="bold")
            ).pack(anchor="w", pady=(10, 5))
            
            if field_name == "notes":
                entry = ctk.CTkTextbox(form, height=100)
                if enclosure and enclosure[field_name]:
                    entry.insert("1.0", enclosure[field_name])
            else:
                entry = ctk.CTkEntry(form, height=35)
                if enclosure and enclosure[field_name]:
                    entry.insert(0, str(enclosure[field_name]))
            
            entry.pack(fill="x", pady=(0, 5))
            entries[field_name] = entry
        
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
            command=lambda: self.save_enclosure(entries, enclosure, dialog),
            width=120
        )
        save_btn.pack(side="right", padx=5)
    
    def save_enclosure(self, entries, enclosure, dialog):
        """Save enclosure"""
        try:
            data = {}
            for key, widget in entries.items():
                if isinstance(widget, ctk.CTkTextbox):
                    data[key] = widget.get("1.0", "end-1c").strip()
                else:
                    data[key] = widget.get().strip()
            
            if not data['name']:
                messagebox.showerror("Error", "Name is required")
                return
            
            if enclosure:
                query = """
                    UPDATE enclosures SET
                        name = %s, type = %s, capacity = %s, location = %s, notes = %s
                    WHERE id = %s
                """
                params = (data['name'], data['type'], data['capacity'] or 0, 
                         data['location'], data['notes'], enclosure['id'])
            else:
                query = """
                    INSERT INTO enclosures (name, type, capacity, location, notes)
                    VALUES (%s, %s, %s, %s, %s)
                """
                params = (data['name'], data['type'], data['capacity'] or 0, 
                         data['location'], data['notes'])
            
            self.db.execute_query(query, params)
            
            messagebox.showinfo("Success", f"Enclosure {'updated' if enclosure else 'added'} successfully")
            dialog.destroy()
            self.load_enclosures()
        
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save enclosure: {e}")
    
    def delete_enclosure(self, enclosure):
        """Delete enclosure"""
        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete {enclosure['name']}?"):
            try:
                self.db.execute_query("DELETE FROM enclosures WHERE id = %s", (enclosure['id'],))
                messagebox.showinfo("Success", "Enclosure deleted successfully")
                self.load_enclosures()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete enclosure: {e}")