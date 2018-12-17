var chartr = null;

$(document).ready(function() {


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
  if($('#menu').hasClass('reveal'))
  {
    $('#menu').removeClass('reveal');
    $('#bars').removeClass('fa-spin');
    $('#core').removeClass('reveal-bis');
    return true;
  }
  else return false;
}

function connection() {
  var mail = $('#usr').val();
  var pass = $('#pwd').val();
  var data = {"email": mail,"password" : pass};
  fetch('/connection', {
    headers: {
      'Content-Type': 'application/json'
    },
    method: 'POST',
    body: JSON.stringify(data)
  })
    .then((response) => {
      if(response.ok) {
        response.json().then((result) => chartr=result);
        return;
      }

      throw new Error('erreur de connection.');
    });

}


function test() {
  fetch('/clicked', {method: 'POST'})
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