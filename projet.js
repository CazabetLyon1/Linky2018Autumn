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

  $(window).scroll(()=>hideSideBar()); //Pour cacher le menu coullisant (ou side bar) lors d'un scroll

});

function hideSideBar() {
  if($('#menu').hasClass('reveal')) //Si la sidebar est visible
  {
    $('#menu').removeClass('reveal');
    $('#bars').removeClass('fa-spin');
    $('#core').removeClass('reveal-bis');
    return true;
  }
  else return false;
}

function connection() {
  var mail = $('#usr').val(); //Récupération des valeurs depuis les inputs de modals
  var pass = $('#pwd').val();
  var data = {"email": mail,"password" : pass};
  $('#load span').remove();
  $('#load').append("<i class=\"fas fa-fw fa-circle-notch fa-spin\"></i>");
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
        response.json().then((result) => chart=JSON.parse(result)); //La réponse est sous forme de Promise, il a donc fallut récupérer le résultat et la stocker dans une variable
        return;
      }
      else 
      {
        console.log("dqsdqdd");
        $('#load').append("<span style=\"color:red;\">Erreur lors de la connexion, veuillez réessayer.</span>");
      }
      throw new Error('erreur de connection.');
    });

}