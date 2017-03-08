"use strict";

var urlCodes = {
  'all_all' : 's6ew-h6mp',
  'all_narratives' : 'nsyy-je5y',
  'bank-account_all' : 't9fg-cqmi',
  'bank-account_narratives' : 'ytxv-uppu',
  'credit-card_all' : '7zpz-7ury',
  'credit-card_narratives' : 'wycs-qcs4',
  'credit-reporting_all' : 'xa48-juie',
  'credit-reporting_narratives' : 'ur78-i5sn',
  'debt-collection_all' : 'ckyu-ku28',
  'debt-collection_narratives' : 'dx9u-5nhx',
  'money-transfer_all' : '3hjq-88e9', // + virtual currency
  'money-transfer_narratives' : 'd644-vf4p', // + virtual currency
  'mortgage_all' : 'g5qz-smft',
  'mortgage_narratives' : 'gfmg-6ppu',
  'other_all' : 'b239-tvpx',
  'other_narratives' : 'yjne-fppi',
  'payday-loan_all' : '6hp8-hzag',
  'payday-loan_narratives' : 'xiq2-ahjv',
  'prepaid-card_all' : '6yuf-367p',
  'prepaid-card_narratives' : '2t2q-2pud',
  'student-loan_all' : 'eew7-9yf2',
  'student-loan_narratives' : 'j875-kipn',
  'consumer-loan_all' : 'wfbn-zkat',
  'consumer-loan_narratives' : 'uqjt-9neg'
};

/**
 * Generates a url for complaint data. Uses
 * category & include params to derive a url code,
 * then constructs url from base & code and adds
 * format extension.
 *
 *
 * @param  {string} category
 * @param  {string} include
 * @param  {string} format
 */


var configureComplaintURL = function(category, include, format) {
    var baseURL = 'https://data.consumerfinance.gov/api/views/';
    var code = urlCodes[category + '_' + include];
    var queryParam = '?accessType=DOWNLOAD';
    if (code && format) {
      return baseURL + code + '/rows.' + format + queryParam;
    }
}

module.exports = configureComplaintURL;
