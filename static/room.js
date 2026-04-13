const wallOrder = ['front', 'right', 'back', 'left'];
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