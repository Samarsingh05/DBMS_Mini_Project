import tkinter as tk
from tkinter import messagebox
import json
import os
from tkinter import ttk
import mysql.connector
from mysql.connector import Error

# File path for temporary login storage
TEMP_LOGIN_FILE = "customer_login.json"

# Database configuration
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Samar05@',
    'database': 'library2'
}

# Dark theme color scheme
COLORS = {
    'bg_primary': "#1a1b26",
    'bg_secondary': "#24283b",
    'primary': "#7aa2f7",
    'primary_hover': "#89b4f7",
    'secondary': "#9ece6a",
    'secondary_hover': "#a9d67a",
    'text_primary': "#c0caf5",
    'text_secondary': "#a9b1d6",
    'accent': "#bb9af7",
    'error': "#f7768e",
    'border': "#414868"
}

def get_db_connection():
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        return connection
    except Error as e:
        messagebox.showerror("Database Error", f"Could not connect to database: {str(e)}")
        return None

def save_temp_login(credentials):
    try:
        with open(TEMP_LOGIN_FILE, 'w') as file:
            json.dump(credentials, file)
    except Exception as e:
        print(f"Error saving login: {str(e)}")

class AuthenticationApp:
    def __init__(self, master):
        self.master = master
        master.title("Library Management System")
        master.geometry("800x600")
        master.configure(bg=COLORS['bg_primary'])
        
        self.style = ttk.Style()
        self.style.configure('Custom.TEntry', padding='10 5')
        
        self.setup_main_container()
        self.create_welcome_screen()

    def setup_main_container(self):
        self.main_container = tk.Frame(
            self.master, 
            bg=COLORS['bg_primary'],
            highlightbackground=COLORS['border'],
            highlightthickness=1
        )
        self.main_container.place(relx=0.5, rely=0.5, anchor="center")

    def create_welcome_screen(self):
        header_frame = tk.Frame(
            self.main_container, 
            bg=COLORS['bg_primary']
        )
        header_frame.pack(pady=20, padx=40)

        icon_label = tk.Label(
            header_frame, 
            text="📚", 
            font=('Arial', 40), 
            bg=COLORS['bg_primary'],
            fg=COLORS['text_primary']
        )
        icon_label.pack()

        title_label = tk.Label(
            header_frame, 
            text="Library Management System",
            font=('Helvetica', 24, 'bold'),
            fg=COLORS['text_primary'],
            bg=COLORS['bg_primary']
        )
        title_label.pack(pady=10)

        subtitle_label = tk.Label(
            header_frame,
            text="Please select your user type to continue",
            font=('Helvetica', 12),
            fg=COLORS['text_secondary'],
            bg=COLORS['bg_primary']
        )
        subtitle_label.pack()

        buttons_frame = tk.Frame(self.main_container, bg=COLORS['bg_primary'])
        buttons_frame.pack(pady=30)

        self.create_hover_button(
            buttons_frame, 
            "Admin Login",
            COLORS['primary'],
            self.admin_login,
            "👤"
        )

        self.create_hover_button(
            buttons_frame,
            "Customer Login",
            COLORS['secondary'],
            self.customer_login,
            "👥"
        )

    def create_hover_button(self, parent, text, color, command, icon=""):
        frame = tk.Frame(parent, bg=COLORS['bg_primary'])
        frame.pack(pady=10)

        btn = tk.Button(
            frame,
            text=f"{icon} {text}",
            font=('Helvetica', 12, 'bold'),
            bg=color,
            fg=COLORS['bg_primary'],
            width=20,
            height=2,
            bd=0,
            command=command,
            cursor="hand2"
        )
        btn.pack(pady=5)

        hover_color = COLORS['primary_hover'] if color == COLORS['primary'] else COLORS['secondary_hover']
        
        def on_enter(e):
            btn['bg'] = hover_color

        def on_leave(e):
            btn['bg'] = color

        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)

    def create_login_screen(self, title, login_command, register_command):
        self.clear_screen()
        self.setup_main_container()
        
        header_frame = tk.Frame(self.main_container, bg=COLORS['bg_primary'])
        header_frame.pack(pady=20, padx=40)

        back_btn = tk.Button(
            header_frame,
            text="← Back",
            font=('Helvetica', 11, 'bold'),
            bg=COLORS['bg_primary'],
            fg=COLORS['text_secondary'],
            bd=0,
            padx=18,
            pady=8,
            cursor="hand2",
            activebackground=COLORS['bg_primary'],
            activeforeground=COLORS['text_primary'],
            command=self.return_to_welcome
        )
        back_btn.pack(anchor="w", pady=(12, 5), padx=10)

        tk.Label(
            header_frame,
            text=title,
            font=('Helvetica', 24, 'bold'),
            fg=COLORS['text_primary'],
            bg=COLORS['bg_primary']
        ).pack(pady=10)

        form_frame = tk.Frame(self.main_container, bg=COLORS['bg_primary'])
        form_frame.pack(pady=20)

        # Username
        username_frame = tk.Frame(form_frame, bg=COLORS['bg_primary'])
        username_frame.pack(pady=10, fill="x", padx=40)

        tk.Label(
            username_frame,
            text="Username",
            font=('Helvetica', 10),
            fg=COLORS['text_secondary'],
            bg=COLORS['bg_primary']
        ).pack(anchor="w")

        self.username_entry = tk.Entry(
            username_frame,
            font=('Helvetica', 12),
            bg=COLORS['bg_secondary'],
            fg=COLORS['text_primary'],
            width=30,
            bd=1,
            relief="solid",
            insertbackground=COLORS['text_primary']
        )
        self.username_entry.pack(pady=5, ipady=8)

        # Password
        password_frame = tk.Frame(form_frame, bg=COLORS['bg_primary'])
        password_frame.pack(pady=10, fill="x", padx=40)

        tk.Label(
            password_frame,
            text="Password",
            font=('Helvetica', 10),
            fg=COLORS['text_secondary'],
            bg=COLORS['bg_primary']
        ).pack(anchor="w")

        self.password_entry = tk.Entry(
            password_frame,
            font=('Helvetica', 12),
            bg=COLORS['bg_secondary'],
            fg=COLORS['text_primary'],
            width=30,
            show="•",
            bd=1,
            relief="solid",
            insertbackground=COLORS['text_primary']
        )
        self.password_entry.pack(pady=5, ipady=8)

        buttons_frame = tk.Frame(self.main_container, bg=COLORS['bg_primary'])
        buttons_frame.pack(pady=20)

        # Login button
        self.login_btn = tk.Button(
            buttons_frame,
            text="Login",
            font=('Helvetica', 12, 'bold'),
            bg=COLORS['primary'],
            fg=COLORS['bg_primary'],
            width=25,
            height=2,
            bd=0,
            command=login_command
        )
        self.login_btn.pack(pady=5)

        # Register button
        self.register_btn = tk.Button(
            buttons_frame,
            text="Create New Account",
            font=('Helvetica', 12),
            bg=COLORS['secondary'],
            fg=COLORS['bg_primary'],
            width=25,
            height=2,
            bd=0,
            command=register_command
        )
        self.register_btn.pack(pady=5)

        # Add hover effects
        self.add_button_hover_effects()

    def add_button_hover_effects(self):
        def on_enter(button, hover_color):
            button.configure(bg=hover_color)

        def on_leave(button, original_color):
            button.configure(bg=original_color)

        self.login_btn.bind("<Enter>", lambda e: on_enter(self.login_btn, COLORS['primary_hover']))
        self.login_btn.bind("<Leave>", lambda e: on_leave(self.login_btn, COLORS['primary']))
        
        self.register_btn.bind("<Enter>", lambda e: on_enter(self.register_btn, COLORS['secondary_hover']))
        self.register_btn.bind("<Leave>", lambda e: on_leave(self.register_btn, COLORS['secondary']))

    def return_to_welcome(self):
        self.clear_screen()
        self.setup_main_container()
        self.create_welcome_screen()

    def admin_login(self):
        self.create_login_screen("Admin Login", self.admin_login_verify, self.admin_register)

    def customer_login(self):
        self.create_login_screen("Customer Login", self.customer_login_verify, self.customer_register)

    def admin_login_verify(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        
        if not username or not password:
            messagebox.showerror("Error", "Please enter both username and password")
            return

        connection = get_db_connection()
        if connection:
            try:
                cursor = connection.cursor(buffered=True)
                
                # Call the stored procedure for admin verification
                cursor.callproc('VerifyAdminCredentials', (username, password))
                
                # Fetch the result
                for result in cursor.stored_results():
                    admin = result.fetchone()
                
                if admin:
                    messagebox.showinfo("Success", f"Welcome, {username}!")
                    self.master.destroy()
                    import main
                    main.start_library_system(user_type="admin")
                else:
                    messagebox.showerror("Error", "Invalid Admin Credentials")

            except Error as e:
                messagebox.showerror("Database Error", str(e))
            finally:
                cursor.close()
                connection.close()


    def customer_login_verify(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        
        if not username or not password:
            messagebox.showerror("Error", "Please enter both username and password")
            return

        connection = get_db_connection()
        if connection:
            try:
                cursor = connection.cursor(buffered=True)
                
                # Call the stored procedure for customer verification
                cursor.callproc('VerifyCustomerCredentials', (username, password))
                
                # Fetch the result
                for result in cursor.stored_results():
                    customer = result.fetchone()
                
                if customer:
                    messagebox.showinfo("Success", f"Welcome, {username}!")
                    save_temp_login({username: password})
                    self.master.destroy()
                    import main
                    main.start_library_system(user_type="customer", username=username)
                else:
                    messagebox.showerror("Error", "Invalid Customer Credentials")

            except Error as e:
                messagebox.showerror("Database Error", str(e))
            finally:
                cursor.close()
                connection.close()


    def admin_register(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        
        if not username or not password:
            messagebox.showerror("Error", "Please enter both username and password")
            return

        connection = get_db_connection()
        if connection:
            try:
                cursor = connection.cursor(buffered=True)
                
                # Call RegisterAdmin stored procedure instead of direct SQL
                cursor.callproc('RegisterAdmin', (username, password))
                connection.commit()
                
                messagebox.showinfo("Success", f"Admin {username} registered successfully!")

            except Error as e:
                if "username already exists" in str(e).lower():
                    messagebox.showerror("Error", "Username already exists")
                else:
                    messagebox.showerror("Database Error", str(e))
            finally:
                cursor.close()
                connection.close()

    def customer_register(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        
        if not username or not password:
            messagebox.showerror("Error", "Please enter both username and password")
            return

        connection = get_db_connection()
        if connection:
            try:
                cursor = connection.cursor(buffered=True)
                
                # Call RegisterCustomer stored procedure instead of direct SQL
                cursor.callproc('RegisterCustomer', (username, password))
                connection.commit()
                
                messagebox.showinfo("Success", f"Customer {username} registered successfully!")

            except Error as e:
                if "username already exists" in str(e).lower():
                    messagebox.showerror("Error", "Username already exists")
                else:
                    messagebox.showerror("Database Error", str(e))
            finally:
                cursor.close()
                connection.close()

    def clear_screen(self):
        for widget in self.master.winfo_children():
            widget.destroy()

def start_authentication():
    root = tk.Tk()
    app = AuthenticationApp(root)
    root.mainloop()

if __name__ == "__main__":
    start_authentication()