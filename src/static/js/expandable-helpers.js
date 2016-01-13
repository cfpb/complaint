'use strict';
var $ = global.jQuery;

/**
 * Helper methods for expandables.
 * 
 * Caches the expandables and expandable targets in a page,
 * then offers methods to interact with them: activating,
 * filtering, and checking or toggling their state. 
 * 
 * Pass in optional el to target specific part of page.
 *
 * @param  {string} el optional 
 */
 
function expandableHelpers (el) {
  var selectors = {
    expandableContent: '.expandable_content',
    expandableTrigger: '.expandable_target',
    expandable: '.expandable',
    selectedExpandableClass: 'expandable__expanded'
  }
  
  var $el = $(el).length ? $(el) : $('body');
  var $expandableTriggers = $el.find(selectors.expandableTrigger);
  var $expandables = $el.find(selectors.expandable);
  
  var utils = {
    selectors: selectors,
    $expandableTriggers: $expandableTriggers,
    $expandables: $expandables
  }
  
  utils.filterExpandables = function (selector) {
    return $expandables.filter(selector);
  }
  
  utils.getOpenExpandables = function () {
    return utils.filterExpandables('.' + selectors.selectedExpandableClass);
  }
  
  utils.isExpandableTriggerVisible = function () {
    return $expandableTriggers.first().is(':visible');
  }
  
  utils.activateExpandables = function () {
    if (!$expandables.get(0).expand) {
      $expandables.expandable();      
    }
  }
  
  utils.openExpandableWithoutAnimation = function ($expandable) {
    $expandable.addClass(selectors.selectedExpandableClass);
    $expandable.find(selectors.expandableContent).attr('aria-expanded', 'true').css({'display': ''});
    $expandable.find(selectors.expandableTrigger).attr('aria-pressed', 'true');
  }
  
  utils.closeExpandableWithoutAnimation = function ($expandable) {
    $expandable.removeClass(selectors.selectedExpandableClass);
    $expandable.find(selectors.expandableContent).attr('aria-expanded', 'false').hide();
    $expandable.find(selectors.expandableTrigger).attr('aria-pressed', 'false');
  }
  
  utils.toggleExpandable = function ($selected, accordion) {
    if (accordion) {
      utils.closeExpandableWithoutAnimation($expandables);
    }
    if ($selected) {
      utils.openExpandableWithoutAnimation($selected);
    }
  }
  
  utils.toggleAllExpandables = function (expandablesVisible) {
    if (expandablesVisible) {
      utils.closeExpandableWithoutAnimation(utils.getOpenExpandables());
      utils.activateExpandables();
    } else {
      utils.openExpandableWithoutAnimation($expandables);
    }
  }

  return utils;
}

module.exports = expandableHelpers;
