let current = 0;
function turn(direction) {
    current += direction * 90;
    document.getElementById('room').style.transform = `rotateY(${current}deg)`;
}