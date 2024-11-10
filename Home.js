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



/* Mouse Effect */
let start = new Date().getTime();
const originPosition = { x: 0, y: 0 };
const last = {
    starTimestamp: start,
    starPosition: originPosition,
    mousePosition: originPosition
}

const config = {
    starAnimationDuration: 1500,
    minimumTimeBetweenStars: 250,
    minimumDistanceBetweenStars: 75,
    glowDuration: 150, // Increased glow duration for smoother animation
    maximumGlowPointSpacing: 5, // Reduced spacing for a smoother trail
    colors: ["249 146 253", "252 254 255"],
    sizes: ["1.4rem", "1rem", "0.6rem"],
    animations: ["fall-1", "fall-2", "fall-3"]
}

let count = 0;

const rand = (min, max) => Math.floor(Math.random() * (max - min + 1)) + min,
    selectRandom = items => items[rand(0, items.length - 1)];

const withUnit = (value, unit) => `${value}${unit}`,
    px = value => withUnit(value, "px"),
    ms = value => withUnit(value, "ms");

const calcDistance = (a, b) => {
    const diffX = b.x - a.x,
        diffY = b.y - a.y;
    return Math.sqrt(Math.pow(diffX, 2) + Math.pow(diffY, 2));
}

const appendElement = element => {
    document.body.appendChild(element);
};

const removeElement = (element, delay) => setTimeout(() => {
    document.body.removeChild(element);
}, delay);

const createGlowPoint = position => {
    const glow = document.createElement("div");

    glow.className = "glow-point";

    glow.style.left = px(position.x);
    glow.style.top = px(position.y);

    appendElement(glow);
    removeElement(glow, config.glowDuration);
}

const determinePointQuantity = distance => Math.max(
    Math.floor(distance / config.maximumGlowPointSpacing),
    1
);

const createGlow = (last, current) => {
    const distance = calcDistance(last, current),
        quantity = determinePointQuantity(distance);

    const dx = (current.x - last.x) / quantity,
        dy = (current.y - last.y) / quantity;

    Array.from(Array(quantity)).forEach((_, index) => {
        const x = last.x + dx * index,
            y = last.y + dy * index;

        createGlowPoint({ x, y });
    });
}

const updateLastMousePosition = position => last.mousePosition = position;

const adjustLastMousePosition = position => {
    if (last.mousePosition.x === 0 && last.mousePosition.y === 0) {
        last.mousePosition = position;
    }
};

const handleOnMove = e => {
    const mousePosition = { x: e.clientX, y: e.clientY }
    adjustLastMousePosition(mousePosition);

    createGlow(last.mousePosition, mousePosition);
    updateLastMousePosition(mousePosition);
}

window.onmousemove = e => handleOnMove(e);
window.ontouchmove = e => handleOnMove(e.touches[0]);
document.body.onmouseleave = () => updateLastMousePosition(originPosition);
