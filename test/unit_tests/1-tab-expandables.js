var chai = require("chai");
var sinon = require("sinon");
var sinonChai = require("sinon-chai");
var expect = chai.expect;
chai.use(sinonChai);
var jsdom = require('mocha-jsdom');
var $;
var jQuery;
var tabExpandables;
var tabModule;
var handleResize;
var helpers;
var selectors = {
  dataAttr: 'data-category',
  nav: '.tab_nav',
  btn: '.tab_btn',
  selectedBtnClass: 'selected-button'
};

describe('Tab expandables', function() {
  jsdom({
    file: 'test/unit_tests/fixtures/tab-expandables.html',
    console: false
  });

  before(function () {
    $ = global.jQuery = require('../../src/vendor/jquery/dist/jquery.js');
    require('../../src/vendor/jquery.easing/js/jquery.easing.js');
    require('../../src/vendor/cf-expandables/src/js/cf-expandables.js');
    tabModule = require('../../src/static/js/tab-expandables.js');
    handleResize = require('../../src/static/js/handle-resize');    
    tabExpandables = tabModule('body', selectors);
    tabExpandables.init();  
    helpers = tabExpandables.helpers;  
  });
  
  beforeEach(function () {
      sandbox = sinon.sandbox.create();
  });
  
  afterEach(function () {
      sandbox.restore();
  });
  
  describe('Update tabs', function() {
    var tabButtons, firstButton, secondButton;
    
    beforeEach(function () {
        tabButtons = $(selectors.btn);
        firstButton = $(tabButtons[0]);
        secondButton = $(tabButtons[1]);
        tabButtons.removeClass(selectors.selectedBtnClass);
        secondButton.addClass(selectors.selectedBtnClass);
    });
    
    it('clicking a tab button should call updateTabs', function() {
      expect(firstButton.hasClass(selectors.selectedBtnClass)).to.be.false;
      expect(secondButton.hasClass(selectors.selectedBtnClass)).to.be.true;

      firstButton.click(); 
      expect(firstButton.hasClass(selectors.selectedBtnClass)).to.be.true;
      expect(secondButton.hasClass(selectors.selectedBtnClass)).to.be.false;
    });
    
    it('clicking a nav button should activate the associated tab button and inactivate the other buttons', function() {
      expect(firstButton.hasClass(selectors.selectedBtnClass)).to.be.false;
      expect(secondButton.hasClass(selectors.selectedBtnClass)).to.be.true;

      var firstCategory = firstButton.data('category');
      var firstNavButton = $('.tab_nav').filter('[data-category="' + firstCategory + '"]');
      $(firstNavButton).click(); 
      expect(firstButton.hasClass(selectors.selectedBtnClass)).to.be.true;
      expect(secondButton.hasClass(selectors.selectedBtnClass)).to.be.false;
    });
    
    it('clicking a tab button should call toggle expandables function', function() {
      var toggleExpandableSpy = sandbox.spy(helpers, 'toggleExpandable');
      var firstCategory = firstButton.data('category');
      var firstTab = $('.expandable').filter('[data-category="' + firstCategory + '"]');
      
      firstButton.click();
      var toggleExpandableSpyArgs = toggleExpandableSpy.args[0];
      expect(toggleExpandableSpy).to.have.been.called;     
      expect(toggleExpandableSpyArgs[0][0]).to.deep.equal(firstTab[0]);      
      expect(toggleExpandableSpyArgs[1]).to.equal(true);
    })
    
    it('clicking a tab button should show the corresponding tab and hide the others', function() {
      var firstCategory = firstButton.data('category');
      var firstTab = $('.expandable').filter('[data-category="' + firstCategory + '"]');
      var secondCategory = secondButton.data('category');
      var secondTab = $('.expandable').filter('[data-category="' + secondCategory + '"]');
      var expandedClass = 'expandable__expanded';
      $('.expandable').removeClass(expandedClass);
      secondTab.addClass(expandedClass);
      expect(firstTab.hasClass(expandedClass)).to.be.false;
      expect(secondTab.hasClass(expandedClass)).to.be.true;
      
      firstButton.click();      
      expect(firstTab.hasClass(expandedClass)).to.be.true;
      expect(secondTab.hasClass(expandedClass)).to.be.false;
    })
  });
  
  it('syncTabsWithExpandables should call updateTabs with the first open expandable if there are open expandables', function() {  
    var getOpenExpandablesSpy = sandbox.stub(helpers, 'getOpenExpandables', function () {
      return helpers.$expandables;
    });
    var updateTabsSpy = sandbox.spy(tabExpandables, 'updateTabs');
    expect(getOpenExpandablesSpy).not.to.have.been.called;
    expect(updateTabsSpy).not.to.have.been.called;
    
    tabExpandables.syncTabsWithExpandables();
    expect(getOpenExpandablesSpy).to.have.been.calledOnce;
    expect(updateTabsSpy).to.have.been.calledOnce;
    expect(updateTabsSpy).to.have.been.calledWith(helpers.$expandables[0]);
  });
  
  it('syncTabsWithExpandables should call updateTabs with the first tab button if there are no open expandables', function() {  
    var $btns = $(selectors.btn);
    var getOpenExpandablesSpy = sandbox.stub(helpers, 'getOpenExpandables', function () {
      return [];
    });
    var updateTabsSpy = sandbox.spy(tabExpandables, 'updateTabs');
    expect(getOpenExpandablesSpy).not.to.have.been.called;
    expect(updateTabsSpy).not.to.have.been.called;
    
    tabExpandables.syncTabsWithExpandables();
    expect(getOpenExpandablesSpy).to.have.been.calledOnce;
    expect(updateTabsSpy).to.have.been.calledOnce;
    expect(updateTabsSpy).to.have.been.calledWith($btns[0]);
  });
  
});
