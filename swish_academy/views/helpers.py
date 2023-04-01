"""
swish_academy helper functions.

URLs include:
none
"""

import hashlib
import pathlib
import uuid
import flask
import swish_academy


def execute_get_likes(connection, post_id):
    """Execute a 'like' SQL Query."""
    cur = connection.execute(
        "SELECT owner, postid "
        "FROM likes "
        "WHERE postid = ? and owner = ?",
        (post_id, flask.session['username'],)
    )

    result = cur.fetchall()

    return result


def hash_password(password_unsalted, salt=uuid.uuid4().hex):
    """Hash a password."""
    algorithm = 'sha512'
    hash_obj = hashlib.new(algorithm)
    password_salted = salt + password_unsalted
    hash_obj.update(password_salted.encode('utf-8'))
    password_hash = hash_obj.hexdigest()
    password_hashed = "$".join([algorithm, salt, password_hash])

    return password_hashed


def save_file(fobj):
    """Save a file and returns it's unique name."""
    fileobj = fobj
    filename = fileobj.filename
    stem = uuid.uuid4().hex
    suffix = pathlib.Path(filename).suffix
    uuid_basename = f"{stem}{suffix}"
    path = swish_academy.app.config["UPLOAD_FOLDER"]/uuid_basename
    fileobj.save(path)

    return uuid_basename


class HTTPError(Exception):
    """HTTP Request Error Class."""

    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        """Init for HTTP Request."""
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        """to_dict for HTTP Request."""
        return_value = dict(self.payload or ())
        return_value['message'] = self.message
        return_value['status_code'] = self.status_code
        return return_value


@swish_academy.app.errorhandler(HTTPError)
def handle_httperror(error):
    """Handle HTTP Request Error."""
    response = flask.jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


def check_if_logged_in(connection):
    """Check if user is logged in."""
    if ('username' not in flask.session) and (not flask.request.authorization):
        raise HTTPError('Forbidden', status_code=403)

    if flask.request.authorization:
        username = flask.request.authorization['username']
        password = flask.request.authorization['password']
        # check if username and password are valid
        cur = connection.execute(
            "SELECT username, password "
            "FROM users "
            "WHERE username == ? ",
            (username,)
        )

        login_details = cur.fetchall()

        if not login_details:
            raise HTTPError('Forbidden', status_code=403)
        db_password_split = login_details[0]['password'].split('$')

        password_db_string = hash_password(
            password, db_password_split[1])

        if password_db_string != login_details[0]['password']:
            raise HTTPError('Forbidden', status_code=403)
        flask.session['username'] = username
