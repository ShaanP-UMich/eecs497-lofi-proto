"""
swish_academy login view.

URLs include:
a bunch of login related ones
"""

import os
import hashlib
import uuid
import flask
import swish_academy
from swish_academy.views.helpers import hash_password
from swish_academy.views.posts import save_file


def operation_login(connection):
    """Handle /accounts/ login POST."""
    if (flask.request.form['username'] == "" or
            flask.request.form['password'] == ""):
        flask.abort(400)

    cur = connection.execute(
        "SELECT username, password "
        "FROM users "
        "WHERE username == ? ",
        (flask.request.form['username'],)
    )

    login_details = cur.fetchall()

    if not login_details:
        flask.abort(403)
    else:
        db_password_split = login_details[0]['password'].split('$')

        password_db_string = hash_password(
            flask.request.form['password'], db_password_split[1])

        if password_db_string != login_details[0]['password']:
            flask.abort(403)
        else:
            flask.session['username'] = flask.request.form['username']


def operation_create(connection):
    """Handle /accounts/ create POST."""
    if (flask.request.form['username'] == "" or
            flask.request.form['password'] == "" or
            flask.request.form['fullname'] == "" or
            flask.request.form['email'] == "" or
            flask.request.files['file'] == ""):
        flask.abort(400)

    uuid_basename = save_file(flask.request.files['file'])

    # Query database
    cur = connection.execute(
        "SELECT username "
        "FROM users ",
        ()
    )
    existing_usernames = cur.fetchall()

    # Checking if form username already exists in database
    for usernames in existing_usernames:
        if usernames['username'] == flask.request.form['username']:
            flask.abort(409)

    password_db_string = hash_password(flask.request.form['password'])

    cur = connection.execute(
        "INSERT INTO users(username, fullname, email, filename, password) \
            VALUES (?, ?, ?, ?, ?)",
        (flask.request.form['username'],
         flask.request.form['fullname'],
         flask.request.form['email'],
         uuid_basename,
         password_db_string,)
    )

    flask.session['username'] = flask.request.form['username']


def operation_delete(connection):
    """Handle /accounts/ delete POST."""
    if 'username' not in flask.session:
        flask.abort(403)
    else:
        cur = connection.execute(
            "SELECT filename "
            "FROM users "
            "WHERE username = ?",
            (flask.session['username'],)
        )

        user_icon_file = cur.fetchall()[0]['filename']

        user_icon_path = swish_academy.app.config["UPLOAD_FOLDER"] / \
            user_icon_file

        os.remove(user_icon_path)

        cur = connection.execute(
            "SELECT filename "
            "FROM posts "
            "WHERE owner = ? ",
            (flask.session['username'],)
        )

        user_post_files = cur.fetchall()

        for file in user_post_files:
            user_post_path = swish_academy.app.config["UPLOAD_FOLDER"] / \
                file['filename']
            os.remove(user_post_path)

        cur = connection.execute(
            "DELETE from users "
            "WHERE username = ? ",
            (flask.session['username'],)
        )

        flask.session.clear()


def operation_edit_account(connection):
    """Handle /accounts/ edit_account POST."""
    if 'username' not in flask.session:
        flask.abort(403)
    else:
        if (flask.request.form['fullname'] == "" or
                flask.request.form['email'] == ""):
            flask.abort(400)

        cur = connection.execute(
            "SELECT filename "
            "FROM users "
            "WHERE username = ?",
            (flask.session['username'],)
        )

        user_pfp = cur.fetchone()

        cur = connection.execute(
            "UPDATE users "
            "SET fullname = ?, email = ?"
            "WHERE username = ? ",
            (flask.request.form['fullname'], flask.request.form['email'],
             flask.session['username'],)
        )

        if flask.request.files.to_dict().get('file').filename != "":
            # pfp provided

            user_pfp_path = swish_academy.app.config["UPLOAD_FOLDER"]
            user_pfp_path = user_pfp_path/user_pfp['filename']
            os.remove(user_pfp_path)

            uuid_basename = save_file(flask.request.files['file'])

            cur = connection.execute(
                "UPDATE users "
                "SET filename = ?"
                "WHERE username = ?",
                (uuid_basename, flask.session['username'])
            )


def operation_update_password(connection):
    """Handle /accounts/ update_password POST."""
    if 'username' not in flask.session:
        flask.abort(403)

    old_password = flask.request.form['password']
    new_password = flask.request.form['new_password1']
    confirm_password = flask.request.form['new_password2']

    if (old_password == "" or new_password == ""
            or confirm_password == ""):
        flask.abort(400)

    cur = connection.execute(
        "SELECT password "
        "FROM users "
        "WHERE username = ?",
        (flask.session['username'],)
    )

    db_password = cur.fetchone()['password']

    db_password_split = db_password.split('$')
    algorithm = 'sha512'
    salt = db_password_split[1]
    hash_obj = hashlib.new(algorithm)
    password_salted = salt + old_password
    hash_obj.update(password_salted.encode('utf-8'))
    password_hash = hash_obj.hexdigest()
    user_password_hashed = "$".join([algorithm, salt, password_hash])

    if user_password_hashed != db_password:
        flask.abort(403)

    if new_password != confirm_password:
        flask.abort(401)

    salt = uuid.uuid4().hex
    hash_obj = hashlib.new(algorithm)
    password_salted = salt + new_password
    hash_obj.update(password_salted.encode('utf-8'))
    password_hash = hash_obj.hexdigest()
    new_password_hashed = "$".join([algorithm, salt, password_hash])

    cur = connection.execute(
        "UPDATE users "
        "SET password = ? ",
        (new_password_hashed,)
    )


@swish_academy.app.route('/accounts/', methods=['POST'])
def do_accounts():
    """Handle POST."""
    # Connect to database
    connection = swish_academy.model.get_db()

    print(flask.request.form)
    print(flask.request.form['operation'])

    if flask.request.form['operation'] == 'login':
        operation_login(connection)
    elif flask.request.form['operation'] == 'create':
        operation_create(connection)
    elif flask.request.form['operation'] == 'delete':
        operation_delete(connection)
    elif flask.request.form['operation'] == 'edit_account':
        operation_edit_account(connection)
    elif flask.request.form['operation'] == 'update_password':
        operation_update_password(connection)

    if not flask.request.args.get('target'):  # this for sure works
        return flask.redirect(flask.url_for('show_index'))
    return flask.redirect(flask.request.args.get('target'))


@swish_academy.app.route('/isLoggedIn/', methods=['GET'])
def get_is_logged_in():
    if 'username' not in flask.session:
        return flask.jsonify({
            "loggedIn": False,
            "username": None
        })
    else:
        return flask.jsonify({
            "loggedIn": True,
            "username": flask.session['username']
            })
