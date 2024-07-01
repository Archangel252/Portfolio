// Wait for the DOM content to be fully loaded
document.addEventListener("DOMContentLoaded", function() {
    // Get a reference to the menu bar image element
    const menuBarImage = document.getElementById('menu-bar');

    // Get a reference to the dropdown menu
    const dropdownMenu = document.querySelector('.dropdown');

    // Add a click event listener to the menu bar image
    menuBarImage.addEventListener('click', function() {
        // Toggle the display of the dropdown menu
        dropdownMenu.style.display = (dropdownMenu.style.display === 'inline') ? 'none' : 'inline';

    });
});
const button = document.getElementById('feedback'); // create object for the button
var popup = document.querySelector('.popup');
popup.style.display = 'none';
  button.addEventListener('click', function() { //listen for click
    if(popup.style.display === 'none')
    {
        popup.style.display = 'grid';
    }else
    {
        popup.style.display = 'none';
    }
  });
  