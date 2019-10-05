from flask import render_template, url_for, request
from flask_googlemaps import GoogleMaps, Map
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
from app import app

GoogleMaps(
    app,
    key="AIzaSyCsQCeigbcKX6ru5F_kCarl-fbmOgL3J8M"  # This API key is restricted by IP address, you can put your own
    # Google Maps API key here
)

class SearchForm(Form):
    location = StringField('Location:', validators=[validators.required()])
    food = StringField('Food type:', validators=[validators.required()])


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


@app.route('/review')
def review():
    return render_template('review.html')


@app.route('/search', methods=['GET', 'POST'])
def search():
    search_form = SearchForm(request.form)

    if request.method == 'POST':
        location=request.form['location']
        radius=request.form['radius']
        price=request.form['price']
        food=request.form['food']

    # creating a map in the view
    mymap = Map(
        identifier="view-side",
        lat=37.4419,
        lng=-122.1419,
        markers=[(37.4419, -122.1419)]
    )

    return render_template('search.html', form=search_form, mymap=mymap)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
