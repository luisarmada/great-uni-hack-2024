// JavaScript to toggle between light and meme themes with sound effect and theme persistence
function toggleTheme() {
    document.body.classList.toggle('meme-theme');

    // Play a meme sound when toggling
    const audio = new Audio('ding.mp3'); // Add a funny meme sound file here
    audio.play();

    // Save the theme preference
    if (document.body.classList.contains('meme-theme')) {
        localStorage.setItem('theme', 'meme');
    } else {
        localStorage.setItem('theme', 'light');
    }
}

// Check for saved theme preference on page load
document.addEventListener('DOMContentLoaded', () => {
    if (localStorage.getItem('theme') === 'meme') {
        document.body.classList.add('meme-theme');
    }
});
