'use strict';

require('./nemo');
require('./nemo-shim');
require('./submit-a-complaint');

var urlCodes = {
  'all_all' : 's6ew-h6mp',
  'all_narratives' : 'nsyy-je5y',
  'bank-account_all' : 't9fg-cqmi',
  'bank-account_narratives' : 'ytxv-uppu',
  'credit-card_all' : '7zpz-7ury',
  'credit-card_narratives' : 'wycs-qcs4',
  'credit-reporting_all' : 'xa48-juie',
  'credit-reporting_narratives' : 'ur78-i5sn',
  'debt-collection_all' : 'ckyu-ku28',
  'debt-collection_narratives' : 'dx9u-5nhx',
  'money-transfer_all' : 'uha4-cwwn',
  'money-transfer_narratives' : 'njq8-tnnk',
  'mortgage_all' : 'g5qz-smft',
  'mortgage_narratives' : 'gfmg-6ppu',
  'other_all' : 'b239-tvpx',
  'other_narratives' : 'yjne-fppi',
  'payday-loan_all' : '6hp8-hzag',
  'payday-loan_narratives' : 'xiq2-ahjv',
  'prepaid-card_all' : '6yuf-367p',
  'prepaid-card_narratives' : '2t2q-2pud',
  'student-loan_all' : 'eew7-9yf2',
  'student-loan_narratives' : 'j875-kipn',
  'consumer-loan_all' : 'wfbn-zkat',
  'consumer-loan_narratives' : 'uqjt-9neg'
};

var lastClicked = 'bank-account'; // Tracks the last thing the user clicked to respond to window resize


/**
  * Assigns handlers to tooltips
  * @param { object } $elem - jQuery object
  */
function toolTipper( $elem ) {
  // position tooltip-container based on the element clicked
  var ttc = $('#tooltip-container'),
      name = $elem.attr('data-tooltip-target'),
      content = $('[data-tooltip-name="' + name + '"]').html(),
      innerTip = ttc.find( '.innertip' ),
      outerTip = ttc.find( '.outertip' ),
      newTop,
      newLeft,
      tipset,
      tipOffset;

  ttc.width( $('#ccdb-landing').width() / 3 );

  ttc.find('.content').html( content );
  $('[data-tooltip-current-target]').removeAttr('data-tooltip-current-target');
  $elem.attr( 'data-tooltip-current-target', true );

  ttc.show();
  newTop = $elem.offset().top + $elem.outerHeight() + 10;
  newLeft = $elem.offset().left + ( $elem.outerWidth() / 2 ) - ( ttc.outerWidth(true) / 2 );
  ttc.css( { 'top': newTop, 'left': newLeft } );

  if ( ttc.offset().left + ttc.outerWidth(true) > $(window).width()) {
    newLeft = $(window).width() - ttc.outerWidth(true) - 20;
    ttc.css( 'left', newLeft );
  }
  // check offset again, properly set tips to point to the element clicked
  tipOffset = Math.floor( ttc.outerWidth() / 2 );
  innerTip.css('left', Math.floor( tipOffset - ( innerTip.outerWidth() / 2 ) ) );
  outerTip.css('left', Math.floor( tipOffset - ( outerTip.outerWidth() / 2 ) ) );

  $( 'html' ).on('click', 'body:not(#tooltip-container a)', function() {
    ttc.hide();
    ttc.find( '.content' ).html('');
    $('[data-tooltip-current-target]').removeAttr('data-tooltip-current-target');
    $( 'html' ).off('click');
  });
}


$(document).ready( function() {

  $( '.category-buttons button' ).click( function() {
    lastClicked = $(this).attr('data-category');
    $('.category-buttons button').removeClass('selected-button');
    $(this).addClass('selected-button');
    $('.complaint-container').hide();
    $( '.complaint-container[data-container-for="' + lastClicked + '"]' ).show();
  });

  $( '.category-buttons button' ).hover(
    function() {
      var $textBox = $(this).find('.text-content');
      $(this).addClass('hover-button');
      $textBox.css( 'left', ( $textBox.outerWidth() - $(this).outerWidth() ) / 2 * -1 );
    },
    function() {
      $(this).removeClass('hover-button');
    }
  );

  $( 'button.category-next' ).click( function() {
    lastClicked = $(this).attr('data-category');
    $('.category-buttons button[data-category="' + lastClicked + '"]').click();
  });

  $( '.expandable-bar' ).click( function() {
    var $complaint = $( '.complaint-container[data-container-for="' + $(this).attr('data-category') + '"]' );
    if ( $complaint.is(':visible') ) {
      $complaint.slideUp();
      $(this).find('.cf-icon-minus-round').removeClass('cf-icon-minus-round').addClass('cf-icon-plus-round');
    } else {
      $complaint.slideDown();
      $(this).find('.cf-icon-plus-round').removeClass('cf-icon-plus-round').addClass('cf-icon-minus-round');
      lastClicked = $(this).attr( 'data-category' );
    }
  });

  // Show the Bank accounts tab on load.
  if ( $('.category-buttons').is(':visible') ) {
    $( '.category-buttons button' )[0].click();
  }

  // Tooltip handler
  $('[data-tooltip-target]').click( function( ev ) {
    ev.preventDefault();
    ev.stopPropagation();
    toolTipper( $(this) );
  });

  // Tooltip resize handler
  $(window).resize( function() {
    if ( $('#tooltip-container').is(':visible') ) {
      $('#tooltip-container').hide();
      toolTipper( $('[data-tooltip-current-target]') );
    }
  });

  $('.download-radio').click( function() {
    var url = 'https://data.consumerfinance.gov/views/',
        category = $('.download-radio input:checked').val(),
        include = $('#download_include option:selected').val(),
        code = urlCodes[category + '_' + include],
        format = $('#download_format option:selected').val();
    $('#download-data-btn').attr( 'href', url + code + '/rows.' + format );
  });

  $('#download_format, #download_include').on( 'change', function() {
    $('.download-radio input:checked').click();
  });

  $('.publication-criteria a, .list__links .pdf, .pdf').removeClass('pdf');

  $( window ).resize( function() {
    if ( $( '.category-buttons' ).is( ':visible' ) ) {
      $( '.category-buttons button[data-category="' + lastClicked + '"]' ).click();
    } else {
      $( '.complaint-container:visible' ).each( function() {
        var $expandableBar = $( '.expandable-bar[data-category="' + lastClicked + '"]' );
        lastClicked = $( this ).attr( 'data-container-for' );
        $expandableBar.find( '.cf-icon-plus-round' ).removeClass( 'cf-icon-plus-round' ).addClass( 'cf-icon-minus-round' );
      });
    }
  });

});

