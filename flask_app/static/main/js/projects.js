function loadVideo(path, id) {
    var videoContainer = document.getElementById(id);
    videoContainer.innerHTML = `
        <div class="responsive-iframe-container">
            <iframe src="${path}" frameborder="0" allowfullscreen></iframe>
        </div>
    `;
}