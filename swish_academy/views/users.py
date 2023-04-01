"""
swish_academy users view.

URLs include:
a bunch of user related ones
"""

import flask
import swish_academy


@swish_academy.app.route('/users/<user_url_slug>/')
def show_users(user_url_slug):
    """Display / route."""
    if 'username' not in flask.session:
        return flask.redirect(flask.url_for('show_login'))

    # Connect to database
    connection = swish_academy.model.get_db()

    # verfies user_url_slug exists
    cur = connection.execute(
        "SELECT users.username, users.fullname, "
        "COUNT(posts.postid) as total_posts "
        "FROM users "
        "LEFT JOIN posts "
        "ON posts.owner = username "
        "WHERE users.username = ? ",
        (user_url_slug, )
    )
    user = cur.fetchone()
    if user['username'] is None:
        flask.abort(404)

    context = {}

    context["username"] = user_url_slug
    context["fullname"] = user["fullname"]
    context["total_posts"] = user["total_posts"]

    cur = connection.execute(
        "SELECT COUNT(CASE WHEN username2 = ? "
        "THEN username1 ELSE NULL END) as followers, "
        "COUNT(CASE WHEN username1 = ? "
        "THEN username2 ELSE NULL END) as following "
        "FROM following ",
        (user_url_slug, user_url_slug, )
    )
    follow_info = cur.fetchone()
    context["followers"] = follow_info["followers"]
    context["following"] = follow_info["following"]

    logname_follows_username = False
    # Find out if logged in user is following user_url_slug
    cur = connection.execute(
        "SELECT username2 "
        "FROM following "
        "WHERE username1 == ?",
        (flask.session['username'],)
    )

    logged_in_followees = cur.fetchall()

    for user in logged_in_followees:

        if user["username2"] == user_url_slug:
            logname_follows_username = True

    context["logname_follows_username"] = logname_follows_username

    # Query database for post information
    cur = connection.execute(
        "SELECT postid, filename as img_url "
        "FROM posts "
        "WHERE owner == ?",
        (user_url_slug, )
    )
    posts = cur.fetchall()
    context["posts"] = posts

    return flask.render_template("user.html", **context)


@swish_academy.app.route('/users/<user_url_slug>/followers/')
def show_followers(user_url_slug):
    """Display / route."""
    if 'username' not in flask.session:
        return flask.redirect(flask.url_for('show_login'))

    # Connect to database
    connection = swish_academy.model.get_db()

    cur = connection.execute(
        "SELECT username "
        "FROM users "
        "WHERE username = ? ",
        (user_url_slug,)
    )

    followers = cur.fetchone()

    if followers is None:
        flask.abort(404)

    cur = connection.execute(
        "SELECT users.username, users.filename as user_img_url, "
        "(EXISTS (SELECT following.username2 FROM following "
        "WHERE following.username1 = ? "
        "AND users.username = following.username2)) "
        "as logname_follows_username "
        "FROM users "
        "WHERE EXISTS (SELECT following.username1 FROM following "
        "WHERE following.username2 = ? "
        "AND users.username = following.username1)",
        (flask.session["username"], user_url_slug, )
    )
    followers = cur.fetchall()

    context = {"current_page": flask.request.path}
    context["followers"] = followers
    context["username"] = user_url_slug
    context["logname"] = flask.session['username']
    return flask.render_template("followers.html", **context)


@swish_academy.app.route('/users/<user_url_slug>/following/')
def show_following(user_url_slug):
    """Display / route."""
    if 'username' not in flask.session:
        return flask.redirect(flask.url_for('show_login'))

    # Connect to database
    connection = swish_academy.model.get_db()

    cur = connection.execute(
        "SELECT username "
        "FROM users "
        "WHERE username = ? ",
        (user_url_slug,)
    )

    following = cur.fetchone()

    if following is None:
        flask.abort(404)

    cur = connection.execute(
        "SELECT users.username, users.filename as user_img_url, "
        "(EXISTS (SELECT following.username2 FROM following "
        "WHERE following.username1 = ? "
        "AND users.username = following.username2)) "
        "as logname_follows_username "
        "FROM users "
        "WHERE EXISTS (SELECT following.username2 FROM following "
        "WHERE following.username1 = ? "
        "AND users.username = following.username2)",
        (flask.session["username"], user_url_slug, )
    )

    following = cur.fetchall()

    context = {"current_page": flask.request.path}
    context["following"] = following
    context["username"] = user_url_slug
    context["logname"] = flask.session['username']
    return flask.render_template("following.html", **context)


@swish_academy.app.route('/following/', methods=['POST'])
def do_following():
    """Handle POST."""
    connection = swish_academy.model.get_db()

    cur = connection.execute(
        "SELECT username1, username2 "
        "FROM following "
        "WHERE username1 = ? AND username2 = ? ",
        (flask.session['username'], flask.request.form['username'],)
    )
    result = cur.fetchone()

    if flask.request.form["operation"] == "follow":
        # make logname follow username
        # in db: (username1, username2) means username1 follows username2

        if result:
            flask.abort(409)
        cur = connection.execute(
            "INSERT INTO following(username1, username2) \
            VALUES (?, ?) ",
            (flask.session['username'], flask.request.form['username'], )
        )

    elif flask.request.form["operation"] == "unfollow":
        # delete (flask.session['username'], username) from the "following" db

        if not result:
            flask.abort(409)

        cur = connection.execute(
            "DELETE FROM following  \
            WHERE username1 = ? AND username2 = ? ",
            (flask.session['username'], flask.request.form['username'],)
        )

    if not flask.request.args.get('target'):  # this for sure works
        return flask.redirect(flask.url_for('show_index'))

    return flask.redirect(flask.request.args.get('target'))
