from tkinter import *
from PIL import ImageTk, Image
from tkinter import messagebox
import pymysql

def bookRegister():
    bookid = bookInfo1.get()
    title = bookInfo2.get()
    author = bookInfo3.get()
    genre = bookInfo4.get()
    status = "Avail"
    
    # Validate inputs
    if not all([bookid, title, author, genre]):
        messagebox.showerror("Error", "Please fill in all fields")
        return

    insertBooks = f"INSERT INTO {bookTable} (bookid, title, author, genre, status) VALUES (%s, %s, %s, %s, %s)"
    
    try:
        # Use parameterized query to prevent SQL injection
        cur.execute(insertBooks, (bookid, title, author, genre, status))
        con.commit()
        messagebox.showinfo('Success', "Book added successfully")
        
        # Clear the entries
        bookInfo1.delete(0, END)
        bookInfo2.delete(0, END)
        bookInfo3.delete(0, END)
        bookInfo4.delete(0, END)
        
    except Exception as e:
        messagebox.showerror("Error", f"Can't add data into Database: {str(e)}")
        con.rollback()

def addBook():
    global bookInfo1, bookInfo2, bookInfo3, bookInfo4, Canvas1, con, cur, bookTable, root
    
    root = Tk()
    root.title("Adding Book")
    root.geometry("800x900")
    
    # Database configuration
    mypass = "Samar05@"
    mydatabase = "library2"
    
    try:
        con = pymysql.connect(
            host="localhost",
            user="root",
            password=mypass,
            database=mydatabase
        )
        cur = con.cursor()
        
        bookTable = "books"
        
        Canvas1 = Canvas(root, bg="#373a40")
        Canvas1.pack(expand=True, fill=BOTH)
        
        headingFrame1 = Frame(root)
        headingFrame1.place(relx=0.25, rely=0.1, relwidth=0.5, relheight=0.13)
        
        headingLabel = Label(headingFrame1, text="Adding Book", bg='#ff414d', fg='black', font=('Consolas', 18))
        headingLabel.place(relx=0, rely=0, relwidth=1, relheight=1)
        
        labelFrame = Frame(root, bg='#222831')
        labelFrame.place(relx=0.1, rely=0.3, relwidth=0.8, relheight=0.4)
        
        # Book ID
        lb1 = Label(labelFrame, text="Book ID : ", bg='#222831', fg='white', font=('Consolas', 13))
        lb1.place(relx=0.05, rely=0.15)
        bookInfo1 = Entry(labelFrame)
        bookInfo1.place(relx=0.4, rely=0.15, relwidth=0.55)
        
        # Title
        lb2 = Label(labelFrame, text="Title : ", bg='#222831', fg='white', font=('Consolas', 13))
        lb2.place(relx=0.05, rely=0.3)
        bookInfo2 = Entry(labelFrame)
        bookInfo2.place(relx=0.4, rely=0.3, relwidth=0.55)
        
        # Author
        lb3 = Label(labelFrame, text="Author : ", bg='#222831', fg='white', font=('Consolas', 13))
        lb3.place(relx=0.05, rely=0.45)
        bookInfo3 = Entry(labelFrame)
        bookInfo3.place(relx=0.4, rely=0.45, relwidth=0.55)
        
        # Genre
        lb4 = Label(labelFrame, text="Genre : ", bg='#222831', fg='white', font=('Consolas', 13))
        lb4.place(relx=0.05, rely=0.6)
        bookInfo4 = Entry(labelFrame)
        bookInfo4.place(relx=0.4, rely=0.6, relwidth=0.55)
        
        SubmitBtn = Button(root, text="Submit", bg='#F05454', fg='black', font=('Consolas', 13), command=bookRegister)
        SubmitBtn.place(relx=0.2, rely=0.85, relwidth=0.2)
        
        quitBtn = Button(root, text="Quit", bg='#F05454', fg='black', font=('Consolas', 13), command=root.destroy)
        quitBtn.place(relx=0.6, rely=0.85, relwidth=0.2)
        
    except Exception as e:
        messagebox.showerror("Error", f"Database connection failed: {str(e)}")
        root.destroy()
        return
    
    root.mainloop()