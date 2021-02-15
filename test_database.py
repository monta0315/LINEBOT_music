import sqlite3

conn = sqlite3.connect("test.db")
c = conn.cursor()

#check_table
def create_table():
  c.execute("CREATE TABLE test(push_user string, push_movie string)")

def check_table():
  c.execute("select *from test")

def insert_table(pushes):
  query = "INSERT INTO test VALUES(?,?)"
  c.execute(query,pushes)
  conn.commit()

if __name__ == "__main__":
  #create_table()
  pushes=("aa","bb")
  insert_table(pushes)
  #check_table()
