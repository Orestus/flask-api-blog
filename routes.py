from app import app, db
from flask import jsonify,request
from models import User, Post, Comments
from werkzeug.exceptions import BadRequest, NotFound
from flask_jwt_extended import get_jwt_identity, jwt_required


@app.route('/', methods=['GET'])
def home():
    return jsonify(message = "Hello world")

@app.route('/v1/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data:
        return jsonify(message="Invalid data"), 400
    email = data.get('email')
    username = data.get('username')
    password = data.get('password')
    if not email or not username or not password:
        return jsonify(message="Missing fields!"), 400
    user = User(email=email, username=username)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    return jsonify(message="User registered succesfully! "), 201

@app.route('/v1/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data:
        raise BadRequest("Invalid data")
    email = data.get('email')
    password = data.get('password')
    token, _ = User.authenticate(email, password)
    if not token:
         raise BadRequest("Invalid credentials")
    return jsonify(access_token = token ), 200

@app.route('/v1/posts', methods=['POST'])
@jwt_required()
def add_post():
    user_id = get_jwt_identity()
    data = request.get_json()
    title = data.get('title')
    body = data.get('body')
    if not title or not body:
        raise BadRequest('Missing mandatory fields')
    post = Post(title=title, body=body, author_id=user_id)
    db.session.add(post)
    db.session.commit()
    return jsonify(message='Post added successfully!')




@app.route('/v1/posts', methods=['GET'])
def get_posts():
    posts = Post.query.all()
    return jsonify(posts=[p.to_dict() for p in posts]), 200


@app.route('/v1/posts/<int:post_id>', methods=['GET'])
def get_post(post_id):
    post = Post.query.get(post_id)
    if not post:
        raise NotFount("Post not found")
    return jsonify(posts=post.to_dict()), 200


@app.route('/v1/posts/<int:post_id>', methods=['PATCH'])
@jwt_required()
def update_post(post_id):
    user_id = int(get_jwt_identity())
    post = Post.query.get(post_id)
    if not post:
        raise NotFound("Post not found")
    if post.author_id != user_id:
        raise Forbidden("Permission denied")

    data = request.get_json()
    post.title = data.get('title', post.title)
    post.body = data.get('body', post.body )

    db.session.commit()
    return jsonify(message='Post updated successfully!'), 200


@app.route('/v1/posts/<int:post_id>', methods=['DELETE'])
@jwt_required()
def delete_post(post_id):
    user_id = int(get_jwt_identity())
    #post = Post.query.get(post_id) # old version
    post = db.session.get(Post, post_id)
    if not post:
        raise NotFound('Post not found')
    if post.author_id != user_id:
        raise Forbidden("Permission Denied!")
    db.session.delete(post)
    db.session.commit()
    return jsonify(message="Post delete successfully")


@app.route('/v1/posts/<int:post_id>/comments', methods=['POST'])
@jwt_required()
def add_comment(post_id):
    user_id = int(get_jwt_identity())
    #post = Post.query.get(post_id) # old version
    post = db.session.get(Post, post_id)
    if not post:
        raise NotFound('Post not found')
    data = request.get_json()
    body = data.get('body')
    if not body:
        raise BadRequest("Missing field")
    comment = Comments(body=body, author_id=user_id, post_id=post_id)
    db.session.add(comment)
    db.session.commit()
    return jsonify(message="Comment added successfully"), 200


@app.route('/v1/posts/<int:post_id>/comments', methods=['GET'])
def get_commets(post_id):
    post = db.session.get(Post, post_id)
    if not post:
        raise NotFound("Post not found")
    comments = post.comments.all()
    return jsonify(comments=[c.to_dict() for c in comments]), 200
