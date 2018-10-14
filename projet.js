$( document ).ready(function() {

  // Open navbarSide when button is clicked
  $('#bars').on('click', function() {
    if($('#menu').hasClass('reveal')) $('#menu').removeClass('reveal');
    else  $('#menu').addClass('reveal');
  });


});