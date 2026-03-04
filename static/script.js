fetch('/api/albums')
    .then(response => response.json())
    .then(data => {
        console.log('Data received:', data);

        if(!data || data.length === 0){
            console.log('No data received');
            return;
        }

        const container = document.getElementById('albums-container');

        for (let i = 0; i < data.length; i++){
            const album = data[i];
            const parts = album.name.split(' - ');
            const albumName =  parts[0];
            const artist = parts[1];
            const count = album.count;

            // Making album card
            const card = document.createElement('div');
            card.className = 'album-card';
            card.textContent = albumName + ' - ' + artist +  ': ' + count + ' listens';

            container.appendChild(card);
        }
    })
    .catch(error => {
        console.error('Error fetching albums:', error);
    });