// Waiting  for page load
document.addEventListener("DOMContentLoaded", function () {

    // Toggle password visibility
    const toggle = document.querySelector(".toggle-password");

    if (toggle) {
        toggle.addEventListener("click", function () {

            const input = document.getElementById(this.dataset.target);

            if (input.type === "password") {
                input.type = "text";
                this.classList.remove("bi-eye-slash");
                this.classList.add("bi-eye");
            } else {
                input.type = "password";
                this.classList.remove("bi-eye");
                this.classList.add("bi-eye-slash");
            }

        });
    }

    // Button loading state
    const form = document.querySelector("form");
    const btn = document.querySelector(".btn-login");

    if (form && btn) {
        form.addEventListener("submit", function () {
            btn.innerText = "Logging in...";
            btn.disabled = true;
        });
    }

});