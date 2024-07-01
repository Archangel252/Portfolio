var socket;
    document.addEventListener("keypress", handleKeyPress);
    $(document).ready(function(){
        
        socket = io.connect('https://' + document.domain + ':' + location.port + '/chat');
        //socket = io.connect('http://localhost:8080/chat');
        socket.on('connect', function() {
            socket.emit('joined', {});
        });
        //  updates the states of the chat
        socket.on('status', function(data) {     
            let tag  = document.createElement("p");
            let text = document.createTextNode(data.msg);
            let element = document.getElementById("chat");
            tag.appendChild(text);
            tag.style.cssText = data.style;
            element.appendChild(tag);
            $('#chat').scrollTop($('#chat')[0].scrollHeight);
        });
        // adds chats the the chat box
        socket.on('chat', function(data) {    
            let tag  = document.createElement("p");
            let text = document.createTextNode(data.msg);
            let element = document.getElementById("chat");
            tag.appendChild(text);
            tag.style.cssText = data.style;
            element.appendChild(tag);
            $('#chat').scrollTop($('#chat')[0].scrollHeight);
        });         
    });
   
    // function to exit the chat
    function LeaveChat()
    {
        socket.emit('left', {});
        window.location.href = "/home";
    }
    // inputs the chat when enter is pressed
    function handleKeyPress(event) {
    if (event.key === "Enter") {
        let chatElement = document.getElementById('chatInput'); 
        let chatText = chatElement.value;
        socket.emit('chat', {'text' : chatText});
        chatElement.value = ''        
    }
}