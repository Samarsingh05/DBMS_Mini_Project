from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image
from tkinter import messagebox
import mysql.connector

# Database connection details
DB_NAME = "library2"
DB_USER = "root"
DB_PASSWORD = "Samar05@"
DB_HOST = "localhost"

def display_book_logs():
    root = Tk()
    root.title("Library Management System - View Book Logs")
    root.minsize(width=1200, height=600)
    root.geometry("1200x600")

    # Main Canvas
    Canvas1 = Canvas(root)
    Canvas1.config(bg="#2f3542")
    Canvas1.pack(expand=True, fill=BOTH)

    # Heading Frame
    headingFrame = Frame(root, bg="#ff6b81", bd=5)
    headingFrame.place(relx=0.25, rely=0.1, relwidth=0.5, relheight=0.08)

    headingLabel = Label(headingFrame, text="View Book Logs", bg='#ff6b81', fg='black', 
                         font=('Consolas', 20, 'bold'))
    headingLabel.place(relx=0, rely=0, relwidth=1, relheight=1)

    # Frame for TreeView
    tree_frame = Frame(root, bg='#1e272e')
    tree_frame.place(relx=0.05, rely=0.25, relwidth=0.9, relheight=0.6)

    # Scrollbar
    tree_scroll = ttk.Scrollbar(tree_frame)
    tree_scroll.pack(side=RIGHT, fill=Y)

    # Create TreeView
    tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set, selectmode="extended")
    tree.pack(expand=True, fill=BOTH)

    # Configure scrollbar
    tree_scroll.config(command=tree.yview)

    # Connect to the MySQL database
    try:
        connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )

        cursor = connection.cursor()

        # SQL query to fetch all records from book_logs
        query = "SELECT * FROM book_logs;"
        cursor.execute(query)

        # Fetch all rows
        rows = cursor.fetchall()

        # Get column names
        col_names = [desc[0] for desc in cursor.description]

        # Define columns dynamically based on the fetched column names
        tree["columns"] = col_names

        # Format columns and create headings
        tree.column("#0", width=0, stretch=NO)
        for col in col_names:
            tree.column(col, anchor=W, width=150)
            tree.heading(col, text=col, anchor=W)

        # Style
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview",
                        background="#2c3e50",
                        foreground="white",
                        rowheight=25,
                        fieldbackground="#2c3e50")
        style.configure("Treeview.Heading",
                        background="#34495e",
                        foreground="white",
                        relief="flat")
        style.map("Treeview",
                  background=[("selected", "#3498db")])

        # Check if there are rows and insert data
        if rows:
            for i, row in enumerate(rows):
                tree.insert(parent='', index='end', iid=str(i), values=row)
        else:
            messagebox.showinfo("Information", "No records found in the table 'book_logs'.")

    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Failed to fetch data: {str(err)}")

    finally:
        # Close the database connection
        if connection.is_connected():
            cursor.close()
            connection.close()

    # Quit Button
    quitBtn = Button(root, text="Quit", bg='#ff4757', fg='black',
                     font=('Consolas', 12, 'bold'),
                     command=root.destroy, bd=0)
    quitBtn.place(relx=0.4, rely=0.9, relwidth=0.18, relheight=0.06)

    root.mainloop()

