import MySQLdb

import json


from collections import defaultdict


db = MySQLdb.connect(host="localhost",    # your host, usually localhost
                     user="root",         # your username
                     passwd="root",  # your password
                     db="hive")        # name of the data base

# you must create a Cursor object. It will let
#  you execute all the queries you need
cur = db.cursor()

# Use all the SQL you like
cur.execute("SELECT * FROM people")

cur.execute("TRUNCATE TABLE people;")
cur.execute("TRUNCATE TABLE company;")
cur.execute("TRUNCATE TABLE friend;")
cur.execute("TRUNCATE TABLE food;")
fruit_veg= {'orange': 'fruit', 'apple': 'fruit', 'banana': 'fruit', 'strawberry': 'fruit', 'cucumber': 'fruit', 'beetroot': 'vegetable', 'carrot': 'vegetable', 'celery': 'vegetable'}


with open('people.json') as f:
    d = json.load(f)
    print(type(d))
    try:
        for item in d:
            #print('insert into people values('+str(item['index'])+',"'+str(item['name'])+'",'+str(item['age'])+','+str(item['has_died'])+',"'+item['eyeColor']+'","'+item['address']+'","'+str(item['phone'])+'",'+str(item['company_id'])+');')
            cur.execute('insert into people values('+str(item['index'])+',"'+str(item['name'])+'",'+str(item['age'])+','+str(item['has_died'])+',"'+item['eyeColor']+'","'+item['address']+'","'+str(item['phone'])+'",'+str(item['company_id'])+');')
            for friend in item['friends']:
                cur.execute('insert into friend values('+str(item['index'])+','+str(friend['index'])+');')

            for food in item["favouriteFood"]:
                print(food)
                if not fruit_veg[food]:
                    letter=input()
                    if letter=='f':
                        fruit_veg[food]='fruit'
                    else:
                        fruit_veg[food]='vegetable'
                cur.execute('insert into food values(' + str(item['index']) + ',"' + str(food) +'","'+ str(fruit_veg[food])+'");')
            cur.execute('select * from people;')
            records = cur.fetchall()

        for record in records:
            print(record)
    except:
        print("Already present")


cur = db.cursor()

with open('companies.json') as f:
    d = json.load(f)
    print(type(d))
    try:
        for item in d:
            #print('insert into company values('+str(item['index'])+',"'+str(item['company'])+'");')
            cur.execute('insert into company values('+str(item['index'])+',"'+str(item['company'])+'");')
            cur.execute('select * from company;')
            records = cur.fetchall()
        for record in records:
            print(record)
    except:
        print("Already present")


print(fruit_veg)
# print all the first cell of all the rows
#for row in cur.fetchall():
#    print row[0]p
db.commit()
db.close()