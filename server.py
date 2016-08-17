from flask import Flask, redirect, render_template, request, flash
from mysqlconnection import MySQLConnector

app = Flask(__name__)
app.secret_key = 'secret'

mysql = MySQLConnector(app,'tacosdb')


@app.route('/')
def index():

    return render_template('index.html')

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

# Show a "restaurant detail" page
@app.route('/view/<restaurant_id>')
def show_view(restaurant_id):

    return render_template('view_restaurant.html', restaurant_id=restaurant_id)

# Add a new item for a given restaurant
@app.route('/view/<restaurant_id>', methods=['POST'])
def add_item(restaurant_id):

    return redirect('/view/' + restaurant_id)

# Show the "edit restaurant" page
@app.route('/edit/<restaurant_id>')
def show_edit(restaurant_id):

    return render_template('edit_restaurant.html', restaurant_id=restaurant_id)

# Edit a restaurant
@app.route('/edit/<restaurant_id>', methods=['POST'])
def edit_restaurant(restaurant_id):

    return redirect('/')

# Show the "delete confirmation" page
@app.route('/delete/<restaurant_id>')
def show_delete(restaurant_id):

    return render_template('delete_restaurant.html', restaurant_id=restaurant_id)

# Delete a restaurant
@app.route('/delete/<restaurant_id>', methods=['POST'])
def delete_restaurant(restaurant_id):

    return redirect('/')


app.run(debug=True)

