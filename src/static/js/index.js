'use strict';

require('./nemo');
require('./nemo-shim');
var toolTipper = require('./tooltipper');
var configureComplaintURL = require('./complaint-urls');
var tabExpandables = require('./tab-expandables');


$(document).ready( function() {
  // sync tabs with expandables
  tabExpandables().init();

  // tooltips for tab buttons
    $('.category-buttons button').hover(
      function() {
        var $textBox = $(this).find('.text-content');
        $(this).addClass('hover-button');
        $textBox.css('left', ($textBox.outerWidth() - $(this).outerWidth()) / 2 * -1);
      },
      function() {
        $(this).removeClass('hover-button');
      }
    );

  // Tooltips for info buttons
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

  // download url change handlers
  function updateComplaintDownloadURL () {
    var category = $('.download-radio input:checked').val();
    var include = $('#download_include option:selected').val();
    var format = $('#download_format option:selected').val();
    
    var url = configureComplaintURL(category, include, format);
    
    $('#download-data-btn').attr('href',  url);
  }
  
  $('.download-radio').click( function() {
    updateComplaintDownloadURL();
  });

  $('#download_format, #download_include').on( 'change', function() {
    updateComplaintDownloadURL();
  });

  $('.publication-criteria a, .list__links .pdf, .pdf').removeClass('pdf');
});

