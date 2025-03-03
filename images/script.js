document.addEventListener("DOMContentLoaded", function() {
    fetch('images.csv')
        .then(response => response.text())
        .then(data => {
            const gallery = document.getElementById('gallery');
            const lines = data.split('\n').slice(1); // Skip header line
            lines.forEach(line => {
                const [imgUrl, pageUrl] = line.split(',').map(item => item.trim());
                if (imgUrl && pageUrl) {
                    const link = document.createElement('a');
                    link.href = pageUrl;
                    link.target = "_blank"; // Abrir en una nueva pestaña

                    const img = document.createElement('img');
                    img.src = imgUrl;

                    link.appendChild(img);
                    gallery.appendChild(link);
                }
            });
        });
});
