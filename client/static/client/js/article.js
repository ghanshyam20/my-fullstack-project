document.addEventListener("DOMContentLoaded", () => {

    
    const bookmarkBtn = document.getElementById("bookmark-btn");
    const bookmarkCount = document.getElementById("bookmark-count");

    const likeBtn = document.getElementById("like-btn");
    const likeCount = document.getElementById("like-count");

    const commentToggle = document.getElementById("comment-toggle");
    const commentBox = document.getElementById("comment-box");

    const reportBtn = document.getElementById("submit-report");

    
    let controller = null;

    bookmarkBtn?.addEventListener("click", async (e) => {
        e.preventDefault();

        
        if (controller) controller.abort();
        controller = new AbortController();

        try {
            const res = await fetch(bookmarkBtn.dataset.url, {
                method: "POST",
                headers: {
                    "X-CSRFToken": getCSRFToken()
                },
                signal: controller.signal
            });

            const data = await res.json();

    
            bookmarkCount.textContent = data.total_bookmarks;


            bookmarkBtn.classList.toggle("btn-warning", data.bookmarked);
            bookmarkBtn.classList.toggle("text-dark", data.bookmarked);
            bookmarkBtn.classList.toggle("btn-outline-warning", !data.bookmarked);

        } catch (err) {
            if (err.name !== "AbortError") {
                console.error("Bookmark error:", err);
            }
        }
    });

    
    likeBtn?.addEventListener("click", async () => {

        const res = await fetch(likeBtn.dataset.url);
        const data = await res.json();

        likeCount.textContent = data.total_likes;

        likeBtn.classList.toggle("btn-primary", data.liked);
        likeBtn.classList.toggle("btn-outline-primary", !data.liked);
    });

commentToggle?.addEventListener("click", (e) => {
    e.stopPropagation(); 
    commentBox.classList.toggle("d-none");
});


document.addEventListener("click", (e) => {
    if (!commentBox.contains(e.target) && !commentToggle.contains(e.target)) {
        commentBox.classList.add("d-none");
    }
});

    
    document.querySelectorAll(".clickable-img").forEach(img => {
        img.addEventListener("click", () => {
            document.getElementById("modalImage").src =
                img.dataset.img || img.src;

            new bootstrap.Modal(document.getElementById("imageModal")).show();
        });
    });

    
    reportBtn?.addEventListener("click", async () => {

        const reason = document.getElementById("report-reason").value.trim();

        if (!reason) {
            alert("Please enter a reason");
            return;
        }

        await fetch(`/client/report/${ARTICLE_ID}/`, {
            method: "POST",
            headers: {
                "X-CSRFToken": getCSRFToken(),
                "Content-Type": "application/x-www-form-urlencoded"
            },
            body: `reason=${encodeURIComponent(reason)}`
        });

        alert("Report submitted");
        location.reload();
    });

});



function getCSRFToken() {
    return document.cookie.split('; ')
        .find(row => row.startsWith('csrftoken'))
        ?.split('=')[1];
}



document.querySelectorAll(".edit-btn").forEach(btn => {
    btn.addEventListener("click", () => {

        const parent = document.getElementById(`comment-${btn.dataset.id}`);

        const text = parent.querySelector(".comment-text");
        const editBox = parent.querySelector(".edit-box");
        const input = parent.querySelector(".edit-input");

    
        input.value = btn.dataset.content;

        
        text.classList.add("d-none");
        editBox.classList.remove("d-none");
    });
});


document.querySelectorAll(".cancel-edit").forEach(btn => {
    btn.addEventListener("click", () => {
        const parent = btn.closest(".border");

        parent.querySelector(".comment-text").classList.remove("d-none");
        parent.querySelector(".edit-box").classList.add("d-none");
    });
});

document.querySelectorAll(".save-edit").forEach(btn => {
    btn.addEventListener("click", async () => {

        const id = btn.dataset.id;
        const parent = document.getElementById(`comment-${id}`);
        const input = parent.querySelector(".edit-input");

        const res = await fetch(`/client/edit-comment/${id}/`, {
            method: "POST",
            headers: {
                "X-CSRFToken": getCSRFToken(),
                "Content-Type": "application/x-www-form-urlencoded"
            },
            body: `content=${encodeURIComponent(input.value)}`
        });

        const data = await res.json();

        if (data.success) {
            parent.querySelector(".comment-text").innerText = data.content;

            parent.querySelector(".comment-text").classList.remove("d-none");
            parent.querySelector(".edit-box").classList.add("d-none");
        }
    });
});