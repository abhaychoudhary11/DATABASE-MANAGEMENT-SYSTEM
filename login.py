from tkinter import *
from PIL import ImageTk,Image 
from tkinter import messagebox


def logfun():
    if user.get()=='' or password.get()=='':
        messagebox.showerror('Error', 'Please Enter User Name and Password......!')
    elif user.get()=='Abhay' and password.get()=='au23b1003':
        messagebox.showinfo('Success',f'Welcome {user.get()} in Bank Management System...!')
        home.destroy()
        import maindb
    else:
        messagebox.showerror('Failure','Check your User Name and Password.....!')

home = Tk() 
home.title('BANK DATABASE MANAGEMENT')
home.geometry('1566x790')
home.resizable(True,True)

#backgroundimage
img=Image.open("bgbank.png")
img=img.resize((1566,790))
bg= ImageTk.PhotoImage(img)
Label(home,image=bg,bg='white').place(x=0,y=0)

#frame
frame=Frame(home,width=600,height=400,bg="#095e7d")
frame.place(x=100,y=120)
heading=Label(frame,text='Login',fg='white',bg='#095e7d',font=('Poppins',19,'bold'))
heading.place(x=170,y=5)

#id password    

#ID
ulogo= PhotoImage(file='user1.png')
Label(frame,image=ulogo,width=50,height=50,bg='#095e7d',fg='white').place(x=38,y=59)
Label(frame,text='User Id',fg='white',bg='#095e7d',font=('Poppins',14)).place(x=70,y=90)
user = Entry(frame,width=45,fg='black',border=2,bg="white",font=('Poppins',11))
user.place(x=30,y=120)
    
#PASSWORD   
passwordlogo= PhotoImage(file='password1.png')
Label(frame,image=passwordlogo,width=50,height=50,bg='#095e7d',fg='white').place(x=39,y=159)
Label(frame,text='Password',fg='white',bg='#095e7d',font=('Poppins')).place(x=70,y=190)
password = Entry(frame,width=45,show='*',fg='black',border=2,bg="white",font=('Poppins',11))
password.place(x=30,y=220)

#button
Button(frame,width=20,pady=7,text='Login',bg='#57a1f8',fg='white',border=0,command=logfun).place(x=140 ,y=280)

home.mainloop()
