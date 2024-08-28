import sqlite3

server = sqlite3.connect("Server.db")
cur = server.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS newtable (id int,data int)")
cur.execute("INSERT INTO newtable VALUES (?,?)",(1,1))
cur.execute("INSERT INTO newtable VALUES (?,?)",(1,2))
cur.execute("INSERT INTO newtable VALUES (?,?)",(1,3))
server.commit()