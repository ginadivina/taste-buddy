from flask import flash, request, redirect, render_template, url_for, request
from flask_googlemaps import GoogleMaps, Map
from werkzeug.utils import secure_filename
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
from app import app
from app.database import db_search, add_menu
import os
import requests

google_maps_key = "AIzaSyCsQCeigbcKX6ru5F_kCarl-fbmOgL3J8M"

GoogleMaps(
    app,
    key=google_maps_key  # This API key is restricted by IP address, you can put your own
    # Google Maps API key here
)

app.config['UPLOAD_FOLDER'] = 'uploads'
# add_menu('uploads/dummy_menu.csv')

@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'John Smith'}
    return render_template('base.html', title='Home', user=user)


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)

        print(os.path.exists(app.config['UPLOAD_FOLDER']))
        file = request.files['file']

        if file and file.filename.endswith('.csv'):
            filename = secure_filename(file.filename)
            csv_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            
            try:
                file.save(csv_path)
                print(csv_path)
                add_menu(csv_path)
            except Exception as e:
                print(f'Failed to import menu. Details: {e}')

            return redirect(url_for('upload'))

    else:
        return render_template('upload.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    msg = ''
    conn = db_search.connect()
    cursor = conn.cursor()
    # Account doesnt exists and the form data is valid, now insert new account into accounts table
    cursor.execute('INSERT INTO UserInfo VALUES (NULL, %s, %s, %s, %s, %s, %s, %s, %s, %s)', (Fname, Lname, DOB, Address, State, PostCode, Email, Phone, Password))
    conn.commit()
    msg = 'You have successfully registered!'
    conn.close()
 
    return render_template('register.html', msg=msg)

@app.route('/sign_in', methods=['GET', 'POST'])
def sign_in():
    msg = ''
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['email']
        password = request.form['password']
        # Check if account exists using db_search
        conn = db_search.connect()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM UserInfo WHERE email = %s AND password = %s', (email, password))
        # Fetch one record and return result
        account = cursor.fetchone()
        # If account exists in accounts table in out database
        if account:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['id'] = account['id']
            session['email'] = account['username']
            # Redirect to home page
            return 'Logged in successfully!'
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect email/password!'
    # Show the login form with message (if any)
    return render_template('sign_in.html', msg=msg)

@app.route('/sign_out')
def sign_out():
    return render_template('sign_out.html')

@app.route('/history')
def history():
    return render_template('history.html')


@app.route('/user_profile')
def user_profile():
    return render_template('user_profile.html')

@app.route('/review')
def review():
    return render_template('review.html')

@app.route('/thanks')
def thanks():
    return render_template('thanks.html')

@app.route('/search', methods=['GET', 'POST'])
def search():  # Our main search page interface
    if request.method == 'POST':
        #  Take inputs
        location = request.form['location']
        radius = request.form['radius']
        price = request.form['price']
        food = request.form['food']

        restaurants = db_search()  # Search DB
        print(restaurants[0][1])
        restaurant_markers = []  # Init variables we will be using
        i = 0

        while i < len(restaurants):  # Loop through the restaurants found in DB
            geocode = (requests.get('https://maps.googleapis.com/maps/api/geocode/json?address=' + str(
                restaurants[i]) + '&key=' + google_maps_key)).json()
            restaurant_lat = geocode['results'][0]['geometry']['location']['lat']
            restaurant_lng = geocode['results'][0]['geometry']['location']['lng']
            restaurant_name = restaurants[i][1]
            restaurant_markers.append({
                'lat': restaurant_lat,
                'lng': restaurant_lng,
                'infobox': '<h1>' + restaurant_name + '</h1><br>'
                           '<span class="fa fa-star checked"></span>'
                           '<span class="fa fa-star checked"></span>'
                           '<span class="fa fa-star checked"></span>'
                           '<span class="fa fa-star"></span>'
                           '<span class="fa fa-star"></span><b>(27)</b>'
                           '<img src="/static/deliveroo.jpg"style="width:50px;height:50px;">'
                           '<img src="/static/menulog.jpg"style="width:50px;height:50px;">'
            })
            i += 1

        # Render updated map and markers
        mymap = Map(
            identifier="view-side",
            lat=restaurant_markers[0]['lat'],
            lng=restaurant_markers[0]['lng'],
            markers=restaurant_markers,
            style="height:600px;width:900px"
        )
    else:
        # Default map view
        mymap = Map(
            identifier="view-side",
            lat=-33.8688,
            lng=151.2093,
            style="height:600px;width:900px"
        )

    return render_template('search.html', mymap=mymap)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
