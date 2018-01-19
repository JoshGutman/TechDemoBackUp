# Python PyMongo Demo for Dr. Razi
# Created by Tanner Brelje

from Tkinter import *
from pymongo import MongoClient

# Creates/Load DB
client = MongoClient()
db = client.BioNetFit
users = db.users

app = Tk()

fname = Entry()
lname = Entry()
uname = Entry()
pwd = Entry()
upload = Entry()

fname.grid(row=0, column=1)
lname.grid(row=1, column=1)
uname.grid(row=2, column=1)
pwd.grid(row=3, column=1)
upload.grid(row=4, column=1)


# Create Labels
Label(app, text="First Name:").grid(row=0, column=0)
Label(app, text="Last Name:").grid(row=1, column=0)
Label(app, text="Username:").grid(row=2, column=0)
Label(app, text="Password:").grid(row=3, column=0)
Label(app, text="Upload to:").grid(row=4, column=0)


# Create Button Functions
def gen_user():
    user = {
        "fname": fname.get(),
        "lname": lname.get(),
        "user": uname.get(),
        "pwd": pwd.get()
    }
    users.insert(user)


def upload_ex():
    f = open("example_5.bngl")
    text = f.read()
    users.update({"user": upload.get()}, {'$set': {"file1": text}}, upsert=False)


def display():
    for i in users.find({"user":upload.get()}):
        print(i)


# Create Buttons
button1 = Button(app, text="Create User", command=gen_user)
button2 = Button(app, text="Upload Ex File", command=upload_ex)
button3 = Button(app, text="Display Text Document", command=display)

button1.grid(row=3, column=3)
button2.grid(row=4, column=3)
button3.grid(row=5, columnspan=3)

app.mainloop()
