from flask import Flask, redirect, render_template, request, flash
from mysqlconnection import MySQLConnector

app = Flask(__name__)

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

