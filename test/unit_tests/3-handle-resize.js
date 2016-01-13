var chai = require("chai");
var sinon = require("sinon");
var sinonChai = require("sinon-chai");
var expect = chai.expect;
chai.use(sinonChai);
var jsdom = require('mocha-jsdom');
var handleResize = require('../../src/static/js/handle-resize');

describe('Resize handler', function() {
  
  beforeEach(function () {
      sandbox = sinon.sandbox.create();
  });
  
  jsdom();

  afterEach(function () {
      sandbox.restore();
  });
  
  describe('Error handling: ', function() {
    var errorMessage = "Resize handler needs test and callback.";
    
    it('should throw an error if test and cb params are not present', function() {
      var resize = function() {handleResize()};
      expect(resize).to.throw(errorMessage)
    });

    it('should throw an error if cb param is not present', function() {
      var cb = sandbox.spy();
      var resize = function() {handleResize(null, cb)};
      expect(resize).to.throw(errorMessage)

    });

    it('should throw an error if test param is not a function', function() {
      var cb = sandbox.spy();
      var resize = function() {handleResize('', cb)};
      expect(resize).to.throw(errorMessage)

    });

    it('should throw an error if cb param is not a function', function() {
      var test = sandbox.spy();
      var resize = function() {handleResize(test, '')};
      expect(resize).to.throw(errorMessage)

    });
  });
  
  it('should not call test or callback on init when opts.setup is false', function() {
    var cb = sandbox.spy();
    var test = sandbox.spy();
    expect(test).not.to.have.been.called;
    expect(cb).not.to.have.been.called;
    
    var handler = handleResize(test, cb, {setup: false});
    handler.init();
    expect(test).not.to.have.been.called;
    expect(cb).not.to.have.been.called;
  });
  
  it('should call test but not cb on init when opts.setup defaults to true and test does not return a value', function() {
    var cb = sandbox.spy();
    var test = sandbox.spy(function () {});
    expect(test).not.to.have.been.called;
    expect(cb).not.to.have.been.called;
    
    var handler = handleResize(test, cb);
    handler.init();
    expect(test).to.have.been.calledOnce;
    expect(cb).not.to.have.been.called;
  });
  
  it('should call cb on init when opts.setup defaults to true and test returns value other than undefined', function() {
    var cb = sandbox.spy();
    var test = sandbox.spy(function () {return true;});
    
    var handler = handleResize(test, cb);
    handler.init();
    expect(test).to.have.been.calledOnce;
    expect(cb).to.have.been.calledOnce;
  });
  
  it('should call test but not cb on window resize when test returns the same value each time', function() {
    var cb = sandbox.spy();
    var test = sandbox.spy(function () {return true;});
    
    var handler = handleResize(test, cb);
    handler.init();
    expect(test).to.have.been.calledOnce;
    expect(cb).to.have.been.calledOnce;  
      
    window.dispatchEvent(new Event('resize'));
    expect(test).to.have.been.calledTwice;
    expect(cb).to.have.been.calledOnce;
  });
  
  
  it('should call test and cb on window resize when test returns a different value the second time', function() {
    var cb = sandbox.spy();
    var test = sandbox.spy(function () {return window.innerWidth < 500});
    window.innerWidth = 1024;
    var handler = handleResize(test, cb);
    handler.init();
    expect(test).to.have.been.calledOnce;
    expect(cb).to.have.been.calledOnce;
    
    window.innerWidth = 100;
    window.dispatchEvent(new Event('resize'));
    expect(test).to.have.been.calledTwice;
    expect(cb).to.have.been.calledTwice;
  });
  
  
  it('should call cb with the latest result of the test function', function() {
    var cb = sandbox.spy();
    var test = sandbox.spy(function () {return window.innerWidth});
    window.innerWidth = 1024;
    var handler = handleResize(test, cb);
    handler.init();
    expect(test).to.have.been.calledOnce;
    expect(cb).to.have.been.calledOnce
    expect(cb).to.have.been.calledWith(1024);
    
    window.innerWidth = 100;
    window.dispatchEvent(new Event('resize'));
    expect(test).to.have.been.calledTwice;
    expect(cb).to.have.been.calledTwice;
    expect(cb).to.have.been.calledWith(100);
  });
  
  
  it('should stop listening for window resize events when destroy is called', function() {
    var cb = sandbox.spy();
    var test = sandbox.spy(function () {return window.innerWidth});
    window.innerWidth = 1024;
    var handler = handleResize(test, cb);
    handler.init();
    expect(test).to.have.been.calledOnce;
    expect(cb).to.have.been.calledOnce;
    
    handler.destroy();
    window.innerWidth = 100;
    window.dispatchEvent(new Event('resize'));
    expect(test).to.have.been.calledOnce;
    expect(cb).to.have.been.calledOnce;
  });
  
});
