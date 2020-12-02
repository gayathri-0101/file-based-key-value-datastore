import sqlite3
import os
import time
#The saved database file can be viewed by using DB Browser for SQL lite

#creating a table in our data store to store key value pairs
def create_table():
    conn=sqlite3.connect("key-value data store.db") #if doesnt exists this creates a file
    c=conn.cursor()  
    c.execute("CREATE TABLE IF NOT EXISTS keyvaluetable(key text,value text)")
    ##key and value are of type text
    conn.commit()
    conn.close()
from tkinter import *
from tkinter import messagebox
def create():
    d=[] 
    create_table()
    key=t2.get()      #get the key 
    value=t3.get()     #get the value
    timeout=t4.get()
    conn=sqlite3.connect("key-value data store.db")
    cur=conn.cursor()
    cur.execute("SELECT value FROM keyvaluetable WHERE key=?",(key,)) #find whether it exists
    val=cur.fetchall()
    conn.close()
    if key=="":
        messagebox.showerror("Error","The key is empty")
    elif value=="":
        messagebox.showerror("Error","The value is empty")
    elif len(val)!=0:
        messagebox.showerror("Error","The key is already defined please enter a new one")
    elif len(key)>32:
        messagebox.showerror("Error","The key is more than 32 chars")
    # key is a string always

    elif not(key.isalpha()):
        messagebox.showerror("Error","The key must contain only alphabets")
    else:
      if(len(key))<32:                ## key length capped at 32   
        d.append(key)
        if len(d)<(1024*1020*1024):    #file size should be less than 1GB
          conn=sqlite3.connect("key-value data store.db")
          cur=conn.cursor()
          if timeout==0 or timeout=="":
              cur.execute("INSERT INTO keyvaluetable VALUES(?,?)",(key,value,))
              s="\nThe key value pair created are --> "+key+":"+str(value)
              t5.insert(INSERT,s)
              
          else:
              l=[value,time.time()+int(timeout)]
              cur.execute("INSERT INTO keyvaluetable VALUES(?,?)",(key,value,))
        else:
            messagebox.showerror("Error","Out of memory")
      conn.commit()
      conn.close()
          
#locate the value for the corresponding table in the database and return the value in json format
def read():
    create_table()
    key1=t2.get()
    conn=sqlite3.connect("key-value data store.db")
    cur=conn.cursor()
    cur.execute("SELECT value FROM keyvaluetable WHERE key=?",(key1,))
    val=cur.fetchall()
    if val==[]:                     #if not present in datastore
        messagebox.showerror("Error","Key is not present in data store")
        return
    conn.close()
    s=""
    s=key1+":"+str(val[0])
    #print value as json format
    s="\nThe value at the key is : "+s
    t5.insert(INSERT,s)
    
#to delete the corresponding key and value pair
def delete():
    key1=t2.get()
    conn=sqlite3.connect("key-value data store.db")
    cur=conn.cursor()
    cur.execute("DELETE FROM keyvaluetable WHERE key=?",(key1,))
    s="\nThe key deleted is --> "+key1
    t5.insert(INSERT,s)
    conn.commit()
    conn.close()

def changepath():
    s=t1.get()
    if s!="":
        os.chdir(s)
    return None

#tkinter is used for taking inputs from the user to provide a friendly user interface  
from tkinter import messagebox

root=Tk()

l=Label(root,background="cyan",text="Click next for optional file save path or specify the path and click save and next")

l.grid(row=0,column=0)
l1=Label(root,text="file path(optional)",width=60)
l1.grid(row=1,column=0)

t1=Entry(root,width=60,bd=4)
t1.grid(row=1,column=1)
l7=Label(root,text="Click on SAVE and then proceed")
l7.grid(row=2,column=0)

b1=Button(root,text="save",width=60,height=2,command=changepath)
b1.grid(row=3,column=0)

b2=Button(root,text="proceed",width=60,height=2,command=root.destroy)
b2.grid(row=3,column=1)
root.title("File based key-value datastore")
root.mainloop()


window=Tk()

l2=Label(window,text="Key",background="cyan",width=40)
l2.grid(row=0,column=0)

t2=Entry(window,width=40,bd=4)
t2.grid(row=0,column=1)

l3=Label(window,text="Value",background="cyan",width=40)
l3.grid(row=1,column=0)

t3=Entry(window,width=40,bd=4)
t3.grid(row=1,column=1)

l4=Label(window,text="Time to live(optional)",background="cyan",width=40)
l4.grid(row=2,column=0)

t4=Entry(window,width=40,bd=4)
t4.grid(row=2,column=1)

b3=Button(window,text="create",width=30,command=create)
b3.grid(row=3,column=0)

b4=Button(window,text="read",width=30,command=read)
b4.grid(row=3,column=1)

b5=Button(window,text="delete",width=30,command=delete)
b5.grid(row=3,column=2)

b6=Button(window,text="close",width=30,command=window.destroy)
b6.grid(row=3,column=3)

t5=Text(window,width=90,height=30)
t5.grid(row=4,column=0,columnspan=4)
window.title("File based key-value datastore")
window.mainloop()

