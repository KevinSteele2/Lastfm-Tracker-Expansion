let currentBreedId = null;
let currentAliases = [];
let streak = 0;
 
function loadNewDog() {
    document.getElementById('result-message').textContent = '';
    document.getElementById('guess-input').value = '';
    document.getElementById('guess-input').style.display = 'inline';
    document.querySelector('#guess-area button').style.display = 'inline';
    document.getElementById('next-button').style.display = 'none';
    document.getElementById('dog-image').src = '';
 
    fetch('/api/dogbreed/random')
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                document.getElementById('result-message').textContent = data.error;
                return;
            }
            currentBreedId = data.breed_id;
            currentAliases = data.aliases || [];
            document.getElementById('dog-image').src = data.image_url;
        });
}
 
function submitGuess() {
    const guess = document.getElementById('guess-input').value;
    if (!guess || !currentBreedId) {
        return;
    }
 
    fetch('/api/dogbreed/guess', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ breed_id: currentBreedId, guess: guess, aliases: currentAliases })
    })
        .then(response => response.json())
        .then(data => {
            const message = document.getElementById('result-message');
 
            if (data.correct) {
                streak++;
                document.getElementById('streak').textContent = streak;
                message.textContent = `Correct! It's a ${data.answer}.`;
            } else {
                streak = 0;
                document.getElementById('streak').textContent = streak;
                message.textContent = `Nope, that was a ${data.answer}.`;
            }
 
            document.getElementById('guess-input').style.display = 'none';
            document.querySelector('#guess-area button').style.display = 'none';
            document.getElementById('next-button').style.display = 'inline';
        });
}
 
// Load the first dog when the page opens
loadNewDog();