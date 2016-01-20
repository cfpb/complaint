'use strict';
var assign = require('object-assign');

/**
 * Facilitates functionality that depends on window size.
 * Takes a test function and a callback function,
 * runs the test function when the window resizes,
 * and if the value it returns has changed from the previously
 * stored value, calls cb function and passes it the new test result.
 *
 * Resize functionality will also be called on init, but can
 * be turned off by passing opts object with {setup: false}
 * as third argument.
 * 
 *
 * @param  {function} test 
 * @param  {function} cb 
 * @param  {object} opts optional
 */

function handleResize (test, cb, opts) {
 var prevResult, 
     currentResult, 
     defaultOpts = {setup: true};

 if (typeof test !== 'function' || typeof cb !== 'function') {
   throw new Error("Resize handler needs test and callback.");
 }

 opts = assign(defaultOpts, opts);

 function onResize () { 
   currentResult = test();
   if (currentResult !== prevResult) {
     cb(currentResult);
   }
   prevResult = currentResult;
 }

 function init () {
   if (opts.setup) {
     onResize();
   }
   window.addEventListener('resize', onResize);
 }

 function destroy () {
   window.removeEventListener('resize', onResize);
 }

 return {
   init: init,
   destroy: destroy
 }
}
module.exports = handleResize;
