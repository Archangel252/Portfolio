var boardId;
var NewMembers = [];

document.addEventListener('DOMContentLoaded', function() {

     socket = io.connect('https://' + document.domain + ':' + location.port + '/create');
         //socket = io.connect('https://' + document.domain + ':' + location.port + '/chat');
         socket.on('connect', function() {
             socket.emit('joined', {});
         });
         socket.on('board_id', function(data) {
            // Redirect to the URL provided by the server
            console.log(data);
            var boardId = data.id;
        });
        socket.on('redirect', function(data) {
            // Redirect to the URL provided by the server
            window.location.href = data.url;
        });
    // Get the button by its ID
    var createButton = document.getElementById('create-button');

});

function toboard(){
    var nameInput = document.getElementById('name');
    socket.emit('createboard', {'name' : nameInput.value, 'members' : NewMembers});
    //window.location.href = "/home";
}
function initmember(){
    var memInput = document.getElementById('email');
    NewMembers.push(memInput.value);
    console.log("Added member:", memInput.value);
    memInput.value = '';

}
