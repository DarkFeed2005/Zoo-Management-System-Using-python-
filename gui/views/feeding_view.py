"""
Feeding schedules management view
"""

import customtkinter as ctk
from tkinter import messagebox
from config.database import Database
from services.rbac_service import RBACService

class FeedingView(ctk.CTkFrame):
    def __init__(self, parent, user):
        super().__init__(parent, fg_color="transparent")
        self.user = user
        self.db = Database()
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        self.can_create = RBACService.has_permission(user['role_name'], 'feed_schedules', 'create')
        self.can_update = RBACService.has_permission(user['role_name'], 'feed_schedules', 'update')
        self.can_delete = RBACService.has_permission(user['role_name'], 'feed_schedules', 'delete')
        
        self.create_ui()
        self.load_schedules()
    
    def create_ui(self):
        """Create UI"""
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.grid(row=0, column=0, sticky="ew", pady=(0, 20))
        header_frame.grid_columnconfigure(1, weight=1)
        
        title = ctk.CTkLabel(
            header_frame,
            text="🍖 Feeding Schedules",
            font=ctk.CTkFont(size=28, weight="bold")
        )
        title.grid(row=0, column=0, sticky="w")
        
        if self.can_create:
            add_btn = ctk.CTkButton(
                header_frame,
                text="➕ Add Schedule",
                command=self.show_add_dialog,
                width=150,
                height=35
            )
            add_btn.grid(row=0, column=2, padx=5)
        
        refresh_btn = ctk.CTkButton(
            header_frame,
            text="🔄 Refresh",
            command=self.load_schedules,
            width=120,
            height=35,
            fg_color="gray40",
            hover_color="gray30"
        )
        refresh_btn.grid(row=0, column=3, padx=5)
        
        self.content_frame = ctk.CTkScrollableFrame(self)
        self.content_frame.grid(row=1, column=0, sticky="nsew")
        self.content_frame.grid_columnconfigure(0, weight=1)
    
    def load_schedules(self):
        """Load feeding schedules"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        try:
            query = """
                SELECT fs.*, a.name as animal_name, a.species
                FROM feed_schedules fs
                JOIN animals a ON fs.animal_id = a.id
                ORDER BY fs.schedule_time
            """
            schedules = self.db.execute_query(query, fetch=True)
            
            if not schedules:
                no_data = ctk.CTkLabel(
                    self.content_frame,
                    text="No feeding schedules found. Add your first schedule!",
                    font=ctk.CTkFont(size=16),
                    text_color="gray"
                )
                no_data.grid(row=0, column=0, pady=50)
                return
            
            for idx, schedule in enumerate(schedules):
                self.create_schedule_card(schedule, idx)
        
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load schedules: {e}")
    
    def create_schedule_card(self, schedule, idx):
        """Create schedule card"""
        card = ctk.CTkFrame(self.content_frame)
        card.grid(row=idx, column=0, sticky="ew", pady=10, padx=10)
        card.grid_columnconfigure(1, weight=1)
        
        icon_label = ctk.CTkLabel(
            card,
            text="🍖",
            font=ctk.CTkFont(size=40)
        )
        icon_label.grid(row=0, column=0, rowspan=2, padx=20, pady=20)
        
        info_frame = ctk.CTkFrame(card, fg_color="transparent")
        info_frame.grid(row=0, column=1, sticky="w", padx=10, pady=10)
        
        animal_label = ctk.CTkLabel(
            info_frame,
            text=f"{schedule['animal_name']} ({schedule['species']})",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        animal_label.pack(anchor="w")
        
        details = f"🕒 {schedule['schedule_time']} | {schedule['frequency']}"
        details_label = ctk.CTkLabel(
            info_frame,
            text=details,
            font=ctk.CTkFont(size=13),
            text_color="gray"
        )
        details_label.pack(anchor="w")
        
        food_label = ctk.CTkLabel(
            info_frame,
            text=f"Food: {schedule['feed_item']} ({schedule['quantity']})",
            font=ctk.CTkFont(size=13),
            text_color="gray"
        )
        food_label.pack(anchor="w")
        
        button_frame = ctk.CTkFrame(card, fg_color="transparent")
        button_frame.grid(row=0, column=2, padx=10, pady=10)
        
        if self.can_update:
            edit_btn = ctk.CTkButton(
                button_frame,
                text="✏️ Edit",
                command=lambda s=schedule: self.show_edit_dialog(s),
                width=80,
                height=30
            )
            edit_btn.pack(side="left", padx=2)
        
        if self.can_delete:
            delete_btn = ctk.CTkButton(
                button_frame,
                text="🗑️",
                command=lambda s=schedule: self.delete_schedule(s),
                width=40,
                height=30,
                fg_color="#e74c3c",
                hover_color="#c0392b"
            )
            delete_btn.pack(side="left", padx=2)
    
    def show_add_dialog(self):
        """Show add dialog"""
        self.show_schedule_dialog(None)
    
    def show_edit_dialog(self, schedule):
        """Show edit dialog"""
        self.show_schedule_dialog(schedule)
    
    def show_schedule_dialog(self, schedule=None):
        """Show add/edit dialog"""
        is_edit = schedule is not None
        
        dialog = ctk.CTkToplevel(self)
        dialog.title(f"{'Edit' if is_edit else 'Add'} Feeding Schedule")
        dialog.geometry("500x600")
        dialog.transient(self)
        dialog.grab_set()
        
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (500 // 2)
        y = (dialog.winfo_screenheight() // 2) - (600 // 2)
        dialog.geometry(f"500x600+{x}+{y}")
        
        form = ctk.CTkFrame(dialog)
        form.pack(fill="both", expand=True, padx=20, pady=20)
        
        entries = {}
        
        # Animal selection
        ctk.CTkLabel(
            form,
            text="Animal",
            font=ctk.CTkFont(size=13, weight="bold")
        ).pack(anchor="w", pady=(10, 5))
        
        # Load animals
        animals = self.db.execute_query("SELECT id, name, species FROM animals ORDER BY name", fetch=True)
        animal_options = [f"{a['name']} ({a['species']})" for a in animals]
        animal_map = {f"{a['name']} ({a['species']})": a['id'] for a in animals}
        
        animal_menu = ctk.CTkOptionMenu(form, values=animal_options, height=35)
        if schedule:
            current_name = f"{schedule['animal_name']} ({schedule['species']})"
            if current_name in animal_options:
                animal_menu.set(current_name)
        animal_menu.pack(fill="x", pady=(0, 15))
        entries['animal'] = (animal_menu, animal_map)
        
        # Other fields
        fields = [
            ("feed_item", "Feed Item"),
            ("quantity", "Quantity"),
            ("schedule_time", "Schedule Time (HH:MM)"),
            ("frequency", "Frequency"),
        ]
        
        for field_name, label in fields:
            ctk.CTkLabel(
                form,
                text=label,
                font=ctk.CTkFont(size=13, weight="bold")
            ).pack(anchor="w", pady=(10, 5))
            
            entry = ctk.CTkEntry(form, height=35)
            if schedule and schedule[field_name]:
                entry.insert(0, str(schedule[field_name]))
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
            command=lambda: self.save_schedule(entries, schedule, dialog),
            width=120
        )
        save_btn.pack(side="right", padx=5)
    
    def save_schedule(self, entries, schedule, dialog):
        """Save feeding schedule"""
        try:
            animal_menu, animal_map = entries['animal']
            selected_animal = animal_menu.get()
            animal_id = animal_map.get(selected_animal)
            
            if not animal_id:
                messagebox.showerror("Error", "Please select an animal")
                return
            
            feed_item = entries['feed_item'].get().strip()
            quantity = entries['quantity'].get().strip()
            schedule_time = entries['schedule_time'].get().strip()
            frequency = entries['frequency'].get().strip()
            
            if not all([feed_item, quantity, schedule_time, frequency]):
                messagebox.showerror("Error", "All fields are required")
                return
            
            if schedule:
                query = """
                    UPDATE feed_schedules SET
                        animal_id = %s, feed_item = %s, quantity = %s,
                        schedule_time = %s, frequency = %s
                    WHERE id = %s
                """
                params = (animal_id, feed_item, quantity, schedule_time, frequency, schedule['id'])
            else:
                query = """
                    INSERT INTO feed_schedules (animal_id, feed_item, quantity, schedule_time, frequency)
                    VALUES (%s, %s, %s, %s, %s)
                """
                params = (animal_id, feed_item, quantity, schedule_time, frequency)
            
            self.db.execute_query(query, params)
            
            messagebox.showinfo("Success", f"Schedule {'updated' if schedule else 'added'} successfully")
            dialog.destroy()
            self.load_schedules()
        
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save schedule: {e}")
    
    def delete_schedule(self, schedule):
        """Delete feeding schedule"""
        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this schedule?"):
            try:
                self.db.execute_query("DELETE FROM feed_schedules WHERE id = %s", (schedule['id'],))
                messagebox.showinfo("Success", "Schedule deleted successfully")
                self.load_schedules()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete schedule: {e}")