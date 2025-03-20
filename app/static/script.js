document.addEventListener("DOMContentLoaded", () => {
    // Load top users
    fetch("/users")
        .then(response => response.json())
        .then(data => {
            const usersList = document.getElementById("top-users");
            usersList.innerHTML = "";
            data.forEach(user => {
                const li = document.createElement("li");
                li.textContent = `User ID: ${user.user_id} | Posts: ${user.post_count}`;
                usersList.appendChild(li);
            });
        });

    // Load latest posts
    fetch("/posts?type=latest")
        .then(response => response.json())
        .then(data => {
            const latestList = document.getElementById("latest-posts");
            latestList.innerHTML = "";
            data.forEach(post => {
                const li = document.createElement("li");
                li.textContent = `Post ID: ${post.post_id} | Timestamp: ${post.timestamp}`;
                latestList.appendChild(li);
            });
        });

    // Load popular posts
    fetch("/posts?type=popular")
        .then(response => response.json())
        .then(data => {
            const popularList = document.getElementById("popular-posts");
            popularList.innerHTML = "";
            data.forEach(post => {
                const li = document.createElement("li");
                li.textContent = `Post ID: ${post.post_id} | Comments: ${post.comment_count}`;
                popularList.appendChild(li);
            });
        });
});
