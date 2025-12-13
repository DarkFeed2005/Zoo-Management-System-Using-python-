"""
Tickets management view
"""

import customtkinter as ctk
from tkinter import messagebox
from config.database import Database
from services.rbac_service import RBACService
from datetime import datetime, date

class TicketsView(ctk.CTkFrame):
    def __init__(self, parent, user):
        super().__init__(parent, fg_color="transparent")
        self.user = user
        self.db = Database()
        
        self.grid_columnconfigure(0, weight=2)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        self.can_create = RBACService.has_permission(user['role_name'], 'tickets', 'create')
        
        self.create_ui()
        self.load_ticket_types()
        self.load_today_sales()
    
    def create_ui(self):
        """Create UI"""
        # Title
        title = ctk.CTkLabel(
            self,
            text="🎫 Ticket Management",
            font=ctk.CTkFont(size=28, weight="bold")
        )
        title.grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 20))
        
        # Left side - Sell ticket form
        if self.can_create:
            self.create_sell_form()
        
        # Right side - Today's sales
        self.create_sales_summary()
    
    def create_sell_form(self):
        """Create ticket selling form"""
        form_frame = ctk.CTkFrame(self)
        form_frame.grid(row=1, column=0, sticky="nsew", padx=(0, 10))
        
        ctk.CTkLabel(
            form_frame,
            text="Sell New Ticket",
            font=ctk.CTkFont(size=20, weight="bold")
        ).pack(padx=20, pady=(20, 10))
        
        # Buyer name
        ctk.CTkLabel(
            form_frame,
            text="Buyer Name",
            font=ctk.CTkFont(size=13, weight="bold")
        ).pack(anchor="w", padx=20, pady=(10, 5))
        
        self.buyer_entry = ctk.CTkEntry(form_frame, height=35)
        self.buyer_entry.pack(fill="x", padx=20, pady=(0, 15))
        
        # Ticket type
        ctk.CTkLabel(
            form_frame,
            text="Ticket Type",
            font=ctk.CTkFont(size=13, weight="bold")
        ).pack(anchor="w", padx=20, pady=(0, 5))
        
        self.ticket_type_var = ctk.StringVar(value="Select ticket type")
        self.ticket_type_menu = ctk.CTkOptionMenu(
            form_frame,
            variable=self.ticket_type_var,
            values=["Select ticket type"],
            command=self.on_ticket_type_change,
            height=35
        )
        self.ticket_type_menu.pack(fill="x", padx=20, pady=(0, 15))
        
        # Quantity
        ctk.CTkLabel(
            form_frame,
            text="Quantity",
            font=ctk.CTkFont(size=13, weight="bold")
        ).pack(anchor="w", padx=20, pady=(0, 5))
        
        self.quantity_entry = ctk.CTkEntry(form_frame, height=35)
        self.quantity_entry.insert(0, "1")
        self.quantity_entry.bind("<KeyRelease>", lambda e: self.calculate_total())
        self.quantity_entry.pack(fill="x", padx=20, pady=(0, 15))
        
        # Total price display
        self.total_label = ctk.CTkLabel(
            form_frame,
            text="Total: $0.00",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="#2ecc71"
        )
        self.total_label.pack(pady=20)
        
        # Sell button
        sell_btn = ctk.CTkButton(
            form_frame,
            text="💳 Sell Ticket",
            command=self.sell_ticket,
            height=50,
            font=ctk.CTkFont(size=16, weight="bold"),
            fg_color="#2ecc71",
            hover_color="#27ae60"
        )
        sell_btn.pack(fill="x", padx=20, pady=(0, 20))
    
    def create_sales_summary(self):
        """Create today's sales summary"""
        summary_frame = ctk.CTkFrame(self)
        summary_frame.grid(row=1, column=1, sticky="nsew", padx=(10, 0))
        
        ctk.CTkLabel(
            summary_frame,
            text="Today's Sales",
            font=ctk.CTkFont(size=20, weight="bold")
        ).pack(padx=20, pady=(20, 10))
        
        # Stats
        self.tickets_sold_label = ctk.CTkLabel(
            summary_frame,
            text="0",
            font=ctk.CTkFont(size=36, weight="bold"),
            text_color="#3498db"
        )
        self.tickets_sold_label.pack(pady=10)
        
        ctk.CTkLabel(
            summary_frame,
            text="Tickets Sold",
            font=ctk.CTkFont(size=14),
            text_color="gray"
        ).pack()
        
        self.revenue_label = ctk.CTkLabel(
            summary_frame,
            text="$0.00",
            font=ctk.CTkFont(size=36, weight="bold"),
            text_color="#2ecc71"
        )
        self.revenue_label.pack(pady=(20, 10))
        
        ctk.CTkLabel(
            summary_frame,
            text="Total Revenue",
            font=ctk.CTkFont(size=14),
            text_color="gray"
        ).pack()
        
        # Recent tickets
        ctk.CTkLabel(
            summary_frame,
            text="Recent Tickets",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(pady=(30, 10), padx=20)
        
        self.recent_frame = ctk.CTkScrollableFrame(summary_frame, height=200)
        self.recent_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
    
    def load_ticket_types(self):
        """Load available ticket types"""
        try:
            query = "SELECT * FROM ticket_types WHERE active = 1 ORDER BY name"
            self.ticket_types = self.db.execute_query(query, fetch=True)
            
            if self.ticket_types:
                names = [t['name'] for t in self.ticket_types]
                self.ticket_type_menu.configure(values=names)
                self.ticket_type_var.set(names[0])
                self.calculate_total()
        except Exception as e:
            print(f"Error loading ticket types: {e}")
    
    def on_ticket_type_change(self, choice):
        """Handle ticket type selection change"""
        self.calculate_total()
    
    def calculate_total(self):
        """Calculate total price"""
        try:
            selected = self.ticket_type_var.get()
            if selected == "Select ticket type":
                return
            
            ticket_type = next((t for t in self.ticket_types if t['name'] == selected), None)
            if not ticket_type:
                return
            
            quantity = int(self.quantity_entry.get() or 0)
            total = float(ticket_type['price']) * quantity
            
            self.total_label.configure(text=f"Total: ${total:.2f}")
        except ValueError:
            self.total_label.configure(text="Total: $0.00")
    
    def sell_ticket(self):
        """Sell a ticket"""
        try:
            buyer_name = self.buyer_entry.get().strip()
            if not buyer_name:
                messagebox.showerror("Error", "Please enter buyer name")
                return
            
            selected = self.ticket_type_var.get()
            if selected == "Select ticket type":
                messagebox.showerror("Error", "Please select ticket type")
                return
            
            ticket_type = next((t for t in self.ticket_types if t['name'] == selected), None)
            if not ticket_type:
                return
            
            quantity = int(self.quantity_entry.get() or 0)
            if quantity <= 0:
                messagebox.showerror("Error", "Please enter valid quantity")
                return
            
            total_price = float(ticket_type['price']) * quantity
            
            query = """
                INSERT INTO tickets (ticket_type_id, buyer_name, quantity, total_price, issued_by)
                VALUES (%s, %s, %s, %s, %s)
            """
            params = (ticket_type['id'], buyer_name, quantity, total_price, self.user['id'])
            
            self.db.execute_query(query, params)
            
            messagebox.showinfo("Success", f"Ticket sold successfully!\nTotal: ${total_price:.2f}")
            
            # Clear form
            self.buyer_entry.delete(0, 'end')
            self.quantity_entry.delete(0, 'end')
            self.quantity_entry.insert(0, "1")
            
            # Refresh sales
            self.load_today_sales()
        
        except Exception as e:
            messagebox.showerror("Error", f"Failed to sell ticket: {e}")
    
    def load_today_sales(self):
        """Load today's sales statistics"""
        try:
            query = """
                SELECT COUNT(*) as count, COALESCE(SUM(total_price), 0) as revenue
                FROM tickets
                WHERE issue_date = CURDATE()
            """
            result = self.db.execute_query(query, fetch=True)[0]
            
            self.tickets_sold_label.configure(text=str(result['count']))
            self.revenue_label.configure(text=f"${result['revenue']:.2f}")
            
            # Load recent tickets
            query_recent = """
                SELECT t.*, tt.name as ticket_name
                FROM tickets t
                JOIN ticket_types tt ON t.ticket_type_id = tt.id
                WHERE t.issue_date = CURDATE()
                ORDER BY t.id DESC
                LIMIT 10
            """
            recent_tickets = self.db.execute_query(query_recent, fetch=True)
            
            # Clear recent frame
            for widget in self.recent_frame.winfo_children():
                widget.destroy()
            
            if recent_tickets:
                for ticket in recent_tickets:
                    ticket_item = ctk.CTkFrame(self.recent_frame)
                    ticket_item.pack(fill="x", pady=5)
                    
                    ctk.CTkLabel(
                        ticket_item,
                        text=f"{ticket['buyer_name']}",
                        font=ctk.CTkFont(size=12, weight="bold")
                    ).pack(anchor="w", padx=5)
                    
                    ctk.CTkLabel(
                        ticket_item,
                        text=f"{ticket['ticket_name']} x{ticket['quantity']} - ${ticket['total_price']:.2f}",
                        font=ctk.CTkFont(size=11),
                        text_color="gray"
                    ).pack(anchor="w", padx=5)
            else:
                ctk.CTkLabel(
                    self.recent_frame,
                    text="No tickets sold today",
                    text_color="gray"
                ).pack(pady=20)
        
        except Exception as e:
            print(f"Error loading sales: {e}")