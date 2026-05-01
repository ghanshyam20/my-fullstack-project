function showToast(message) {
    const toastEl = document.getElementById("toast");
    document.getElementById("toast-body").innerText = message;
    new bootstrap.Toast(toastEl).show();
}

document.addEventListener("DOMContentLoaded", () => {

    const likeBtn = document.getElementById("like-btn");
    const bookmarkBtn = document.getElementById("bookmark-btn");
    const reportBtn = document.getElementById("submit-report");

    // image preview
    document.querySelectorAll(".clickable-img").forEach(img => {
        img.addEventListener("click", () => {
            if (img.dataset.locked) {
                showToast("Upgrade to view image");
                return;
            }

            document.getElementById("modalImage").src = img.dataset.src;
            new bootstrap.Modal(document.getElementById("imageModal")).show();
        });
    });

    // for like 
    likeBtn?.addEventListener("click", async () => {
        const res = await fetch(likeBtn.dataset.url);
        const data = await res.json();
        document.getElementById("like-count").innerText = data.total_likes;
        showToast("Liked");
    });

    // for save
    bookmarkBtn?.addEventListener("click", async () => {
        await fetch(bookmarkBtn.dataset.url, {
            method: "POST",
            headers: { "X-CSRFToken": getCSRFToken() }
        });
        showToast("Saved");
    });

    // comment toggle
    document.getElementById("comment-toggle")?.addEventListener("click", () => {
        document.getElementById("comment-box").classList.toggle("d-none");
    });

    // comment submit
    document.getElementById("comment-form")?.addEventListener("submit", (e) => {
        showToast("Comment added");
    });

    // report
    reportBtn?.addEventListener("click", async () => {
        const reason = document.getElementById("report-reason").value;

        await fetch(`/client/report/${ARTICLE_ID}/`, {
            method: "POST",
            headers: {
                "X-CSRFToken": getCSRFToken(),
                "Content-Type": "application/x-www-form-urlencoded"
            },
            body: `reason=${encodeURIComponent(reason)}`
        });

        bootstrap.Modal.getInstance(document.getElementById("reportModal")).hide();
        showToast("Report submitted");
    });

});

// edit comment
function editComment(id) {
    const textEl = document.getElementById(`comment-text-${id}`);
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

// delete comment
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
        showToast("Deleted");
    });
}

function getCSRFToken() {
    return document.cookie.split('; ')
        .find(row => row.startsWith('csrftoken'))
        ?.split('=')[1];
}