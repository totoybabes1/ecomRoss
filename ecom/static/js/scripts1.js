document.addEventListener("DOMContentLoaded", function () {
  // Typing animation for the text
  const text = document.querySelector(".animated-text");
  text.classList.add("typing-animation");

  // Smooth scroll to top when button is clicked
  const button = document.querySelector(".expand-button");
  button.addEventListener("click", function () {
    window.scroll({
      top: 955,
      left: 0,
      behavior: "smooth",
    });
  });

  // Image floating animation
  const img = document.getElementById('floating-img');

  setInterval(() => {
    img.style.transform = 'translate(-50%, -60%)'; // Adjust the Y value to change the distance it moves
    setTimeout(() => {
      img.style.transform = 'translate(-50%, -40%)'; // Adjust the Y value to change the distance it moves
    }, 1000); // Adjust the delay between movements
  }, 2000); // Adjust the interval between movements
});
