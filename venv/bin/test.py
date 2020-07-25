import pymongo
from pymongo import MongoClient

con = MongoClient('192.168.1.2', 27017)
db = con.testdb

my_coll = db.coll_name

emp_rec = {'name':"emp_name", 'address':"emp_addr", 'id':"emp_id"}
rec_id = my_coll.insert_one(emp_rec)