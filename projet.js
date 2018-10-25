$( document ).ready(function() {

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


});