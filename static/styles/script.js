function adjustTableWidth() {
  var scrollWidth = $('.tbl-content').width() - $('.tbl-content table').width();
  $('.tbl-header').css({'padding-right':scrollWidth});
}

$(document).ready(function() {
  adjustTableWidth();
});

$(window).resize(function() {
  adjustTableWidth();
});

function openRecipeWindow(recipe) {
  // Create a new div element to hold the recipe preview
  const recipePreview = document.createElement('div');
  recipePreview.classList.add('recipe-preview');

  // Set the innerHTML of the recipe preview to the recipe information
  recipePreview.innerHTML = recipe;

  // Add the recipe preview to the body of the document
  document.body.appendChild(recipePreview);

  // Create a button to close the recipe preview
  const closeButton = document.createElement('button');
  closeButton.innerHTML = 'Close';

  // Add an event listener to the close button to remove the recipe preview from the page when clicked
  closeButton.addEventListener('click', function() {
    document.body.removeChild(recipePreview);
  });

  // Add the close button to the recipe preview
  recipePreview.appendChild(closeButton);
}

function create_log(pk) {
    const url = '/record/' + pk + '/new-log/';
    window.location.href = url;
}

// function incrementValue(logID) {
//   console.log("Log ID:", logID);
//
//   var temperatureElement = document.getElementById("temperature" + logID);
//   console.log("Temperature element:", temperatureElement);
//
//   var temperatureValue = parseFloat(temperatureElement.innerText);
//   console.log("Temperature value:", temperatureValue);
//
//   temperatureElement.innerText = (temperatureValue + 1).toFixed(1);
//   console.log("New temperature value:", temperatureElement.innerText);
// }
