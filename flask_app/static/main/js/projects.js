function loadVideo(path,id) {
    var videoContainer = document.getElementById(id);
    videoContainer.innerHTML = `<iframe width="560" height="315" src=${path} frameborder="0" allowfullscreen></iframe>`;
}