"""
Animals management view with CRUD operations
"""

import customtkinter as ctk
from tkinter import messagebox
from config.database import Database
from services.rbac_service import RBACService
from datetime import datetime

class AnimalsView(ctk.CTkFrame):
    def __init__(self, parent, user):
        super().__init__(parent, fg_color="transparent")
        self.user = user
        self.db = Database()
        self.selected_animal = None
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        # Check permissions
        self.can_create = RBACService.has_permission(user['role_name'], 'animals', 'create')
        self.can_update = RBACService.has_permission(user['role_name'], 'animals', 'update')
        self.can_delete = RBACService.has_permission(user['role_name'], 'animals', 'delete')
        
        self.create_ui()
        self.load_animals()
    
    def create_ui(self):
        """Create the user interface"""
        # Header
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.grid(row=0, column=0, sticky="ew", pady=(0, 20))
        header_frame.grid_columnconfigure(1, weight=1)
        
        title = ctk.CTkLabel(
            header_frame,
            text="🦁 Animals Management",
            font=ctk.CTkFont(size=28, weight="bold")
        )
        title.grid(row=0, column=0, sticky="w")
        
        # Action buttons
        if self.can_create:
            add_btn = ctk.CTkButton(
                header_frame,
                text="➕ Add Animal",
                command=self.show_add_dialog,
                width=140,
                height=35
            )
            add_btn.grid(row=0, column=2, padx=5)
        
        refresh_btn = ctk.CTkButton(
            header_frame,
            text="🔄 Refresh",
            command=self.load_animals,
            width=120,
            height=35,
            fg_color="gray40",
            hover_color="gray30"
        )
        refresh_btn.grid(row=0, column=3, padx=5)
        
        # Content area with scrollable frame
        self.content_frame = ctk.CTkScrollableFrame(self)
        self.content_frame.grid(row=1, column=0, sticky="nsew")
        self.content_frame.grid_columnconfigure(0, weight=1)
    
    def load_animals(self):
        """Load and display animals"""
        # Clear existing content
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        try:
            query = """
                SELECT a.*, e.name as enclosure_name
                FROM animals a
                LEFT JOIN enclosures e ON a.enclosure_id = e.id
                ORDER BY a.id DESC
            """
            animals = self.db.execute_query(query, fetch=True)
            
            if not animals:
                no_data = ctk.CTkLabel(
                    self.content_frame,
                    text="No animals found. Add your first animal!",
                    font=ctk.CTkFont(size=16),
                    text_color="gray"
                )
                no_data.grid(row=0, column=0, pady=50)
                return
            
            # Create animal cards
            for idx, animal in enumerate(animals):
                self.create_animal_card(animal, idx)
        
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load animals: {e}")
    
    def create_animal_card(self, animal, idx):
        """Create a card for each animal"""
        card = ctk.CTkFrame(self.content_frame)
        card.grid(row=idx, column=0, sticky="ew", pady=10, padx=10)
        card.grid_columnconfigure(1, weight=1)
        
        # Animal icon/emoji based on species
        icon = "🦁" if "lion" in animal['species'].lower() else \
               "🐘" if "elephant" in animal['species'].lower() else \
               "🦒" if "giraffe" in animal['species'].lower() else \
               "🐻" if "bear" in animal['species'].lower() else \
               "🦓" if "zebra" in animal['species'].lower() else "🐾"
        
        icon_label = ctk.CTkLabel(
            card,
            text=icon,
            font=ctk.CTkFont(size=48)
        )
        icon_label.grid(row=0, column=0, rowspan=3, padx=20, pady=20)
        
        # Animal info
        info_frame = ctk.CTkFrame(card, fg_color="transparent")
        info_frame.grid(row=0, column=1, sticky="w", padx=10, pady=10)
        
        name_label = ctk.CTkLabel(
            info_frame,
            text=f"{animal['name']} (#{animal['tag_id']})",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        name_label.pack(anchor="w")
        
        species_label = ctk.CTkLabel(
            info_frame,
            text=f"Species: {animal['species']} | Sex: {animal['sex']}",
            font=ctk.CTkFont(size=13),
            text_color="gray"
        )
        species_label.pack(anchor="w")
        
        enclosure_text = animal['enclosure_name'] if animal['enclosure_name'] else "No enclosure"
        enclosure_label = ctk.CTkLabel(
            info_frame,
            text=f"📍 {enclosure_text} | Health: {animal['health_status']}",
            font=ctk.CTkFont(size=13),
            text_color="gray"
        )
        enclosure_label.pack(anchor="w")
        
        # Action buttons
        button_frame = ctk.CTkFrame(card, fg_color="transparent")
        button_frame.grid(row=0, column=2, padx=10, pady=10)
        
        view_btn = ctk.CTkButton(
            button_frame,
            text="👁️ View",
            command=lambda a=animal: self.view_animal(a),
            width=80,
            height=30
        )
        view_btn.pack(side="left", padx=2)
        
        if self.can_update:
            edit_btn = ctk.CTkButton(
                button_frame,
                text="✏️ Edit",
                command=lambda a=animal: self.show_edit_dialog(a),
                width=80,
                height=30,
                fg_color="gray40",
                hover_color="gray30"
            )
            edit_btn.pack(side="left", padx=2)
        
        if self.can_delete:
            delete_btn = ctk.CTkButton(
                button_frame,
                text="🗑️",
                command=lambda a=animal: self.delete_animal(a),
                width=40,
                height=30,
                fg_color="#e74c3c",
                hover_color="#c0392b"
            )
            delete_btn.pack(side="left", padx=2)
    
    def view_animal(self, animal):
        """View detailed animal information"""
        dialog = ctk.CTkToplevel(self)
        dialog.title(f"Animal Details - {animal['name']}")
        dialog.geometry("500x600")
        dialog.transient(self)
        dialog.grab_set()
        
        # Center dialog
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (500 // 2)
        y = (dialog.winfo_screenheight() // 2) - (600 // 2)
        dialog.geometry(f"500x600+{x}+{y}")
        
        # Content
        content = ctk.CTkScrollableFrame(dialog)
        content.pack(fill="both", expand=True, padx=20, pady=20)
        
        fields = [
            ("Tag ID", animal['tag_id']),
            ("Name", animal['name']),
            ("Species", animal['species']),
            ("Sex", animal['sex']),
            ("Date of Birth", animal['dob']),
            ("Health Status", animal['health_status']),
            ("Last Checkup", animal['last_checkup']),
            ("Notes", animal['notes'] or "No notes")
        ]
        
        for label, value in fields:
            frame = ctk.CTkFrame(content, fg_color="transparent")
            frame.pack(fill="x", pady=5)
            
            ctk.CTkLabel(
                frame,
                text=f"{label}:",
                font=ctk.CTkFont(size=13, weight="bold")
            ).pack(anchor="w")
            
            ctk.CTkLabel(
                frame,
                text=str(value),
                font=ctk.CTkFont(size=13),
                text_color="gray"
            ).pack(anchor="w")
    
    def show_add_dialog(self):
        """Show dialog to add new animal"""
        self.show_animal_dialog(None)
    
    def show_edit_dialog(self, animal):
        """Show dialog to edit animal"""
        self.show_animal_dialog(animal)
    
    def show_animal_dialog(self, animal=None):
        """Show add/edit animal dialog"""
        is_edit = animal is not None
        
        dialog = ctk.CTkToplevel(self)
        dialog.title(f"{'Edit' if is_edit else 'Add'} Animal")
        dialog.geometry("550x700")
        dialog.transient(self)
        dialog.grab_set()
        
        # Center dialog
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (550 // 2)
        y = (dialog.winfo_screenheight() // 2) - (700 // 2)
        dialog.geometry(f"550x700+{x}+{y}")
        
        # Form
        form = ctk.CTkScrollableFrame(dialog)
        form.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Form fields
        entries = {}
        
        fields = [
            ("tag_id", "Tag ID", "text"),
            ("name", "Name", "text"),
            ("species", "Species", "text"),
            ("sex", "Sex", "option"),
            ("dob", "Date of Birth (YYYY-MM-DD)", "text"),
            ("health_status", "Health Status", "text"),
            ("last_checkup", "Last Checkup (YYYY-MM-DD)", "text"),
            ("notes", "Notes", "textbox"),
        ]
        
        for field_name, label, field_type in fields:
            ctk.CTkLabel(
                form,
                text=label,
                font=ctk.CTkFont(size=13, weight="bold")
            ).pack(anchor="w", pady=(10, 5))
            
            if field_type == "option" and field_name == "sex":
                entry = ctk.CTkOptionMenu(
                    form,
                    values=["Male", "Female", "Unknown"],
                    height=35
                )
                if animal:
                    entry.set(animal[field_name])
            elif field_type == "textbox":
                entry = ctk.CTkTextbox(form, height=100)
                if animal and animal[field_name]:
                    entry.insert("1.0", animal[field_name])
            else:
                entry = ctk.CTkEntry(form, height=35)
                if animal and animal[field_name]:
                    entry.insert(0, str(animal[field_name]))
            
            entry.pack(fill="x", pady=(0, 5))
            entries[field_name] = entry
        
        # Buttons
        button_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        button_frame.pack(fill="x", padx=20, pady=(0, 20))
        
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
            command=lambda: self.save_animal(entries, animal, dialog),
            width=120
        )
        save_btn.pack(side="right", padx=5)
    
    def save_animal(self, entries, animal, dialog):
        """Save animal data"""
        try:
            # Get values
            data = {}
            for key, widget in entries.items():
                if isinstance(widget, ctk.CTkTextbox):
                    data[key] = widget.get("1.0", "end-1c").strip()
                elif isinstance(widget, ctk.CTkOptionMenu):
                    data[key] = widget.get()
                else:
                    data[key] = widget.get().strip()
            
            # Validate
            if not data['tag_id'] or not data['name'] or not data['species']:
                messagebox.showerror("Error", "Tag ID, Name, and Species are required")
                return
            
            if animal:  # Update
                query = """
                    UPDATE animals SET
                        tag_id = %s, name = %s, species = %s, sex = %s,
                        dob = %s, health_status = %s, last_checkup = %s, notes = %s
                    WHERE id = %s
                """
                params = (
                    data['tag_id'], data['name'], data['species'], data['sex'],
                    data['dob'] or None, data['health_status'], data['last_checkup'] or None,
                    data['notes'], animal['id']
                )
            else:  # Insert
                query = """
                    INSERT INTO animals (tag_id, name, species, sex, dob, health_status, last_checkup, notes)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """
                params = (
                    data['tag_id'], data['name'], data['species'], data['sex'],
                    data['dob'] or None, data['health_status'], data['last_checkup'] or None,
                    data['notes']
                )
            
            self.db.execute_query(query, params)
            
            messagebox.showinfo("Success", f"Animal {'updated' if animal else 'added'} successfully")
            dialog.destroy()
            self.load_animals()
        
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save animal: {e}")
    
    def delete_animal(self, animal):
        """Delete an animal"""
        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete {animal['name']}?"):
            try:
                self.db.execute_query("DELETE FROM animals WHERE id = %s", (animal['id'],))
                messagebox.showinfo("Success", "Animal deleted successfully")
                self.load_animals()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete animal: {e}")