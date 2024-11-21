from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image
from tkinter import messagebox
import pymysql

# root password and database
mypass = "Samar05@"
mydatabase = "library2"

con = pymysql.connect(host="localhost", user="root", password=mypass, database=mydatabase)
cur = con.cursor()

# Table Name
bookTable = "books"

def View():
    root = Tk()
    root.title("Library Management System - View Books")
    root.minsize(width=1200, height=600)
    root.geometry("1200x600")

    # Main Canvas
    Canvas1 = Canvas(root)
    Canvas1.config(bg="#373a40")
    Canvas1.pack(expand=True, fill=BOTH)

    # Heading Frame
    headingFrame = Frame(root, bg="#ff414d", bd=5)
    headingFrame.place(relx=0.25, rely=0.1, relwidth=0.5, relheight=0.08)

    headingLabel = Label(headingFrame, text="View Books", bg='#ff414d', fg='black', 
                        font=('Consolas', 20, 'bold'))
    headingLabel.place(relx=0, rely=0, relwidth=1, relheight=1)

    # Frame for TreeView
    tree_frame = Frame(root, bg='#222831')
    tree_frame.place(relx=0.05, rely=0.25, relwidth=0.9, relheight=0.6)

    # Scrollbar
    tree_scroll = ttk.Scrollbar(tree_frame)
    tree_scroll.pack(side=RIGHT, fill=Y)

    # Create TreeView
    tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set, selectmode="extended")
    tree.pack(expand=True, fill=BOTH)

    # Configure scrollbar
    tree_scroll.config(command=tree.yview)

    # Define columns
    tree['columns'] = ("BID", "Title", "Author", "Status", "Issued To", "Issue Date", "Return Date", "Fare")

    # Format columns
    tree.column("#0", width=0, stretch=NO)
    tree.column("BID", anchor=W, width=80)
    tree.column("Title", anchor=W, width=200)
    tree.column("Author", anchor=W, width=200)
    tree.column("Status", anchor=CENTER, width=100)
    tree.column("Issued To", anchor=W, width=150)
    tree.column("Issue Date", anchor=CENTER, width=150)
    tree.column("Return Date", anchor=CENTER, width=150)
    tree.column("Fare", anchor=CENTER, width=100)

    # Create headings
    tree.heading("#0", text="", anchor=W)
    tree.heading("BID", text="BID", anchor=W)
    tree.heading("Title", text="Title", anchor=W)
    tree.heading("Author", text="Author", anchor=W)
    tree.heading("Status", text="Status", anchor=CENTER)
    tree.heading("Issued To", text="Issued To", anchor=W)
    tree.heading("Issue Date", text="Issue Date", anchor=CENTER)
    tree.heading("Return Date", text="Return Date", anchor=CENTER)
    tree.heading("Fare", text="Fare", anchor=CENTER)

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

    # SQL Query - Selecting fare from books_issued (bi.fare)
    #JOIN QUERY
    getBooks = """
        SELECT b.bookid, b.title, b.author, b.status, COALESCE(bi.issueto, '-'),
               COALESCE(bi.issue_date, '-'), COALESCE(bi.return_date, '-'), COALESCE(bi.fare, 0)  
        FROM books b
        LEFT JOIN books_issued bi ON b.bookid = bi.bookid                                        
    """

    try:
        cur.execute(getBooks)
        con.commit()
        
        # Clear existing items
        for item in tree.get_children():
            tree.delete(item)
            
        # Insert data
        for i, row in enumerate(cur):
            tree.insert(parent='', index='end', iid=str(i), values=row)
            
    except Exception as e:
        messagebox.showinfo("Error", f"Failed to fetch data: {str(e)}")

    # Quit Button
    quitBtn = Button(root, text="Quit", bg='#F05454', fg='black', 
                     font=('Consolas', 12, 'bold'), 
                     command=root.destroy, bd=0)
    quitBtn.place(relx=0.4, rely=0.9, relwidth=0.18, relheight=0.06)

    root.mainloop()