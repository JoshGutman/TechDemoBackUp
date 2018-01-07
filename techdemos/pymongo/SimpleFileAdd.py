from pymongo import MongoClient
client = MongoClient()
db = client.testDB
files = db.files
f = open('test1.txt')
text = f.read()
doc = {
    "file_name": "test1.txt",
    "contents": text
}
files.insert(doc)
