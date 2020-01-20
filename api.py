import sys
from flask import Flask, jsonify
import flask
import json
from flask_restplus import Resource, Api, fields
import MySQLdb

app = Flask(__name__)
api = Api(app)
indicator = ''
datas = ''
status_code = ''

indicators = api.model('Collection', {
    'indicator_id': fields.String, })


@api.route('/get_employees/<company_id>', methods=['GET'])
class Employees(Resource):
    @api.response(200, 'OK')
    @api.response(500, 'Invalid parameter')
    @api.doc(description="Retrieve employees of a company")
    def get(self, company_id):
        try:
            data_base = MySQLdb.connect(host="localhost",
                                        user=sys.argv[1],
                                        passwd=sys.argv[2],
                                        db=sys.argv[3])
            c = data_base.cursor()
            c.execute(
                "SELECT people.person_name FROM company,people WHERE people.company=company.company_id and company_id="
                + str(company_id) + ';')
            rows = c.fetchall()
            temp = []
            dict1 = {}
            if len(rows) > 0:
                for employee_info in rows:
                    temp.append(employee_info[0])
                dict1['employees'] = temp
                return flask.make_response(jsonify(dict1), 200)
            else:
                return {"message": "No employees found for the company"}, 500
        except:
            return {"message": "Company not found"}, 500
        finally:
            data_base.close()


@api.route('/common_friends/<person1_id>/<person2_id>', methods=['GET'])
class CommonFriends(Resource):
    @api.response(200, 'OK')
    @api.response(500, 'Invalid parameter')
    @api.doc(description="Find common friends who are alive and have brown eyes")
    def get(self, person1_id, person2_id):
        try:
            flag = False
            data_base = MySQLdb.connect(host="localhost",
                                        user=sys.argv[1],
                                        passwd=sys.argv[2],
                                        db=sys.argv[3])

            c = data_base.cursor()
            c.execute("select person_name, age, address, phone from people where person_id=" + str(person1_id) + ";")
            p1 = c.fetchall()
            p1 = p1[0]
            c.execute("select person_name, age, address, phone from people where person_id=" + str(person2_id) + ";")
            p2 = c.fetchall()
            p2 = p2[0]
            c.execute("select p1.person_id, p2.person_id,f1.friend_id,f2.friend_id from people as p1,friend as f1,"
                      "people as p2,friend as f2 where p1.person_id=f1.person_id and p1.person_id="
                      + str(person1_id) + " and p2.person_id=f2.person_id and p2.person_id="
                      + str(person2_id) + " and f1.friend_id=f2.friend_id;")
            rows = c.fetchall()
            temp = []
            dict1 = {}
            if len(rows) > 0:
                for item in rows:
                    temp.append(item[3])
                c.execute("select person_name from people where person_id in("
                          + str(temp)[1:-1] + ") and has_died=0 and eye_color='brown';")
                friends = c.fetchall()
                friend_names = []
                for friend in friends:
                    friend_names.append(friend[0])
                dict1['friends'] = friend_names
                dict1['Person1'] = p1
                dict1['Person2'] = p2
                return flask.make_response(jsonify(dict1), 200)
            else:
                dict1['friends'] = []
                dict1['Person1'] = p1
                dict1['Person2'] = p2
                return flask.make_response(jsonify(dict1), 200)
        except:
            return {"message": "Person ID not found"}, 500
        finally:
            data_base.close()


@api.route('/get_person_info/<person_id>', methods=['GET'])
class PersonData(Resource):
    @api.response(200, 'OK')
    @api.response(500, 'Invalid parameter')
    @api.doc(description="Retrieve employees of a company")
    def get(self, person_id):
        try:
            flag = False
            data_base = MySQLdb.connect(host="localhost",
                                        user=sys.argv[1],
                                        passwd=sys.argv[2],
                                        db=sys.argv[3])

            # if (int(year) < 2013 or int(year) > 2018):
            #    return {"message": "Year not present in database!"}, 500
            c = data_base.cursor()
            c.execute("select p.person_name,p.age from people as p where p.person_id=" + str(person_id) + ";")
            person_info = c.fetchall()
            person_info = person_info[0]
            person = person_info[0]
            age = person_info[1]
            c.execute(
                "select p.person_name,p.age,f.food,f.fruit_veg from people as p, food as f where "
                "p.person_id=f.person_id and p.person_id=" + str(
                    person_id) + ";")
            rows = c.fetchall()
            fruits = []
            vegetables = []
            dict1 = {}
            for item in rows:
                if item[3] == 'fruit':
                    fruits.append(item[2])
                else:
                    vegetables.append(item[2])

            dict1['username'] = person
            dict1['age'] = age
            dict1['fruits'] = fruits
            dict1['vegetables'] = vegetables
            return flask.make_response(jsonify(dict1), 200)

        except:
            return {"message": "Person ID not found"}, 500
        finally:
            data_base.close()


# parser = reqparse.RequestParser()
# parser.add_argument('q', required=False)

if __name__ == '__main__':

    db = MySQLdb.connect(host="localhost",
                                user=sys.argv[1],
                                passwd=sys.argv[2],
                                db=sys.argv[3])

    cur = db.cursor()

    # Use all the SQL you like
    try:
        cur.execute("truncate TABLE people;")
        cur.execute("truncate TABLE company;")
        cur.execute("truncate TABLE friend;")
        cur.execute("truncate TABLE food;")
    except:
        cur.execute("create table company(company_id int primary key, company_name varchar(50));")
        cur.execute("create table food(person_id int, food varchar(50), fruit_veg varchar(10));")
        cur.execute("create table people(person_id int primary key,person_name varchar(50), age int,has_died boolean, "
                    "eye_color varchar(15),address varchar(100),phone varchar(20),company int);")
        cur.execute("create table friend(person_id int,friend_id int);")
    fruit_veg = {'orange': 'fruit', 'apple': 'fruit', 'banana': 'fruit', 'strawberry': 'fruit', 'cucumber': 'fruit',
                 'beetroot': 'vegetable', 'carrot': 'vegetable', 'celery': 'vegetable'}
    with open(sys.argv[4]) as f:
        d = json.load(f)
        try:
            for item in d:
                cur.execute('insert into people values(' + str(item['index']) + ',"' + str(item['name']) + '",' + str(
                    item['age']) + ',' + str(item['has_died']) + ',"' + item['eyeColor'] + '","' + item[
                                'address'] + '","' + str(item['phone']) + '",' + str(item['company_id']) + ');')
                for friend in item['friends']:
                    cur.execute('insert into friend values(' + str(item['index']) + ',' + str(friend['index']) + ');')

                for food in item["favouriteFood"]:

                    if not fruit_veg[food]:
                        print("Enter f if " + str(food) + " is a fruit or v if it is a vegetable")
                        letter = input()
                        if letter == 'f':
                            fruit_veg[food] = 'fruit'
                        else:
                            fruit_veg[food] = 'vegetable'
                    cur.execute('insert into food values(' + str(item['index']) + ',"' + str(food) + '","' + str(
                        fruit_veg[food]) + '");')
                cur.execute('select * from people;')
                records = cur.fetchall()
        except:
            print("Already present")

    cur = db.cursor()

    with open(sys.argv[5]) as f:
        d = json.load(f)
        try:
            for item in d:
                cur.execute('insert into company values(' + str(item['index']) + ',"' + str(item['company']) + '");')
                cur.execute('select * from company;')
                records = cur.fetchall()

        except:
            print("Already present")

    db.commit()
    db.close()
    app.run(debug=False, port=8000)
