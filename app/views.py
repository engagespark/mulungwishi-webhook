from app import mulungwishi_app as url
from flask import render_template


@url.route('/')
def index():
    return render_template('index.html')


@url.route('/<query>')
def print_user_input(query):
    if '=' in query:
        query_container, query_value = query.split('=')
        return 'Your query is {} which is equal to {}'.format(query_container, query_value)
    return "You've entered an incorrect query. Please check and try again. You can try 'url=something relevant'".format(query), 400


@url.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


@url.errorhandler(403)
def page_forbidden(error):
    return render_template('403.html', title='Page Forbidden'), 403


@url.errorhandler(500)
def page_server_error(error):
    return render_template('500.html', title='Server Error'), 500
