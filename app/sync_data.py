import threading
import time
import requests
import os
from dotenv import load_dotenv

load_dotenv()

def sync_data(app):
    url = os.getenv('TEST_SERVER_URL') + '/posts'
    token = os.getenv('AUTH_TOKEN')
    sync_interval = int(os.getenv('SYNC_INTERVAL', 10))

    headers = {"Authorization": f"Bearer {token}"}

    while True:
        try:
            print("Fetching data from test server...")
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                posts = response.json()

                with app.app_context():
                    user_post_count = app.config.setdefault('USER_POST_COUNT', {})
                    post_comment_count = app.config.setdefault('POST_COMMENT_COUNT', [])

                    # Clear old data
                    user_post_count.clear()
                    post_comment_count.clear()

                    for post in posts.get('posts', []):
                        user_id = post.get("user_id")
                        post_id = post.get("id")
                        comment_count = post.get("comment_count")

                        # Increment user post count
                        if user_id:
                            user_post_count[user_id] = user_post_count.get(user_id, 0) + 1

                        # Add to popular posts list
                        if post_id or comment_count:
                            post_comment_count.append({
                                "post_id": post_id,
                                "comment_count": comment_count
                            })

                print(" Data synced successfully!")

            else:
                print(f"Failed to fetch data: {response.status_code} - {response.text}")

        except Exception as e:
            print(f"Sync error: {e}")

        time.sleep(sync_interval)

def start_sync(app):
    thread = threading.Thread(target=sync_data, args=(app,))
    thread.daemon = True
    thread.start()
