from mongoengine import connect

USER = 'admin'
PASSWORD = 'bits123'
DATABASE = 'User_db'

client = connect(
    db='User_db',
    username=USER,
    password=PASSWORD,
    host="mongodb+srv://" + USER + ":" + PASSWORD + "@ancluster.bjfm9.mongodb.net/" + DATABASE + "?retryWrites=true&w=majority"
)
print(client)
