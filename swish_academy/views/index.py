"""
swish_academy index (main) view.

URLs include:
/
"""

import flask
import arrow
import swish_academy
from swish_academy.views.helpers import execute_get_likes


@swish_academy.app.route('/')
def show_index():
    context = {}
    """Display / route."""
    # if 'username' not in flask.session:
    #     return flask.redirect(flask.url_for('show_login'))

    # # Connect to database
    # connection = swish_academy.model.get_db()

    # # Query database
    # logname = flask.session['username']
    # cur = connection.execute(
    #     "SELECT username, fullname "
    #     "FROM users "
    #     "WHERE username != ?",
    #     (logname, )
    # )
    # users = cur.fetchall()
    # # Add database info to context
    # context = {"users": users, "current_page": flask.request.path}

    return flask.render_template("index.html", **context)


@swish_academy.app.route('/explore/')
def show_explore():
    """Display / route."""
    if 'username' not in flask.session:
        return flask.redirect(flask.url_for('show_login'))

    connection = swish_academy.model.get_db()

    logname = flask.session['username']
    context = {}

    cur = connection.execute(
        "SELECT users.username, users.filename as user_img_url "
        "FROM users "
        "WHERE NOT EXISTS (SELECT following.username2 "
        "FROM following WHERE following.username1 = ? "
        "AND users.username = following.username2) AND "
        "users.username != ?",
        (logname, logname, )
    )
    not_following = cur.fetchall()
    context["not_following"] = not_following

    return flask.render_template("explore.html", **context)


@swish_academy.app.route('/uploads/<path:filename>')
def download_file(filename):
    """Display / route."""
    if 'username' not in flask.session:
        flask.abort(403)
    return flask.send_from_directory(swish_academy.app.config['UPLOAD_FOLDER'],
                                     filename, as_attachment=True)
