from flask import render_template, url_for
from app import app


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


@app.route('/search')
def search():
    return render_template('search.html')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
