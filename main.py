from tkinter import *
from PIL import ImageTk, Image
import pymysql
from tkinter import messagebox

from AddBk import *
from DelBk import *
from ViewBk import *
from IsuBk import *
from RtrnBk import *
from srchBk import *
from mdfyBk import *
from IssuedBooks import *
from AllBk import *

mypass = "Samar05@"
mydatabase = "library2"

con = pymysql.connect(host="localhost", user="root", password=mypass, database=mydatabase)
cur = con.cursor()

root = Tk()
root.title("Library")
root.minsize(width=800, height=900)
root.maxsize(width=800, height=900)

same = True
n = 0.35

background_image = Image.open("lib.png")
[imageSizeWidth, imageSizeHeight] = background_image.size
newImageSizeWidth = int(imageSizeWidth * n)
newImageSizeHeight = int(imageSizeHeight * n)
background_image = background_image.resize((newImageSizeWidth, newImageSizeHeight), Image.LANCZOS)
img = ImageTk.PhotoImage(background_image)

Canvas1 = Canvas(root)
Canvas1.create_image(400, 500, image=img)
Canvas1.config(bg="#373a40", width=newImageSizeWidth, height=newImageSizeHeight, bd=0)
Canvas1.pack(expand=True, fill=BOTH)

headingFrame1 = Frame(root, bd=0)
headingFrame1.place(relx=0.2, rely=0.1, relwidth=0.6, relheight=0.14)

headingLabel = Label(headingFrame1, text="Welcome to\nOur Book Barn", bg='#ff414d', fg='black', font=('Consolas', 18))
headingLabel.place(relx=0, rely=0, relwidth=1, relheight=1)

# Define functions to show buttons based on user type
def show_admin_buttons():
    btn0 = Button(root, text="View All Books", bg="#e8e8e8", bd=0, fg='black', font=('Consolas', 13), command=display_book_logs)
    btn0.place(relx=0.28, rely=0.33, relwidth=0.45, relheight=0.07)

    btn1 = Button(root, text="Add A Book", bg="#e8e8e8", bd=0, fg='black', font=('Consolas', 13), command=addBook)
    btn1.place(relx=0.28, rely=0.4, relwidth=0.45, relheight=0.07)

    btn2 = Button(root, text="Delete A Book", bg="#393e46", bd=0, fg='black', font=('Consolas', 13), command=delete)
    btn2.place(relx=0.28, rely=0.47, relwidth=0.45, relheight=0.07)

    btn7 = Button(root, text="Modify A Book", bg="#AAAAAA", bd=0, fg='black', font=('Consolas', 13), command=modify)
    btn7.place(relx=0.28, rely=0.82, relwidth=0.45, relheight=0.07)

def show_customer_buttons():
    messagebox.showinfo("Customer Access", "Limited features are available for customers.")

    btn7 = Button(root, text="Issued Books", bg="#AAAAAA", bd=0, fg='black', font=('Consolas', 13), command=issuedBooks)
    btn7.place(relx=0.28, rely=0.47, relwidth=0.45, relheight=0.07)

btn3 = Button(root, text="Check Book List", bg="#F05454", bd=0, fg='black', font=('Consolas', 13), command=View)
btn3.place(relx=0.28, rely=0.54, relwidth=0.45, relheight=0.07)

btn4 = Button(root, text="Issue A Book", bg="#30475e", bd=0, fg='black', font=('Consolas', 13), command=issueBook)
btn4.place(relx=0.28, rely=0.61, relwidth=0.45, relheight=0.07)

btn5 = Button(root, text="Return A Book", bg="#222831", bd=0, fg='#5c6e91', font=('Consolas', 13), command=returnBook)
btn5.place(relx=0.28, rely=0.68, relwidth=0.45, relheight=0.07)

btn6 = Button(root, text="Search A Book", bg="#65d6ce", bd=0, fg='black', font=('Consolas', 13), command=search)
btn6.place(relx=0.28, rely=0.75, relwidth=0.45, relheight=0.07)

def start_library_system(user_type, username=None):
    global current_user
    if user_type == "admin":
        show_admin_buttons()
    elif user_type == "customer" and username:
        current_user = username  # Set the current user
        show_customer_buttons()
    root.mainloop()


if __name__ == "__main__":
    start_library_system(user_type="admin")