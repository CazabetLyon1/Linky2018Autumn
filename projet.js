$(document).ready(function() {

var chart = null;

  $("#core").load("./accueil.html");
  $("#mod").load("./modal.html");


  // Open navbarSide when button is clicked
  $('#bars').on('click', function() {
    if(!hideSideBar()) {
      $('#menu').addClass('reveal');
      $('#bars').addClass('fa-spin');
      $('#core').addClass('reveal-bis');
    }
  });

  $('#graphique').on('click', function() {
      $("#core").load("./graph.html");
  });

  $('#home').on('click', function() {
    $("#core").load("./accueil.html");
  });

  $(window).scroll(()=>hideSideBar());

});

function hideSideBar() {
  console.log("qfqfqfqfqsf");
  if($('#menu').hasClass('reveal'))
  {
    $('#menu').removeClass('reveal');
    $('#bars').removeClass('fa-spin');
    $('#core').removeClass('reveal-bis');
    return true;
  }
  else return false;
}


function test() {
  var data = {name : "ter"};
      fetch('/clicked', {
        method: 'POST',
        body: JSON.stringify(data)
      })
    .then(function(response) {
      if(response.ok) {
        console.log('click was recorded');
        return;
      }
      throw new Error('Request failed.');
    })
    .catch(function(error) {
      console.log(error);
});
  }