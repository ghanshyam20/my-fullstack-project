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




document.addEventListener("DOMContentLoaded", function () {

  const banner = document.getElementById("cookie-banner");
  const acceptBtn = document.getElementById("accept-cookies");
  const rejectBtn = document.getElementById("reject-cookies");
  const analyticsToggle = document.getElementById("analytics-toggle");

  if (!banner) return;

  // hide if already decided
  const saved = localStorage.getItem("cookie_consent");
  if (saved) {
    banner.style.display = "none";
  }

  // if user accepts → analytics ON
  acceptBtn.addEventListener("click", function () {

    const consentData = {
      necessary: true,
      analytics: true
    };

    localStorage.setItem("cookie_consent", JSON.stringify(consentData));
    banner.style.display = "none";

    console.log("Accepted:", consentData);
  });

  // if user rejects → analytics OFF
  rejectBtn.addEventListener("click", function () {

    const consentData = {
      necessary: true,
      analytics: false
    };

    localStorage.setItem("cookie_consent", JSON.stringify(consentData));
    banner.style.display = "none";

    console.log("Rejected:", consentData);
  });

});

document.addEventListener("DOMContentLoaded", () => {

  // feature expand
  document.querySelectorAll(".feature-box").forEach(box => {
    box.addEventListener("click", () => {
      box.classList.toggle("active");
    });
  });

});