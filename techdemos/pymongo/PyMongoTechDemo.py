# Created by Tanner Brelje

# The following is a realistic demonstration of how MongoDB will interact with
# PyMongo, displaying how files such as .BNGLs will be stored on the database
# connected to the accounts that the users have created.

# To begin, we import PyMongo in order to access the needed functions
from pymongo import MongoClient
# We also connect to the instance of MongoDB on our local machine
client = MongoClient()

# Create a database on the local machine
db = client.BioNetFit
# Create a collection called users
users = db.users

# Lets first add a user with basic information
user1 = {
    "fname": "Tanner",
    "lname": "Brelje",
    "user": "blitz",
    "pwd": "1234"
}
users.insert(user1)

# Now that we have a user on the database,
# we can now attach a file to the user.

# First we read in the text from a BNGL file
f = open("example5.bngl")
text = f.read()

# Then we update the user with the text
# The following updates the user blitz with file1, where upsert
# = false prevents a new db entry from being created.
users.update({"user":"blitz"}, {'$set':{"file1":text}}, upsert=False)

# In order to test if the file was in fact saved, we will print the
# file to the python console.
Col = users.find()
for i in Col:
    print(i)

# This concludes the demonstration





