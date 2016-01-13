'use strict';

require('jquery-easing');
require('./expandable');
require('./nemo');
require('./nemo-shim');
var expandableHelper = require('./expandable-helpers');
var handleResize = require('./handle-resize');

$(document).ready( function() {
  var helpers = expandableHelper();
  var resizeHandler = handleResize(helpers.isExpandableTriggerVisible, helpers.toggleAllExpandables);
  resizeHandler.init();
});


