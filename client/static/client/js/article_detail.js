// toast helper
function showToast(message) {
    const toastEl = document.getElementById("toast");
    if (!toastEl) return;

    document.getElementById("toast-body").innerText = message;

    let toast = bootstrap.Toast.getInstance(toastEl);
    if (!toast) {
        toast = new bootstrap.Toast(toastEl);
    }

    toast.show();
}

document.addEventListener("DOMContentLoaded", () => {

    const likeBtn = document.getElementById("like-btn");
    const bookmarkBtn = document.getElementById("bookmark-btn");
    const reportBtn = document.getElementById("submit-report");

    //image preview 
    document.querySelectorAll(".clickable-img").forEach(img => {
        img.addEventListener("click", () => {
            if (img.dataset.locked) {
                showToast("Upgrade to view image");
                return;
            }

            const modalImg = document.getElementById("modalImage");
            if (modalImg) {
                modalImg.src = img.src;
                new bootstrap.Modal(document.getElementById("imageModal")).show();
            }
        });
    });

    // like
    likeBtn?.addEventListener("click", async () => {
        try {
            const res = await fetch(likeBtn.dataset.url, {
                method: "POST",
                headers: {
                    "X-CSRFToken": getCSRFToken()
                }
            });

            const data = await res.json();

            document.getElementById("like-count").innerText = data.total_likes;

            showToast(data.liked ? "Liked " : "Unliked");

        } catch (err) {
            showToast("Error liking");
        }
    });

    // bookmark
    bookmarkBtn?.addEventListener("click", async () => {
        try {
            const res = await fetch(bookmarkBtn.dataset.url, {
                method: "POST",
                headers: {
                    "X-CSRFToken": getCSRFToken()
                }
            });

            const data = await res.json();

            document.getElementById("bookmark-count").innerText = data.total_bookmarks;

            showToast(data.bookmarked ? "Saved" : "Removed");

            // toggel 
            if (data.bookmarked) {
                bookmarkBtn.classList.add("btn-warning");
                bookmarkBtn.classList.remove("btn-outline-warning");
            } else {
                bookmarkBtn.classList.remove("btn-warning");
                bookmarkBtn.classList.add("btn-outline-warning");
            }

        } catch (err) {
            showToast("Error saving");
        }
    });

    //comment toggle
    document.getElementById("comment-toggle")?.addEventListener("click", () => {
        document.getElementById("comment-box")?.classList.toggle("d-none");
    });

    //comment 
    document.getElementById("comment-form")?.addEventListener("submit", () => {
        showToast("Comment added");
    });

    // report 
    reportBtn?.addEventListener("click", async () => {

        const reasonEl = document.getElementById("report-reason");
        const reason = reasonEl?.value.trim();

        if (!reason) {
            showToast("Enter reason first");
            return;
        }

        try {
            const res = await fetch(`/client/report/${ARTICLE_ID}/`, {
                method: "POST",
                headers: {
                    "X-CSRFToken": getCSRFToken(),
                    "Content-Type": "application/x-www-form-urlencoded"
                },
                body: `reason=${encodeURIComponent(reason)}`
            });

            const data = await res.json();

            if (data.status === "already_reported") {
                showToast("Already reported");
            } else {
                showToast("Report submitted");
            }

            reasonEl.value = "";

            const modal = bootstrap.Modal.getInstance(document.getElementById("reportModal"));
            if (modal) modal.hide();

        } catch (err) {
            showToast("Error reporting");
        }
    });

});


// edit comment
function editComment(id) {
    const textEl = document.getElementById(`comment-text-${id}`);
    if (!textEl) return;

    const newText = prompt("Edit comment", textEl.innerText);
    if (!newText) return;

    fetch(`/client/edit-comment/${id}/`, {
        method: "POST",
        headers: {
            "X-CSRFToken": getCSRFToken(),
            "Content-Type": "application/x-www-form-urlencoded"
        },
        body: `content=${encodeURIComponent(newText)}`
    })
    .then(res => res.json())
    .then(data => {
        if (data.success) {
            textEl.innerText = data.content;
            showToast("Comment updated");
        }
    });
}


//  delete comment
function deleteComment(id) {
    if (!confirm("Delete this comment?")) return;

    fetch(`/client/delete-comment/${id}/`, {
        method: "POST",
        headers: {
            "X-CSRFToken": getCSRFToken()
        }
    })
    .then(() => {
        location.reload();
    });
}


//csrf token helper
function getCSRFToken() {
    return document.cookie.split('; ')
        .find(row => row.startsWith('csrftoken'))
        ?.split('=')[1];
}