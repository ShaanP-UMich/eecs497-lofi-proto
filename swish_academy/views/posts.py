"""
swish_academy posts view.

URLs include:
a bunch of post related ones
"""

import os
import arrow
import flask
import swish_academy
from swish_academy.views.helpers import save_file
from swish_academy.views.index import execute_get_likes


@swish_academy.app.route('/posts/<postid_url_slug>/')
def show_posts(postid_url_slug):
    """Display / route."""
    if 'username' not in flask.session:
        return flask.redirect(flask.url_for('show_login'))

    connection = swish_academy.model.get_db()

    context = {"current_page": flask.request.path}

    cur = connection.execute(
        "SELECT posts.postid, posts.owner, posts.filename as img_url, "
        "users.filename as owner_img_url, "
        "COUNT(DISTINCT likes.likeid) as likes "
        "FROM posts "
        "LEFT JOIN users "
        "ON users.username = posts.owner "
        "LEFT JOIN likes "
        "ON likes.postid = posts.postid "
        "WHERE posts.postid = ? "
        "GROUP BY likes.postid ",
        (postid_url_slug,)
    )
    post = cur.fetchone()
    context = post

    cur = connection.execute(
        "SELECT comments.owner, comments.text, comments.commentid "
        "FROM comments "
        "WHERE comments.postid = ? ",
        (postid_url_slug,)
    )
    comments = cur.fetchall()
    post["comments"] = comments

    result = execute_get_likes(connection, postid_url_slug)

    if result:
        post["liked"] = True
    else:
        post["liked"] = False

    cur = connection.execute(
        "SELECT created "
        "FROM posts "
        "WHERE postid = ? ",
        (postid_url_slug,)
    )

    result = cur.fetchone()

    post["timestamp"] = result['created']

    past = arrow.get(post["timestamp"], 'YYYY-MM-DD HH:mm:ss')
    present = arrow.utcnow()
    post["timestamp"] = past.humanize(present)

    return flask.render_template("post.html", **context)


@swish_academy.app.route('/comments/', methods=['POST'])  # INCOMPLETE
def do_comments():
    """Handle POST."""
    connection = swish_academy.model.get_db()

    print(flask.request.data)

    if flask.request.form["operation"] == 'create':

        if flask.request.form['text'] == "":
            flask.abort(400)
        cur = connection.execute(
            "INSERT INTO comments(owner, postid, text) \
                VALUES (?, ?, ?)",
            (flask.session['username'],
             flask.request.form['postid'],
             flask.request.form['text'],)
        )

    elif flask.request.form['operation'] == 'delete':
        # select from database comment id, and session owner, if none abort
        cur = connection.execute(
            "SELECT owner, commentid "
            "FROM comments "
            "WHERE commentid = ? ",
            (flask.request.form['commentid'],)
        )
        comment_error_check = cur.fetchone()

        if comment_error_check["owner"] != flask.session["username"]:
            flask.abort(403)
        cur = connection.execute(
            "DELETE FROM comments  \
                WHERE commentid = ? ",
            (flask.request.form['commentid'],)
        )

    if not flask.request.args.get('target'):  # this for sure works
        return flask.redirect(flask.url_for('show_index'))

    return flask.redirect(flask.request.args.get('target'))


@swish_academy.app.route('/posts/', methods=['POST'])
def do_posts():
    """Handle POST."""
    connection = swish_academy.model.get_db()

    if flask.request.form["operation"] == 'create':
        if flask.request.files.to_dict().get('file') is None:
            flask.abort(400)

        uuid_basename = save_file(flask.request.files['file'])

        cur = connection.execute(
            "INSERT INTO posts(owner, filename) \
                VALUES (?, ?)",
            (flask.session['username'],
             uuid_basename)
        )

        if not flask.request.args.get('target'):  # this for sure works
            return flask.redirect(flask.url_for('show_users',
                                  user_url_slug=flask.session['username']))

        return flask.redirect(flask.request.args.get('target'))

    if flask.request.form['operation'] == 'delete':
        cur = connection.execute(
            "SELECT owner, postid "
            "FROM posts "
            "WHERE postid = ? ",
            (flask.request.form['postid'],)
        )
        post_error_check = cur.fetchone()

        if post_error_check["owner"] != flask.session["username"]:
            flask.abort(403)
        cur = connection.execute(
            "SELECT filename "
            "FROM posts "
            "WHERE posts.postid = ?",
            (flask.request.form['postid'])
        )
        file = cur.fetchone()
        user_post_path = swish_academy.app.config["UPLOAD_FOLDER"] / \
            file["filename"]
        os.remove(user_post_path)
        cur = connection.execute(
            "DELETE FROM posts  \
                WHERE postid = ? ",
            (flask.request.form['postid'],)
        )
        if not flask.request.args.get('target'):  # this for sure works
            return flask.redirect(flask.url_for('show_users',
                                  user_url_slug=flask.session['username']))
    return flask.redirect(flask.request.args.get('target'))


@swish_academy.app.route('/likes/', methods=['POST'])
def do_likes():
    """Handle POST."""
    connection = swish_academy.model.get_db()
    if flask.request.form["operation"] == 'like':
        cur = connection.execute(
            "SELECT owner, postid "
            "FROM likes "
            "WHERE postid = ? and owner = ? ",
            (flask.request.form['postid'],
             flask.session['username'],)
        )
        errorcheck = cur.fetchone()
        if errorcheck:
            flask.abort(409)
        cur = connection.execute(
            "INSERT INTO likes(owner, postid) \
                VALUES (?, ?)",
            (flask.session['username'],
             flask.request.form['postid'],)
        )

    elif flask.request.form["operation"] == 'unlike':
        cur = connection.execute(
            "SELECT owner, postid "
            "FROM likes "
            "WHERE postid = ? and owner = ? ",
            (flask.request.form['postid'],
             flask.session['username'],)
        )
        errorcheck = cur.fetchone()
        if errorcheck is None:
            flask.abort(409)
        cur = connection.execute(
            "DELETE FROM likes  \
                WHERE postid = ? and owner=? ",
            (flask.request.form['postid'], flask.session['username'])
        )

    if not flask.request.args.get('target'):  # this for sure works
        return flask.redirect(flask.url_for('show_index'))
    return flask.redirect(flask.request.args.get('target'))
