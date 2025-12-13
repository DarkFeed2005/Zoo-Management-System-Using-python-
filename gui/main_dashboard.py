"""
Main dashboard with role-based navigation and content area
"""

import customtkinter as ctk
from tkinter import messagebox
from services.rbac_service import RBACService
from gui.views.animals_view import AnimalsView
from gui.views.enclosures_view import EnclosuresView
from gui.views.tickets_view import TicketsView
from gui.views.dashboard_view import DashboardView
from gui.views.feeding_view import FeedingView
from gui.views.users_view import UsersView

class MainDashboard(ctk.CTkToplevel):
    def __init__(self, user, auth_service):
        super().__init__()
        
        self.user = user
        self.auth_service = auth_service
        self.current_view = None
        
        # Window configuration
        self.title(f"Zoo Management System - {user['role_name'].capitalize()}")
        self.geometry("1400x800")
        
        # Center window
        self.center_window()
        
        # Create main layout
        self.create_layout()
        
        # Show default view
        self.show_dashboard()
    
    def center_window(self):
        """Center window on screen"""
        self.update_idletasks()
        width = 1400
        height = 800
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')
    
    def create_layout(self):
        """Create main layout with sidebar and content area"""
        # Main container
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Sidebar
        self.sidebar = ctk.CTkFrame(self, width=250, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_rowconfigure(20, weight=1)
        
        # Logo/Title in sidebar
        logo_label = ctk.CTkLabel(
            self.sidebar,
            text="🦁 Zoo Manager",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        
        # User info
        user_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        user_frame.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="ew")
        
        ctk.CTkLabel(
            user_frame,
            text=f"👤 {self.user['username']}",
            font=ctk.CTkFont(size=13)
        ).pack(anchor="w")
        
        ctk.CTkLabel(
            user_frame,
            text=f"Role: {self.user['role_name'].capitalize()}",
            font=ctk.CTkFont(size=11),
            text_color="gray"
        ).pack(anchor="w")
        
        # Separator
        separator = ctk.CTkFrame(self.sidebar, height=2, fg_color="gray30")
        separator.grid(row=2, column=0, padx=20, pady=10, sticky="ew")
        
        # Navigation buttons
        self.nav_buttons = {}
        row_start = 3
        
        # Get accessible modules for user role
        modules = RBACService.get_accessible_modules(self.user['role_name'])
        
        # Define all possible navigation items
        nav_items = [
            ('dashboard', '🏠 Dashboard', self.show_dashboard),
            ('animals', '🦁 Animals', self.show_animals),
            ('enclosures', '🏛️ Enclosures', self.show_enclosures),
            ('feeding', '🍖 Feeding', self.show_feeding),
            ('tickets', '🎫 Tickets', self.show_tickets),
            ('users', '👥 Users', self.show_users),
            ('staff', '👔 Staff', self.show_staff),
            ('reports', '📊 Reports', self.show_reports),
            ('audit', '📋 Audit Logs', self.show_audit),
        ]
        
        current_row = row_start
        for module_key, label, command in nav_items:
            if module_key in modules:
                btn = ctk.CTkButton(
                    self.sidebar,
                    text=label,
                    command=command,
                    font=ctk.CTkFont(size=14),
                    height=40,
                    fg_color="transparent",
                    hover_color="gray25",
                    anchor="w"
                )
                btn.grid(row=current_row, column=0, padx=10, pady=5, sticky="ew")
                self.nav_buttons[module_key] = btn
                current_row += 1
        
        # Logout button at bottom
        logout_btn = ctk.CTkButton(
            self.sidebar,
            text="🚪 Logout",
            command=self.handle_logout,
            font=ctk.CTkFont(size=14),
            height=40,
            fg_color="#e74c3c",
            hover_color="#c0392b"
        )
        logout_btn.grid(row=21, column=0, padx=10, pady=20, sticky="ew")
        
        # Content area
        self.content_frame = ctk.CTkFrame(self, corner_radius=0)
        self.content_frame.grid(row=0, column=1, sticky="nsew", padx=0, pady=0)
        self.content_frame.grid_columnconfigure(0, weight=1)
        self.content_frame.grid_rowconfigure(0, weight=1)
    
    def clear_content(self):
        """Clear current content view"""
        if self.current_view:
            self.current_view.destroy()
            self.current_view = None
    
    def set_active_nav(self, active_key):
        """Highlight active navigation button"""
        for key, btn in self.nav_buttons.items():
            if key == active_key:
                btn.configure(fg_color="gray25")
            else:
                btn.configure(fg_color="transparent")
    
    def show_dashboard(self):
        """Show dashboard view"""
        self.clear_content()
        self.set_active_nav('dashboard')
        self.current_view = DashboardView(self.content_frame, self.user)
        self.current_view.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
    
    def show_animals(self):
        """Show animals management view"""
        self.clear_content()
        self.set_active_nav('animals')
        self.current_view = AnimalsView(self.content_frame, self.user)
        self.current_view.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
    
    def show_enclosures(self):
        """Show enclosures management view"""
        self.clear_content()
        self.set_active_nav('enclosures')
        self.current_view = EnclosuresView(self.content_frame, self.user)
        self.current_view.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
    
    def show_feeding(self):
        """Show feeding schedules view"""
        self.clear_content()
        self.set_active_nav('feeding')
        self.current_view = FeedingView(self.content_frame, self.user)
        self.current_view.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
    
    def show_tickets(self):
        """Show tickets management view"""
        self.clear_content()
        self.set_active_nav('tickets')
        self.current_view = TicketsView(self.content_frame, self.user)
        self.current_view.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
    
    def show_users(self):
        """Show users management view"""
        self.clear_content()
        self.set_active_nav('users')
        self.current_view = UsersView(self.content_frame, self.user)
        self.current_view.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
    
    def show_staff(self):
        """Show staff management view"""
        self.clear_content()
        self.set_active_nav('staff')
        # TODO: Implement StaffView
        placeholder = ctk.CTkLabel(
            self.content_frame,
            text="Staff Management - Coming Soon",
            font=ctk.CTkFont(size=24)
        )
        self.current_view = placeholder
        placeholder.grid(row=0, column=0)
    
    def show_reports(self):
        """Show reports view"""
        self.clear_content()
        self.set_active_nav('reports')
        # TODO: Implement ReportsView
        placeholder = ctk.CTkLabel(
            self.content_frame,
            text="Reports - Coming Soon",
            font=ctk.CTkFont(size=24)
        )
        self.current_view = placeholder
        placeholder.grid(row=0, column=0)
    
    def show_audit(self):
        """Show audit logs view"""
        self.clear_content()
        self.set_active_nav('audit')
        # TODO: Implement AuditView
        placeholder = ctk.CTkLabel(
            self.content_frame,
            text="Audit Logs - Coming Soon",
            font=ctk.CTkFont(size=24)
        )
        self.current_view = placeholder
        placeholder.grid(row=0, column=0)
    
    def handle_logout(self):
        """Handle logout"""
        if messagebox.askyesno("Logout", "Are you sure you want to logout?"):
            self.destroy()