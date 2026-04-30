


document.addEventListener("DOMContentLoaded", () => {

  // for ui effects
  document.querySelectorAll("input").forEach(input => {
    input.addEventListener("focus", () => {
      input.parentElement.style.transform = "translateX(3px)";
    });
    input.addEventListener("blur", () => {
      input.parentElement.style.transform = "translateX(0)";
    });
  });

  const btn = document.querySelector(".btn-main");
  const form = document.querySelector("form");

  if (form && btn) {
    form.addEventListener("submit", () => {
      btn.innerText = "Creating...";
      btn.disabled = true;
    });
  }

  // password toggle
  ["password1", "password2"].forEach(field => {

    const input = document.getElementById(`id_${field}`);
    if (!input) return;

    const wrapper = input.closest(".mb-3");
    wrapper.style.position = "relative";

    const icon = document.createElement("i");
    icon.className = "bi bi-eye-slash toggle-password";

    icon.style.position = "absolute";
    icon.style.top = "38px";   
    icon.style.right = "12px";
    icon.style.cursor = "pointer";
    icon.style.color = "#6c757d";

    icon.addEventListener("click", () => {
      if (input.type === "password") {
        input.type = "text";
        icon.classList.replace("bi-eye-slash", "bi-eye");
      } else {
        input.type = "password";
        icon.classList.replace("bi-eye", "bi-eye-slash");
      }
    });

    wrapper.appendChild(icon);
  });

});