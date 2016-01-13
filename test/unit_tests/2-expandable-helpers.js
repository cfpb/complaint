var chai = require("chai");
var sinon = require("sinon");
var sinonChai = require("sinon-chai");
var expect = chai.expect;
chai.use(sinonChai);
var jsdom = require('mocha-jsdom');
var $;
var jQuery;

var contentSelector = '.expandable_content';
var triggerSelector = '.expandable_target';
var expandableSelector = '.expandable';
var selectedExpandableClass = 'expandable__expanded';
var helpers, $expandables, $expandableTriggers;
var handleResize;

describe('Expandable helpers', function() {
  jsdom({
    file: 'test/unit_tests/fixtures/expandables.html',
    console: false
  });

  before(function () {
    $ = global.jQuery = require('../../src/vendor/jquery/dist/jquery.js');
    require('../../src/vendor/jquery.easing/js/jquery.easing.js');
    require('../../src/static/js/expandable.js');
    expandableHelpers = require('../../src/static/js/expandable-helpers.js');
    helpers = expandableHelpers();
    $expandables = helpers.$expandables;
    $expandableTriggers = helpers.$expandableTriggers;
  });
  
  beforeEach(function () {
      sandbox = sinon.sandbox.create();
  });
  
  afterEach(function () {
      sandbox.restore();
  });
  
  describe('cache tests: ', function() {  
    it('should cache expandables', function() {
      var expandables = $(expandableSelector);
      expect(expandables.length).to.equal($expandables.length);
      expandables.each(function (ind, item) {
        expect(item).to.deep.equal(helpers.$expandables[ind]);
      })
    });
  
    it('should cache expandable triggers', function() {
      var expandableTriggers = $(triggerSelector);
      expect(expandableTriggers.length).to.equal($expandableTriggers.length);
      expandableTriggers.each(function (ind, item) {
        expect(item).to.deep.equal($expandableTriggers[ind]);
      })
    });
  });
  
  describe('filter tests: ', function() {    
    it('should filter expandables', function() {
      $expandables.removeClass('test-class').first().addClass('test-class');
      var filtered = helpers.filterExpandables('.test-class');
      expect(filtered.length).to.equal(1);
      expect(filtered[0]).to.deep.equal($expandables[0]);
      $expandables.removeClass('test-class');
    });
    
    it('should get zero open expandables', function() {
      $expandables.removeClass(selectedExpandableClass);
      var openExpandables = helpers.getOpenExpandables();
      expect(openExpandables.length).to.equal(0);
    });
    
    it('should get one open expandable', function() {
      $expandables.removeClass(selectedExpandableClass).first().addClass(selectedExpandableClass);
      var openExpandables = helpers.getOpenExpandables();
      expect(openExpandables.length).to.equal(1);
      expect(openExpandables[0]).to.deep.equal($expandables[0]);
    });
  });
  
  describe('status tests: ', function() {
    it('should return false from isExpandableTriggerVisible if targets are hidden', function() {
      $expandableTriggers.hide();      
      expect(helpers.isExpandableTriggerVisible()).to.be.false;
    })
    
    it('should return true from isExpandableTriggerVisible if targets are shown', function() {
      $expandableTriggers.show();
      expect(helpers.isExpandableTriggerVisible()).to.be.true;
    })
  });
  
  describe('open and close tests: ', function() {
    var expandable, content, trigger;
    beforeEach(function () {
      expandable = $expandables.first();
      content = expandable.find(contentSelector);
      trigger = expandable.find(triggerSelector);
    })
    
    it('should open an expandable and update its aria attributes', function() {      
      expandable.removeClass(selectedExpandableClass);
      content.attr('aria-expanded', 'false');
      trigger.attr('aria-pressed', 'false');
      expect(expandable.hasClass(selectedExpandableClass)).to.be.false;
      expect(content.attr('aria-expanded')).to.equal('false');
      expect(trigger.attr('aria-pressed')).to.equal('false');
      
      helpers.openExpandableWithoutAnimation(expandable);
      expect(expandable.hasClass(selectedExpandableClass)).to.be.true;
      expect(content.attr('aria-expanded')).to.equal('true');
      expect(trigger.attr('aria-pressed')).to.equal('true');
    });
    
    it('should close an expandable and update its aria attributes', function() {
      expandable.addClass(selectedExpandableClass);
      content.attr('aria-expanded', 'true');
      trigger.attr('aria-pressed', 'true');
      expect(expandable.hasClass(selectedExpandableClass)).to.be.true;
      expect(content.attr('aria-expanded')).to.equal('true');
      expect(trigger.attr('aria-pressed')).to.equal('true');
      
      helpers.closeExpandableWithoutAnimation(expandable);
      expect(expandable.hasClass(selectedExpandableClass)).to.be.false;
      expect(content.attr('aria-expanded')).to.equal('false');
      expect(trigger.attr('aria-pressed')).to.equal('false');
    })
  });
  
  describe('expandable toggle tests: ', function() {
    var expandable, openSpy, closeSpy;
    
    beforeEach(function () {
      expandable = $expandables.first();
      openSpy = sandbox.stub(helpers, 'openExpandableWithoutAnimation');
      closeSpy = sandbox.stub(helpers, 'closeExpandableWithoutAnimation');
    });
    
    it('toggleExpandable should open an expandable', function() {
      helpers.toggleExpandable(expandable);
      expect(openSpy).to.have.been.calledOnce;
      expect(openSpy).to.have.been.calledWith(expandable);
      expect(closeSpy).not.to.have.been.called;
    });
    
    it('toggleExpandable should close other expandables when accordion is true', function() {
      helpers.toggleExpandable(expandable, true);
      expect(openSpy).to.have.been.calledOnce;
      expect(openSpy).to.have.been.calledWith(expandable);
      expect(closeSpy).to.have.been.calledOnce;
      expect(closeSpy).to.have.been.calledWith($expandables);
    })
  });
  
  describe('all expandable toggle tests: ', function() {
    var expandable, openSpy, closeSpy, activateSpy;
    
    beforeEach(function () {
      expandable = $expandables.first();
      openSpy = sandbox.stub(helpers, 'openExpandableWithoutAnimation');
      closeSpy = sandbox.stub(helpers, 'closeExpandableWithoutAnimation');
      activateSpy = sandbox.stub(helpers, 'activateExpandables');
    });
    
    it('toggleAllExpandables should close open expandables and activate expandables when it is passed true', function() {
      helpers.toggleAllExpandables(true);
      expect(closeSpy).to.have.been.calledOnce;
      expect(activateSpy).to.have.been.calledOnce;
    });
    
    it('toggleAllExpandables should open all expandables when it is not passed true', function() {
      helpers.toggleAllExpandables();
      expect(openSpy).to.have.been.calledOnce;
      expect(openSpy).to.have.been.calledWith($expandables);
    })
  });
  
});
