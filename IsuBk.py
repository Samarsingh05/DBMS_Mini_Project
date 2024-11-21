from tkinter import *
from PIL import ImageTk, Image
import json
from tkinter import messagebox
from datetime import datetime, timedelta
import pymysql 

mypass = "Samar05@"
mydatabase = "library2"

con = pymysql.connect(host="localhost", user="root", password=mypass, database=mydatabase)
cur = con.cursor()

ISSUED_BOOKS = "issued_books.json"
issueTable = "books_issued"
bookTable = "books"

allBookids = []

def issue():
    global issueBtn, labelFrame, lb1, inf1, inf2, quitBtn, root, Canvas1

    bookid = inf1.get()
    issueto = inf2.get()
    issue_datetime = datetime.now()
    issue_date = issue_datetime.strftime('%Y-%m-%d')
    issue_time = issue_datetime.strftime('%H:%M:%S')

    issueBtn.destroy()
    labelFrame.destroy()
    lb1.destroy()
    inf1.destroy()
    inf2.destroy()

    extractBookid = f"SELECT bookid FROM {bookTable}"
    try:
        cur.execute(extractBookid)
        allBookids.extend([i[0] for i in cur])

        #NESTED QUERY

        if bookid in allBookids:
            checkAvail = f"""
            SELECT status 
            FROM {bookTable} 
            WHERE bookid = (SELECT bookid FROM {bookTable} WHERE bookid = '{bookid}') 
            AND status IN ('avail', 'available','AVAILABLE','Available')
            """

            cur.execute(checkAvail)
            check = cur.fetchone()

            if check:
                # Check if customer exists in database
                checkCustomer = "SELECT username FROM customer_credentials WHERE username = %s"
                cur.execute(checkCustomer, (issueto,))
                customer = cur.fetchone()
                
                if not customer:
                    messagebox.showinfo("Error", "Invalid Username. Customer not found.")
                    return

                issueSql = f"INSERT INTO {issueTable} (bookid, issueto, issue_date, issue_time, fare) VALUES ('{bookid}', '{issueto}', '{issue_date}', '{issue_time}', 10)"

                try:
                    cur.execute(issueSql)
                    con.commit()
                    messagebox.showinfo('Success', "Book Issued Successfully")

                    issued_data = {"bookid": bookid, "issued_to": issueto, "issue_date": issue_date, "issue_time": issue_time, "fare": 10}
                    try:
                        with open("issued_books.json", "r+") as file:
                            data = json.load(file)
                            data.append(issued_data)
                            file.seek(0)
                            json.dump(data, file, indent=4)
                    except FileNotFoundError:
                        with open("issued_books.json", "w") as file:
                            json.dump([issued_data], file, indent=4)
                    except json.JSONDecodeError:
                        with open("issued_books.json", "w") as file:
                            json.dump([issued_data], file, indent=4)

                    root.after(1200000, update_fare, issued_data, bookid) 

                except Exception as e:
                    messagebox.showinfo("Error", f"Failed to issue book: {str(e)}")
            else:
                messagebox.showinfo('Message', "Book Already Issued")
        else:
            messagebox.showinfo("Error", "Book ID not present")

    except Exception as e:
        messagebox.showinfo("Error", f"Can't fetch Book IDs: {str(e)}")

    allBookids.clear()
    root.destroy()

def update_fare(issued_data, bookid):
    # Update fare in the JSON file every 20 minutes
    issued_data["fare"] += 20

    try:
        with open("issued_books.json", "r+") as file:
            data = json.load(file)
            for i, book in enumerate(data):
                if book["bookid"] == bookid:
                    data[i] = issued_data
                    break
            file.seek(0)
            json.dump(data, file, indent=4)
    except Exception as e:
        messagebox.showinfo("Error", f"Failed to update issued books file: {str(e)}")

    # Schedule the next fare update in another 20 minutes
    root.after(1200000, update_fare, issued_data, bookid)

def issueBook():
    global issueBtn, labelFrame, lb1, inf1, inf2, quitBtn, root, Canvas1

    root = Tk()
    root.title("Issuing Book")
    root.minsize(width=800, height=900)
    root.maxsize(width=800, height=900)

    Canvas1 = Canvas(root)
    Canvas1.config(bg="#373a40")
    Canvas1.pack(expand=True, fill=BOTH)

    headingFrame1 = Frame(root, bd=0)
    headingFrame1.place(relx=0.25, rely=0.1, relwidth=0.5, relheight=0.13)

    headingLabel = Label(headingFrame1, text="Issuing Books", bg='#ff414d', fg='black', font=('Consolas', 18))
    headingLabel.place(relx=0, rely=0, relwidth=1, relheight=1)

    labelFrame = Frame(root, bg='#222831')
    labelFrame.place(relx=0.1, rely=0.35, relwidth=0.8, relheight=0.4)

    lb1 = Label(labelFrame, text="Book ID:", bg='#222831', fg='white', font=('Consolas', 13))
    lb1.place(relx=0.05, rely=0.2)
    inf1 = Entry(labelFrame)
    inf1.place(relx=0.3, rely=0.2, relwidth=0.62)

    lb2 = Label(labelFrame, text="Issued To:", bg='#222831', fg='white', font=('Consolas', 13))
    lb2.place(relx=0.05, rely=0.6)
    inf2 = Entry(labelFrame)
    inf2.place(relx=0.3, rely=0.6, relwidth=0.62)

    issueBtn = Button(root, text="Issue", bg='#F05454', fg='black', bd=0, font=('Consolas', 13), command=issue)
    issueBtn.place(relx=0.092, rely=0.9, relwidth=0.20, relheight=0.08)

    quitBtn = Button(root, text="Quit", bg='#F05454', fg='black', bd=0, font=('Consolas', 13), command=root.destroy)
    quitBtn.place(relx=0.70, rely=0.9, relwidth=0.20, relheight=0.08)

    root.mainloop()