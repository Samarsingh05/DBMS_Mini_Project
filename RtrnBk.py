from tkinter import *
from PIL import ImageTk, Image
from tkinter import messagebox
import json
from datetime import date
import pymysql


mypass = "Samar05@"
mydatabase = "library2"

con = pymysql.connect(host="localhost", user="root", password=mypass, database=mydatabase)
cur = con.cursor()

issueTable = "books_issued"
bookTable = "books"

allBookids = []

def returnn():
    global allBookids, bookInfo1, root
    
    bookid = bookInfo1.get()
    allBookids = []

    extractBookid = f"SELECT bookid FROM {issueTable}"
    try:
        cur.execute(extractBookid)
        allBookids = [i[0] for i in cur.fetchall()]
        
        if bookid in allBookids:
            deleteIssued = f"DELETE FROM {issueTable} WHERE bookid = %s"

            
            try:
                cur.execute(deleteIssued, (bookid,))
                con.commit()
                
                messagebox.showinfo('Success', "Book Returned Successfully")

                update_fare = f"UPDATE {issueTable} SET fare = NULL WHERE bookid = '{bookid}'"

                try:
                    with open("issued_books.json", "r+") as file:
                        issued_data = json.load(file)
                        updated_data = [entry for entry in issued_data if entry["bookid"] != bookid]
                        file.seek(0)
                        json.dump(updated_data, file, indent=4)
                        file.truncate()
                except FileNotFoundError:
                    messagebox.showinfo("Error", "issued_books.json file not found.")
                except json.JSONDecodeError:
                    messagebox.showinfo("Error", "Error decoding issued_books.json file.")
            except Exception as e:
                messagebox.showinfo("Error", f"Failed to return book: {str(e)}")
        else:
            messagebox.showinfo("Error", "Book ID not found in issued records")
        
        root.destroy()
    except Exception as e:
        messagebox.showinfo("Error", f"Can't fetch Book IDs: {str(e)}")
        root.destroy()

def returnBook(): 
    global bookInfo1, SubmitBtn, quitBtn, Canvas1, con, cur, root, labelFrame, lb1
    
    root = Tk()
    root.title("Returning Book")
    root.minsize(width=800, height=900)

    Canvas1 = Canvas(root, bg="#373a40")
    Canvas1.pack(expand=True, fill=BOTH)
        
    headingFrame1 = Frame(root)
    headingFrame1.place(relx=0.25, rely=0.1, relwidth=0.5, relheight=0.13)

    headingLabel = Label(headingFrame1, text="Returning Books", bg='#ff414d', fg='black', font=('Consolas', 18))
    headingLabel.place(relx=0, rely=0, relwidth=1, relheight=1)

    labelFrame = Frame(root, bg='#222831')
    labelFrame.place(relx=0.1, rely=0.35, relwidth=0.8, relheight=0.4)

    lb1 = Label(labelFrame, text="Book ID:", bg='#222831', fg='white', font=('Consolas', 13))
    lb1.place(relx=0.05, rely=0.5)

    bookInfo1 = Entry(labelFrame)
    bookInfo1.place(relx=0.3, rely=0.5, relwidth=0.62)

    SubmitBtn = Button(root, text="Return", bg='#F05454', fg='black', command=returnn)
    SubmitBtn.place(relx=0.092, rely=0.9, relwidth=0.20, relheight=0.08)

    quitBtn = Button(root, text="Quit", bg='#F05454', fg='black', command=root.destroy)
    quitBtn.place(relx=0.70, rely=0.9, relwidth=0.20, relheight=0.08)

    root.mainloop()
