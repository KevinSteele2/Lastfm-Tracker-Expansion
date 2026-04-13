const wallOrder = ['front', 'right', 'back', 'left'];
let current = 0;

function turn(direction) {
    document.getElementById(`wall-${wallOrder[current]}`).classList.remove('active');
    current = (current + direction + 4) % 4;
    document.getElementById(`wall-${wallOrder[current]}`).classList.add('active');
    document.getElementById('room').style.transform = `rotateY(${current * 90}deg)`;
}

document.getElementById('wall-front').classList.add('active');