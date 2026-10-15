# Blog REST API (Flask)

A simple blog REST API built with Python and Flask as a hands-on learning project. Users can register and log in, then create and manage posts and comments. Authentication is done with JWT access tokens.

> **Note:** This is a practice project. It runs on Flask's development server and uses SQLite, so it is not meant for production use.

## Features

- Register and log in (passwords are hashed, an access token is issued on login)
- Read, add, update and delete posts
- Read and add new comments on a post
- Users can only modify their own posts.
- Code split into modules (models, routes, app setup, config)
- Dockerized and deployed on an AWS EC2 instance

## Tech stack

- Python, Flask
- Flask-SQLAlchemy, Flask-Migrate (SQLite)
- Flask-JWT-Extended, Werkzeug (authentication, password hashing)
- Postman (API testing)
- Docker

## Project structure

```
Blog/
├── app.py            # creates the Flask app, database and JWT objects
├── config.py         # app settings: database URL, JWT secret key
├── models.py         # database classes: User, Post, Comment
├── routes.py         # API routes
├── run.py            # imports and runs the application
├── migrations/       # database migrations (Flask-Migrate)
├── instance/         # SQLite database (blog.db) with demo data
├── requirements.txt
└── Dockerfile
```

## Run locally

```bash
# create and activate a virtual environment
python -m venv venv
venv\Scripts\activate          # Windows
source venv/bin/activate       # Linux / macOS

# install dependencies
pip install -r requirements.txt

# start the app
flask run
```

The API is now available at `http://127.0.0.1:5000`.

## Try it quickly

The repository includes a SQLite database (`instance/blog.db`) with some demo posts and comments, so you can check how it works right away. Reading data doesn't require authentication. Open these URLs in a browser or send GET requests from Postman:

- All posts: `http://127.0.0.1:5000/v1/posts`
- A single post: `http://127.0.0.1:5000/v1/posts/1`
- Comments for a post: `http://127.0.0.1:5000/v1/posts/1/comments`

## Run with Docker

### Pull the image from Docker Hub

docker pull orestus50/flask_api_blog
docker run -d -p 5000:5000 --name flask-blog orestus50/flask_api_blog

### Or build it yourself

docker build -t flask-blog-api .
docker run -d -p 5000:5000 --name flask-blog flask-blog-api

### Run on an AWS EC2 instance (Ubuntu)

1. In the instance's security group, add an inbound rule: TCP, port 5000.
2. Install Docker: sudo apt update && sudo apt install -y docker.io
3. (Optional) To avoid using 'sudo' for every docker command: sudo usermod -aG docker $USER && newgrp docker
4. Pull and run the image:
   sudo docker pull orestus50/flask_api_blog
   sudo docker run -d -p 5000:5000 --name flask-blog orestus50/flask_api_blog

5. Open `http://<EC2-public-IP>:5000/v1/posts` in a browser. Use the public IP instead of `127.0.0.1` in all the example URLs.

## API endpoints

| Method | Route | Auth required | Description |
|--------|-------|:-------------:|-------------|
| POST | `/v1/register` | No | Register a new user |
| POST | `/v1/login` | No | Log in and receive an access token |
| GET | `/v1/posts` | No | List all posts |
| GET | `/v1/posts/<post_id>` | No | Get a single post |
| POST | `/v1/posts` | Yes | Add a new post |
| DELETE | `/v1/posts/<post_id>` | Yes (owner only) | Delete a post |
| GET | `/v1/posts/<post_id>/comments` | No | List comments for a post |
| POST | `/v1/posts/<post_id>/comments` | Yes | Add a comment to a post |

See `routes.py` for the exact routes.

## Usage examples

All request bodies are JSON (in Postman: Body > raw > JSON).

### Register

`POST /v1/register`

```json
{
    "email": "user1@test.com",
    "username": "user1",
    "password": "123456"
}
```

### Log in

`POST /v1/login`

```json
{
    "email": "user1@test.com",
    "password": "123456"
}
```

The response contains an access token:

```json
{
    "access_token": "eyJhbGciOiJ..."
}
```

The token expires after 15 minutes (the library default). Log in again to get a fresh one.

### Authenticated requests

Add the token to the request headers:

```
Authorization: Bearer <your_access_token>
```

### Add a post

`POST /v1/posts`

```json
{
    "title": "The best post ever",
    "body": "The post does not have to be the best ever, it only needs to be considered as one"
}
```

### Add a comment

`POST /v1/posts/1/comments`

```json
{
    "body": "this is a very good post, keep going!"
}
```

### Delete a post

`DELETE /v1/posts/2`

Requires the access token, and you can only delete a post you created.

## Notes

- The SQLite database and the JWT secret key in `config.py` are demo values, kept in the repository on purpose so the project works out of the box.
- Tables are managed with Flask-Migrate (`flask db` commands).
