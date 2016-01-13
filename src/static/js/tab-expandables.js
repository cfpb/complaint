'use strict';
var $ = global.jQuery;
require('../../vendor/jquery.easing/js/jquery.easing.js')
require('../../vendor/cf-expandables/src/js/cf-expandables.js');

var handleResize = require('./handle-resize');
var expandableHelper = require('./expandable-helpers');

/**
 * Manages tabs that become expandables at certain screen sizes.
 * 
 * When tab button or tab navigation button is clicked,
 * updates active state of tab buttons and shows/hides related
 * expandable based on a shared data attribute on button & expandable.
 *
 * Also keeps tabs and expandables in sync. On window resize, 
 * checks whether tabs or expandables are currently visible. 
 * If tabs are visible, checks for current open expandable and activates
 * associated tab button. If no tabs are expanded, opens the first tab
 * and activates its button.
 *
 * Pass in optional el to target part of the page, and an optional
 * tabSelectors object to use different selectors for tab and tab nav
 * buttons, class for selected buttons, or identifying data attribute.
 *
 * @param  {string} el optional 
 * @param  {object} tabSelectors optional
 */

function tabExpandables (el, tabSelectors) {    
    var $el = $(el).length ? $(el) : $('body');
    var defaultSelectors = {
      dataAttr: 'data-category',
      nav: '.tab_nav',
      btn: '.tab_btn',
      selectedBtnClass: 'selected-button'
    };
    
    tabSelectors = $.extend(defaultSelectors, tabSelectors);
    
    var $btns = $(tabSelectors.btn);
    var $navs = $(tabSelectors.nav);
    var helpers = expandableHelper()
    
    var utils = {
      helpers: helpers
    }
    
    utils.updateTabs = function (selectedBtn) {
      var selectedCategory = $(selectedBtn).attr(tabSelectors.dataAttr);
      var selectedFilter = '[' + tabSelectors.dataAttr + '="' + selectedCategory + '"]';
      var selectClass = tabSelectors.selectedBtnClass;
      var $selectedTab = helpers.filterExpandables(selectedFilter);
      
      $btns.removeClass(selectClass).filter(selectedFilter).addClass(selectClass);
      helpers.toggleExpandable($selectedTab, true);
    }
    
    utils.syncTabsWithExpandables = function () {
      var openExpandables = helpers.getOpenExpandables();
      if (openExpandables.length > 0) {
        utils.updateTabs(openExpandables[0]);
      } else {
        utils.updateTabs($btns[0]);
      }
    }
    
    utils.init = function () {
      utils.resizeHandler = handleResize(helpers.isExpandableTriggerVisible, utils.syncTabsWithExpandables);
      utils.resizeHandler.init();
      
      $el.on('click', tabSelectors.btn + ', ' + tabSelectors.nav, function() {
        utils.updateTabs(this);
      });
    }
    
    return utils;
}

module.exports = tabExpandables;
