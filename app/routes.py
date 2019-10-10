from flask import render_template, url_for, request
from flask_googlemaps import GoogleMaps, Map
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
from app import app
from app.database import db_search
import requests

google_maps_key = "AIzaSyCsQCeigbcKX6ru5F_kCarl-fbmOgL3J8M"

GoogleMaps(
    app,
    key=google_maps_key  # This API key is restricted by IP address, you can put your own
    # Google Maps API key here
)


@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'John Smith'}
    return render_template('base.html', title='Home', user=user)


@app.route('/upload')
def upload():
    return render_template('upload.html')


@app.route('/sign_in')
def sign_in():
    return render_template('sign_in.html')


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


@app.route('/search', methods=['GET', 'POST'])
def search():

    if request.method == 'POST':
        location=request.form['location']
        radius=request.form['radius']
        price = request.form['price']
        food=request.form['food']
        restaurant = db_search()
        geocode = (requests.get('https://maps.googleapis.com/maps/api/geocode/json?address=' + restaurant + '&key=' + google_maps_key)).json()
        restaurant_lat = geocode['results'][0]['geometry']['location']['lat']
        restaurant_lng = geocode['results'][0]['geometry']['location']['lng']
        mymap = Map(
            identifier="view-side",
            lat=restaurant_lat,
            lng=restaurant_lng,
            markers=[(restaurant_lat, restaurant_lng)],
            style="height:600px;width:900px"
        )
    else:
        # creating a map in the view
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
