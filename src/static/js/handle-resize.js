'use strict';

var defaultOpts = {setup: true};
// TODO: polyfills for addEventListener & bind for IE8

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
 
function resizeHandler (test, cb, opts) {
  // TODO: handle errors in args
  // test & cb are required functions;
  // opts is optional object
  this.test = test;
  this.cb = cb;
  this.opts = opts || defaultOpts;
}

resizeHandler.prototype.handleResize = function () { 
  var currentResult = this.test();
  if (currentResult !== this.prevResult) {
    this.cb(currentResult);
  }
  this.prevResult = currentResult;
}

resizeHandler.prototype.init = function () {
  window.addEventListener('resize', this.handleResize.bind(this));
  if (this.opts.setup) {
    this.handleResize();
  }
}

resizeHandler.prototype.destroy = function () {
  window.removeEventListener('resize', this.handleResize);
}

module.exports = resizeHandler;
