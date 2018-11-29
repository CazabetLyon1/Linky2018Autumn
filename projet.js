$(document).ready(function() {

var chart = null;

  $("#core").load("./accueil.html");
  $("#mod").load("./modal.html");





  // Open navbarSide when button is clicked
  $('#bars').on('click', function() {
    if($('#menu').hasClass('reveal')) {
      $('#menu').removeClass('reveal');
      $('#bars').removeClass('fa-spin');
      $('#core').removeClass('reveal-bis');
    }
    else{ 
     $('#menu').addClass('reveal');
     $('#bars').addClass('fa-spin');
     $('#core').addClass('reveal-bis');
   }
  });

  $('#graphique').on('click', function() {
    $("#core").html("");
      if(chart === null)
        grap("myChart");
      $("#graph").css("display","block");
  });

  $('#home').on('click', function() {
    $("#core").load("./accueil.html");
    $("#graph").css("display","none");
  });

});