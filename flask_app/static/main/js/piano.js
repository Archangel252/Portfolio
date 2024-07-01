//sound URLs
const sound = {
    65: "http://carolinegabriel.com/demo/js-keyboard/sounds/040.wav",
    87: "http://carolinegabriel.com/demo/js-keyboard/sounds/041.wav",
    83: "http://carolinegabriel.com/demo/js-keyboard/sounds/042.wav",
    69: "http://carolinegabriel.com/demo/js-keyboard/sounds/043.wav",
    68: "http://carolinegabriel.com/demo/js-keyboard/sounds/044.wav",
    70: "http://carolinegabriel.com/demo/js-keyboard/sounds/045.wav",
    84: "http://carolinegabriel.com/demo/js-keyboard/sounds/046.wav",
    71: "http://carolinegabriel.com/demo/js-keyboard/sounds/047.wav",
    89: "http://carolinegabriel.com/demo/js-keyboard/sounds/048.wav",
    72: "http://carolinegabriel.com/demo/js-keyboard/sounds/049.wav",
    85: "http://carolinegabriel.com/demo/js-keyboard/sounds/050.wav",
    74: "http://carolinegabriel.com/demo/js-keyboard/sounds/051.wav",
    75: "http://carolinegabriel.com/demo/js-keyboard/sounds/052.wav",
    79: "http://carolinegabriel.com/demo/js-keyboard/sounds/053.wav",
    76: "http://carolinegabriel.com/demo/js-keyboard/sounds/054.wav",
    80: "http://carolinegabriel.com/demo/js-keyboard/sounds/055.wav",
    186: "http://carolinegabriel.com/demo/js-keyboard/sounds/056.wav"
};
//define the most recent set keys
let pressedKeys = ""; 

const text = document.getElementById("old-one-text");

const keys = document.querySelectorAll(".keys");

const piano = document.querySelector(".piano");

const keysDivs = document.querySelectorAll('.keys div');

const keyTexts = document.querySelectorAll('.key-text');

// Loop through each div element
keysDivs.forEach(function(div) {
    // Add event listener for mouseover event
    div.addEventListener('mouseover', function() {
        // Select the child element with the class "key-text" and toggle its visibility
        keyTexts.forEach(function(keyText) {
            keyText.style.display = 'block';
        });
    });

    div.addEventListener('mouseout', function() {
        // Loop through all ".key-text" elements and set their visibility to "hidden"
        keyTexts.forEach(function(keyText) {
            keyText.style.display = 'none';
        });
    });
});

function keyupListener(event){
    const keyChar = event.key.toLowerCase();
    const keyDiv = document.getElementById(keyChar);
    keyDiv.style.backgroundColor = '';
}
// Add a keydown event listener 
function keydownListener(event) {
    const keyCode = event.keyCode;
    const keyChar = event.key.toLowerCase();

    // Check if exists 
    if (sound[keyCode]) {
        // make an audio object
        const audio = new Audio(sound[keyCode]);

        const keyDiv = document.getElementById(keyChar);
        keyDiv.style.backgroundColor = 'yellow';

        // Play
        audio.play();

        
        
    }
    pressedKeys += event.key;
    if (pressedKeys.length >= 8){
        if (pressedKeys == "weseeyou"){
            text.textContent = "I have Awoken";

            const creepyAudio = "https://orangefreesounds.com/wp-content/uploads/2020/09/Creepy-piano-sound-effect.mp3?_=1";
            const audio = new Audio(creepyAudio);

            audio.play();

            keys.forEach(function(element) {
                // Set the display property to "none"
                element.style.display = "none";
            });

            
            
            piano.style.backgroundImage = "url('../static/main/images/texture.jpeg')";
            //remove event listener
            document.removeEventListener("keydown", keydownListener);
        } else{
            pressedKeys = pressedKeys.substring(1);
        }
    }

};
document.addEventListener("keydown", keydownListener);
document.addEventListener("keyup", keyupListener);

