var chart = null;

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
  $('#load').append("<i class=\"fas fa-fw fa-circle-notch fa-spin\"></i>")
  fetch('/connection', {
    headers: {
      'Content-Type': 'application/json'
    },
    method: 'POST',
    body: JSON.stringify(data)
  })
    .then((response) => {
      $('#load i').remove();
      if(response.ok) {
        $('#ModalGraphique').modal("hide");
        response.json().then((result) => chart=JSON.parse(result));
        return;
      }

      throw new Error('erreur de connection.');
    });

}