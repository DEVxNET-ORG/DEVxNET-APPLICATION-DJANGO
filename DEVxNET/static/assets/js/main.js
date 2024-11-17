AOS.init({
  offset: 120,
  delay: 0,
  duration: 900,
  easing: "ease",
  once: false,
  mirror: false,
  anchorPlacement: "top-bottom",
});

// Function to remove overlay and enable sound
document.getElementById('playButton').addEventListener('click', function() {
    const video = document.getElementById('myVideo');
    video.muted = false; // Unmute the video
    video.play(); // Ensure video is playing

    // Hide the overlay
    document.getElementById('overlay').style.display = 'none';
});