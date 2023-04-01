"""REST API for posts."""
from json.encoder import INFINITY
import flask
import swish_academy
from swish_academy.views.helpers import HTTPError
from swish_academy.views.helpers import check_if_logged_in


@swish_academy.app.route('/api/v1/')
def get_api_resource_urls():
    """Return API resource URLs."""
    context = {
        "comments": "/api/v1/comments/",
        "likes": "/api/v1/likes/",
        "posts": "/api/v1/posts/",
        "url": "/api/v1/"
    }

    return flask.jsonify(**context)


@swish_academy.app.route('/api/v1/posts/')
def get_api_v1_posts():
    """GET /api/v1/posts/ endpoint."""
    connection = swish_academy.model.get_db()

    check_if_logged_in(connection)

    size = flask.request.args.get("size", default=10, type=int)
    page = flask.request.args.get("page", default=0, type=int)
    print("pepper")
    print(flask.request.args)
    if not flask.request.args:
        print("the args is nothing!!!")
    postid_lte = flask.request.args.get(
        "postid_lte", default=INFINITY, type=int)

    if size < 0 or page < 0:
        raise HTTPError('Bad Request', status_code=400)

    context = {}
    context["next"] = ""

    cur = connection.execute(
        "SELECT posts.postid, "
        "('/api/v1/posts/' || posts.postid || '/') as url "
        "FROM posts "
        "INNER JOIN following "
        "ON (posts.owner = following.username2 "
        "AND following.username1 = ? ) OR posts.owner = ? "
        "LEFT JOIN users "
        "ON posts.owner = users.username "
        "WHERE posts.postid <= ?"
        "GROUP BY posts.postid "
        "ORDER BY posts.postid DESC "
        "LIMIT ? "
        "OFFSET ?",
        (flask.session['username'], flask.session['username'],
         postid_lte, size, size*page)
    )

    results = cur.fetchall()
    print(results)

    count = len(results)

    if postid_lte == INFINITY:
        postid_lte = results[0]["postid"]

    if count >= size:
        context["next"] = f'/api/v1/posts/?size={size}&page={page+1}' \
            f'&postid_lte={postid_lte}'

    context["results"] = results
    if flask.request.args:
        context["url"] = flask.request.full_path
    else:
        context["url"] = flask.request.path

    return flask.jsonify(**context)


@swish_academy.app.route('/api/v1/posts/<int:postid_url_slug>/')
def get_v1_posts_postid(postid_url_slug):
    """GET /api/v1/posts/<postid>/ endpoint."""
    connection = swish_academy.model.get_db()
    check_if_logged_in(connection)

    cur = connection.execute(
        "SELECT commentid, (owner == ?) as lognameOwnsThis, "
        "owner, ('/users/' || owner || '/') as ownerShowUrl, "
        "text, ('/api/v1/comments/' || commentid || '/') as url "
        "FROM comments "
        "WHERE postid = ? ",
        (flask.session['username'], postid_url_slug)
    )

    context = {}

    result = cur.fetchall()

    for comment in result:
        if comment["lognameOwnsThis"] == 1:
            comment["lognameOwnsThis"] = True
        else:
            comment["lognameOwnsThis"] = False

    context["comments"] = result

    cur = connection.execute(
        "SELECT created, filename "
        "FROM posts "
        "WHERE postid = ?",
        (postid_url_slug,)
    )

    current_post = cur.fetchone()
    if not current_post:
        raise HTTPError('Forbidden', status_code=404)

    context["comments_url"] = f'/api/v1/comments/?postid={postid_url_slug}'
    context["created"] = current_post["created"]
    context["imgUrl"] = f'/uploads/{current_post["filename"]}'

    cur = connection.execute(
        "SELECT (owner == ?) as lognameLikesThis, "
        "COUNT(DISTINCT likeid) as numLikes, "
        "('/api/v1/likes/' || likeid || '/') as url  "
        "FROM likes "
        "WHERE postid = ? ",
        ((flask.session['username']), postid_url_slug)
    )

    likes_result = cur.fetchone()

    if likes_result["lognameLikesThis"] == 1:
        likes_result["lognameLikesThis"] = True
    else:
        likes_result["lognameLikesThis"] = False
        likes_result["url"] = None

    context['likes'] = likes_result

    cur = connection.execute(
        "SELECT postid, users.filename as ownerImgUrl, owner "
        "FROM posts "
        "INNER JOIN users "
        "ON posts.owner = users.username "
        "WHERE postid = ? ",
        (postid_url_slug,)
    )
    post_result = cur.fetchone()
    context["owner"] = post_result["owner"]
    context["ownerImgUrl"] = f'/uploads/{post_result["ownerImgUrl"]}'
    context["ownerShowUrl"] = f'/users/{post_result["owner"]}/'
    context["postShowUrl"] = f'/posts/{postid_url_slug}/'
    context["postid"] = postid_url_slug
    context["url"] = f'/api/v1/posts/{postid_url_slug}/'

    return flask.jsonify(**context)


@swish_academy.app.route('/api/v1/likes/', methods=['POST'])
def post_api_v1_likes_postid():
    """POST /api/v1/comments/?postid=<postid> endpoint."""
    postid = flask.request.args.get('postid')
    connection = swish_academy.model.get_db()
    check_if_logged_in(connection)

    context = {}
    cur = connection.execute(
        "SELECT likes.likeid, "
        "('/api/v1/likes/' || likes.likeid || '/') as url "
        "FROM likes "
        "INNER JOIN posts "
        "ON posts.postid = likes.postid AND  likes.owner = ? "
        "WHERE likes.postid = ? ",
        (flask.session['username'], postid)
    )

    is_liked = cur.fetchone()

    # if is_liked is not None:
    if is_liked is not None:
        context = is_liked
        return flask.jsonify(**context), 200

    cur = connection.execute(
        "INSERT INTO likes(owner, postid) \
                VALUES (?, ?)",
        (flask.session['username'], postid,)
    )

    cur = connection.execute(
        "SELECT last_insert_rowid() as likeid, "
        "('/api/v1/likes/' || last_insert_rowid() || '/') as url "
        "FROM likes",
        ()
    )

    context = cur.fetchone()

    return flask.jsonify(**context), 201


@swish_academy.app.route('/api/v1/likes/<int:likeid_url_slug>/', methods=['DELETE'])
def delete_api_v1_likes_likeid(likeid_url_slug):
    """DELETE /api/v1/likes/<likeid>/ endpoint."""
    connection = swish_academy.model.get_db()
    check_if_logged_in(connection)

    cur = connection.execute(
        "SELECT likeid "
        "FROM likes "
        "WHERE likeid = ?",
        (likeid_url_slug,)
    )
    errorcheck = cur.fetchone()
    if errorcheck is None:
        raise HTTPError('Not Found', status_code=404)

    cur = connection.execute(
        "SELECT likeid, owner "
        "FROM likes "
        "WHERE likeid = ? ",
        (likeid_url_slug,
         )
    )

    like_owner_errorcheck = cur.fetchone()
    if flask.session['username'] != like_owner_errorcheck['owner']:
        raise HTTPError('Forbidden', status_code=403)

    cur = connection.execute(
        "DELETE FROM likes "
        "WHERE likeid = ? and owner = ? ",
        (likeid_url_slug, flask.session["username"])
    )

    context = {}

    return flask.jsonify(**context), 204


@swish_academy.app.route('/api/v1/comments/', methods=['POST'])
def post_api_v1_comments():
    """POST /api/v1/comments/?postid=<postid> endpoint."""
    postid = flask.request.args.get('postid')
    print("request json:")
    print(flask.request.json)
    text = flask.request.json.get('text', None)
    print(text)
    connection = swish_academy.model.get_db()
    check_if_logged_in(connection)

    # INSERT INTO comments(owner, postid, text)
    cur = connection.execute(
        "INSERT INTO comments(owner, postid, text) "
        "VALUES (?, ?, ?) ",
        (flask.session['username'],
         postid,
         text)
    )

    context = {}

    cur = connection.execute(
        "SELECT last_insert_rowid() as commentid "
        "FROM comments",
        ()
    )

    context = cur.fetchone()
    context['lognameOwnsThis'] = True
    context["owner"] = flask.session["username"]
    context["ownerShowUrl"] = f'/users/{flask.session["username"]}'
    context["text"] = text
    context["url"] = f'/api/v1/comments/{context["commentid"]}'

    return flask.jsonify(**context), 201


@swish_academy.app.route('/api/v1/comments/<int:commentid_url_slug>/',
                    methods=['DELETE'])
def delete_api_v1_comments_commentid(commentid_url_slug):
    """DELETE /api/v1/comments/<commentid>/ endpoint."""
    connection = swish_academy.model.get_db()
    check_if_logged_in(connection)

    cur = connection.execute(
        "SELECT commentid "
        "FROM comments "
        "WHERE commentid = ? ",
        (commentid_url_slug,)
    )
    errorcheck = cur.fetchone()
    print(errorcheck)
    if errorcheck is None:
        raise HTTPError('Not Found', status_code=404)

    cur = connection.execute(
        "SELECT commentid, owner "
        "FROM comments "
        "WHERE commentid = ? ",
        (commentid_url_slug,)
    )

    like_owner_errorcheck = cur.fetchone()
    if flask.session['username'] != like_owner_errorcheck['owner']:
        raise HTTPError('Forbidden', status_code=403)

    cur = connection.execute(
        "DELETE FROM comments "
        "WHERE commentid = ? and owner = ? ",
        (commentid_url_slug, flask.session["username"])
    )

    context = {}

    return flask.jsonify(**context), 204
