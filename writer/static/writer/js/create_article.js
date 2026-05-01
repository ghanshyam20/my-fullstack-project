document.addEventListener("DOMContentLoaded", function () {

  /* quill editor */
  const editorEl = document.getElementById("editor");
  const hiddenContent = document.getElementById("hidden-content");
  const form = document.querySelector("form");

  let quill = null;

  if (editorEl) {
    quill = new Quill("#editor", {
      theme: "snow",
      placeholder: "Write your article like a real tech blog...",
      modules: {
        toolbar: [
          [{ header: [1, 2, 3, false] }],
          ["bold", "italic", "underline", "strike"],
          [{ list: "ordered" }, { list: "bullet" }],
          ["blockquote", "code-block"],
          ["link"],
          ["clean"]
        ]
      }
    });
  }

  if (form && hiddenContent && quill) {
    form.addEventListener("submit", function () {
      hiddenContent.value = quill.root.innerHTML;
    });
  }

  /* image preview */
  const input = document.getElementById("image-input");
  const preview = document.getElementById("image-preview");

  if (input && preview) {

    input.addEventListener("change", function () {

      preview.innerHTML = "";

      const files = Array.from(input.files);

      if (files.length === 0) return;

      files.forEach((file, index) => {

        /* validation */
        if (!file.type.startsWith("image/")) {
          console.warn(file.name + " skipped (not image)");
          return;
        }

        if (file.size > 3 * 1024 * 1024) {
          console.warn(file.name + " too large");
          return;
        }

        const reader = new FileReader();

        reader.onload = function (e) {

          /*card */
          const wrapper = document.createElement("div");
          wrapper.classList.add("preview-box");

          /* image */
          const img = document.createElement("img");
          img.src = e.target.result;

          /* name  */
          const name = document.createElement("small");
          name.textContent = file.name;

          /* remove button  */
          const removeBtn = document.createElement("button");
          removeBtn.type = "button";
          removeBtn.innerHTML = "×";
          removeBtn.classList.add("remove-btn");

          removeBtn.addEventListener("click", function () {
            wrapper.remove();
          });

          /* append */
          wrapper.appendChild(removeBtn);
          wrapper.appendChild(img);
          wrapper.appendChild(name);

          preview.appendChild(wrapper);
        };

        reader.readAsDataURL(file);
      });

    });
  }

});