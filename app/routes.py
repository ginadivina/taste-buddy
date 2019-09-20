from flask import render_template, url_for, request
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
from app import app


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
        food=request.form['food']

    return render_template('search.html', form=search_form)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
