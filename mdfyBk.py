from tkinter import *
from PIL import ImageTk, Image
from tkinter import messagebox
import pymysql


mypass = "Samar05@"
mydatabase = "library2"

con = pymysql.connect(host="localhost", user="root", password=mypass, database=mydatabase)
cur = con.cursor()

bookTable = "books"

def modify():
    global bookInfo1, bookInfo2, bookInfo3, bookInfo4, Canvas1, con, cur, bookTable, root

    root = Tk()
    root.title("Modifying Books")
    root.minsize(width=800, height=900)
    root.maxsize(width=800, height=900)

    Canvas1 = Canvas(root)
    Canvas1.config(bg="#373a40")
    Canvas1.pack(expand=True, fill=BOTH)

    headingFrame1 = Frame(root, bd=0)
    headingFrame1.place(relx=0.25, rely=0.1, relwidth=0.5, relheight=0.08)

    headingLabel = Label(headingFrame1, text="Modifying Books", bg='#ff414d', fg='black', font=('Consolas', 18))
    headingLabel.place(relx=0, rely=0, relwidth=1, relheight=1)

    labelFrame = Frame(root, bg='#222831')
    labelFrame.place(relx=0.1, rely=0.2, relwidth=0.8, relheight=0.6)

    # Book ID to modify
    lb1 = Label(labelFrame, text="Book ID of book to modify: ", bg='#222831', fg='white', font=('Consolas', 13))
    lb1.place(relx=0.05, rely=0.1)

    bookInfo1 = Entry(labelFrame)
    bookInfo1.place(relx=0.45, rely=0.1, relwidth=0.30)

    # Modification Section
    lb3 = Label(labelFrame, text="New Title: ", bg='#222831', fg='white', font=('Consolas', 13))
    lb3.place(relx=0.05, rely=0.5)

    bookInfo3 = Entry(labelFrame)
    bookInfo3.place(relx=0.20, rely=0.5, relwidth=0.55)

    lb4 = Label(labelFrame, text="New Author: ", bg='#222831', fg='white', font=('Consolas', 13))
    lb4.place(relx=0.05, rely=0.6)

    bookInfo4 = Entry(labelFrame)
    bookInfo4.place(relx=0.20, rely=0.6, relwidth=0.55)

    def searchBook():
        bookid = bookInfo1.get().strip()

        query = "SELECT * FROM books WHERE bookid = %s"
        try:
            cur.execute(query, (bookid,))
            book = cur.fetchone()
            if book:
                messagebox.showinfo("Book Found", f"BID: {book[0]}, Title: {book[1]}, Author: {book[2]}")
            else:
                messagebox.showinfo("Not Found", "No book with this ID exists.")
        except Exception as e:
            messagebox.showinfo("Error", str(e))

    def modifyBook():
        bookid = bookInfo1.get().strip()
        title_updt = bookInfo3.get().strip()
        author_updt = bookInfo4.get().strip()

        # Ensure title and author are not empty
        if not title_updt or not author_updt:
            messagebox.showinfo("Invalid Input", "Title and Author fields cannot be empty.")
            return

        try:
            # Only update the title and author in the books table
            query = "UPDATE books SET title = %s, author = %s WHERE bookid = %s"
            cur.execute(query, (title_updt, author_updt, bookid))
            con.commit()
            
            messagebox.showinfo("Success", "Book details updated successfully.")

        except Exception as e:
            messagebox.showinfo("Error", str(e))


    SubmitBtn = Button(labelFrame, text="Find", bg='#F05454', fg='black', bd=0, font=('Consolas', 13), command=searchBook)
    SubmitBtn.place(relx=0.8, rely=0.1, relwidth=0.12, relheight=0.04)

    ModifyBtn = Button(labelFrame, text="Modify", bg='#F05454', fg='black', bd=0, font=('Consolas', 13), command=modifyBook)
    ModifyBtn.place(relx=0.8, rely=0.6, relwidth=0.12, relheight=0.04)

    quitBtn = Button(root, text="Quit", bg='#F05454', fg='black', bd=0, font=('Consolas', 13), command=root.destroy)
    quitBtn.place(relx=0.37, rely=0.9, relwidth=0.28, relheight=0.08)

    root.mainloop()

if __name__ == "__main__":
    modify()
