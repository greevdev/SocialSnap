document.addEventListener("DOMContentLoaded", function () {
    const likeButtons = document.querySelectorAll(".like-button");

    likeButtons.forEach((likeButton) => {
        likeButton.addEventListener("click", updateLikes);
    });
});

function updateLikes(event) {
    event.preventDefault();

    const likeButton = event.currentTarget;
    const postId = likeButton.getAttribute("data-post-id");

    fetch(`/like/${postId}/`, {
        method: "POST",
        headers: {
            "X-CSRFToken": getCookie("csrftoken"),
        },
    })
        .then((response) => response.json())
        .then((data) => {
            const likesCount = likeButton.querySelector(".likes-count");
            likesCount.textContent = data.likes_count;

            const likedSpan = likeButton.querySelector(".liked");
            likedSpan.classList.toggle("active", data.liked); // Toggle the active class

            const heartIcon = likedSpan.querySelector("i"); // Get the <i> element
            heartIcon.style.color = data.liked ? "red" : "white"; // Set color based on liked status
        })
        .catch((error) => {
            console.error("Error:", error);
        });
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";");
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === name + "=") {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}