var chai = require("chai");
var sinon = require("sinon");
var sinonChai = require("sinon-chai");
var expect = chai.expect;
chai.use(sinonChai);
require( 'mocha-jsdom' )();
var resizeHandler = require('../../src/static/js/handle-resize');

describe('Resize handler', function() {
  
  beforeEach(function () {
      sandbox = sinon.sandbox.create();
  });

  afterEach(function () {
      sandbox.restore();
  });

  it('should call handleResize on init by default', function() {
    var resizeMethod = sandbox.stub(resizeHandler.prototype, 'handleResize')
    var cb = sandbox.spy();
    var test = sandbox.spy();
    var handler = new resizeHandler(test, cb);
    handler.init();
    expect(resizeMethod).to.have.been.called;
    handler.destroy();
  });

  it('should not call handleResize on init when opts.setup is false', function() {
    var resizeMethod = sandbox.stub(resizeHandler.prototype, 'handleResize')
    var cb = sandbox.spy();
    var test = sandbox.spy();
    var handler = new resizeHandler(test, cb, {setup: false});
    handler.init();
    expect(resizeMethod).not.to.have.been.called;
    handler.destroy();
  });

  it('should call handleResize on window resize event', function() {
    var resizeMethod = sandbox.stub(resizeHandler.prototype, 'handleResize')
    var cb = sandbox.spy();
    var test = sandbox.spy();
    var handler = new resizeHandler(test, cb, {setup: false});
    handler.init();
    expect(resizeMethod).not.to.have.been.called;
    window.dispatchEvent(new Event('resize'));
    expect(resizeMethod).to.have.been.calledOnce;
    handler.destroy();
  });
  
  it('handleResize should run test callback', function() {
    var cb = sandbox.spy();
    var test = sandbox.spy();
    var handler = new resizeHandler(test, cb);
    handler.init();
    expect(test).to.have.been.called;
    expect(cb).not.to.have.been.called;
    handler.destroy();
  })
  
  it('handleResize should call cb after running test if test returns a value other than undefined', function() {
    var cb = sandbox.spy();
    var test = sandbox.spy(function () {return true;});
    var handler = new resizeHandler(test, cb);
    handler.init();
    expect(test).to.have.been.called;
    expect(cb).to.have.been.called;
    handler.destroy();
  })
  
});
