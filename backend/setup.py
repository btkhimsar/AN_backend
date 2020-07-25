from mongoengine import connect

USER = 'admin'
PASSWORD = 'bits123'
DATABASE = 'tempdb'

client = connect(
    db='tempdb',
    username=USER,
    password=PASSWORD,
    host="mongodb+srv://" + USER + ":" + PASSWORD + "@cluster.m7hqs.mongodb.net/" + DATABASE + "?retryWrites=true&w=majority"
)
print(client)
