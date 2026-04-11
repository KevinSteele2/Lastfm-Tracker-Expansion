function loadAlbums(){
    const username = document.getElementById('username-input').value;
    const container = document.getElementById('albums-container');
    container.innerHTML = '<div class="loading">loading albums...</div>'
    fetch(`/api/albums?username=${username}`)
        .then(response => response.json())
        .then(data => {
            console.log('Data received:', data);

            if(!data || data.length === 0){
                console.log('No data received');
                return;
            }

            container.innerHTML = '';

            for (let i = 0; i < data.length; i++){
                const album = data[i];
                const parts = album.name.split(' - ');
                const albumName =  parts[0];
                const artist = parts[1];
                const count = album.count;

                // Making album card
                const card = document.createElement('div');
                card.className = 'album-card';
                
                const img = document.createElement('img');
                img.src = album.cover || '';
                img.alt = albumName;

                if(count >= 30){
                    img.classList.add('border-purple');
                }
                else if (count >= 20){
                    img.classList.add('border-blue');
                }
                else if (count >= 10){
                    img.classList.add('border-gold');
                }
                else if (count >= 5){
                    img.classList.add('border-silver');
                }

                const label = document.createElement('p');
                label.textContent = albumName + ' - ' + artist + ': ' + count + ' listens';

                card.appendChild(img)
                card.appendChild(label);
                container.appendChild(card);
            }
        })

        .catch(error => {
            console.error('Error fetching albums:', error);
            container.innerHTML = '<div class="loading">Error loading albums</div>';
        });
}

document.getElementById('username-input').addEventListener('keydown', function(event) {
    if (event.key === 'Enter'){
        loadAlbums();
    }
});