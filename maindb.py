from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
from tkinter import ttk
from tkinter import filedialog
import csv
import mysql.connector  
import subprocess 

def connectdb():
    try:
        global conn
        conn = mysql.connector.connect(
            host='localhost',      
            user='root',                  
            password='Sona0807',    
            database='assignment_3'          
        )
        global cur
        cur = conn.cursor()
        conn.commit()
    except Exception as e:
        messagebox.showerror('Database Error', f'Error connecting to the database: {e}')



def showaccountdetail():
    swindow = Tk()
    swindow.title("Search Account Details")
    swindow.geometry("400x200")

    aidlabel = Label(swindow, text="Enter Account ID:")
    aidlabel.pack()
    aidentry = Entry(swindow, width=30)
    aidentry.pack()

    def searchaccount():
        aid = int(aidentry.get())
        cur.execute("SELECT a.AId, c.Name, a.AType, a.Balance, c.Address, c.Contact, c.Email FROM accounts a JOIN customer c ON a.CId = c.CId WHERE a.AId = %s", (aid,))
        rows = cur.fetchall()
        dframe.delete(*dframe.get_children())
        for row in rows:
            dframe.insert('', 'end', values=row)
        swindow.destroy()

    sbuttom = Button(swindow, text="Search", command=searchaccount)
    sbuttom.pack()

    swindow.mainloop()

def addaccount():
    wwindow = Tk()
    wwindow.title("Add Account")
    wwindow.geometry("400x500")

    aidlabel = Label(wwindow, text="Enter Account ID:")
    aidlabel.pack()
    aidentry = Entry(wwindow, width=30)
    aidentry.pack()

    cidlabel = Label(wwindow, text="Enter Customer ID:")
    cidlabel.pack()
    cidentry = Entry(wwindow, width=30)
    cidentry.pack()

    atypelabel = Label(wwindow, text="Enter Account Type (Current, Saving, FD):")
    atypelabel.pack()
    atypeentry = Entry(wwindow, width=30)
    atypeentry.pack()

    blabel = Label(wwindow, text="Enter Initial Balance:")
    blabel.pack()
    bentry = Entry(wwindow, width=30)
    bentry.pack()

    def add_account():
        try:
            account_id = int(aidentry.get())
            customer_id = int(cidentry.get())
            account_type = atypeentry.get()
            initial_balance = float(bentry.get())
            cur.execute("SELECT COUNT(*) FROM customer WHERE CId = %s", (customer_id,))
            if cur.fetchone()[0] == 0:
                messagebox.showerror("Error", "Customer ID does not exist")
                return
            cur.execute("SELECT COUNT(*) FROM accounts WHERE AId = %s", (account_id,))
            if cur.fetchone()[0] > 0:
                messagebox.showerror("Error", "Account ID already exists")
                return
            cur.execute("INSERT INTO accounts (AId, CId, AType, Balance) VALUES (%s, %s, %s, %s)", 
                        (account_id, customer_id, account_type, initial_balance))
            conn.commit()
            cur.execute("SELECT a.AId, c.Name, a.AType, a.Balance, c.Address, c.Contact, c.Email "
                        "FROM accounts a JOIN customer c ON a.CId = c.CId "
                        "WHERE a.AId = %s", (account_id,))
            rows = cur.fetchall()
            dframe.delete(*dframe.get_children())
            for row in rows:
                dframe.insert('', 'end', values=row)

            messagebox.showinfo("Success", "Account added successfully")
        except ValueError:
            messagebox.showerror("Error", "Invalid input. Please enter numeric values for IDs and Balance.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
        finally:
            wwindow.destroy()

    add_button = Button(wwindow, text="Add Account", command=add_account)
    add_button.pack()
    wwindow.mainloop()

def withdraw():
    wwindow = Tk()
    wwindow.title("Withdrawal")
    wwindow.geometry("300x150")

    aidlabel = Label(wwindow, text="Enter Account ID:")
    aidlabel.pack()
    aidentry = Entry(wwindow, width=30)
    aidentry.pack()

    amountlabel = Label(wwindow, text="Enter amount to withdraw:")
    amountlabel.pack()
    amountentry = Entry(wwindow, width=30)
    amountentry.pack()

    def withdraw_amount():
        aid = int(aidentry.get())
        amount = int(amountentry.get())
        cur.execute("SELECT Balance FROM accounts WHERE AId = %s", (aid,))
        balance = cur.fetchone()[0]
        if balance >= amount:
            cur.execute("UPDATE accounts SET Balance = Balance - %s WHERE AId = %s", (amount, aid))
            conn.commit()
            messagebox.showinfo("Success", "Withdrawal successful")
            cur.execute("SELECT a.AId, c.Name, a.AType, a.Balance, c.Address, c.Contact, c.Email FROM accounts a JOIN customer c ON a.CId = c.CId WHERE a.AId = %s", (aid,))
            rows = cur.fetchall()
            dframe.delete(*dframe.get_children())
            for row in rows:
                dframe.insert('', 'end', values=row)
        else:
            messagebox.showerror("Error", "Insufficient balance")
        wwindow.destroy()

    wbutton = Button(wwindow, text="Withdraw", command=withdraw_amount)
    wbutton.pack()
    wwindow.mainloop()

def deposit():
    dwindow = Tk()
    dwindow.title("Deposit")
    dwindow.geometry("300x150")

    aidlabel = Label(dwindow, text="Enter Account ID:")
    aidlabel.pack()
    aidentry = Entry(dwindow, width=30)
    aidentry.pack()

    amountlabel = Label(dwindow, text="Enter amount to deposit:")
    amountlabel.pack()
    amountentry = Entry(dwindow, width=30)
    amountentry.pack()

    def deposit_amount():
        aid = int(aidentry.get())
        amount = int(amountentry.get())
        cur.execute("SELECT Balance FROM accounts WHERE AId = %s", (aid,))
        balance = cur.fetchone()[0]
        cur.execute("UPDATE accounts SET Balance = Balance + %s WHERE AId = %s", (amount, aid))
        conn.commit()
        messagebox.showinfo("Success", "Deposit successful")
        cur.execute("SELECT a.AId, c.Name, a.AType, a.Balance, c.Address, c.Contact, c.Email FROM accounts a JOIN customer c ON a.CId = c.CId WHERE a.AId = %s", (aid,))
        rows = cur.fetchall()
        dframe.delete(*dframe.get_children())
        for row in rows:
            dframe.insert('', 'end', values=row)
        dwindow.destroy()

    dbutton = Button(dwindow, text="Deposit", command=deposit_amount)
    dbutton.pack()
    dwindow.mainloop()

def showtransaction():
    twindow = Tk()
    twindow.title("Show Transaction")
    twindow.geometry("400x200")

    cnamelabel = Label(twindow, text="Enter Customer Name:")
    cnamelabel.pack()
    cnameentry = Entry(twindow, width=30)
    cnameentry.pack()

    def searchtransaction():
        customer_name = cnameentry.get()
        cur.execute("select a.AId, c.Name, a.AType, a.Balance, c.Address, c.Contact, c.Email from accounts a join customer c on a.CId = c.CId where c.Name = %s", (customer_name,))
        rows = cur.fetchall()
        dframe.delete(*dframe.get_children())
        for row in rows:
            dframe.insert('', 'end', values=row)
        twindow.destroy()

    sbutton = Button(twindow, text="Search", command=searchtransaction)
    sbutton.pack()

    twindow.mainloop()

def exporttransaction():
    exwindow = Tk()
    exwindow.title("Export Transaction History")
    exwindow.geometry("400x200")

    cnamelabel = Label(exwindow, text="Customer Name:")
    cnamelabel.pack()
    cnameentry = Entry(exwindow, width=30)
    cnameentry.pack()

    aidlabel = Label(exwindow, text="Account ID:")
    aidlabel.pack()
    aidentry = Entry(exwindow, width=30)
    aidentry.pack()

    def export():
        customer_name = cnameentry.get()
        account_id = aidentry.get()
        if not account_id:
            messagebox.showerror("Error", "Please enter the account ID")
            return
        cur.execute("SELECT t.TId, t.TDate, t.TType, t.Amount, c.Name, c.Address, c.Contact, c.Email FROM customer c JOIN accounts a ON c.CId = a.CId JOIN transaction t ON a.AId = t.AId WHERE a.AId = %s", (account_id,))
        rows = cur.fetchall()
        if not rows:
            messagebox.showerror("Error", "No transaction history found for the account")
            return
        with open('transaction_history.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["TId", "TDate", "TType", "Amount", "Name", "Address", "Contact", "Email"])
            writer.writerows(rows)
        messagebox.showinfo("Success", "Transaction history exported to transaction_history.csv")
        exwindow.destroy()

    export_button = Button(exwindow, text="Export", command=export)
    export_button.pack()

    exwindow.mainloop()

# Initialize the main window
mainbank = Tk()
mainbank.geometry('1566x790')
mainbank.title("Book Management System")
mainbank.resizable(True, True)

# Set the background of the application
img=Image.open("maingbg.png")
img=img.resize((1566,790))
bg= ImageTk.PhotoImage(img)
Label(mainbank,image=bg,bg='white').place(x=0,y=0)
heading=Label(mainbank,text='BANK MANAGEMENT SYSTEM',fg='white',bg='#095e7d',font=('Poppins',25,'bold'))
heading.place(x=520,y=30)

#up frame
uframe=Frame(mainbank,width=1366,height=350,bg="white")
uframe.place(x=90,y=120)

#down frame 
doframe=Frame(mainbank,width=1366,height=230,bg='white')
doframe.place(x=90,y=540)

# uaccount detail
adframe = Frame(uframe, width=200, height=200, bg='sky blue')
adframe.place(x=40, y=70)
btn1=Button(uframe,width=20,pady=7,text='Account Detail',bg='#57a1f8',fg='white',border=0,command=showaccountdetail).place(x=65 ,y=290)
adimg=ImageTk.PhotoImage(file='accountdetail.png')
Label(adframe,image=adimg,bg='white').place(x=6.5,y=6.5)

#add account
aaframe = Frame(uframe, width=200, height=200, bg='sky blue')
aaframe.place(x=255, y=70)
btn1=Button(uframe,width=20,pady=7,text='Add Account',bg='#57a1f8',fg='white',border=0,command=addaccount).place(x=285 ,y=290)
aaimg=ImageTk.PhotoImage(file='createaccount.png')
Label(aaframe,image=aaimg,bg='white',height=180,width=180).place(x=6.5,y=6.5)

# withdraw
wframe = Frame(uframe, width=200, height=200, bg='sky blue')
wframe.place(x=470, y=70)
btn2=Button(uframe,width=20,pady=7,text='Withdrawal',bg='#57a1f8',fg='white',border=0,command=withdraw).place(x=495 ,y=290)
wimg=ImageTk.PhotoImage(file='withdrawal.png')
Label(wframe,image=wimg,bg='white',height=180,width=180).place(x=6.5,y=6.5)

# deposti frame
dframe = Frame(uframe, width=200, height=200, bg='sky blue')
dframe.place(x=690, y=70)
btn3=Button(uframe,width=20,pady=7,text='Deposit',bg='#57a1f8',fg='white',border=0,command=deposit).place(x=715 ,y=290)
dimg=ImageTk.PhotoImage(file='deposit.png')
Label(dframe,image=dimg,bg='white',height=180,width=180).place(x=6.5,y=6.5)

# transaction
tframe = Frame(uframe, width=200, height=200, bg='sky blue')
tframe.place(x=910, y=70)
btn4=Button(uframe,width=20,pady=7,text='Show Transaction',bg='#57a1f8',fg='white',border=0,command=showtransaction).place(x=935 ,y=290)
timg=ImageTk.PhotoImage(file='showtransaction.png')
Label(tframe,image=timg,bg='white',height=180,width=180).place(x=6.5,y=6.5)

# exporttransaction
exframe = Frame(uframe, width=200, height=200, bg='sky blue')
exframe.place(x=1130, y=70)
btn5=Button(uframe,width=20,pady=7,text='Export Transaction',bg='#57a1f8',fg='white',border=0,command=exporttransaction).place(x=1155 ,y=290)
eximg=ImageTk.PhotoImage(file='exporttransaction.png')
Label(exframe,image=eximg,bg='white',height=180,width=180).place(x=6.5,y=6.5)

# result in down frame
dframe = ttk.Treeview(doframe, columns=('AId', 'Name', 'AType', 'Balance','Address','Contact','Email'))
dframe.pack(fill='both', expand=True)

# column
dframe.column("#0", width=0, stretch=NO)
dframe.column("AId", anchor=W, width=100)
dframe.column("Name", anchor=W, width=200)
dframe.column("AType", anchor=W, width=100)
dframe.column("Balance", anchor=W, width=100)
dframe.column("Address", anchor=W, width=300)
dframe.column("Contact", anchor=W, width=200)
dframe.column("Email", anchor=W, width=200)

# Create headings
dframe.heading("#0", text="", anchor=W)
dframe.heading("AId", text="Account ID", anchor=W)
dframe.heading("Name", text="Customer Name", anchor=W)
dframe.heading("AType", text="Account Type", anchor=W)
dframe.heading("Balance", text="Balance", anchor=W)
dframe.heading("Address", text="Address", anchor=W)
dframe.heading("Contact", text="Contact", anchor=W)
dframe.heading("Email", text="Email", anchor=W)


connectdb()
mainbank.mainloop()
if conn.is_connected(): 
    conn.close()

