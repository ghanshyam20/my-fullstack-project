document.addEventListener("DOMContentLoaded", () => {

 
  const elements = document.querySelectorAll(".reveal");

  function reveal() {
    const trigger = window.innerHeight - 100;

    elements.forEach(el => {
      if (el.getBoundingClientRect().top < trigger) {
        el.classList.add("active");
      }
    });
  }

  window.addEventListener("scroll", reveal);
  reveal();


  document.querySelectorAll(".feature-box").forEach(box => {
    box.addEventListener("click", () => {
      box.classList.toggle("active");
    });
  });

});