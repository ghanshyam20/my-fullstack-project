document.addEventListener("DOMContentLoaded", function () {

  setTimeout(function () {
    const alerts = document.querySelectorAll(".auto-hide");

    alerts.forEach(function(alert) {
      alert.classList.remove("show");
    });

  }, 3000);

});