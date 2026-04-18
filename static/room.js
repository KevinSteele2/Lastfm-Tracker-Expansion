const wallOrder = ['front', 'right', 'back', 'left'];
const wallLinks = {
    'front': '/lastfm',
    'right': 'https://kale-terrier-sk3x.squarespace.com/',
    'back': null,
    'left': null
};

let current = 0;
let rotation = 0;

function turn(direction) {
    document.getElementById(`wall-${wallOrder[current]}`).classList.remove('active');
    current = (current + direction + 4) % 4;
    rotation += direction * 90;
    document.getElementById(`wall-${wallOrder[current]}`).classList.add('active');
    document.getElementById('room').style.transform = `translate(-50%, -50%) rotateY(${rotation}deg)`;
}

document.getElementById('wall-front').classList.add('active');

document.getElementById('click-zone').addEventListener('click', function() {
    const link = wallLinks[wallOrder[current]];
    if (link) window.location.href = link;
});