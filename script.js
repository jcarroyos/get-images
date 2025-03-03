document.addEventListener("DOMContentLoaded", function() {
    fetch('images.csv')
        .then(response => response.text())
        .then(data => {
            const gallery = document.getElementById('gallery');
            const lines = data.split('\n').slice(1);
            lines.forEach(line => {
                const [imgUrl, pageUrl] = line.split(',').map(item => item.trim());
                if (imgUrl && pageUrl) {
                    const fileName = imgUrl.substring(imgUrl.lastIndexOf('/') + 1);
                    const link = document.createElement('a');
                    link.href = pageUrl;
                    link.target = "_blank";

                    const img = document.createElement('img');
                    img.src = `./images/${fileName}`;

                    link.appendChild(img);
                    gallery.appendChild(link);
                }
            });
        });
});
