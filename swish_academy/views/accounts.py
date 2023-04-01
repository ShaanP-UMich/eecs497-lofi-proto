"""
swish_academy accounts view.

URLs include:
a bunch of account related ones
"""

import flask
import swish_academy


@swish_academy.app.route('/accounts/login/')
def show_login():
    """Display / route."""
    # if 'username' in flask.session:
    #     return flask.redirect(flask.url_for('show_index'))

    # context = {}
    # return flask.render_template("login.html", **context)
    return flask.jsonify({"text": "hello"})


@swish_academy.app.route('/accounts/password/')
def show_password():
    """Display / route."""
    if 'username' not in flask.session:
        return flask.redirect(flask.url_for('show_login'))

    context = {}
    return flask.render_template("password.html", **context)


@swish_academy.app.route('/accounts/delete/')
def show_delete():
    """Display / route."""
    if 'username' not in flask.session:
        return flask.redirect(flask.url_for('show_login'))

    context = {}
    return flask.render_template("delete.html", **context)


@swish_academy.app.route('/accounts/create/')
def show_create():
    """Display / route."""
    if 'username' in flask.session:
        return flask.redirect(flask.url_for('show_edit'))

    context = {}
    return flask.render_template("create.html", **context)


@swish_academy.app.route('/accounts/edit/')
def show_edit():
    """Display / route."""
    if 'username' not in flask.session:
        return flask.redirect(flask.url_for('show_login'))

    connection = swish_academy.model.get_db()

    context = {}

    cur = connection.execute(
        "SELECT users.fullname, users.email, users.filename "
        "FROM users "
        "WHERE users.username = ? ",
        (flask.session['username'],)
    )

    user = cur.fetchone()

    context["fullname"] = user["fullname"]
    context["email"] = user["email"]
    context["owner_img_url"] = user['filename']

    return flask.render_template("edit.html", **context)


@swish_academy.app.route('/accounts/logout/', methods=['POST'])
def do_logout():
    """Handle POST."""
    print("logging out current user")

    flask.session.clear()
    return flask.redirect(flask.url_for('show_login'))
