"""
Dashboard view with statistics and quick info
"""

import customtkinter as ctk
from config.database import Database
from datetime import datetime

class DashboardView(ctk.CTkFrame):
    def __init__(self, parent, user):
        super().__init__(parent, fg_color="transparent")
        self.user = user
        self.db = Database()
        
        self.grid_columnconfigure((0, 1, 2, 3), weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        # Title
        title = ctk.CTkLabel(
            self,
            text="📊 Dashboard Overview",
            font=ctk.CTkFont(size=28, weight="bold")
        )
        title.grid(row=0, column=0, columnspan=4, sticky="w", pady=(0, 20))
        
        # Load and display statistics
        self.load_statistics()
        
        # Recent activity section
        self.create_recent_activity()
    
    def load_statistics(self):
        """Load and display key statistics"""
        stats = self.get_statistics()
        
        # Stat cards
        cards_data = [
            ("🦁 Total Animals", stats['animals'], "#3498db"),
            ("🏛️ Enclosures", stats['enclosures'], "#2ecc71"),
            ("🎫 Today's Tickets", stats['tickets_today'], "#e74c3c"),
            ("👥 System Users", stats['users'], "#f39c12"),
        ]
        
        for idx, (title, value, color) in enumerate(cards_data):
            self.create_stat_card(idx, title, value, color)
    
    def create_stat_card(self, col, title, value, color):
        """Create a statistics card"""
        card = ctk.CTkFrame(self, fg_color=color, corner_radius=10)
        card.grid(row=1, column=col, padx=10, pady=10, sticky="nsew")
        
        ctk.CTkLabel(
            card,
            text=title,
            font=ctk.CTkFont(size=14),
            text_color="white"
        ).pack(pady=(20, 5))
        
        ctk.CTkLabel(
            card,
            text=str(value),
            font=ctk.CTkFont(size=36, weight="bold"),
            text_color="white"
        ).pack(pady=(5, 20))
    
    def create_recent_activity(self):
        """Create recent activity section"""
        activity_frame = ctk.CTkFrame(self)
        activity_frame.grid(row=2, column=0, columnspan=4, sticky="nsew", pady=20)
        activity_frame.grid_columnconfigure(0, weight=1)
        
        title = ctk.CTkLabel(
            activity_frame,
            text="Recent Activity",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        title.grid(row=0, column=0, sticky="w", padx=20, pady=(20, 10))
        
        # Activity list
        activity_text = ctk.CTkTextbox(activity_frame, height=200)
        activity_text.grid(row=1, column=0, sticky="nsew", padx=20, pady=(0, 20))
        
        # Load recent activities
        activities = self.get_recent_activities()
        for activity in activities:
            activity_text.insert("end", f"• {activity}\n")
        
        activity_text.configure(state="disabled")
    
    def get_statistics(self):
        """Fetch statistics from database"""
        try:
            # Count animals
            animals = self.db.execute_query(
                "SELECT COUNT(*) as count FROM animals",
                fetch=True
            )[0]['count']
            
            # Count enclosures
            enclosures = self.db.execute_query(
                "SELECT COUNT(*) as count FROM enclosures",
                fetch=True
            )[0]['count']
            
            # Count today's tickets
            tickets_today = self.db.execute_query(
                "SELECT COUNT(*) as count FROM tickets WHERE issue_date = CURDATE()",
                fetch=True
            )[0]['count']
            
            # Count users
            users = self.db.execute_query(
                "SELECT COUNT(*) as count FROM users WHERE is_active = 1",
                fetch=True
            )[0]['count']
            
            return {
                'animals': animals,
                'enclosures': enclosures,
                'tickets_today': tickets_today,
                'users': users
            }
        except Exception as e:
            print(f"Error loading statistics: {e}")
            return {
                'animals': 0,
                'enclosures': 0,
                'tickets_today': 0,
                'users': 0
            }
    
    def get_recent_activities(self):
        """Get recent system activities"""
        try:
            query = """
                SELECT u.username, a.action, a.entity, a.created_at
                FROM audit_logs a
                JOIN users u ON a.user_id = u.id
                ORDER BY a.created_at DESC
                LIMIT 10
            """
            activities = self.db.execute_query(query, fetch=True)
            
            result = []
            for activity in activities:
                time = activity['created_at'].strftime("%Y-%m-%d %H:%M")
                result.append(
                    f"{time} - {activity['username']} {activity['action']} {activity['entity']}"
                )
            
            return result if result else ["No recent activities"]
        except Exception as e:
            print(f"Error loading activities: {e}")
            return ["Unable to load activities"]