from replit import db

class ReplDB():
  def store(self,key,value):
    db[str(key)] = value
  def get(self,key):
    return db[str(key)]
  def exists(self,key):
    return str(key) in db
  def delete(self,key):
    db.delete(str(key))