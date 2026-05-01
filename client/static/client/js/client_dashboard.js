function showToast(msg) {
    const toast = new bootstrap.Toast(document.getElementById("toast"));
    document.getElementById("toast-body").innerText = msg;
    toast.show();
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

            document.getElementById("modalImage").src = img.src;
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

    // bookmark for  article 
    bookmarkBtn?.addEventListener("click", async () => {
        await fetch(bookmarkBtn.dataset.url, {
            method: "POST",
            headers: { "X-CSRFToken": getCSRFToken() }
        });

        showToast("Saved");
    });

    // for report 
    reportBtn?.addEventListener("click", async () => {

        const reason = document.getElementById("report-reason").value.trim();

        if (!reason) {
            showToast("Enter reason first");
            return;
        }

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

        document.getElementById("report-reason").value = "";
        bootstrap.Modal.getInstance(document.getElementById("reportModal")).hide();
    });

    // comment TOGGLE
    document.getElementById("comment-toggle")?.addEventListener("click", () => {
        document.getElementById("comment-box").classList.toggle("d-none");
    });

});

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
            showToast("Updated");
        }
    });
}

function getCSRFToken() {
    return document.cookie.split('; ')
        .find(row => row.startsWith('csrftoken'))
        ?.split('=')[1];
}