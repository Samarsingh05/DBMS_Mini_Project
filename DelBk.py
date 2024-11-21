from tkinter import *
from PIL import ImageTk,Image
from tkinter import messagebox
import pymysql


# root password and database
mypass = "Samar05@"
mydatabase="library2"

con = pymysql.connect(host="localhost",user="root",password=mypass,database=mydatabase)
cur = con.cursor()

# book table names
issueTable = "books_issued" 
bookTable = "books" #Book Table


def deleteBook():
    bookid = bookInfo1.get()

    # Check if the book is issued
    checkIssuedSql = f"SELECT * FROM {issueTable} WHERE bookid = '{bookid}'"
    
    try:
        cur.execute(checkIssuedSql)
        issuedBook = cur.fetchone()
        
        if issuedBook:
            # If the book is issued, show a prompt
            messagebox.showinfo('Error', 'This book is currently issued and cannot be deleted.')
        else:
            # If the book is not issued, proceed with deletion
            deleteSql = f"DELETE FROM {bookTable} WHERE bookid = '{bookid}'"
            
            cur.execute(deleteSql)
            con.commit()
            messagebox.showinfo('Success', 'Book has been deleted successfully.')
    except Exception as e:
        print(e)
        messagebox.showinfo('Error', 'An error occurred. Please recheck the Book ID.')

    bookInfo1.delete(0, END)
    root.destroy()
    
def delete(): 
    
    global bookInfo1,bookInfo2,bookInfo3,bookInfo4,Canvas1,con,cur,bookTable,root
    
    root = Tk()
    root.title("Deleting Book")
    root.minsize(width=800,height=900)
    root.maxsize(width=800,height=900)

    
    Canvas1 = Canvas(root)
    
    Canvas1.config(bg="#373a40")
    Canvas1.pack(expand=True,fill=BOTH)
        
    headingFrame1 = Frame(root,bd=0)
    headingFrame1.place(relx=0.25,rely=0.1,relwidth=0.5,relheight=0.13)

    headingLabel = Label(headingFrame1, text="Deleting Books", bg='#ff414d', fg='black', font=('Consolas',18))
    headingLabel.place(relx=0,rely=0, relwidth=1, relheight=1)


    labelFrame = Frame(root,bg='#222831')
    labelFrame.place(relx=0.1,rely=0.35,relwidth=0.8,relheight=0.4)  
        
    # Book ID to Delete
    lb2 = Label(labelFrame,text="Book ID : ", bg='#222831', fg='white', font=('Consolas',13))
    lb2.place(relx=0.05,rely=0.5)
        
    bookInfo1 = Entry(labelFrame)
    bookInfo1.place(relx=0.3,rely=0.5, relwidth=0.62)
    
    #Submit Button
    SubmitBtn = Button(root,text="Submit",bg='#F05454', fg='black', bd=0, font=('Consolas',13),command=deleteBook)
    SubmitBtn.place(relx=0.092,rely=0.9, relwidth=0.20,relheight=0.08)
    
    quitBtn = Button(root,text="Quit",bg='#F05454', fg='black', bd=0, font=('Consolas',13), command=root.destroy)
    quitBtn.place(relx=0.70,rely=0.9, relwidth=0.20,relheight=0.08)
    
    root.mainloop()