//image preview
document.addEventListener("DOMContentLoaded", () => {

    document.querySelectorAll(".article-img").forEach(img => {
        img.addEventListener("click", () => {
            const modalImg = document.getElementById("modalImage");

            if (modalImg) {
                modalImg.src = img.src;
                new bootstrap.Modal(document.getElementById("imageModal")).show();
            }
        });
    });

});


// filter 
const filterSelect = document.getElementById("filterSelect");

if (filterSelect) {

    const params = new URLSearchParams(window.location.search);
    const currentType = params.get("type");

    if (currentType) {
        filterSelect.value = currentType;
    }

    filterSelect.addEventListener("change", function () {
        const url = new URL(window.location.href);

        if (this.value === "latest") {
            url.searchParams.delete("type");
        } else {
            url.searchParams.set("type", this.value);
        }

        window.location.href = url.toString();
    });
}