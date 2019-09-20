from flask import render_template
from app import app

@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'John Smith'}
    return render_template('base.html', title='Home', user=user)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404