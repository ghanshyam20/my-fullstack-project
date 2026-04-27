document.addEventListener("DOMContentLoaded", () => {


  document.querySelectorAll("input").forEach(input => {

    input.addEventListener("focus", () => {
      input.parentElement.style.transform = "translateX(3px)";
    });

    input.addEventListener("blur", () => {
      input.parentElement.style.transform = "translateX(0)";
    });

  });

  const btn = document.querySelector(".btn-main");

  if (btn) {
    btn.addEventListener("click", () => {
      btn.style.transform = "scale(0.97)";
      setTimeout(() => {
        btn.style.transform = "";
      }, 150);
    });
  }

    
  const form = document.querySelector("form");

  if (form) {
    form.addEventListener("submit", () => {
      btn.innerText = "Creating...";
      btn.disabled = true;
    });
  }

});