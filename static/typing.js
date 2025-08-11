// Loading saat submit
let chatForm = document.getElementById("chatForm");
let loading = document.getElementById("loading");

chatForm.addEventListener("submit", function () {
  loading.classList.remove("hidden");
});

// Efek mengetik
let typingElement = document.getElementById("typingText");
if (typingElement) {
  let text = typingElement.dataset.response || "";
  let index = 0;

  function typeEffect() {
    if (index < text.length) {
      typingElement.innerHTML += text.charAt(index);
      index++;
      setTimeout(typeEffect, 30); // kecepatan ketik
    }
  }

  if (text.trim() !== "") {
    typeEffect();
  }
}
