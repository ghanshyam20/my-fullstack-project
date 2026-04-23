const dropArea = document.getElementById("drop-area");
const fileInput = document.getElementById("fileElem");

if (dropArea && fileInput) {

  ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(event => {
    dropArea.addEventListener(event, e => e.preventDefault());
  });

  dropArea.addEventListener("dragover", () => {
    dropArea.classList.add("bg-white");
  });

  dropArea.addEventListener("dragleave", () => {
    dropArea.classList.remove("bg-white");
  });

  dropArea.addEventListener("drop", (e) => {
    fileInput.files = e.dataTransfer.files;
    dropArea.classList.remove("bg-white");
  });

}