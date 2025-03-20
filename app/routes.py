from flask import Blueprint, render_template, jsonify, request, current_app
import requests
import os
from dotenv import load_dotenv

load_dotenv()

bp = Blueprint('routes', __name__)

# -------------------------
# Home Page Route
# -------------------------
@bp.route('/')
def home():
    return render_template('index.html')

# -------------------------
# Get Users Route
# -------------------------
@bp.route('/users')
def users():
    url = os.getenv('TEST_SERVER_URL')
    token = os.getenv('AUTH_TOKEN')

    if not url:
        return "TEST_SERVER_URL is missing in .env file", 500
    if not token:
        return "ACCESS_TOKEN is missing in .env file", 500
    
    url += '/users'
    headers = {'Authorization': f'Bearer {token}'}

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        users_data = response.json().get('users', {})
        return render_template('users.html', users=users_data)
    else:
        return f"Failed to fetch users: {response.status_code} - {response.text}"

# -------------------------
#  Get User Posts Route
# -------------------------
@bp.route('/users/<int:user_id>/posts')
def user_posts(user_id):
    url = f"{os.getenv('TEST_SERVER_URL')}/users/{user_id}/posts"
    token = os.getenv('AUTH_TOKEN')
    headers = {'Authorization': f'Bearer {token}'}

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        posts_data = response.json().get('posts', [])
        return render_template('posts.html', posts=posts_data)
    else:
        return f"Failed to fetch posts: {response.status_code} - {response.text}"

# -------------------------
#  Get Comments for Post Route
# -------------------------
@bp.route('/posts/<int:post_id>/comments')
def get_comments(post_id):   # ✅ Fixed parameter name
    url = f"{os.getenv('TEST_SERVER_URL')}/posts/{post_id}/comments"
    token = os.getenv('AUTH_TOKEN')
    headers = {'Authorization': f'Bearer {token}'}

    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            comments = response.json().get('comments', [])
            return render_template('comments.html', comments=comments)
        else:
            return f"Failed to fetch comments: {response.status_code} - {response.text}"
    except Exception as e:
        return f"Error fetching comments: {e}"

# -------------------------
# Top Users (based on post count)
# -------------------------
# @bp.route('/users/top', methods=['GET'])
# def get_top_users():
#     user_post_count = current_app.config.get('USER_POST_COUNT', {})
#     users_data = current_app.config.get('USERS', {})

#     if not user_post_count:
#         return jsonify({"error": "No user data available"}), 404
    
#     top_users = sorted(user_post_count.items(), key=lambda x: x[1], reverse=True)[:10]
    
#     result = [
#         {"user_id": user_id, "name": users_data.get(str(user_id), "Unknown"), "post_count": count}
#         for user_id, count in top_users
#     ]
    
#     return jsonify(result)

# # -------------------------
# # Popular Posts (based on comment count)
# # -------------------------
# @bp.route('/posts/popular', methods=['GET'])
# def get_popular_posts():
#     post_comment_count = current_app.config.get('POST_COMMENT_COUNT', [])
    
#     if not post_comment_count:
#         return jsonify({"error": "No post data available"}), 404
    
#     # Sort based on comment count in descending order
#     popular_posts = sorted(post_comment_count, key=lambda x: x['comment_count'], reverse=True)[:10]
    
#     return jsonify(popular_posts)

# -------------------------
# Register Routes
# -------------------------
def register_routes(app):
    app.register_blueprint(bp)
