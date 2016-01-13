'use strict';

/**
  * Assigns handlers to tooltips
  * @param { object } $elem - jQuery object
  */
var toolTipper = function ( $elem ) {
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

  // check offset again, properly set tips to point to the element clicked
  tipOffset = Math.floor( ttc.outerWidth() / 2 );
  innerTip.css('left', Math.floor( tipOffset - ( innerTip.outerWidth() / 2 ) ) );
  outerTip.css('left', Math.floor( tipOffset - ( outerTip.outerWidth() / 2 ) ) );


    // Prevent tooltip from falling off the left side of screens
    if (newLeft < 20) {
      var elemCenter = $elem.offset().left + ( $elem.width() / 2 ),
          pagePadding = 20;
      ttc.css('left', pagePadding);
      innerTip.css('left', elemCenter - ( innerTip.outerWidth() / 2 ) - pagePadding );
      outerTip.css('left', elemCenter - ( outerTip.outerWidth() / 2 ) - pagePadding );
    }

    // Prevent tooltip from falling off the right side of screens
    if ( ttc.offset().left + ttc.outerWidth(true) >$(window).width()) {
      var elemCenter = $elem.offset().left + ( $elem.width() / 2 ),
          elemRightOffset = $(window).width() - elemCenter,
          pagePadding = 20;
      newLeft = $(window).width() - ttc.outerWidth(true) - pagePadding;
      ttc.css( 'left', newLeft );
      innerTip.css('left', ttc.outerWidth() - ( innerTip.outerWidth() / 2 ) - elemRightOffset + pagePadding );
      outerTip.css('left', ttc.outerWidth() - ( outerTip.outerWidth() / 2 ) - elemRightOffset + pagePadding );
    }

  $( 'html' ).on('click', 'body:not(#tooltip-container a)', function() {
    ttc.hide();
    ttc.find( '.content' ).html('');
    $('[data-tooltip-current-target]').removeAttr('data-tooltip-current-target');
    $( 'html' ).off('click');
  });
}

module.exports = toolTipper;
