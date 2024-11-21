import json
from tkinter import messagebox, Tk, Listbox, Scrollbar, Frame
import pymysql

def issuedBooks():
    # Database connection
    try:
        con = pymysql.connect(host="localhost", user="root", password="Samar05@", database="library2")
        cur = con.cursor()
    except pymysql.MySQLError as e:
        messagebox.showinfo("Error", f"Database connection failed: {e}")
        return

    # Load the customer username from customer_login.json
    try:
        with open("customer_login.json", "r") as file:
            customer_data = json.load(file)
            username = next(reversed(customer_data), None)
            
            if not username:
                messagebox.showinfo("Error", "No username found in customer_login.json.")
                return
    except FileNotFoundError:
        messagebox.showinfo("Error", "customer_login.json file not found.")
        return
    except json.JSONDecodeError:
        messagebox.showinfo("Error", "Error decoding customer_login.json file.")
        return
    
    # Query the count of books issued to the user
    #AGGREGATE QUERY
    count_query = f"SELECT COUNT(*) FROM books_issued WHERE issueto = '{username}'"
    cur.execute(count_query)
    total_books_issued = cur.fetchone()[0]
    
    # Load issued_books.json and filter books for this username
    try:
        with open("issued_books.json", "r") as file:
            issued_data = json.load(file)
            
            # Filter books issued to the current customer
            user_books = [entry for entry in issued_data if entry["issued_to"] == username]
            
            if not user_books:
                messagebox.showinfo("Info", f"No books issued to {username}.")
                return
    except FileNotFoundError:
        messagebox.showinfo("Error", "issued_books.json file not found.")
        return
    except json.JSONDecodeError:
        messagebox.showinfo("Error", "Error decoding issued_books.json file.")
        return

    # Create the Tkinter window to display issued books
    root = Tk()
    root.title("Books Issued to You")
    root.geometry("400x400")

    # Create a listbox with a scrollbar to display issued books
    frame = Frame(root)
    frame.pack(pady=10)
    
    scroll = Scrollbar(frame, orient="vertical")
    listbox = Listbox(frame, yscrollcommand=scroll.set, width=50, height=15)
    scroll.config(command=listbox.yview)
    scroll.pack(side="right", fill="y")
    listbox.pack(side="left", fill="both", expand=True)

    # Display total count and issued books in the listbox
    listbox.insert("end", f"Books issued to {username}:")
    listbox.insert("end", f"Total books issued: {total_books_issued}")
    listbox.insert("end", "-" * 40)

    for book in user_books:
        listbox.insert("end", f"Book ID: {book['bookid']}, Issue Date: {book['issue_date']}")
    
    root.mainloop()
    con.close()

# Run the function to display issued books for the current user
if __name__ == "__main__":
    issuedBooks()
