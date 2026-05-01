document.addEventListener("DOMContentLoaded", function () {

  const input = document.getElementById("image-input");
  const preview = document.getElementById("image-preview");
  const fileNameText = document.getElementById("file-name");

  if (!input) return;

  input.addEventListener("change", function () {

    const files = Array.from(input.files);

    if (files.length === 0) {
      if (fileNameText) fileNameText.textContent = "";
      preview.innerHTML = "";
      return;
    }

    // show file count
    if (fileNameText) {
      fileNameText.textContent = files.length + " file(s) selected";
    }

    // clear previous preview
    if (preview) preview.innerHTML = "";

    files.forEach(file => {

      if (!file.type.startsWith("image/")) return;

      const reader = new FileReader();

      reader.onload = function (e) {

        const wrapper = document.createElement("div");
        wrapper.classList.add("preview-box");

        const img = document.createElement("img");
        img.src = e.target.result;

        const name = document.createElement("small");
        name.textContent = file.name;

        wrapper.appendChild(img);
        wrapper.appendChild(name);

        if (preview) preview.appendChild(wrapper);
      };

      reader.readAsDataURL(file);
    });

  });

});