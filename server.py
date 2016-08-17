from flask import Flask, redirect, render_template, request, flash
from mysqlconnection import MySQLConnector

app = Flask(__name__)

app.secret_key = 'secret'

mysql = MySQLConnector(app,'tacosdb')


@app.route('/')
def index():
    query = "SELECT * FROM restaurants"
    result = mysql.query_db(query)

    return render_template('index.html', restaurants=result)

# Show the "add restaurant" page
@app.route('/add')
def show_add():

    return render_template('add_restaurant.html')

# Add a new restaurant
@app.route('/add/new', methods=['POST'])
def add():
    data = request.form
    isValid = True
    # validation for length
    if len(data['name']) < 2:
        isValid = False
    if len(data['street_num']) < 2: # pick a length? regex?
        isValid = False
    if len(data['city']) < 2:
        isValid = False
    if len(data['zip']) < 5 or len(data['zip']) > 5:
        isValid = False
    if len(data['price']) > 2 or len(data['price']) < 1:
        isValid = False
    # v2 add sql query if entry exists - street number + zipcode
    if not isValid:
        flash("invalid entry! try again")
        return redirect('/add')
    else:
        query = '''INSERT INTO restaurants (name, street_num, city, zip, 
        price) VALUES (:name, :street_num, :city, :zip, :price);'''
        data = {
				'name' : data['name'],
				'street_num' : data['street_num'],
				'city' : data['city'],
				'zip' : data['zip'],
				'price' : data['price'],
				 }
        print data
        user = mysql.query_db(query,data)
        return redirect('/')

#George's feature----------------------------------------------------------

# Show a "restaurant detail" page
@app.route('/view/<restaurant_id>')
def show_view(restaurant_id):
    info_query = "SELECT * FROM restaurants WHERE id = " + restaurant_id
    info = mysql.query_db(info_query)

    item_query = "SELECT * FROM items WHERE restaurant_id =  " + restaurant_id
    items = mysql.query_db(item_query)

    return render_template('view.html', info=info[0], items=items)

# Add a new item for a given restaurant
@app.route('/view/<restaurant_id>', methods=['POST'])
def add_item(restaurant_id):
    if not request.form['item']:
        flash("You cannot submit an empty value")
        return redirect('/view/'+restaurant_id)
    else:
        query = "INSERT INTO items (name, restaurant_id) "\
        "VALUES (:name, :id)"
        data = {
            "name": request.form['item'],
            "id": restaurant_id
        }
        mysql.query_db(query,data)
        return redirect('/view/'+restaurant_id)

#George's feature end----------------------------------------------------------

# Show the "edit restaurant" page
@app.route('/edit/<restaurant_id>')
def show_edit(restaurant_id):

    return render_template('edit.html', restaurant_id=restaurant_id)

# Edit a restaurant
@app.route('/edit/<restaurant_id>', methods=['POST'])
def edit_restaurant(restaurant_id):
    data = {
    "restaurant_name" : request.form['restaurant_name'],
    "street_num" : request.form['street'],
    "city" : request.form['city'],
    "zip_code" : request.form['zip_code'],
    "price" : request.form['price'],
    "restaurant_id" : restaurant_id
    }
    query = "update restaurants set name=:restaurant_name, street_num=:street_num, "\
    " city=:city, zip=:zip_code, price=:price where id=:restaurant_id"
    mysql.query_db(query, data)
    print data
    return redirect('/')

# Show the "delete confirmation" page
@app.route('/delete/<restaurant_id>')
def show_delete(restaurant_id):
    query = "SELECT name, id from restaurants WHERE id = :id"
    data = {'id': restaurant_id}

    result = mysql.query_db(query, data)

    return render_template('delete_conf.html', restaurant_data=result[0])

# Delete a restaurant
@app.route('/delete/<restaurant_id>', methods=['POST'])
def delete_restaurant(restaurant_id):
    query = "DELETE FROM restaurants WHERE id = :id"
    data = {'id': restaurant_id}

    mysql.query_db(query, data)

    return redirect('/')


app.run(debug=True)

