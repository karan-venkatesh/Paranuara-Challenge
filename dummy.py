class employee(Resource):
    @api.response(201, 'Created')
    @api.response(200, 'OK')
    @api.response(404, 'Invalid Indicator')
    @api.doc(description="Add a new collection")
    @api.expect(indicators, validate=True)
    def post(self):
        global indicator
        global datas
        ind_id = request.json
        indicator = ind_id['indicator_id']
        indicator_id = ind_id['indicator_id']
        response = requests.get("http://api.worldbank.org/v2/countries/all/indicators/{}?date=2013:2018&format=json&per_page= 100".format(indicator_id))
        if len(response.json()) > 1:
            data = response.json()[1]
            datas = data
            create_db("data.db")
        else:
            return 404
        conn = sqlite3.connect("data.db")
        c = conn.cursor()
        c.execute("SELECT data FROM collections WHERE indicator_id=?", (indicator_id,))
        rows = c.fetchall()
        conn.close()
        if status_code == '200':
            return {"location": "/collections/{}".format(indicator_id), "collection_id": "{}".format(indicator_id),
                    "creation_time": "{}".format(json.loads(rows[0][0])['creation_time']),
                    "indicator": "{}".format(indicator_id)}, 200
        elif status_code == '201':
            return {"location": "/collections/{}".format(indicator_id), "collection_id": "{}".format(indicator_id),
                    "creation_time": "{}".format(json.loads(rows[0][0])['creation_time']),
                    "indicator": "{}".format(indicator_id)}, 201

    @api.response(200, 'OK')
    @api.doc(description="Get all collections")



    def get(self):
        try:
            conn = sqlite3.connect("data.db")
            c = conn.cursor()
            c.execute("SELECT * FROM collections")
            rows = c.fetchall()
            return_list = []
            for i in range(len(rows)):
                dict1 = {}
                dict1['location'] = '/collections/{}'.format(rows[i][0])
                dict1['collection_id'] = rows[i][0]
                dict1['creation_time'] = json.loads(rows[i][1])['creation_time']
                dict1['indicator'] = rows[i][0]
                return_list.append(dict1)
            return jsonify(return_list)
        except Error:
            return "Error"
        finally:
            conn.close()


@api.route('/collections/<collection_id>')
class CollectionByID(Resource):
    @api.response(200, 'OK')
    @api.doc(description="Delete a collection")
    def delete(self, collection_id):
        try:
            conn = sqlite3.connect("data.db")
            c = conn.cursor()
            c.execute("SELECT COUNT(*) FROM collections WHERE indicator_id=?", (collection_id,))
            rows = c.fetchall()
            if rows[0][0] > 0:
                c.execute("DELETE FROM collections WHERE indicator_id=?", (collection_id,))
                conn.commit()
                return {"message": "Collection {} is removed from the database!".format(collection_id)}, 200
            else:
                return {"message": "Id not present in database!"}
        except Error:
            return "Unexpected error"
        finally:
            conn.close()

    @api.response(200, 'OK')
    @api.doc(description="Retrieve a collection based on ID")
    def get(self, collection_id):
        try:
            conn = sqlite3.connect("data.db")
            c = conn.cursor()
            c.execute("SELECT data FROM collections WHERE indicator_id=?", (collection_id,))
            rows = c.fetchall()
            if rows > 0:
                return (json.loads(rows[0][0]), 200)
            else:
                return {"message": "Id not present in database!"}
        except Error:
            return "Unexpected error"
        finally:
            conn.close()
