function openImage(img) {
    const modalImg = document.getElementById("modalImage");
    modalImg.src = img.src;
}


function toggleLike() {
    const btn = document.getElementById("like-btn");
    const url = btn.dataset.url;

    fetch(url)
        .then(res => res.json())
        .then(data => {

            // update count
            document.getElementById('like-count').innerText = data.total_likes;

            // update button style
            if (data.liked) {
                btn.classList.remove("btn-outline-primary");
                btn.classList.add("btn-primary");
            } else {
                btn.classList.remove("btn-primary");
                btn.classList.add("btn-outline-primary");
            }

        });
}

function scrollToComments() {
    const section = document.getElementById("comment-section");

    if (section) {
        section.scrollIntoView({ behavior: "smooth" });
    }
}


function toggleBookmark() {
    const btn = document.getElementById("bookmark-btn");
    const url = btn.dataset.url;

    fetch(url)
        .then(res => res.json())
        .then(data => {

            // update count
            document.getElementById("bookmark-count").innerText = data.total_bookmarks;

            // toggle style
            if (data.bookmarked) {
                btn.classList.remove("btn-outline-warning");
                btn.classList.add("btn-warning");
            } else {
                btn.classList.remove("btn-warning");
                btn.classList.add("btn-outline-warning");
            }

        });
}

function submitReport(articleId) {
    const reason = document.getElementById("report-reason").value;

    fetch(`/client/report/${articleId}/`, {
        method: "POST",
        headers: {
            "Content-Type": "application/x-www-form-urlencoded",
            "X-CSRFToken": getCSRFToken()
        },
        body: `reason=${reason}`
    })
    .then(res => res.json())
    .then(data => {

        if (data.status === "reported") {
            alert("Report submitted ");
        } else {
            alert("You already reported this ");
        }

        location.reload();
    });
}


// CSRF helper
function getCSRFToken() {
    return document.cookie.split('; ')
        .find(row => row.startsWith('csrftoken'))
        ?.split('=')[1];
}