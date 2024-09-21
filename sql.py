import sqlite3

server = sqlite3.connect("Test.db")
cur = server.cursor()
cur.execute('''CREATE TABLE IF NOT EXISTS Media(
                id INTEGER PRIMARY KEY, title TEXT, 
                type TEXT,
                onchapter INTEGER,  chapters INTEGER,
                status TEXT
                )''')
values = {
    'id':3, 'title':'jack', 'type':None,
    'onchapter':None,'chapters':6,'status':'Ongoing'
}
cur.execute(
    """INSERT INTO Media (onchapter, chapters, status)
     VALUES (:onchapter, :chapters, :status);""", 
    values
)
server.commit()